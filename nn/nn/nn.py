import os

from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
from io import BytesIO

import numpy as np


LIBRARY_PATH = os.path.dirname(__file__)
MODEL_PATH = os.path.join(LIBRARY_PATH, 'model.h5')


class ImageClassifier:
    def __init__(self):
        self.model = load_model(MODEL_PATH)
        self.model._make_predict_function()

    def score(self, img):
        img = Image.open(BytesIO(img)).convert('RGB').resize((64, 64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.
        res = self.model.predict(img)
        return 1 - res[0][0]