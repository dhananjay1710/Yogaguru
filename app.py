from flask import Flask, render_template, request, url_for
from flask.globals import session
from werkzeug.utils import redirect
import os
from utils.calculateAngle import calculate_angle
from utils.runCNN import run_cnn
from utils.runOpenpose import run_openpose 
from utils.calculateDifferences import calculate_differences
from utils.calculateScore import calculate_score
from utils.runRf import run_rf
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fsupload')
def upload_fs():
    return render_template('fsUpload.html')

@app.route('/fstry', methods = ['GET', 'POST'])
def try_fs():
    user_img = request.files['user_image']
    curr_idx = len(os.listdir('static/UserUpload/test'))
    user_img_name = 'user_' + str(curr_idx) + '.jpg'
    session['user_img_name'] = user_img_name
    session['curr_idx'] = curr_idx
    user_img.save(os.path.join('static/UserUpload/test', user_img_name))
    return redirect(url_for('run_fs'))

@app.route('/fsrun')
def run_fs():
    input_pose = run_cnn()
    pose_coordinates = run_openpose(session['user_img_name'])
    input_angles = calculate_angle(pose_coordinates)
    f = open("AngleValues/angles.json")
    angle_dict = json.load(f)
    ideal_angles = angle_dict[input_pose]
    diff_matrix = calculate_differences(input_angles, ideal_angles)
    score = calculate_score(diff_matrix)
    session['pose'] = input_pose
    session['score'] = score
    return redirect(url_for('display'))


@app.route('/lwupload')
def upload_lw():
    return render_template('lwUpload.html')

@app.route('/lwtry', methods = ['GET', 'POST'])
def try_lw():
    user_img = request.files['user_image']
    curr_idx = len(os.listdir('static/UserUpload/test'))
    user_img_name = 'user_' + str(curr_idx) + '.jpg'
    session['user_img_name'] = user_img_name
    session['curr_idx'] = curr_idx
    user_img.save(os.path.join('static/UserUpload/test', user_img_name))
    return redirect(url_for('run_lw'))

@app.route('/lwrun')
def run_lw():
    pose_coordinates = run_openpose(session['user_img_name'])
    input_angles = calculate_angle(pose_coordinates)
    input_pose = run_rf(input_angles)
    f = open("AngleValues/angles.json")
    angle_dict = json.load(f)
    ideal_angles = angle_dict[input_pose]
    diff_matrix = calculate_differences(input_angles, ideal_angles)
    score = calculate_score(diff_matrix)
    session['pose'] = input_pose
    session['score'] = score
    return redirect(url_for('display'))
    
@app.route('/display')
def display():
    return render_template('display.html', img_name = session['user_img_name'], score = session['score'], pose = session['pose'])

if __name__ == '__main__':
    app.run()