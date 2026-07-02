from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as parse_date

def generate_schedule(tasks):
    """
    Intelligent scheduling engine:
    - Sorts tasks by priority (highest first), then by nearest deadline.
    - Sequentially allocates time slots starting from current time.
    - Identifies if a task conflicts (exceeds its deadline).
    """
    # Sort tasks: highest priority first, then closest deadline
    tasks = sorted(
        tasks,
        key=lambda x: (-x.priority, parse_date(x.deadline) if getattr(x, 'deadline', None) else datetime.max.replace(tzinfo=timezone.utc))
    )

    schedule = []
    # Start scheduling from the current time in UTC
    current_time = datetime.now(timezone.utc)

    for task in tasks:
        start = current_time
        end = start + timedelta(hours=task.estimated_hours)

        # Parse deadline safely
        try:
            deadline = parse_date(task.deadline)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
        except Exception:
            deadline = end + timedelta(days=1)  # Fallback

        # Conflict check: did we schedule it past its deadline?
        conflict = end > deadline

        schedule.append({
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "estimated_hours": task.estimated_hours,
            "deadline": task.deadline,
            "completed": task.completed,
            "google_event_id": task.google_event_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "conflict": conflict
        })

        current_time = end

    return schedule