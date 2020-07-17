
##############################################################################################################
##############################################################################################################
##############################################################################################################
##########          ###          ####  ##  ##  ##         ###         ########################################
##############  #######  ######  ####  ##  ##  ##  ##########  #####  ########################################
##############  #######  ######  ####  ##  ##  ##         ###         ########################################
##############  #######  ######  ####  ##  ##  ##  ##########  ##   ##########################################
##############  #######          #####        ###         ###  ####   ########################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

##############################################################################################################
##############################################################################################################
##############################################################################################################
###########       ####  ########       ##       ##        ##         ###         #############################
###########  ####  ###  ########  ###  ##  ##########  #####  ##########  #####  #############################
###########      #####  ########       ##       #####  #####         ###         #############################
###########  ####  ###  ########  ###  #######  #####  #####  ##########  ##   ###############################
###########       ####        ##  ###  ##       #####  #####         ###  ####   #############################
##############################################################################################################
##############################################################################################################
##############################################################################################################




print("Tower Blaster MultiPlayer Clone - Python TUI Client Made By Huzaifa Irfan")



##############################################################################################################
#########################################  User Configurations ###############################################
##############################################################################################################


####################
# Get User Name from the User
####################

username=input("Enter Your Name??\n")




#importing Server Address from Conf
# serveraddress='http://localhost:3050/'
from conf import serveraddress







####################
#Importing
####################
from os import system,name
import time



####################
# import Socketio client
####################

import socketio

sio = socketio.Client()








##############################################################################################################
#########################################  Main Menu Function  ###############################################
##############################################################################################################
   

####################
# The Main Menu Function
####################

def menu():
    exit=False

    while(not exit):
        clearscreen()
        print("C. Create Game")
        print("J. Join Game")
        print("H. Help")
        print("X. Exit Game")
        ch=input("Enter Letters to Start")
        if ch=="c"or ch=="C":
            exitter("Creating Game")
            sio.emit('getdifficulties')
            exit=True
        elif ch=="H" or ch=="h":
            clearscreen()
            print("Stack Numbers in Increasing order Smaller at top and Larger at Bottom to Win")
            exitter("To Main Menu")
        elif ch=="j" or ch=="J":
            exitter("Fetching Games")
            sio.emit('fetchgames')
            exit=True
        elif ch=="x"or ch=="X":
            sio.disconnect()
            exit=True
            exitter("Bye Bye")
        else:
            exitter("Please Choose from Above")




##############################################################################################################
#########################################  some useful func for TUI  #########################################
##############################################################################################################

####################
# some useful func for TUI
####################

def clearscreen():

        # for windows 
    if name == 'nt': 
        system('cls') 
        print("\n")

    # for mac and linux(here, os.name is 'posix') 
    else: 
        system('clear') 
        print("\n")

    print("Tower Blaster MultiPlayer Clone - Python TUI Client Made By Huzaifa Irfan")

def exitter(msg):
    print(msg)
    input("Return")




####################
# Ask a Number With Highest Number range
####################

def asknumrange(msg,high):
	anum=None
	while(anum==None):
		try:
			anum=int(input(msg))
		except:
			print(f"Number required (from 1-{high})")
			continue

		if (anum <1 or anum >high):
			print(f"Write a Number (from 1-{high})")
			anum=None

	return anum








##############################################################################################################
#########################################  SocketIO Event Listeners  #########################################
##############################################################################################################



####################
# Got the Difficulty Level List for server
####################

@sio.event
def senddifficulties(levels):
    
    for i in range(0,len(levels)):

        print(i+1,":",levels[i]["name"],"Range:",levels[i]["low"],"-",levels[i]["high"],"Tower Height:",levels[i]["towerheight"],"Questions:",levels[i]["getagain"])

    num=asknumrange("Select Difficulty ID",len(levels))
    #num = 1-range len(levels) included
    sio.emit('creategame',num)




####################
# First Connection Established Message
####################

