

const socket = io("/")


let name;

if (localStorage.getItem("name")==null){

name = prompt("What is Your name?")
localStorage.setItem("name" , `${name}`)

}

    name = localStorage.getItem("name")
    
    socket.emit("Connection", name)



// const inpform = document.getElementById('inpform')
// const inpbox = document.getElementById('inpbox')
// const chatbox = document.getElementById('chatbox')


function hideall(){
  document.getElementById("mainmenu").style.display = "none";
  document.getElementById("startgamemenu").style.display = "none";
  document.getElementById("fetchgamemenu").style.display = "none";
  document.getElementById("helpmenu").style.display = "none";
  document.getElementById("TheGame").style.display = "none";
}


function showhelpmenu(){
  hideall()
  document.getElementById("helpmenu").style.display = "block";
}


function showmainmenu(){
  socket.emit('noplay')
  hideall()
  document.getElementById("mainmenu").style.display = "block";
}


function getdifficulties(){
  socket.emit("getdifficulties")
}

function getfreegames(){
  socket.emit("fetchgames")
}





function creategame(diffid){
  socket.emit('creategame',diffid)
}


socket.on("senddifficulties", levels => {

  var diffmenu=document.getElementById("diffmenu")

  diffmenu.innerHTML=""

  var diffEl=""
  for (var i = 0; i <= levels.length - 1; i++) {

  diffEl = diffEl + `<input type="button" class="btn-success" value="${levels[i]["name"]}" onclick="creategame(${i+1})">`
  
  }
  diffEl = diffEl + `<input type="button" class="btn-success" value="Main Menu" onclick="showmainmenu()">`

diffmenu.innerHTML=diffEl

hideall()
document.getElementById("startgamemenu").style.display="block"


})







socket.on("gamecreated", levels => {

  var diffmenu=document.getElementById("diffmenu")

  diffmenu.innerHTML=""

  var diffEl="<h2>Game Created</h2>"

  diffEl = diffEl + `<h3>Waiting for Other Player to Join</h3>`


  diffEl = diffEl + `<input type="button" class="btn-success" value="Leave Game" onclick="showmainmenu()">`

diffmenu.innerHTML=diffEl

hideall()
document.getElementById("startgamemenu").style.display="block"

})






function joingame(gameid){
  console.log(gameid)
  socket.emit("joingame",gameid)
}


socket.on("showgames", freegames => {

  var freegamesmenu=document.getElementById("freegamesmenu")

  freegamesmenu.innerHTML=""

  var gameEl=""

  gameEl = gameEl + `<input type="button" class="btn-danger" value="Main Menu" onclick="showmainmenu()">`

  for (var i = 0; i <= freegames.length - 1; i++) {

    gameEl = gameEl + `<input type="button" class="btn-success" value="${freegames[i]["creator"]} - ${freegames[i]["difficulty"]["name"]}" onclick="joingame(${freegames[i]["gameid"]})">`
  
  }


  freegamesmenu.innerHTML=gameEl

hideall()
document.getElementById("fetchgamemenu").style.display="block"

})
