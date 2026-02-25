from datetime import datetime, timedelta

def generate_schedule(tasks):
    """
    Simple intelligent scheduler:
    - Sort by priority (high first)
    - Then by nearest deadline
    - Assign sequential time slots
    """

    tasks = sorted(
        tasks,
        key=lambda x: (-x.priority, x.deadline)
    )

    schedule = []
    current_time = datetime.now()

    for task in tasks:
        start = current_time
        end = start + timedelta(hours=task.estimated_hours)

        schedule.append({
            "task": task.title,
            "start": start,
            "end": end,
            "deadline": task.deadline
        })

        current_time = end

    return schedule