@sio.event
def connect():
    print(sio.sid)
    print('Connection established')
    menu()



####################
#new game Created by User
####################

@sio.event
def gamecreated():
    clearscreen()
    print("Game created")
    print("Waiting for Player to Join")


####################
# The user with Game ID is not Free
####################

@sio.event
def notfree(player1name):
    clearscreen()
    exitter(f"{player1name} Not Free")
    menu()


####################
# Opponent Left COmmand
####################

@sio.event
def opponentleft(opponentname):
    clearscreen()
    exitter(f"{opponentname} left the game.")
    menu()


####################
# The Main Loading and Display Function
####################

@sio.event
def loadinggame(loader):
    clearscreen()
    print(loader["yourname"],"Playing Game with",loader["opponentname"])


    space="                                             "
    
    print(loader["opponentname"],space,loader["yourname"])
    print("Score:",loader["opponentscore"],space,"Score:",loader["yourscore"],"\n")

    i=1
    for item in loader["game"]:
        print("    X",space,i,":",item)
        i=i+1

    print("\n")

    print("Questions left:" ,loader["getagain"])

    if(loader["turn"]==True):
        print("Your Turn",loader["yourname"])

        print("Running : ",loader["running"])


        if(loader["getagain"]>0):
            askq=input("Want to use Question? y / N")
            if askq=="y"or askq=="Y":
                sio.emit('getquestion')
            else:
                num=asknumrange("Select your Height",(i-1))
                sio.emit('changetower',num)

        else:
            num=asknumrange("Select your Height",(i-1))
            sio.emit('changetower',num)





    else:
        print(loader["opponentname"]," Turn")








    
####################
# Go to Main Menu after sending Other Person
####################

@sio.event
def tomainmenu():
    clearscreen()
    menu()



####################
# Play Again Asker
####################


def playagain():
    print("Do you want to play Again? Y/n ")
    ans=input("")
    if ans=="n"or ans=="N":
        sio.emit('noplay')
    else:
        sio.emit('playagain')
        print("Waiting for other Player to Respond!!")



####################
# User Win Situation
####################

@sio.event
def winner(obj):
    clearscreen()
    print("You Win")

    space="                                             "
    
    print(obj["opponentname"],space,obj["yourname"])

    height= len(obj["yourgame"])

    for i in range(0,height):
        print(obj["opponentgame"][i],space,obj["yourgame"][i])

    print("\n")

    playagain()


####################
# User Lose Situation
####################

@sio.event
def looser(obj):
    clearscreen()
    print("You Lose")

    space="                                             "
    
    print(obj["opponentname"],space,obj["yourname"])

    height= len(obj["yourgame"])

    for i in range(0,height):
        print(obj["opponentgame"][i],space,obj["yourgame"][i])

    print("\n")

    playagain()





####################
# Showing any Free Games Available
####################

@sio.event
def showgames(freegames):
    clearscreen()
    print("Free Games")
    # print(freegames)
    if len(freegames)>0:

        for i in range(0,len(freegames)):
            print(i+1,":",freegames[i]["creator"],freegames[i]["difficulty"]["name"],"Range:",freegames[i]["difficulty"]["low"],"-",freegames[i]["difficulty"]["high"]," Tower Height:",freegames[i]["difficulty"]["towerheight"]," Questions:",freegames[i]["difficulty"]["getagain"])
        
        gamenum=asknumrange("Enter Game ID",len(freegames))

        #send the game id of the user
        sio.emit('joingame', freegames[gamenum-1]["gameid"])



    else:
        menu()





####################
# Disconnected from The Server
####################

@sio.event
def disconnect():
    print('Disconnected from server')










##############################################################################################################
#########################################  The Socket Connection and Waiting  ################################
##############################################################################################################






clearscreen()




####################
# Connecting to SocketIO Server
####################

sio.connect(serveraddress)

####################
# Sending UserName First
####################

sio.emit('Connection', username)





####################
# Wait LOOP
####################

sio.wait()

exitter("Exiting the Game")