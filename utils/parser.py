import re
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def guess_time_slot(text):
    time_labels = ["morning", "afternoon", "evening", "night", "any"]
    result = classifier(text, time_labels, multi_label=False)
    slot = result["labels"][0] if result["scores"][0] > 0.4 else "any"
    if slot == "night":
        slot = "evening"
    return slot

def parse_goals(goal_text):
    raw_text = goal_text.strip()
    text_lower = raw_text.lower()
    duration = None
    unit_match = re.search(r'(\d+)\s*(hour|hr|h)', text_lower)
    non_time_units = re.search(r'\b(pages?|chapters?|articles?)\b', text_lower)

    if unit_match:
        duration = int(unit_match.group(1))
    elif non_time_units:
        duration = 1

    freq_match = re.search(r'(\d+)\s*(x|times)', text_lower)
    times = int(freq_match.group(1)) if freq_match else None

    if not times:
        if duration and duration >= 3:
            times = min(duration, 5)
        else:
            times = 1

    if not duration:
        duration = times

    per_session = round(duration / times, 2)

    time_slot = guess_time_slot(text_lower)
    
    if "every evening" in text_lower:
        times = 7
        time_slot = "evening"
    elif "every morning" in text_lower:
        times = 7
        time_slot = "morning"
    elif "every afternoon" in text_lower:
        times = 7
        time_slot = "afternoon"


    constraint = None
    before_match = re.search(r"before (\w+)", text_lower)
    after_match = re.search(r"after (\w+)", text_lower)
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    only_day_match = re.search(r"every (\w+)", text_lower)

    if before_match and after_match:
        constraint = f"conflict_before_{before_match.group(1)}_after_{after_match.group(1)}"
    elif before_match:
        constraint = f"before_{before_match.group(1)}"
    elif after_match:
        constraint = f"after_{after_match.group(1)}"
    elif "not on weekends" in text_lower:
        constraint = "no_weekends"
    elif only_day_match:
        possible_day = only_day_match.group(1).lower()
        if possible_day in day_names:
            constraint = f"only_{possible_day}"

    task = raw_text
    task = re.sub(r'\d+\s*(hours?|hrs?|h|times?|x|chapters?|pages?)', '', task, flags=re.IGNORECASE)
    task = re.sub(r'\b(once|twice|thrice|every)\b', '', task, flags=re.IGNORECASE)
    task = re.sub(r'\b(in the|at the)?\s*(morning|afternoon|evening|night)', '', task, flags=re.IGNORECASE)
    task = re.sub(r'not on weekends|before \w+|after \w+|only \w+', '', task, flags=re.IGNORECASE)
    task = re.sub(r'\bbut\b', '', task, flags=re.IGNORECASE)
    task = re.sub(r'\s+', ' ', task).strip("-• ")
    task = task.capitalize() if task else "Unnamed task"

    return {
        "task": task,
        "times": times,
        "total_hours": duration,
        "per_session": per_session,
        "slot": time_slot,
        "constraint": constraint
    }
