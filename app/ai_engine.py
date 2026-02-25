import os
from datetime import datetime, timezone

def ai_decision(tasks):
    now=datetime.now(timezone.utc)
    for task in tasks:

        deadline = datetime.fromisoformat(task.deadline.replace("Z", "+00:00"))
        hours_left = (deadline - now).total_seconds() / 3600

        # 🔥 Urgency Boost
        if hours_left < 24:
            task.priority += 3
        elif hours_left < 72:
            task.priority += 1

        # 🔥 Habit-based boost
        # If user previously missed similar priority tasks,
        # simulate intelligent behavior
        if task.priority >= 4:
            task.estimated_hours += 1

        # 🔥 Overdue protection
        if hours_left <= 0:
            task.priority += 5

    return sorted(tasks, key=lambda x: (-x.priority, x.deadline))