from classes.Task import Task

async def new_task(owner: str, task_name: str = "None") -> Task:
    task = Task(task_name, owner)
    return task

async def view_task(task_id: int) -> Task:
    pass

async def view_all_tasks(view_archive: bool = False) -> "list[Task]":
    pass

async def archive_task(task_id: int) -> None:
    pass

async def delete_task(task_id: int) -> None:
    pass
