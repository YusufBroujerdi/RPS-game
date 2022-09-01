# RPS Game

> The Goal of this project is to create a Rock-Paper-Scissors game that reads the player's hand sign in play.

## Milestone 1

- I began by setting up a GitHub repo.

## Milestone 2

- For this milestone, I created a machine learning model that can read one of three hand signs - "rock", "paper", or "scissors" (or "nothing"). I did this through google's accessible "teachable machine" web-based tool.

## Milestone 3

- This milestone involved setting up a virtual environment. In other words, I used the package manager conda to create a virtual environment, then installed the needed packages within this environment. In practice, I ran the following commands:

```bash
conda create --name rps_environment
conda activate rps_environment
conda install pip
pip install opencv-python
pip install tensorflow
pip install ipykernel'''

The first 2 commands create and go into the new rps_environment. The latter 4 commands install the package manager pip then install the needed packages through pip.

I also downloaded the model I created in milestone 2 and checked it worked fine using the file RPS-Template.py provided by AiCore. This file sets up a camera to read hand signs, feeds the camera's data to the model, then collects the results from the model and stores them in the List called "prediction".

## Milestone 4

- I finally began writing python code. I wrote the code for the file manual_rps.py:

'''python
import random


get_computer_choice = lambda: random.choice(['Rock', 'Paper', 'Scissors'])
get_user_choice = lambda: input('Please choose between Rock, Paper or Scissors: ')
sign_converter = {'Rock' : 0, 'Paper' : 1, 'Scissors' : 2}
victory_converter = ['Draw', 'User wins', 'Computer wins']



def get_winner(user_choice, computer_choice):
    user_number = sign_converter[user_choice]
    computer_number = sign_converter[computer_choice]
    return victory_converter[(user_number - computer_number) % 3]



def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    
    if user_choice not in sign_converter:
        print("Invalid choice. Game aborted.")
        return
    
    print(f'Computer chose {computer_choice}')
    print(get_winner(user_choice, computer_choice))



if __name__ == '__main__':
    play()
'''

get_computer_choice and get_user_choice are fairly self-explanatory lambda functions. sign_converter and victory_converter are used for the get_winner function. Essentially, due to the circular nature of how rock, paper and scissors counter one another, we can use modulo arithmetic to circumvent the need for a massive list of if-elif-else statements for each of the 9 possible configurations. We could have even written get_winner as a single-line lambda function, but I thought this would be too ugly to read.

Some minor flow control was added to play() in the event the user enters an invalid string. Though this will likely be superfluous given the fact the final inputs will come from a camera.
