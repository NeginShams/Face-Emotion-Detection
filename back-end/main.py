

from flask import Flask, jsonify
from flask import request
import numpy as np
import cv2
import tensorflow as tf
import os
#import matplotlib.pyplot as plt

# FACE_DETECTOR_PATH = "{base_path}/haarcascade_frontalface_default.xml".format(
#     base_path=os.path.abspath(os.path.dirname(__file__)))


app = Flask(__name__)



people = [
    {
        'name': 'Negin',
        'last_name': 'Shams'
    },
    {
        'name': 'Negar',
        'last_name': 'Shams'
    }
]


@app.route('/people')
def get_people():
    return jsonify({'people': people})


@app.route('/post_person', methods=['POST'])
def add_person():
    # print(request.data)

    #frame  = np.array(request.get_json())
    #img_float32 = np.float32(frame)

    data = request.json
    # print(data)
    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    frame = np.array(data['arr'], dtype='uint8')
    # print(frame.shape)
    # print(frame)
    #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # print("*************************************")
    #img_float32 = np.float32(frame)

    model = tf.keras.models.load_model('fer_final.h5')
    #model = tf.keras.models.load_model('fer3.h5')
    #model = tf.keras.models.load_model('transfer_model.h5')
    # print(model.summary())

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print("*************************************")
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    #print('Found {} faces!'.format(len(faces)))
    if len(faces) == 0:
        return "face not detected"
    # print(type(faces))
    # print(faces)
    # print(faceCascade)
    # print(len(faces))
    # print("*************************************")
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        facess = faceCascade.detectMultiScale(roi_gray)
        if len(faces) == 0:
            return "face not detected"
        else:
            for (ex, ey, ew, eh) in facess:
                face_roi = roi_color[ey: ey+eh, ex:ex + ew]

    try:
        final_image = cv2.resize(face_roi, (224, 224))
        final_image = np.expand_dims(final_image, axis=0)
        Predictions = model.predict(final_image)

    except:
        return "face not detected"
    # print(np.argmax(Predictions))

    if np.argmax(Predictions) == 0:
        return "angry"

    if np.argmax(Predictions) == 1:
        return "disgust"

    if np.argmax(Predictions) == 2:
        return "fear"

    if np.argmax(Predictions) == 3:
        return "happy"

    if np.argmax(Predictions) == 4:
        return "neutral"

    if np.argmax(Predictions) == 5:
        return "sad"

    if np.argmax(Predictions) == 6:
        return "surprise"

        # return jsonify(request.get_json())


app.run(port=5000)
