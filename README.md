# 🧠 AI Weekly Planner

An intelligent weekly planner that takes free-text goals and automatically generates a smart, constraint-aware schedule for your week. Built with Python, Transformers, and Streamlit.

---

## 🧩 Features

✅ Natural Language Task Parsing (via Hugging Face Transformers)  
✅ Supports day-specific constraints (e.g., "before Thursday", "every Tuesday")  
✅ Respects preferred time slots (morning, afternoon, evening)  
✅ Schedules recurring tasks (e.g., "Workout every morning")  
✅ Avoids time conflicts and daily overload (8h max/day)  
✅ Skips logically impossible constraints (e.g., "before Wednesday after Friday")   
✅ Clear visual schedule and terminal debug output

---

## 📥 Example Input
Workout every morning

Read 200 pages before Thursday

Go to gym 3x not on weekends

Check LinkedIn every Tuesday

Write blog before Wednesday after Friday

Study ML 40 hours

Do react project every evening

Study math every evening

Write blog every evening


---

## 📅 Example Output

🗓️ Weekly Schedule (by Time Slot)
    
    Monday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Read (1.0h)
    
    Evening:
    Go to gym (1.0h)
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Tuesday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Go to gym (1.0h)
    
    Evening:
    Check linkedin tuesday (1.0h)
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Wednesday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Go to gym (1.0h)
    
    Evening:
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Thursday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Rest
    
    Evening:
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Friday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Rest
    
    Evening:
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Saturday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Rest
    
    Evening:
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)
    
    Sunday
    Morning:
    Workout (1.0h)
    
    Afternoon:
    Rest
    
    Evening:
    Do react project (1.0h)
    Study math (1.0h)
    Write blog (1.0h)


## 🚀 How to Run

```bash
git clone https://github.com/YOUR_USERNAME/ai-weekly-planner.git
cd ai-weekly-planner
pip install -r requirements.txt
streamlit run app.py



