from flask import Flask, render_template, redirect, request, session
from hash import hash_pw, check_pw

app = Flask(__name__)
app.secret_key = 'chs2022'

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)