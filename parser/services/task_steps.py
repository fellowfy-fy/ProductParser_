from parser.models import ParseTask, TaskStatusChoices

from rest_framework.exceptions import APIException


def check_task_steps(task: ParseTask):
    new_status: TaskStatusChoices | None = None

    # if task.status == TaskStatusChoices.SETTINGS and task.is_urls_valid:
    #     # Move to paused if urls valid
    #     new_status = TaskStatusChoices.PAUSED
    if task.status not in [TaskStatusChoices.CREATED, TaskStatusChoices.CANCELLED] and not task.is_urls_valid():
        print("MOVING TO SETUP")
        # Move to settings if not set
        new_status = TaskStatusChoices.SETTINGS

    if new_status:
        task.status = new_status
        task.save(update_fields=["status"])


def change_task_status(task: ParseTask, status: TaskStatusChoices):
    status_curr = task.status
    if status_curr == status:
        return

    if status in [TaskStatusChoices.CREATED, TaskStatusChoices.RUN]:
        raise APIException("Запрещенный статус задачи")

    task.status = status
    task.save(update_fields=["status"])
