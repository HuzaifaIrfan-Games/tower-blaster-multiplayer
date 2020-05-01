
from os import system
import time

def clearscreen():
    system("cls")
    print("Tower Blaster MultiPlayer Clone - Python TUI Client")

def exitter(msg):
    print(msg)
    input("Return")





import socketio

sio = socketio.Client()

username=input("Enter Your Name??\n")
# username="player"


            



def menu():
    exit=False





    while(not exit):
        clearscreen()
        print("C. Create Game")
        print("J. Join Game")
        print("X. Exit Game")
        ch=input("Enter Number to Start")
        if ch=="c"or ch=="C":
            exitter("Creating Game")
            sio.emit('getdifficulties')
            exit=True
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






@sio.event
def senddifficulties(levels):
    
    for i in range(0,len(levels)):

        print(i+1,":",levels[i]["name"],"Range:",levels[i]["low"],"-",levels[i]["high"],"Tower Height:",levels[i]["towerheight"],"Questions:",levels[i]["getagain"])

    num=asknumrange("Select Difficulty ID",len(levels))

    sio.emit('creategame',num)



@sio.event
def connect():
    print(sio.sid)
    print('Connection established')
    menu()



@sio.event
def gamecreated():
    clearscreen()
    print("Game created")
    print("Waiting for Player to Join")




@sio.event
def notfree(player1name):
    clearscreen()
    exitter(f"{player1name} Not Free")
    menu()


@sio.event
def opponentleft(opponentname):
    clearscreen()
    exitter(f"{opponentname} left the game.")
    menu()


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



@sio.event
def nextturn(gameobj):
    clearscreen()
    


@sio.event
def tomainmenu():
    clearscreen()
    menu()


def playagain():
    print("Do you want to play Again? Y/n ")
    ans=input("")
    if ans=="n"or ans=="N":
        sio.emit('noplayagain')
    else:
        sio.emit('playagain')
        print("Waiting for other Player to Respond!!")


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




@sio.event
def showgames(freegames):
    clearscreen()
    print("Free Games")
    # print(freegames)
    if len(freegames)>0:

        for i in range(0,len(freegames)):
            print(i+1,":",freegames[i]["creator"],freegames[i]["difficulty"]["name"],freegames[i]["difficulty"]["low"],"-",freegames[i]["difficulty"]["high"]," Tower Height:",freegames[i]["difficulty"]["towerheight"]," Questions:",freegames[i]["difficulty"]["getagain"])
        
        gamenum=asknumrange("Enter Game ID",len(freegames))

        sio.emit('joingame', freegames[gamenum-1]["gameid"])



    else:
        menu()







@sio.event
def disconnect():
    print('Disconnected from server')




clearscreen()

sio.connect('http://localhost:5000/')

sio.emit('Connection', username)






sio.wait()

exitter("Exiting the Game")