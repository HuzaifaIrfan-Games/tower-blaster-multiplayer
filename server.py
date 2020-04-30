

port=5000

print("Tower Blaster Multiplayer Clone Server")
import time
import random


from flask import Flask, render_template, session, request,jsonify, send_from_directory, \
copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect


async_mode = None

app = Flask(__name__, static_url_path='')
import logging
logss = logging.getLogger('werkzeug')
logss.disabled = True

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)





users={}

games={}


difficulty={"high":40,"low":1,"getagain":5}



def makegame(gotgameid):
    #generate game
    print("Generating Game")

    global difficulty

    gen=list(range(difficulty["low"],difficulty["high"]+1))

    each=10

    #gen for player 1

    p1game=[]

    for i in range(0,each):
        num=random.choice(gen)
        p1game.append(num)
        gen.remove(num)

    games[gotgameid]["game"]["player1"]["game"]=p1game

    games[gotgameid]["game"]["player1"]["getagain"]=difficulty["getagain"]


    #gen for player 2
    p2game=[]

    for i in range(0,each):
        num=random.choice(gen)
        p2game.append(num)
        gen.remove(num)

    games[gotgameid]["game"]["player2"]["game"]=p2game

    games[gotgameid]["game"]["player2"]["getagain"]=difficulty["getagain"]


    games[gotgameid]["game"]["remaining"]=gen



def getarandom(gotgameid):
    gen=games[gotgameid]["game"]["remaining"]
    num=random.choice(gen)
    gen.remove(num)
    games[gotgameid]["game"]["remaining"]=gen
    return num


@socketio.on('Connection')
def Connection(username):
    global users
    userobj={"userid":request.sid,"username":username,"connected":True,"opponent":None,"gameid":None}
    users[request.sid]=userobj
    # print(users)
    # emit("sendgame",{"players":players,"gameplay":gameplay},broadcast=True)



@socketio.on('creategame')
def creategame():
    global users
    global games
    gameid=str(random.getrandbits(128))

    users[request.sid]["gameid"]=gameid

    gameobj={"gameid":gameid,"creator":users[request.sid]["username"],"player1":request.sid,"p1again":None,"player2":None,"p2again":None,"game":None}
    games[gameid]=gameobj
    # print(users)
    emit("gamecreated")




@socketio.on('fetchgames')
def fetchgames():
    global games
    freegames=[]
    for game in games.values():
        if game["player2"]==None:
            freegames.append(game)

    emit("showgames",freegames)




@socketio.on('noplayagain')
def noplayagain():
    global games
    global users

    senderid=request.sid
    opponentid=users[request.sid]["opponent"]
    gotgameid=users[request.sid]["gameid"]

    users[opponentid]["gameid"]=None
    users[opponentid]["opponent"]=None

    users[senderid]["gameid"]=None
    users[senderid]["opponent"]=None

    emit("opponentleft",users[request.sid]["username"],room=opponentid)

    emit("tomainmenu",room=senderid)

    
    if games[gotgameid]["player1"]==senderid:
        games[gotgameid]["p1again"]=False

    if games[gotgameid]["player2"]==senderid:
        games[gotgameid]["p2again"]=False





@socketio.on('playagain')
def playagain():
    global games
    global users
    
    senderid=request.sid
    opponentid=users[request.sid]["opponent"]
    if not (users[request.sid]["gameid"]==None):
        gotgameid=users[request.sid]["gameid"]


        
        if games[gotgameid]["player1"]==senderid:
            games[gotgameid]["p1again"]=True

        if games[gotgameid]["player2"]==senderid:
            games[gotgameid]["p2again"]=True

        print(games[gotgameid])
        if ((games[gotgameid]["p1again"]==True) and (games[gotgameid]["p2again"]==True)):
            games[gotgameid]["p1again"]=None
            games[gotgameid]["p2again"]=None



            #refresh gameplay
            makegame(gotgameid)
            


#send their own game to players
            emit("loadinggame",{"yourname":games[gotgameid]["game"]["player1"]["username"],"yourscore":games[gotgameid]["game"]["player1"]["score"],"game":games[gotgameid]["game"]["player1"]["game"],"opponentname":games[gotgameid]["game"]["player2"]["username"],"opponentscore":games[gotgameid]["game"]["player2"]["score"],"turn":games[gotgameid]["game"]["player1"]["turn"],"getagain":games[gotgameid]["game"]["player1"]["getagain"]}  ,room=games[gotgameid]["player1"])
            emit("loadinggame",{"yourname":games[gotgameid]["game"]["player2"]["username"],"yourscore":games[gotgameid]["game"]["player2"]["score"],"game":games[gotgameid]["game"]["player2"]["game"],"opponentname":games[gotgameid]["game"]["player1"]["username"],"opponentscore":games[gotgameid]["game"]["player1"]["score"],"turn":games[gotgameid]["game"]["player2"]["turn"],"getagain":games[gotgameid]["game"]["player2"]["getagain"]}  ,room=games[gotgameid]["player2"])




# def chkdelpearl(gotgameid,gameplay,row,n):
#     global games
#     leftinrow=0
#     for item in gameplay[row-1]:
#         if item==1:
#             leftinrow= leftinrow+1
    
#     if leftinrow>=n:
#         tempgameplay=gameplay
#         removed=0
#         temprow=gameplay[row-1]
#         length=len(temprow)
#         for i in range(0,length):
#             if removed < n:
#                 if temprow[i]==1:
#                     temprow[i]=0
#                     removed= removed+1

        
#         tempgameplay[row-1]=temprow
#         games[gotgameid]["game"]["gameplay"]=tempgameplay

