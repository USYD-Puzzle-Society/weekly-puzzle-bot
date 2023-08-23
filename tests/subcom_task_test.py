import pytest
import pytest_asyncio

from src.subcom_task import *
from src.subcom_task_errors import TaskNotFoundError

class TestClass:
    @pytest_asyncio.fixture(autouse=True)
    async def async_setup(self):
        await clear()
        yield
        await clear()

    @pytest.mark.asyncio
    async def test_create_one_task(self):  
        await new_task('alice')
        task_list = await view_all_tasks()
        assert len(task_list) == 1

    @pytest.mark.asyncio
    async def test_create_multiple_tasks(self):  
        await new_task('alice', 'Write EOS Hunt')
        await new_task('bob', 'Purchase Prizes')
        task_list = await view_all_tasks()
        assert len(task_list) == 2

    @pytest.mark.asyncio
    async def test_view_task(self):  
        task = await new_task('alice')
        assert task == await view_task(task.task_id)

    @pytest.mark.asyncio
    async def test_view_all_tasks(self):  
        tasks = []
        tasks.append(await new_task('alice', 'Write EOS Hunt'))
        tasks.append(await new_task('bob', 'Purchase Prizes'))
        assert tasks == await view_all_tasks(view_archive=False)

    @pytest.mark.asyncio
    async def test_archive_task(self):  
        task = await new_task('alice')
        await archive_task(task.task_id)
        task = await view_task(task.task_id)
        assert task.archived == True
        assert len(await view_all_tasks()) == 0
        assert len(await view_all_tasks(view_archive=True)) == 1
        assert (await view_all_tasks(view_archive=True))[0] == task

    @pytest.mark.asyncio
    async def test_delete_task(self):  
        task = await new_task('alice')
        await delete_task(task.task_id)
        assert len(await view_all_tasks()) == 0
        with pytest.raises(TaskNotFoundError):
            await view_task(task.task_id)
