from flask import Flask,  flash, redirect, request, render_template, make_response, url_for
import json
import sys 
#import pandas as pd

app = Flask(__name__)

@app.route("/") 
def helloworld():
    return "Hello, World!"

@app.route("/name") 
def name():
    return "Chanachot Khamchum ID672110226"

if __name__ == "__main__":   # run code 
    app.run(host='localhost',debug=True,port=5001)