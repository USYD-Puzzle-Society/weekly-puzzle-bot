import asyncio
import pytest

from src.subcom_task import *
from src.subcom_task_errors import TaskNotFoundError

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

def test_view_all_tasks():
    tasks = []
    tasks.append(new_task('alice', 'Write EOS Hunt'))
    tasks.append(new_task('bob', 'Purchase Prizes'))
    assert tasks == view_all_tasks(view_archive=False)

def test_archive_task():
    task = new_task('alice')
    archive_task(task.task_id)
    task = view_task(task.task_id)
    assert task.archived == True
    assert len(view_all_tasks()) == 0
    assert len(view_all_tasks(view_archive=True)) == 1
    assert view_all_tasks(view_archive=True)[0] == task

def test_delete_task():
    task = new_task('alice')
    delete_task(task.task_id)
    assert len(view_all_tasks()) == 0
    with pytest.raises(TaskNotFoundError):
        view_task(task.task_id)
