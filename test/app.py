from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    print(url_for('static',filename='styles/custom.css'))
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, allow_unsafe_werkzeug=True)