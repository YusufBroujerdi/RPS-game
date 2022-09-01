import cv2
from keras.models import load_model
import numpy as np
import manual_rps as man
import time


model = load_model('keras_model.h5', compile=False)
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def update_picture():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)



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



def metronome(counter, start_of_tick):
    if time.time() < start_of_tick + 1.7:
        return counter, start_of_tick
    else:
        print(counter - 1)
        return counter - 1, start_of_tick + 1.7
    


if __name__ == '__main__':
    
    key_pressed = False
    countdown_ended = False
    counter = 6
    
    
    while True:
        
        update_picture()
        
        if cv2.waitKey(1) == ord('q'):
            print('Prepare to choose!')
            key_pressed = True
            start_of_tick = time.time()

        if key_pressed == True:
            
            counter, start_of_tick = metronome(counter, start_of_tick)
            if counter == 0:
                countdown_ended = True
        
        if countdown_ended == True:
            print(get_prediction())
            break
    
    
    cap.release()
    cv2.destroyAllWindows()