#         left=0
#         for arow in tempgameplay:
#             for item in arow:
#                 if item==1:
#                     left=left+1
        
#         if left<=1:
#             return 1


#     return 0







# @socketio.on('removepearls')
# def removepearls(obj):
#     global games
#     global users
#     senderid=request.sid
#     gotgameid=users[senderid]["gameid"]
    
#     # print(obj)
#     gameplay=games[gotgameid]["game"]["gameplay"]





#     if games[gotgameid]["player1"]==senderid:
#         #sender is player1
#         if games[gotgameid]["game"]["player1"]["turn"]==True:
#             #its player1 turn
#             win=chkdelpearl(gotgameid,gameplay,obj["row"],obj["pearls"])

#             # change turns
#             games[gotgameid]["game"]["player1"]["turn"] = not games[gotgameid]["game"]["player1"]["turn"]
#             games[gotgameid]["game"]["player2"]["turn"] = not games[gotgameid]["game"]["player2"]["turn"]


#             if win==1:
#                 games[gotgameid]["game"]["player1"]["score"]=games[gotgameid]["game"]["player1"]["score"]+1
#                 emit("winner" ,room=games[gotgameid]["player1"])
#                 emit("looser" ,room=games[gotgameid]["player2"])



#             else:

#                 #emit next turn
#                 emit("nextturn",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player2"]["username"],"turn":games[gotgameid]["game"]["player1"]["turn"]}  ,room=games[gotgameid]["player1"])
#                 emit("nextturn",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player1"]["username"],"turn":games[gotgameid]["game"]["player2"]["turn"]}  ,room=games[gotgameid]["player2"])







#     if games[gotgameid]["player2"]==senderid:
#         #sender is player2
#         if games[gotgameid]["game"]["player2"]["turn"]==True:
#             #its player2 turn
#             win=chkdelpearl(gotgameid,gameplay,obj["row"],obj["pearls"])

#             # change turns
#             games[gotgameid]["game"]["player1"]["turn"] = not games[gotgameid]["game"]["player1"]["turn"]
#             games[gotgameid]["game"]["player2"]["turn"] = not games[gotgameid]["game"]["player2"]["turn"]

#             if win==1:
#                 games[gotgameid]["game"]["player2"]["score"]=games[gotgameid]["game"]["player2"]["score"]+1
#                 emit("winner" ,room=games[gotgameid]["player2"])
#                 emit("looser" ,room=games[gotgameid]["player1"])




#             else:

#                 #emit next turn
#                 emit("nextturn",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player2"]["username"],"turn":games[gotgameid]["game"]["player1"]["turn"]}  ,room=games[gotgameid]["player1"])
#                 emit("nextturn",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player1"]["username"],"turn":games[gotgameid]["game"]["player2"]["turn"]}  ,room=games[gotgameid]["player2"])













@socketio.on('joingame')
def joingame(gotgameid):
    global games
    global users

    if games[gotgameid]["player2"]==None:
        games[gotgameid]["player2"]=request.sid
        users[request.sid]["gameid"]=gotgameid
        users[request.sid]["opponent"]=games[gotgameid]["player1"]
        users[games[gotgameid]["player1"]]["opponent"]=games[gotgameid]["player2"]


        # game creation
        games[gotgameid]["game"]={"gameid":gotgameid,"player1":{"username":users[games[gotgameid]["player1"]]["username"],"score":0,"turn":False,"game":[]},"player2":{"username":users[games[gotgameid]["player2"]]["username"],"score":0,"turn":True,"game":[]}}
        makegame(gotgameid)

        games[gotgameid]["running"]=getarandom(gotgameid)

        #send their own game to players

        emit("loadinggame",{"yourname":games[gotgameid]["game"]["player1"]["username"],"yourscore":games[gotgameid]["game"]["player1"]["score"],"game":games[gotgameid]["game"]["player1"]["game"],"opponentname":games[gotgameid]["game"]["player2"]["username"],"opponentscore":games[gotgameid]["game"]["player2"]["score"],"turn":games[gotgameid]["game"]["player1"]["turn"],"getagain":games[gotgameid]["game"]["player1"]["getagain"]}  ,room=games[gotgameid]["player1"])
        emit("loadinggame",{"yourname":games[gotgameid]["game"]["player2"]["username"],"yourscore":games[gotgameid]["game"]["player2"]["score"],"game":games[gotgameid]["game"]["player2"]["game"],"opponentname":games[gotgameid]["game"]["player1"]["username"],"opponentscore":games[gotgameid]["game"]["player1"]["score"],"turn":games[gotgameid]["game"]["player2"]["turn"],"getagain":games[gotgameid]["game"]["player2"]["getagain"]}  ,room=games[gotgameid]["player2"])




    

    else:
        emit("notfree",games[gotgameid]["creator"])








@socketio.on('disconnect')
def disconnected():
    global users
    global games
    users[request.sid]["connected"]=False
    print(users[request.sid]["username"],"Disconnected")

    opponentid=users[request.sid]["opponent"]
    gameid=users[request.sid]["gameid"]

    if not(gameid == None):
        games[gameid]["player2"]="noone"
    if not(opponentid == None):
        users[opponentid]["gameid"]=None
        users[opponentid]["opponent"]=None
        emit("opponentleft",users[request.sid]["username"],room=opponentid)


if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)