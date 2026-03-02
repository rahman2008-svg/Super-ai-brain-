from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# Example API route: search Wikipedia
@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "")
    try:
        summary = wikipedia.summary(query, sentences=2)
        return jsonify({"result": summary})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Host 0.0.0.0 makes it accessible in Render/any server
    app.run(host="0.0.0.0", port=5000, debug=True)
