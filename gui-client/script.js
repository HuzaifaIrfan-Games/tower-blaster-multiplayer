

const socket = io("/")


let name="";

if (localStorage.getItem("name")==null){


while(name==""|| name==null){
  name = prompt("What is Your name?")
  console.log(name)
}

localStorage.setItem("name" , `${name}`)

}


    name = localStorage.getItem("name")
    
    socket.emit("Connection", name)

    showmainmenu()





function resetGame(){
  hideall()
  localStorage.removeItem("name")

  location.reload();
return false;

}








function hideall(){
  document.getElementById("mainmenu").style.display = "none";
  document.getElementById("startgamemenu").style.display = "none";
  document.getElementById("fetchgamemenu").style.display = "none";
  document.getElementById("helpmenu").style.display = "none";
  document.getElementById("TheGame").style.display = "none";
  document.getElementById("settings").style.display = "none";
}


function showsettings(){
  hideall()
  document.getElementById("settings").style.display = "block";
}


function showhelpmenu(){
  hideall()
  document.getElementById("helpmenu").style.display = "block";
}


function showmainmenu(){
  socket.emit('noplay')



  var mainmenu=document.getElementById("mainmenu")

  mainmenu.innerHTML=`

  <h1 align="center">Main Menu</h1>

  <h3 align="center">Asalaam O Alaikum, ${name} </h3>

  <div class="buttons">
  
  
        <input type="button" onclick="getdifficulties()" class="btn-success" value="Start Game">
        
        <input type="button" onclick="getfreegames()" class="btn-success" value="Fetch Game">
  
        <input type="button" onclick="showsettings()" class="btn-success" value="Settings">
        
        <input type="button" onclick="showhelpmenu()" class="btn-success" value="Help!!">
      </div>


`




  hideall()
  document.getElementById("mainmenu").style.display = "block";
}


function showmessage(msg){
  hideall()
  document.getElementById("TheGame").style.display = "block";
  var gamecontent=document.getElementById("TheGame")

  gamecontent.innerHTML=""

  var gameEl=`<div class="buttons">

  

  <h3>${msg}</h3>
  <input type="button" class="btn-danger" value="Main Menu" onclick="showmainmenu()">
    
  </div>`

gamecontent.innerHTML=gameEl

}



socket.on("tomainmenu", () => {
  hideall()
  document.getElementById("mainmenu").style.display = "block";
})




socket.on("notfree", player1name => {

  showmessage(`${player1name} is Busy`)
 

})

socket.on("opponentleft", opponentname => {

showmessage(`Opponent ${opponentname} Left`)
 

})









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
  diffEl = diffEl + `<input type="button" class="btn-danger" value="Main Menu" onclick="showmainmenu()">`

diffmenu.innerHTML=diffEl

hideall()
document.getElementById("startgamemenu").style.display="block"


})







socket.on("gamecreated", levels => {

  var diffmenu=document.getElementById("diffmenu")

  diffmenu.innerHTML=""

  var diffEl="<h2>Game Created</h2>"

  diffEl = diffEl + `<h3>Waiting for Other Player to Join</h3>`


  diffEl = diffEl + `<input type="button" class="btn-danger" value="Leave Game" onclick="showmainmenu()">`

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



function getquestion(){
  socket.emit('getquestion')
}

function changetower(num){
  socket.emit('changetower',num)
}






socket.on("loadinggame", loader => {


  hideall()
  document.getElementById("TheGame").style.display = "block";
  var gamecontent=document.getElementById("TheGame")

  gamecontent.innerHTML=""

  var gameEl=`<div id="gameplay">


  <div class="space-betweenrow">

  <div>${loader["yourname"]} playing game with ${loader["opponentname"]}</div>
    <div><input type="button" class="btn-danger" value="Main Menu" onclick="showmainmenu()"></div>
    </div>

    

    <div class="space-aroundrow">
    <div>${loader["opponentname"]} : ${loader["opponentscore"]}</div>    <div>${loader["yourname"]} :  ${loader["yourscore"]}</div>

    </div>

    <div class="space-aroundrow">
    `
    if(loader["turn"]==true){
      gameEl=gameEl + `<div>Your Turn</div>`
     gameEl=gameEl + `<div> Now :  ${loader["running"]}</div>`
    
    if(loader["getagain"]>0){
      gameEl=gameEl + `<div>
      <input type="button" class="btn-primary" value="Questions : ${loader["getagain"]}" onclick="getquestion()">
      
      </div>
      `
    } 

  }else{
    gameEl=gameEl + `<div>Opponent's Turn</div>`
  }

    gameEl=gameEl + `
    </div>

  <div class="tower">
    `




  for (var i = 0; i <= loader["game"].length - 1; i++) {

    gameEl = gameEl + `<input type="button" class="btn-success" value="${loader["game"][i]}" onclick="changetower(${i+1})">`
  
  }

  

  gameEl = gameEl + `</div>
  
  </div>`

gamecontent.innerHTML=gameEl

})



function playingagain(){
  socket.emit('playagain')
  showmessage(`Waiting for Other Player to respond!!`)
}




function playagain(loader,win){

  hideall()
  document.getElementById("TheGame").style.display = "block";
  var gamecontent=document.getElementById("TheGame")

  gamecontent.innerHTML=""

  var gameEl=`<div id="gameplay">


  <div class="space-betweenrow">

  <div>${loader["yourname"]} playing game with ${loader["opponentname"]}</div>
    <div><input type="button" class="btn-danger" value="Main Menu" onclick="showmainmenu()"></div>
    </div>

    <div class="space-aroundrow">
      <div>${loader["opponentname"]}</div>    <div>${loader["yourname"]}</div>
    </div>



    <div class="space-aroundrow">`


if(win==true){
  gameEl=gameEl + `<h3>You Win</h3>`
}else{
  gameEl=gameEl + `<h3>You Lose</h3>`
}


gameEl=gameEl + `
    
  </div>

    <div class="space-aroundrow">

    <input type="button" class="btn-success" value="I Want to Play Again" onclick="playingagain()">
    
    </div>
  
      <div class="space-aroundrow">
      `
  

//Opponent Tower


    gameEl=gameEl + `

  <div class="tower">
    `

  for (var i = 0; i <= loader["opponentgame"].length - 1; i++) {

    gameEl = gameEl + `<input type="button" class="btn-success" value="${loader["opponentgame"][i]}">`
  
  }



  gameEl = gameEl + `</div>`






//Your Tower



    gameEl=gameEl + `

  <div class="tower">
    `

  for (var i = 0; i <= loader["yourgame"].length - 1; i++) {

    gameEl = gameEl + `<input type="button" class="btn-success" value="${loader["yourgame"][i]}" >`
  
  }



  gameEl = gameEl + `</div>`





  gameEl = gameEl + ` </div>
  
  </div>`

gamecontent.innerHTML=gameEl


}











socket.on("winner", obj => {

  playagain(obj,true)


})


socket.on("looser", obj => {

  playagain(obj,false)
  
  
  })















socket.on("disconnect", () => {
console.log("Disconnected from server")
hideall()
document.getElementById("mainmenu").style.display = "block";
})



