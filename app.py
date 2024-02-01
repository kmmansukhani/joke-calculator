import re
from flask import Flask, request, render_template
import openai

app = Flask(__name__)
openai.api_key = "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"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_joke")
def create_joke_input():
    return render_template("create_joke_input.html")

@app.route("/evaluate_joke")
def evaluate_joke_input():
    return render_template("evaluate_joke_input.html")

@app.route("/explain_joke")
def explain_joke_input():
    return render_template("explain_joke_input.html")


@app.route("/create_joke_result", methods=["POST"])
def create_joke():
    context = request.form["context"]
    prompt = f"Create a joke about {context}: "
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=1.0,
    )
    joke = completion.choices[0].text
    return render_template("create_joke_result.html", joke=joke)

@app.route("/evaluate_joke_result", methods=["POST"])
def evaluate_joke():
    setup = request.form["setup"]
    punchline = request.form["punchline"]
    prompt = '''
    Pretend like you have a decent sense of humor. How funny is the following joke (1-10) and why. Make the explanation funny. 
    Format your response like the following:
    Rating: x/10
    Explanation: ...
    '''
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + setup + " " + punchline,
        max_tokens=1024,
        temperature=1.0,
    )
    response = completion.choices[0].text
    response_lines = response.split("\n")
    if len(response_lines) < 4:
        rating = "0/10"
        explanation = "Put some more effort into this."
    else:
        rating = response_lines[2].strip()  # 'Rating: 8/10'
        explanation = response_lines[3].strip()  # 'Explanation: I laughed far more than I probably should have, and my neighbours thought I was going crazy!'
        rating = rating.split(":")[1].strip()  # '8/10'
        explanation = explanation.split(":")[1].strip()  # 'I laughed far more than I probably should have, and my neighbours thought I was going crazy!'
    return render_template("evaluate_joke_result.html", rating=rating, explanation=explanation)
@app.route("/explain_joke_result", methods=["POST"])
def explain_joke():
    print("here")
    setup = request.form["setup"]
    punchline = request.form["punchline"]
    prompt = '''
    Explain the joke "''' + setup + ''' ''' + punchline + '''" in a funny way.
    '''
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=1.0,
    )
    explanation = completion.choices[0].text
    return render_template("explain_joke_result.html", explanation=explanation)
