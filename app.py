from flask import Flask, render_template, request, jsonify
import sqlite3
import wikipedia
import os

# Flask app
app = Flask(__name__)
wikipedia.set_lang("bn")  # বাংলা Wikipedia

DB_PATH = "super_ai.db"

# DB থেকে answer fetch
def get_answer_from_db(question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT answer FROM knowledge WHERE question=?", (question,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# DB-তে answer save
def save_answer_to_db(question, answer):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

# Wikipedia থেকে answer
def get_answer_from_wikipedia(question):
    try:
        summary = wikipedia.summary(question, sentences=2)
        return summary + "\n\nSource: Wikipedia 📚"
    except:
        return None

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "প্রশ্ন দিতে হবে।"})
    
    answer = get_answer_from_db(question)
    if answer:
        return jsonify({"answer": answer})
    
    wiki_answer = get_answer_from_wikipedia(question)
    if wiki_answer:
        return jsonify({"answer": wiki_answer})

    return jsonify({"answer": "আমি এখনো জানি না। তুই আমাকে শিখিয়ে দে।"})

@app.route("/teach", methods=["POST"])
def teach():
    data = request.get_json()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    if not question or not answer:
        return jsonify({"status": "error", "message": "Question ও Answer দিতে হবে।"})
    
    save_answer_to_db(question, answer)
    return jsonify({"status": "success", "message": "শেখানো সম্পন্ন!"})

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
