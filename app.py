from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import tensorflow as tf
from PIL import Image
from io import BytesIO

app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1


def funcPredict(model, img):
    target_size = (256, 256)
    img = img.resize(target_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    pred = model.predict(img_array)

    pred_class_index = np.argmax(pred[0])
    class_labels = [
        "Apple",
        "Banana",
        "avocado",
        "cherry",
        "kiwi",
        "mango",
        "orange",
        "pinenapple",
        "strawberries",
        "watermelon",
    ]
    pred_class = class_labels[pred_class_index]
    confidence = round(100 * np.max(pred[0]), 2)

    return pred_class, confidence


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/after", methods=["POST"])
def after():
    img = request.files["file1"]
    img.save("static/file.jpg")
    img_path = "static/file.jpg"
    model_path = "static/csfruits.h5"  # เปลี่ยนเครื่องหมาย \ เป็น / เพื่อให้เหมาะสมกับทุกแพลตฟอร์ม

    if not os.path.exists(model_path):
        return "Model file not found", 404

    model = load_model(model_path, compile=False)
    img = image.load_img(img_path, target_size=(256, 256))
    predicted_class, confidence = funcPredict(model, img)

    return render_template(
        "prediction.html", prediction=predicted_class, confidence=confidence
    )


@app.route("/get_predict", methods=["POST"])
def get_predict():
    img_data = request.files["file"].read()
    img = Image.open(BytesIO(img_data))
    model_path = "static/csfruits.h5"  # เปลี่ยนเครื่องหมาย \ เป็น / เพื่อให้เหมาะสมกับทุกแพลตฟอร์ม

    if not os.path.exists(model_path):
        return "Model file not found", 404

    model = load_model(model_path, compile=False)
    img = img.resize((256, 256))
    predicted_class, confidence = funcPredict(model, img)

    return jsonify({"prediction": predicted_class, "confidence": confidence})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
