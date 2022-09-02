import cv2
from keras.models import load_model
import numpy as np
import manual_rps as man
import time


class RPSGame:
    
    
    def __init__(self):
        
        self.model = load_model('keras_model.h5', compile = False)
        self.cap = cv2.VideoCapture(0)
        self.data = np.ndarray(shape = (1, 224, 224, 3), dtype = np.float32)
        
        self.countdown_started = False
        self.counter = 5
        self.countdown_ended = False
        self.start_of_tick = np.Inf
        
        self.computer_wins = 0
        self.player_wins = 0
        
        self.start_of_sign_tick = np.Inf
        self.hand_sign_updated = True
        self.current_hand_sign = 'Nothing'
        self.word_position_map = {'Rock' : 210, 'Paper' : 190, 'Scissors': 140, 'Nothing': 150}
    
    
    
    def update_picture(self):
        
        ret, frame = self.cap.read()
              
        if self.countdown_started:

            self.hand_sign_updated, self.start_of_sign_tick = self.metronome(self.hand_sign_updated, self.start_of_sign_tick, 0.3)
            
            if self.hand_sign_updated != 1:
                self.current_hand_sign = self.get_prediction()
                self.hand_sign_updated = 1
            
            cv2.putText(frame, str(self.counter), (250, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (200, 135, 255), 3, 2)
            cv2.putText(frame, self.current_hand_sign, (self.word_position_map[self.current_hand_sign], 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (200, 135, 255), 3, 2)
        
        cv2.imshow('Game', frame)
    
    
    
    def get_prediction(self):
        
        #Captures and modifies an image from the webcam, before feeding it into the model.
        ret, frame = self.cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1
        self.data[0] = normalized_image
        
        prediction = self.model.predict(self.data, verbose = 0)
        prediction_number = np.argmax(prediction)
        return man.reverse_sign_converter[prediction_number]
    
    
    
    #Metronome is intended to run continuously and modify a given "state" whenever a specific span of time has passed since a previous tick.
    def metronome(self, state, tick, span):
        
        if time.time() < tick + span:
            return (state, tick)
        
        else:
            return(state - 1, tick + span)
    
    
    
    def continue_round(self):
        
        if cv2.waitKey(1) == ord('q') and not self.countdown_started:
                    
            print('\nPrepare to choose!')
            self.start_of_tick = time.time()
            self.start_of_sign_tick = time.time()
            self.countdown_started = True
            
        if self.countdown_started:
                
            self.counter, self.start_of_tick = self.metronome(self.counter, self.start_of_tick, 1.3)
                
            if self.counter == 0:
                self.countdown_ended = True
        
        return
    
    
    
    def compute_round(self):
        
        player_choice = self.get_prediction()
                
        if player_choice == 'Nothing':
            
            print('Hand sign not detected. Round nullified.')
                    
        else:
                    
            computer_choice = man.get_computer_choice()
            print(f'Player chose {player_choice}, computer chose {computer_choice}.')
            result = man.get_winner(player_choice, computer_choice)
            print(result)
                    
            if result == 'Player wins round.':
                self.player_wins+=1
            if result == 'Computer wins round.':
                self.computer_wins+=1
        
        print(f'Computer has won {self.computer_wins} rounds.')
        print(f'You have won {self.player_wins}.')
        
        if self.computer_wins != 3 and self.player_wins != 3:
            print('Press q to start the countdown.')
    
    
    
    def play_game(self):
        
        print('\n\nWelcome to my Rock Paper Scissors game! Press q to start the countdown!')
        
        while True:
            
            self.update_picture()
            self.continue_round()
            
            if self.countdown_ended:
                self.compute_round()
                self.countdown_started = False
                self.counter = 5
                self.countdown_ended = False
            
            if self.computer_wins == 3:
                print('\nThe computer has won!\n')
                break
            
            if self.player_wins == 3:
                print('\nThe player has won!\n')
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        return



if __name__ == '__main__':
    player_match = RPSGame()
    player_match.play_game()