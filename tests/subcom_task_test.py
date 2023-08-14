from src.subcom_task import *

def setup_function():
    clear()

def test_create_one_task():
    new_task('bob')
    task_list = view_all_tasks()
    assert len(task_list) == 1