var count = 0
var options = ['d)','e)','f)','g)','h)','i)','j)']
var added_options = ['a', 'b', 'c']
var question_type = []
var option_count = []

function mc(){
  document.getElementById("mc").remove();
  document.getElementById("wr").remove();

  let = question_id = count.toString() + "answer' name='mc'><br></form>"
  document.getElementById("question_type").innerHTML += 
      "<label for='mc'>a)</label>";  
  document.getElementById("question_type").innerHTML += 
      ("<form><input type='text' id='" + question_id)
  document.getElementById("question_type").innerHTML += 
      ("<label>b)<form><input type='text' id="+question_id + "</label>")
  document.getElementById("question_type").innerHTML += 
      ("<label>c)<form><input type='text' id="+question_id + "</label>") 
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>";  
  
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>";  

  question_type.push('Multiple Choice') ;
  }
  
function wr(){
  document.getElementById("mc").remove();
  document.getElementById("wr").remove();
  question_type.push('Written Response'); 
  }



function add_option(){
  document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();

  let op = "<label>".concat(options.shift())
  document.getElementById("question_type").innerHTML += op
  document.getElementById("question_type").innerHTML += 
      ("<form><input type='text' id=" + "'"+ count.toString() + "answer' name='mc'><br></form></label>");
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>";  
  document.getElementById("question_type").innerHTML += 
      "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>";  
  }

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

  added_options = ['a', 'b', 'c']
  options = ['d)','e)','f)','g)','h)','i)','j)']
}

async function publish(){
  const title = document.getElementById('Title').value
  const description = document.getElementById('Description').value

  let question_list = []
  if (count > 0){ 
    let q = []
    for(let i = 0; i <= count ;i++){
      let question_id = 'Question' + '_' + i.toString()
      let question_title = document.getElementById(question_id).value
      q.push(question_type[i])
      q.push(question_title)
      let mc_option_list = []
      for(let v = 0; v < added_options.length; v++){
        let answer = document.getElementById((i.toString()+'answer')).value
        mc_option_list.push(answer)
      }
      q.push(mc_option_list)
    }
    question_list.push(q)
  }
  else{
    let q = []
    q.push(document.getElementById('Question_0').value)
    q.push(question_type[0])
    let mc_option_list = []
    for(let i = 0; i<added_options.length; i++){
      let answer = document.getElementById((count.toString()+'answer')).value
      mc_option_list.push(answer)
    }
    q.push(mc_option_list)
    question_list.push(q)
  }

  const survey_data = {
                      'email':'shouyue@buffalo.edu', 
                      'title':title, 
                      'description':description, 
                      'questions':question_list, 
                      'expired_date': '2022-03-22',
                      'visibility': 'public'
                    }

    // email=data['email']
    // title=data['title']
    // description=data['description']
    // questions=data['questions']
    // expired=data['expired_date']
    // status=data['visibility']

  var xhr = new XMLHttpRequest();
  var url = "http://127.0.0.1:5000/submitSurvey";//should not be hard coded
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var json = JSON.parse(xhr.responseText);
          console.log(json.email + ", " + json.password);
      }
  };
  var data = JSON.stringify(survey_data);
  xhr.send(data);
  
  }