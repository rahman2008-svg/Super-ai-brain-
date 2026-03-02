from flask import Flask, render_template, request, jsonify
import sqlite3
import wikipedia
import os

# ======================
# Flask app setup
# ======================
app = Flask(__name__)
wikipedia.set_lang("bn")  # বাংলা Wikipedia

# ======================
# Database setup
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "super_ai.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            question TEXT PRIMARY KEY,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ======================
# Database functions
# ======================
def get_answer_from_db(question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT answer FROM knowledge WHERE question = ?",
        (question,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def save_answer_to_db(question, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO knowledge (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

# ======================
# Wikipedia fallback
# ======================
def get_answer_from_wikipedia(question):
    try:
        summary = wikipedia.summary(question, sentences=2)
        return summary + "\n\n📚 Source: Wikipedia"
    except:
        return None

# ======================
# Routes
# ======================
@app.route("/")
def home():
    return "✅ Super AI Brain is running!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "❌ প্রশ্ন দিতে হবে।"})

    # 1️⃣ Check database
    answer = get_answer_from_db(question)
    if answer:
        return jsonify({"answer": answer})

    # 2️⃣ Check Wikipedia
    wiki_answer = get_answer_from_wikipedia(question)
    if wiki_answer:
        return jsonify({"answer": wiki_answer})

    # 3️⃣ Nothing found
    return jsonify({"answer": "🤖 আমি এখনো জানি না। তুমি আমাকে শেখাতে পারো।"})

@app.route("/teach", methods=["POST"])
def teach():
    data = request.get_json()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()

    if not question or not answer:
        return jsonify({
            "status": "error",
            "message": "প্রশ্ন এবং উত্তর দুটোই দিতে হবে।"
        })

    save_answer_to_db(question, answer)
    return jsonify({
        "status": "success",
        "message": "✅ নতুন জ্ঞান সংরক্ষণ করা হয়েছে!"
    })

# ======================
# Run app (Render ready)
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
