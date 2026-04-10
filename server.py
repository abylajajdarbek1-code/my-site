from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'faces'

# ===== Басты бет =====
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

# ===== Жүктеу =====
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    name = request.form.get("name")

    if file and name:
        filename = f"{name}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

    return redirect('/')

# ===== ӨШІРУ =====
@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect('/')

app.run(debug=True)