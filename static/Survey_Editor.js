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
var added_options = ['a', 'b', 'c']
function add_option(){
  document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();
  let op = "<label>".concat(options.shift())
  document.getElementById("question_type").innerHTML += op
  document.getElementById("question_type").innerHTML += 
      "<form><input type='text' id='answer' name='mc'><br></form></label>"; 
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>";  
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>";  
  }

var count = 0
function add_question(){
  document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();
  count++
  var head = "<h5>Question(s):</h5><form><input type='text' id='Question"+"_"+count.toString()+"'"
  var tail = "name='fname'><br></form>"

  document.getElementById("question_type").innerHTML += (head+tail)
  
  document.getElementById("question_type").innerHTML += 
  "<button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>"
  document.getElementById("question_type").innerHTML += 
  "<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>"
  }

function publish(){
  const title = document.getElementById('Title').value
  const description = document.getElementById('Description').value

  let question_list = []
  for(let i = 0;i<count ;i++){
  let question_title = document.getElementById('Question').value
  question_list.push(question_title)
}

  let mc_option_list = []
  for(let i = 0; i<add_option.length; i++){
    let answer = document.getElementById('answer').value
    mc_option_list.push(answer)
  }
  let question_type = "Multiple Choice"
  const survey_data = [title, description, question_list, question_type, mc_option_list]

  fetch("http://10.84.104.6:8000/survey_data", 
  {
  method: 'POST',
  headers: {
  'Content-type': 'application/json',
  'Accept': 'application/json'
  },

  body:JSON.stringify(survey_data)}).then(res=>{
  if(res.ok){
  return res.json()
  }
  else
  {
  alert("something is wrong")
  }
  }).then(jsonResponse=>{
 
    // Log the response data in the console
    console.log(jsonResponse)
    } 
    ).catch((err) => console.error(err));
    

  // window.location.replace("https://theuselessweb.site/ducksarethebest.com/");

  }