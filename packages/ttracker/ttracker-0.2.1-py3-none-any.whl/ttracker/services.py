import dataclasses
import datetime
from ttracker.models import Task
from ttracker.orm import CSVAdapter, Repository


def create_task(name: str, start: bool):
    with Repository(CSVAdapter(".ttracker.csv")) as r:
        if name in [t.name for t in r.all_tasks()]:
            raise ValueError(
                "Task already exists with that name. Please remove the existing one before adding another."
            )
        if start:
            new_task = Task(name, datetime.datetime.now())
        else:
            new_task = Task(name, None)

        r.save_task(new_task)


def start_task(name: str):
    with Repository(CSVAdapter(".ttracker.csv")) as r:
        task = r.get_task(name)
        if not task:
            raise ValueError("Task does not exist.")

        if task.active:
            raise ValueError("Task already started.")

        new_task = dataclasses.replace(
            task, start_active_timestamp=datetime.datetime.now()
        )

        r.save_task(new_task)


def stop_task(name: str) -> tuple[str, str]:
    with Repository(CSVAdapter(".ttracker.csv")) as r:
        task = r.get_task(name)
        if not task:
            raise ValueError("Task does not exist.")

        if not task.active:
            raise ValueError("Task not started.")

        old_total_time = task.cumulative_time
        increase = datetime.datetime.now() - task.start_active_timestamp  # type: ignore
        new_total_time = old_total_time + round(increase.total_seconds())

        new_task = dataclasses.replace(
            task, start_active_timestamp=None, cumulative_time=new_total_time
        )

        r.save_task(new_task)

        return seconds_to_jira_time(increase.total_seconds()), seconds_to_jira_time(
            new_total_time
        )


def delete_task(name: str):
    with Repository(CSVAdapter(".ttracker.csv")) as r:
        task = r.get_task(name)
        if not task:
            raise ValueError("Task does not exist.")
        if task.active:
            raise ValueError("Task started. Stop the task before running this command.")

        r.delete_task(task)
    return seconds_to_jira_time(task.cumulative_time)


def list_tasks():
    with Repository(CSVAdapter(".ttracker.csv")) as r:
        all_tasks = r.all_tasks()
        return all_tasks


def seconds_to_jira_time(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    jira_time_format = ""
    if days > 0:
        jira_time_format += f"{int(days)}d "
    if hours > 0:
        jira_time_format += f"{int(hours)}h "
    if minutes > 0:
        jira_time_format += f"{int(minutes)}m"

    if jira_time_format == "":
        jira_time_format = "0m"
    return jira_time_format.strip()
