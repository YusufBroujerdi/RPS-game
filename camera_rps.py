import cv2
from keras.models import load_model
import numpy as np
import manual_rps as man
import time

class RPSGame:
    
    def __init__(self):
        
        self.model = load_model('keras_model.h5', compile=False)
        self.cap = cv2.VideoCapture(0)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.key_pressed


    def update_picture(self):
        ret, frame = self.cap.read()
        cv2.imshow('frame', frame)



    def get_prediction(self):
        
        #Captures and modifies an image from the webcam, before feeding it into the model.
        ret, frame = self.cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1
        self.data[0] = normalized_image
        
        prediction = self.model.predict(self.data)
        prediction_number = np.argmax(prediction)
        return man.reverse_sign_converter[prediction_number]



    def metronome(counter, start_of_tick):
        if time.time() < start_of_tick + 1.7:
            return counter, start_of_tick
        else:
            print(counter - 1)
            return counter - 1, start_of_tick + 1.7



    def continue_round(key_pressed, counter, countdown_ended):
        
        if cv2.waitKey(1) == ord('q'):
                    
            print('Prepare to choose!')
            start_of_tick = time.time()
            key_pressed = True
            
        if key_pressed:
                
            counter, start_of_tick = metronome(counter, start_of_tick)
                
            if counter == 0:
                get_prediction()
                countdown_ended = True
        
        return key_pressed, counter, countdown_ended



    def play_game():
        
        key_pressed = False
        counter = 6
        countdown_ended = False
        computer_wins = 0
        player_wins = 0
        
        
        while True:
            
            
            update_picture()
            key_pressed, counter, countdown_ended = continue_round(key_pressed, counter, countdown_ended)
            
            
            if countdown_ended:
                player_choice = get_prediction()
                
                if player_choice == 'Nothing':
                    print('Hand sign not detected. Round nullified.')
                    
                else:
                    result = man.get_winner(player_choice, man.get_computer_choice())
                    print(result)
                    if result == 'Player wins round':
                        player_wins+=1
                    if result == 'Computer wins round':
                        computer_wins+=1
                
                key_pressed = False
                counter = 6
                countdown_ended = False
                print(f'computer has won {computer_wins} rounds')
                print(f'You have won {player_wins}')
            
            
            if computer_wins == 3:
                print('The computer has won!')
                break
            
            
            if player_wins == 3:
                print('The player has won!')
                break
        
        
        return



play_game()
cap.release()
cv2.destroyAllWindows()