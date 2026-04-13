# 🧠 Brain Tumor Detection using CNN and Flask

This project uses **Convolutional Neural Networks (CNN)** to detect brain tumors from MRI images. It classifies the tumor into four categories: **Glioma**, **Meningioma**, **Pituitary**, and **No Tumor**. The model is trained using TensorFlow and deployed using a Flask web application.

---

## 📁 Project Structure

brain-tumor-detection/
├── static/
│ └── styles.css
├── templates/
│ ├── index.html
│ └── result.html
├── model/
│ └── tumor_classifier.h5
├── tumor_info.py
├── app.py
├── utils.py
└── README.md

---

## 🧪 Model Overview

- **Input shape:** Grayscale MRI images of size `256x256`
- **Architecture:** Custom CNN with dropout, batch normalization
- **Classes:** `Glioma`, `Meningioma`, `Pituitary`, `No Tumor`
- **Frameworks:** TensorFlow, Keras
- **Training techniques:** Data Augmentation, Early Stopping, Model Checkpointing

---

## 🌐 Web App Features

- ✅ Upload MRI brain scan image
- ✅ Predict tumor type
- ✅ Show prediction confidence chart
- ✅ Display tumor information
- ✅ Fully responsive UI
- ✅ Tabbed layout for tumor details, chart, and architecture

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Zyaan27/brain-tumor-detection.git
cd brain-tumor-detection

2. Install Dependencies

pip install -r requirements.txt
Note: Make sure you have Python 3.7+ and TensorFlow installed.

3. Start the Flask App
python app.py
Then open your browser and go to: http://127.0.0.1:5000

🧠 Tumor Classes & Info
Each prediction includes tumor type and confidence, along with additional information:

Glioma: Cancer in glial cells

Meningioma: Tumor from meninges

Pituitary: Tumor in pituitary gland

No Tumor: Normal MRI scan

📈 Result Visualization
Includes:

📊 Probability bar chart

🧾 Tumor details

🧬 CNN architecture image

🧠 Image preview

🧰 Technologies Used
Python

TensorFlow / Keras

Flask

OpenCV / PIL

HTML + CSS + JavaScript

📂 Dataset
The model was trained on a publicly available dataset from Kaggle

🙋‍♂️ Author
Mohammed Zyaan C
📧 cmdzyaan27@gmail.com
📱 8072372498
🌍 Vellore, India

⭐ Acknowledgements
TensorFlow and Keras community

Kaggle dataset contributors

Flask documentation

OpenCV/Pillow for image processing






