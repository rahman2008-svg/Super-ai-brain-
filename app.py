# app.py
import os
from flask import Flask

# Flask app তৈরি
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Super AI App is running 🚀"

# Optional: অন্য route
@app.route("/about")
def about():
    return "This is a demo AI app built with Flask!"

# Main execution: Render expects the port via env variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render PORT assign করবে
    app.run(host="0.0.0.0", port=port, debug=True)
