from app import storage
from app.models import TaskCreate, TaskPriority, TaskStatus

sample_tasks = [
    TaskCreate(
        title='Write project requirements',
        description='Capture scope, acceptance criteria, and API surface for the task tracker.',
        priority=TaskPriority.HIGH,
        assignee=None,
        status=TaskStatus.TODO,
    ),
    TaskCreate(
        title='Estimate work effort',
        description='Provide time estimates for each major task.',
        priority=TaskPriority.MEDIUM,
        assignee='Lina',
        status=TaskStatus.TODO,
    ),
    TaskCreate(
        title='Design the board layout',
        description='Create the page structure and sample task card design.',
        priority=TaskPriority.MEDIUM,
        assignee='Jamie',
        status=TaskStatus.IN_PROGRESS,
    ),
    TaskCreate(
        title='Implement API validation',
        description='Add validation rules to ensure correct task payloads.',
        priority=TaskPriority.HIGH,
        assignee='Priya',
        status=TaskStatus.IN_PROGRESS,
    ),
    TaskCreate(
        title='Set up repository',
        description='Initialize the repo and verify directories are in place.',
        priority=TaskPriority.LOW,
        assignee='Alex',
        status=TaskStatus.DONE,
    ),
    TaskCreate(
        title='Confirm design tokens',
        description='Review color and spacing tokens used in the UI.',
        priority=TaskPriority.LOW,
        assignee=None,
        status=TaskStatus.DONE,
    ),
]

if __name__ == '__main__':
    # Reset in-memory storage (safe for dev/testing)
    try:
        storage._reset()
    except Exception:
        pass

    for t in sample_tasks:
        created = storage.add_task(t)
        print('Added:', created.id, created.title, created.status.value)

    print(f'Seed complete: {len(sample_tasks)} tasks')
