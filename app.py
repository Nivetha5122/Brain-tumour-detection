from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ==============================
# LOAD MODEL
# ==============================
MODEL_PATH = "model/tumor_classifier.h5"

if not os.path.exists(MODEL_PATH):
    print("Model file not found! Check path:", MODEL_PATH)
    exit()

model = load_model(MODEL_PATH)
print(" Model loaded successfully!")

# ==============================
# PRINT ACCURACY IN CMD
# ==============================
try:
    test_path = "dataset/test"   # ⚠️ CHANGE if needed

    if not os.path.exists(test_path):
        raise Exception("Test dataset folder not found!")

    test_gen = ImageDataGenerator(rescale=1/255.0)

    test_set = test_gen.flow_from_directory(
        test_path,
        target_size=(128, 128),
        batch_size=32
    )

    loss, acc = model.evaluate(test_set, verbose=1)

    print("\n====== MODEL ACCURACY ======")
    print(f"Test Accuracy : {acc*100:.2f}%")
    print(f"Test Loss     : {loss:.4f}")
    print("============================\n")

except Exception as e:
    print("Accuracy check failed:", e)

# ==============================
# CONFIGURATION
# ==============================
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# HELPER FUNCTIONS
# ==============================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_tumor(image_path):
    try:
        img = image.load_img(image_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = float(np.max(predictions) * 100)

        class_labels = ["Glioma Tumor", "Meningioma Tumor", "No Tumor", "Pituitary Tumor"]

        # Print in CMD
        print("\n====== PREDICTION RESULT ======")
        print(f"Predicted Class : {class_labels[predicted_class]}")
        print(f"Confidence      : {confidence:.2f}%")
        print("================================\n")

        tumor_info = {
            "Glioma Tumor": {
                "description": "Tumor in brain/spinal cord",
                "symptoms": "Headaches, seizures",
                "treatment": "Surgery, chemo, radiation"
            },
            "Meningioma Tumor": {
                "description": "Tumor in brain membranes",
                "symptoms": "Vision issues, headaches",
                "treatment": "Surgery/radiation"
            },
            "No Tumor": {
                "description": "No tumor detected",
                "symptoms": "None",
                "treatment": "Not required"
            },
            "Pituitary Tumor": {
                "description": "Hormone-related tumor",
                "symptoms": "Vision, hormonal imbalance",
                "treatment": "Medication/surgery"
            }
        }

        return {
            "class": class_labels[predicted_class],
            "confidence": round(confidence, 2),
            "info": tumor_info[class_labels[predicted_class]]
        }

    except Exception as e:
        print(" Prediction Error:", str(e))
        return None


# ==============================
# ROUTES
# ==============================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        if 'file' not in request.files:
            return render_template('predict.html', error="No file uploaded")

        file = request.files['file']

        if file.filename == '':
            return render_template('predict.html', error="No file selected")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            result = predict_tumor(filepath)

            if result is None:
                return render_template('predict.html', error="Prediction failed")

            return render_template(
                'result.html',
                result=result,
                image_path='uploads/' + filename
            )

        return render_template('predict.html', error="Invalid file type")

    return render_template('predict.html')


# ==============================
# RUN APP
# ==============================
if __name__ == '__main__':
    print("\n Flask App Running...")
    app.run(debug=True)