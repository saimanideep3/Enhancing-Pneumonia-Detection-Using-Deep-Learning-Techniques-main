import os
import sqlite3
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load_model('pneumonia_detection_model.h5')

# Define upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure the database exists
def init_db():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        sex TEXT,
        place TEXT,
        filename TEXT,
        prediction TEXT,
        probability REAL
    )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize the database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    place = request.form.get('place')

    print(f"DEBUG: Received - Name: {name}, Age: {age}, Sex: {sex}, Place: {place}")

    # Check if file exists
    if 'file' not in request.files:
        print("DEBUG: No file part")
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        print("DEBUG: No selected file")
        return 'No selected file'

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image
        img = load_img(filepath, target_size=(224, 224))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0) / 255.0

        # Predict result
        prediction = model.predict(img)
        probability = float(prediction[0][0])  

        # Debugging output
        print(f"DEBUG: Raw Prediction Value: {prediction}")
        print(f"DEBUG: Probability: {probability}")

        # Determine class label
        result = 'Pneumonia' if probability > 0.5 else 'Normal'
        print(f"DEBUG: Final Prediction: {result}")

        # Store in database
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO predictions (name, age, sex, place, filename, prediction, probability) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, age, sex, place, filename, result, probability))
        conn.commit()
        conn.close()

        # Render result page
        return render_template('result.html', name=name, age=age, sex=sex, place=place, result=result, probability=probability, filename=filename)
    


@app.route('/saved_data')
def saved_data():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()

    print("DEBUG: Sending Data to Template ->", data)  # Debugging output in the terminal

    return render_template('history.html', data=list(data))


if __name__ == '__main__':
    app.run(debug=True)
