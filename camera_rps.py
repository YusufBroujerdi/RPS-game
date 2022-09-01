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
        self.key_pressed = False
        self.counter = 6
        self.countdown_ended = False
        self.start_of_tick = np.Inf
        self.computer_wins = 0
        self.player_wins = 0



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



    def metronome(self):
        if time.time() < self.start_of_tick + 1.7:
            return
        else:
            print(self.counter - 1)
            self.counter -= 1
            self.start_of_tick += 1.7



    def continue_round(self):
        
        if cv2.waitKey(1) == ord('q'):
                    
            print('Prepare to choose!')
            self.start_of_tick = time.time()
            self.key_pressed = True
            
        if self.key_pressed:
                
            self.metronome()
                
            if self.counter == 0:
                self.countdown_ended = True
        
        return



    def play_game(self):
        
        
        while True:
            
            
            self.update_picture()
            self.continue_round()
            
            
            if self.countdown_ended:
                player_choice = self.get_prediction()
                
                if player_choice == 'Nothing':
                    print('Hand sign not detected. Round nullified.')
                    
                else:
                    
                    computer_choice = man.get_computer_choice()
                    print(f'Player chose {player_choice}, computer chose {computer_choice}')
                    result = man.get_winner(player_choice, computer_choice)
                    print(result)
                    
                    if result == 'Player wins round':
                        self.player_wins+=1
                    if result == 'Computer wins round':
                        self.computer_wins+=1
                
                self.key_pressed = False
                self.counter = 6
                self.countdown_ended = False
                print(f'computer has won {self.computer_wins} rounds')
                print(f'You have won {self.player_wins}')
            
            
            if self.computer_wins == 3:
                print('The computer has won!')
                break
            
            
            if self.player_wins == 3:
                print('The player has won!')
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        return



player_match = RPSGame()
player_match.play_game()