from flask import Flask, render_template, request, jsonify, session
from chatbot import answer_with_context

app = Flask(__name__)
app.secret_key = 'some_secret_key_for_sessions'  # Required for session management

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"]
    
    # Retrieve previous history from session
    history = session.get("history", {"prev": None, "prev2": None})

    # Get response from chatbot
    response = answer_with_context(user_input, history)

    # Update session history
    history["prev2"] = history.get("prev")
    history["prev"] = {"question": user_input, "answer": response}
    session["history"] = history

    return jsonify({"response": response})

@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = {"prev": None, "prev2": None}
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
