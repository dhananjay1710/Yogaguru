import joblib

def run_rf(angles):
    model = joblib.load("models/random_forest.joblib")
    angles_num = []
    for key in angles:
        angles_num.append(angles[key])
    prediction_angles = []
    prediction_angles.append(angles_num)
    output = model.predict(prediction_angles)
    poses = ['Goddess', 'Half Moon', 'Tree', 'Triangle', 'Warrior2']
    predicted_pose = poses[output[0]]
    return predicted_pose
