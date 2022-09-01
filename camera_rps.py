import cv2
from keras.models import load_model
import numpy as np
import manual_rps as man


model = load_model('keras_model.h5', compile=False)
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)



def get_prediction():
    
    #Captures and modifies an image from the webcam, before feeding it into the model.
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image
    
    prediction = model.predict(data)
    prediction_number = np.argmax(prediction)
    return man.reverse_sign_converter[prediction_number]



if __name__ == '__main__':

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            print(get_prediction())
            break
        
    cap.release()
    cv2.destroyAllWindows()
