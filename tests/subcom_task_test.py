from src.subcom_task import *

def setup_function():
    clear()

def test_create_one_task():
    new_task('alice')
    task_list = view_all_tasks()
    assert len(task_list) == 1

def test_create_multiple_tasks():
    new_task('alice', 'Write EOS Hunt')
    new_task('bob', 'Purchase Prizes')
    task_list = view_all_tasks()
    assert len(task_list) == 2

def test_view_task():
    task = new_task('alice')
    assert task == view_task(task.task_id)