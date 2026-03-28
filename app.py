from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"
# LOGIN PAGE
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect('/dashboard')
    return render_template("login.html")


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# CHATBOT
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    reply = ""
    emotion = ""
    style = ""

    if request.method == 'POST':
        user_input = request.form['message']
        text = user_input.lower()

        # 🎭 Emotion Detection
        if "sad" in text or "stress" in text or "frustrated" in text:
            emotion = "sad"
            style = "Supportive"
        elif "happy" in text or "excited" in text or "good" in text:
            emotion = "happy"
            style = "Energetic"
        else:
            emotion = "neutral"
            style = "Teaching"

        # 🧠 Topic Detection + Smart Reply
        if "python" in text:
            session['topic'] = "python"
            reply = "Python is a simple programming language used for web development, AI, and more."

        elif "loop" in text:
            session['topic'] = "loop"
            reply = "A loop is used to repeat a block of code multiple times."

        elif "data structure" in text:
            session['topic'] = "ds"
            reply = "Data structures are used to store and organize data efficiently."

        elif "exam" in text:
            session['topic'] = "general"
            reply = "Try studying in small parts and revise regularly for better results."

        elif "how are you" in text:
            session['topic'] = "general"
            reply = "I'm doing great 😊 I'm here to help you learn!"

        else:
            session['topic'] = "general"
            reply = "That's a great question! Try breaking it into smaller parts and we’ll learn step by step."

        # 🎯 Emotion-based Tone Adjustment
        if emotion == "sad":
            reply = "Don't worry 😊 I’ll help you.\n\n" + reply
        elif emotion == "happy":
            reply = "Great energy! 🚀\n\n" + reply

    return render_template("chatbot.html", reply=reply, emotion=emotion, style=style)
# QUIZ
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    topic = session.get('topic', 'general')
    question = ""
    answer_correct = ""
    result = ""

    # 🎯 Set question based on topic
    if topic == "python":
        question = "What is Python?"
        answer_correct = "language"

    elif topic == "loop":
        question = "What is a loop used for?"
        answer_correct = "repeat"

    elif topic == "ds":
        question = "What do data structures do?"
        answer_correct = "organize"

    else:
        question = "2 + 2 = ?"
        answer_correct = "4"

    # 🎯 Check answer
    if request.method == 'POST':
        user_answer = request.form['answer'].lower()

        if answer_correct in user_answer:
            result = "Correct!"
        else:
            result = "Wrong answer!"

    return render_template("quiz.html", question=question, result=result)
app.run(debug=True)