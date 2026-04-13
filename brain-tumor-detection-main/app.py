from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Load the trained model
model = load_model("best_brain_tumor_model.keras")

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_tumor(image_path):
    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(256, 256), color_mode="grayscale")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype("float32") / 255.0
    
    # Make prediction
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = float(np.max(predictions) * 100)
    
    # Class labels and information
    class_labels = ["Glioma Tumor", "Meningioma Tumor", "No Tumor", "Pituitary Tumor"]
    
    tumor_info = {
        "Glioma Tumor": {
            "description": "Glioma is a type of tumor that occurs in the brain and spinal cord. Gliomas begin in the gluey supportive cells (glial cells) that surround nerve cells and help them function.",
            "symptoms": "Headaches, nausea, vomiting, seizures, memory loss, personality changes, weakness on one side of the body.",
            "treatment": "Treatment typically involves surgery to remove as much of the tumor as possible, followed by radiation therapy and chemotherapy."
        },
        "Meningioma Tumor": {
            "description": "Meningioma is a tumor that arises from the meninges — the membranes that surround the brain and spinal cord. Most meningiomas grow very slowly.",
            "symptoms": "Headaches, seizures, vision problems, hearing loss, memory problems, weakness in arms or legs.",
            "treatment": "Small, slow-growing meningiomas may not require immediate treatment. Options include surgery, radiation therapy, and in rare cases, chemotherapy."
        },
        "No Tumor": {
            "description": "No signs of brain tumor detected in the MRI scan. However, regular check-ups are recommended if you experience any neurological symptoms.",
            "symptoms": "N/A",
            "treatment": "Maintain a healthy lifestyle with regular exercise and balanced diet. Consult a doctor if you experience any unusual symptoms."
        },
        "Pituitary Tumor": {
            "description": "Pituitary tumors are abnormal growths that develop in the pituitary gland. Most are benign (noncancerous).",
            "symptoms": "Headaches, vision problems, nausea, vomiting, changes in weight, mood changes, hormonal imbalances.",
            "treatment": "Treatment may include surgery, radiation therapy, or medication to shrink the tumor or regulate hormone production."
        }
    }
    
    result = {
        "class": class_labels[predicted_class],
        "confidence": confidence,
        "info": tumor_info[class_labels[predicted_class]]
    }
    
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
             return render_template('predict.html', error="No file part in the request.")

        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('predict.html', error="No file selected.")

            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)


            # Make prediction
            result = predict_tumor(filepath)
            relative_path = 'uploads/' + filename

            
            return render_template('result.html', 
                                 result=result, 
                                 image_path=relative_path)
         # File is not allowed
        return render_template('predict.html', error="Invalid file type. Please upload a JPG or PNG image.")
    
    return render_template('predict.html')
    

if __name__ == '__main__':
    app.run(debug=True)
