import streamlit as st
from utils.parser import parse_goals
from utils.scheduler import distribute_tasks

st.set_page_config(page_title="AI Weekly Planner", layout="centered")
st.title("📅 AI Weekly Planner (NLP-Powered)")

user_input = st.text_area("Enter your weekly goals (1 per line):", height=200, placeholder="""
Examples:
- Workout every morning
- Study Python 6 hours
- Go jogging 3x not on weekends
- Check LinkedIn every Tuesday
- Write blog before Wednesday after Friday
""")

if st.button("Generate Weekly Plan"):
    goals = user_input.strip().splitlines()
    parsed_tasks = []

    print("\n📄 Parsed Task Logs:")
    for goal in goals:
        if goal.strip():
            parsed = parse_goals(goal)
            parsed_tasks.append(parsed)
            print(parsed)

    weekly_plan = distribute_tasks(parsed_tasks)

    st.subheader("🗓️ Weekly Schedule (by Time Slot)")
    for day, slots in weekly_plan.items():
        st.markdown(f"### **{day}**")
        for slot, task_list in slots.items():
            st.write(f"**{slot}:**")
            for task in task_list:
                st.markdown(f"- {task}")
