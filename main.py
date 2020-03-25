from flask import Flask, render_template

@app.route('/')
def home():
    return "hello_world"