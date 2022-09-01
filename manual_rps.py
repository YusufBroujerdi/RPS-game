import random


get_computer_choice = lambda: random.choice(['Rock', 'Paper', 'Scissors'])
get_user_choice = lambda: input('Please choose between Rock, Paper or Scissors: ')
sign_converter = {'Rock' : 0, 'Paper' : 1, 'Scissors' : 2}
reverse_sign_converter = ['Rock', 'Paper', 'Scissors', 'Nothing']
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