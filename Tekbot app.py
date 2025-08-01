from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load study materials
with open('data/materials.json') as f:
    study_materials = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message").lower()

    if "lecture" in user_input or "exam" in user_input:
        return jsonify({"response": get_reminders()})
    elif "material" in user_input or "notes" in user_input:
        return jsonify({"response": get_materials()})
    elif "school info" in user_input or "knust" in user_input:
        return jsonify({"response": "KNUST is one of the leading science and tech universities in Ghana. You can check their portal at https://apps.knust.edu.gh."})
    else:
        return jsonify({"response": "Hi! I'm TekBot 🤖. Ask me about KNUST, lectures, exams, or study materials."})

def get_reminders():
    try:
        with open('reminders.json') as f:
            reminders = json.load(f)
        today = datetime.now().strftime("%Y-%m-%d")
        today_reminders = [r for r in reminders if r["date"] == today]
        if today_reminders:
            return "\n".join([f"{r['type'].title()} - {r['title']} at {r['time']}" for r in today_reminders])
        else:
            return "No reminders for today 🎉"
    except:
        return "No reminders set."

def get_materials():
    output = ""
    for course, links in study_materials.items():
        output += f"\n📘 {course}:\n"
        for link in links:
            output += f" - {link}\n"
    return output.strip()

if __name__ == '__main__':
    app.run(debug=True)
