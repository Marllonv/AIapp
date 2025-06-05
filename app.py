import os
import pickle
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# Caminho para o modelo treinado
MODEL_PATH = ''

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)