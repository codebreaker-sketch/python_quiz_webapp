from flask import Flask, request, redirect, url_for, render_template_string
import webbrowser
import threading

app = Flask(__name__)

class Quiz:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.user_name = ""
        self.records = []

    def add_question(self, question, answer):
        self.questions.append((question, answer))

    def reset(self):
        self.score = 0

quiz = Quiz()
quiz.add_question("What is the Currency of Turkey?", "Lira")
quiz.add_question("What is 2 + 2?", "4")
quiz.add_question("What is the chemical symbol for water?", "H2O")
quiz.add_question("Who wrote 'The Call of the Marching Bell'?", "Allama Iqbal")
quiz.add_question("Capital of Sirilanka is?", "Colombo")

@app.route('/')
def index():
    return redirect(url_for('get_username'))

@app.route('/username', methods=['GET', 'POST'])
def get_username():
    if request.method == 'POST':
        quiz.user_name = request.form['username']
        return redirect(url_for('take_quiz', question_num=0))
    
    username_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enter Username</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #F0FFF0;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: #20B2AA;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 80%;
                max-width: 400px;
                text-align: center;
            }
            h1 {
                margin-top: 0;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                width: calc(100% - 22px);
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                autocomplete: off;
            }
            button {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 4px;
            }
            button:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Enter Your Username</h1>
            <form method="post">
                <input type="text" name="username" required autocomplete="off">
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(username_template)

@app.route('/quiz/<int:question_num>', methods=['GET', 'POST'])
def take_quiz(question_num):
    if question_num >= len(quiz.questions):
        return redirect(url_for('result'))

    question, answer = quiz.questions[question_num]
    if request.method == 'POST':
        user_answer = request.form['answer']
        if user_answer.lower() == answer.lower():
            quiz.score += 1
        return redirect(url_for('take_quiz', question_num=question_num + 1))
    
    quiz_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quiz</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #F0FFF0;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: #20B2AA;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 80%;
                max-width: 800px;
                display: flex;
                justify-content: space-between;
            }
            .question-container {
                width: 70%;
            }
            .score-container {
                width: 25%;
                border-left: 2px solid #ddd;
                padding-left: 20px;
            }
            h1, h2 {
                margin-top: 0;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                width: calc(100% - 22px);
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                autocomplete: off;
            }
            button {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                border-radius: 4px;
            }
            button:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="question-container">
                <h1>Question {{ question_num + 1 }}</h1>
                <p>{{ question }}</p>
                <form method="post">
                    <input type="text" name="answer" required autocomplete="off">
                    <button type="submit">Submit</button>
                </form>
            </div>
            <div class="score-container">
                <h2>Score</h2>
                <p>Current Score: {{ score }}</p>
                <p>Total Questions: {{ total_questions }}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(quiz_template, question=question, question_num=question_num, score=quiz.score, total_questions=len(quiz.questions))

@app.route('/result')
def result():
    score = quiz.score
    total_questions = len(quiz.questions)
    quiz.records.append((quiz.user_name, score))
    quiz.reset()
    
    result_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Result</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #FFDAB9;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: #98FB98;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 80%;
                max-width: 800px;
                text-align: center;
            }
            h1 {
                margin-top: 0;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 4px;
            }
            a:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Quiz Result</h1>
            <p>{{ username }}, your score is: {{ score }} out of {{ total_questions }}</p>
            <h2>Previous Records</h2>
            <ul>
                {% for name, record in records %}
                    <li>{{ name }}: {{ record }}</li>
                {% endfor %}
            </ul>
            <a href="/">Take the quiz again</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(result_template, username=quiz.user_name, score=score, total_questions=total_questions, records=quiz.records)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start a thread to open the browser
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
