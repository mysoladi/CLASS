import imp
from flask import Flask, render_template
import csv

app = Flask(__name__)

with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.Dictreader(csvfile)
    dinosaurs = {row['Slug']:{'name':row['name'], 'description': row['description'], 'image': row['image'], 'image-credit': row['image-credit'], 'source-url': row['source-url'], 'source-credit': row['source-credit']} for row in data}


@app.route('/')
def hiindex():
    return render_template('index.html', dinosaurs=dinosaurs)