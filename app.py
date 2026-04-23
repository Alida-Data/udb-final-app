from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Assistant IA UDB - Backend Ready"

if __name__ == "__main__":
    app.run()
