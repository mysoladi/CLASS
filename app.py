import imp
from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

DINO_PATH = app.root_path + '/dinosaurs.csv'
DINO_KEYS = ['slug', 'name', 'description', 'image', 'image-credit', 'source-url', 'source-credit']

with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinosaurs = {row['slug']:{'name':row['name'], 'description': row['description'], 'image': row['image'], 'image-credit': row['image-credit'], 'source-url': row['source-url'], 'source-credit': row['source-credit']} for row in data}


@app.route('/')
@app.route('/dino')
@app.route('/dino/<dino>')
def index(dino = None):
    if dino and dino in dinosaurs.keys():
        dinosaur = dinosaurs[dino]
        return render_template('dino.html', dinosaur = dinosaur)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)

# with open("top10.csv", 'r') as csvfile:
#     data = csv.DictReader(csvfile)
#     dinos = [{row['rank']:{'name':row['name'], 'votes': row['votes']} for row in data}]

# @app.route('/favorites')
# def favorite():
#     return render_template('favorite.html', dinos=dinos)

@app.route('/about')
def about():
    return render_template('about.html')



def get_dinos():
    try:
        with open(DINO_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            dinosaurs = {}
            for dino in data:
                dinosaurs[dino['slug']] = dino
    except Exception as e:
        print(e)
    return dinosaurs

def set_dinos(dinosaurs):
    try:
        with open(DINO_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=DINO_KEYS)
            writer.writeheader()
            for dino in dinosaurs.values():
                writer.writerow(dino)
    except Exception as err:
        print(err)

@app.route('/add-dino', methods =['GET', 'POST'])
def add_dino():
    if request.method == 'POST':
        dinosaurs = get_dinos()
        newDino = {}

        newDino['slug'] = request.form['slug']
        newDino['name'] = request.form['name']
        newDino['description'] = request.form['description']
        newDino['image'] = request.form['image']
        newDino['image-credit'] = request.form['image-credit']
        newDino['source-url'] = request.form['source-url']
        newDino['source-credit'] = request.form['source-credit']

        return redirect(url_for('index'))

    else:
        return render_template('add-dino.html')




@app.route('/dino-quiz', methods =['GET', 'POST'])
def dino_quiz():
    if request.method == 'POST':

        quizguesses = {}
        quizguesses['q1'] = request.form['continents']
        quizguesses['q2'] = request.form.getlist('dinosaur')
        quizguesses['q3'] = request.form['eggs']
        quizguesses['q4'] = request.form['extinct']

        quizguesses['q2'] =  " and ".join(quizguesses['q2'])

        quizAnswers = {
            'q1' : 'North America',
            'q2' : 'Triceratops and Stegosaurus',
            'q3' : 'true',
            'q4' : '66'
        }

        return render_template('quiz-results.html', quizguesses = quizguesses, quizAnswers = quizAnswers)
    
    else:
        return render_template('dino-quiz.html')