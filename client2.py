import socket
import errno
import time
import random
from os import system


_ = system('clear')

# User will choose their nicknames
print("-------------------------------------------------------------------")
print("|            Welcome to the Snake and Ladder Game                  |") 
print("|                      Version: 1.0.0                              |")
print("|              Developed by: nurin,syaf,qila                       |")
print("-------------------------------------------------------------------")


print ("Name will display on server")
nickname = input("Choose your nickname: ")

# put the ip address of server and same socket to be conneting with the server side 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.253.3', 8888))

# this is for effect for delay effect for 1 second after performing of any action
WAIT  = 1
MAX_VAL = 50

# this is the value is when player get this value and they will go down as there will be snakes 
snakes = {
    21: 5,
    42: 20,
    49: 39,
}

# this is the value is when player get this value and they will go up as there will be stairs
ladders = {
    5: 43,
    10: 48,
    13: 48,
}


message_support_player = [
    "It is your turn",
    "Go ahead.",
    "Please proceed.",
    "Let's go ahead and win this together.",
    "Are you ready?, Here we go.",
    "",

]


snakeBite = [
    "Oops",
    "OMG !",
    "you got snake bite",
    "oh no !!",
    "auchhhhhh "
]


ladderPoint = [
    "Phew",
    "woww",
    "nailed it",
    "oh my God...",
    "yaayyy"
]



def welcome_msg():
#function  to welcome user to the program
    msg = """
    Welcome to Snake and Ladder Game.
   Rules:
      1. Initally both the players are at starting position i.e. 0. 
         Take it in turns to roll the dice. 
         Move forward the number of spaces shown on the dice.
      2. If you lands at the bottom of a ladder, you can move up to the top of the ladder.
      3. If you lands on the head of a snake, you must slide down to the bottom of the snake.
      4. The first player to get to the FINAL position is the winner.
      5. Hit enter to roll the dice.
    Snake          Ladder
    49 go to 39    5  go to 43
    42 go to 20    10 go to 48
    21 go to  5    13 go to 46
    """
    print(msg)

def UserDiceValue():
#function suspends (waits) execution of the current thread for a given number of seconds.
    time.sleep(WAIT)
    diceValue = random.randint(1,6)
    print("Its a " + str(diceValue))
    return diceValue


def got_snake_bite(old_value, current_value, player_name):
    print("\n" + random.choice(snakeBite).upper() + " ~~~~~~~~>")
    print("\n" + player_name + " got a snake bite. Down from " + str(old_value)+ " to " + str(current_value))

def got_ladder_jump(old_value, current_value, player_name):
    print("\n" + random.choice(ladderPoint).upper() + " ########")
    print("\n" + player_name + " climbed the ladder from " + str(old_value) + " to " + str(current_value))




def snake_ladder(player_name, current_value, diceValue):
    time.sleep(WAIT)
    old_value = current_value
    current_value = current_value + diceValue

    if current_value > MAX_VAL:
        print("You need " + str(MAX_VAL - old_value) + " to win this game. Keep trying,OKAY !" )
        return old_value

    print("\n" + player_name + " moved from " + str(old_value) + " to " + str(current_value))
    if current_value in snakes:
        final_value = snakes.get(current_value)
        got_snake_bite(current_value, final_value, player_name)

    elif current_value in ladders:
        final_value = ladders.get(current_value)
        got_ladder_jump(current_value, final_value, player_name)

    else:
        final_value = current_value

    return final_value

# messages when the player win the games
# request if player want to play the game
def check_win(player_name, position):
    time.sleep(WAIT)
    if MAX_VAL == position:
        print("\n\n\nThats it.\n\n" + player_name + " won the game.")
        print("Congratulations " + player_name)
        print("\nThank you for playing the game.\n\n")
        again=input("\nDo you want to play again? (y/n) ")
        if again == 'n':
           sys.exit(1)

#gamestart
def startgame():
    while True:
        try:
            # Receive Message From Server
            # If 'USER' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(nickname.encode('ascii'))
            else:
                 time.sleep(WAIT)
                 player_name = nickname
                 time.sleep(WAIT)
                 player_current_position = 0
                 round = 0
                 while True:
                      welcome_msg()
                      time.sleep(WAIT)
                      print("Round:")
                      print(round)
                      print("\nCurrent position :")
                      print(player_current_position)
                      input_1 = input("\n" + player_name + ": " + random.choice(message_support_player) + " Press the "enter" key for the roll dice: ")
                      print("\nRolling dice...")
                      diceValue = UserDiceValue()
                      time.sleep(WAIT)
                      print(player_name + " moving....")
                      player_current_position = snake_ladder(player_name, player_current_position, diceValue)
                      time.sleep(3)
                      round=round+1


                      check_win(player_name, player_current_position)

                      _ = system('clear')

        except socket.error as e:
           print (str(e))
           sys.exit()


startgame()
