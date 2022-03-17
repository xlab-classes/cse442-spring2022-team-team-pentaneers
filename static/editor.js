function isConnect() {
  alert("properly connected");
}

function mc(){
document.getElementById("mc").remove();
document.getElementById("wr").remove();
document.getElementById("question_type").innerHTML += 
    "<label for='mc'>a)</label>";  
document.getElementById("question_type").innerHTML += 
    "<form><input type='text' id='answer' name='mc'><br></form>";  
document.getElementById("question_type").innerHTML += 
    "<label>b)<form><input type='text' id='answer' name='mc'><br></form></label>";  
document.getElementById("question_type").innerHTML += 
    "<label>c)<form><input type='text' id='answer' name='mc'><br></form></label>";  
document.getElementById("question_type").innerHTML += 
    "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>";  

document.getElementById("question_type").innerHTML += 
    "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>";  
}

function wr(){
document.getElementById("mc").remove();
document.getElementById("wr").remove();
}
var options = ['d)','e)','f)','g)','h)','i)','j)']
function add_option(){
document.getElementById("add-mc").remove();
document.getElementById("add-question").remove();
var op = "<label>".concat(options.shift())
document.getElementById("question_type").innerHTML += op
document.getElementById("question_type").innerHTML += 
    "<form><input type='text' id='answer' name='mc'><br></form></label>"; 
document.getElementById("question_type").innerHTML += 
    "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>";  
document.getElementById("question_type").innerHTML += 
    "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>";  
}

function add_question(){
document.getElementById("add-mc").remove();
document.getElementById("add-question").remove();
document.getElementById("question_type").innerHTML += 
"<h5>Question(s):</h5><form><input type='text' id='Question' name='fname'><br></form>"
document.getElementById("question_type").innerHTML += 
" <button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>"
document.getElementById("question_type").innerHTML += 
"<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>"
}