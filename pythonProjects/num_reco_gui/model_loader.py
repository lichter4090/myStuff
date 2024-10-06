import numpy as np
from tensorflow.keras.models import load_model


class Model:
    def __init__(self, model_file_path):
        self.model = load_model(model_file_path)
        self.last_number = None
        self.confidence = None

    def predict_image(self, lst_of_pixels: list):
        if len(lst_of_pixels) != 28 * 28:
            raise RuntimeError("Image is not ", 28 * 28)

        if not any(lst_of_pixels):  # if all values are 0
            self.last_number = None
            return

        image = np.array([lst_of_pixels])

        probabilities = self.model.predict(image)
        self.last_number = np.argmax(probabilities)
        self.confidence = np.max(probabilities)

    def get_predicted_num(self):
        return self.last_number

    def get_confidence(self):
        return self.confidence
