import random

def distribute_tasks(task_list):
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    slots = ["Morning", "Afternoon", "Evening"]
    daily_hour_limit = 8

    weekly_plan = {day: {slot: [] for slot in slots} for day in week}
    daily_totals = {day: 0.0 for day in week}
    daily_tasks = {day: set() for day in week}

    def is_valid_day(day, constraint):
        if constraint == "no_weekends" and day in ["Saturday", "Sunday"]:
            return False
        if constraint and constraint.startswith("before_"):
            cutoff = constraint.split("_")[1].capitalize()
            if week.index(day) >= week.index(cutoff):
                return False
        if constraint and constraint.startswith("after_"):
            cutoff = constraint.split("_")[1].capitalize()
            if week.index(day) <= week.index(cutoff):
                return False
        if constraint and constraint.startswith("only_"):
            allowed = constraint.split("_")[1].capitalize()
            return day == allowed
        return True

    def has_conflict(constraint):
        return constraint and constraint.startswith("conflict_")

    for task in task_list:
        if task["times"] == 7 and task["slot"].lower() in slots:
            for day in week:
                if not is_valid_day(day, task.get("constraint")):
                    continue
                if daily_totals[day] + task["per_session"] > daily_hour_limit:
                    continue
                slot = task["slot"].capitalize()
                if task["task"] in daily_tasks[day]:
                    continue
                entry = f"{task['task']} ({task['per_session']}h)"
                weekly_plan[day][slot].append(entry)
                daily_tasks[day].add(task["task"])
                daily_totals[day] += task["per_session"]
            task["scheduled"] = True

    for task in task_list:
        if task.get("scheduled"):
            continue
        if has_conflict(task.get("constraint", "")):
            print(f"⚠️ Skipping unschedulable task: {task['task']} — conflicting constraints")
            continue

        assigned = 0
        times = task["times"]
        slot_pref = task.get("slot", "any").capitalize()
        constraint = task.get("constraint")

        valid_options = [
            (day, slot)
            for day in week if is_valid_day(day, constraint)
            for slot in slots
            if slot_pref == "Any" or slot == slot_pref
        ]

        valid_options.sort(key=lambda x: len(weekly_plan[x[0]][x[1]]))

        for day, slot in valid_options:
            if assigned >= times:
                break
            if daily_totals[day] + task["per_session"] > daily_hour_limit:
                continue
            if task["task"] in daily_tasks[day]:
                continue
            entry = f"{task['task']} ({task['per_session']}h)"
            weekly_plan[day][slot].append(entry)
            daily_tasks[day].add(task["task"])
            daily_totals[day] += task["per_session"]
            assigned += 1

        if assigned < times:
            print(f"⚠️ Could not schedule all sessions for: {task['task']} — Assigned {assigned}/{times}")

    for day in week:
        for slot in slots:
            if not weekly_plan[day][slot]:
                weekly_plan[day][slot].append("Rest")

    return weekly_plan
