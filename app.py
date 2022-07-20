from flask import Flask

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def index():
    return 'INDEX PAGE'

if __name__ == "__main__":
    app.run(debug=True)