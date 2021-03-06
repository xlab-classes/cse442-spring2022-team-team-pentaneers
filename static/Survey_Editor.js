var count = 0
var options = ['c)','d)','e)','f)','g)','h)','i)','j)']
var added_options = ['a', 'b']
var question_type = []
var option_count = []
var mc_options = {}
var visible = 'public'

function mc(){
  document.getElementById("mc").remove();
  document.getElementById("wr").remove();

  const subject = document.querySelector('#question_type');

  let question_id = count.toString() + "answer' name='mc'><br></form>"

  subject.insertAdjacentHTML("beforeend", "<label for='mc'>a)</label>")

  subject.insertAdjacentHTML("beforeend", ("<form><input type='text' onkeydown='return event.key != 'Enter';' id='1" + question_id))

  subject.insertAdjacentHTML("beforeend", ("<label>b)<form><input type='text' onkeydown='return event.key != 'Enter';' id='2" + question_id + "</label>"))


  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>")
  
  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>")
  
  mc_options[count] = 2
  question_type.push('Multiple Choice') ;
  }
  
function wr(){
  document.getElementById("mc").remove();
  document.getElementById("wr").remove();
  question_type.push('Short Response');
  const subject = document.querySelector('#question_type');

  // let question_id = count.toString() + "wr' name='wr'><br></form>"

  // subject.insertAdjacentHTML("beforeend", "<br><form><input type='text' onkeydown='return event.key != 'Enter';' id='" + question_id)

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>")

}

function private(){
  visible = 'private'
  alert('This survey will be private.')
}

function public(){
  visible = 'public'
  alert('This survey will be public.')
}


function add_option(){
  document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();

  const subject = document.querySelector('#question_type');
  mc_options[count] += 1
  let to_add = mc_options[count] 
  let op = "<label>".concat(options.shift())
  op += "<form><input type='text' onkeydown='return event.key != 'Enter';' id='" + to_add.toString() + count.toString() + "answer' name='mc'><br></form></label>"
  subject.insertAdjacentHTML("beforeend", op)

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>");

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>");  

  }

function add_question(){
  if (question_type[question_type.length - 1] == 'Multiple Choice'){
    document.getElementById("add-mc").remove();
  }
  document.getElementById("add-question").remove();
  count++

  const subject = document.querySelector('#question_type');
  var head = "<h5>Question " + (count + 1).toString() + ":</h5><form><input type='text' onkeydown='return event.key != 'Enter';' id='Question_"+count.toString()+"'" + "name='fname'><br></form>"

  subject.insertAdjacentHTML("beforeend", head)

  subject.insertAdjacentHTML("beforeend", "<button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>")

  subject.insertAdjacentHTML("beforeend", "<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>")

  added_options = ['a', 'b']
  options = ['c)','d)','e)','f)','g)','h)','i)','j)']
}

async function publish(){
  let success = true
  const title = document.getElementById('Title').value
  if(title == ''){
    alert("You are missing a title!")
    success = false;
  }
  const description = document.getElementById('Description').value
  var date=document.getElementById('expiredDate').value
  var timestamp = +new Date(date)/1000
  let question_list = []
  if (question_type.length == 0 && title != ''){
    alert('You must include at least one question with a minimum of two options.')
    success = false;
  }
  else{
    if (count > 0){
      for(let i = 0; i <= count ;i++){
        let q = []
        let question_id = 'Question' + '_' + i.toString()
        let question_title = document.getElementById(question_id).value

        
        q.push(question_title)
        q.push(question_type[i])
        if(question_type[i] == 'Multiple Choice'){
          let mc_option_list = []
          
          for(let v = 0; v < mc_options[i]; v++){
            let answer = document.getElementById(((v+1).toString() + i.toString()+'answer')).value
              if (answer == '' && question_title != '' && v < 2 && mc_option_list.length > 0){
                alert("\u2022Please include at least two options for question " + (i + 1).toString() + '.\n\n' + '\u2022IF you dont wan\'t to include the question in your survey then please DELETE the question title!')
                success = false
                break;
              }
              if (answer != '' && question_title != '' && v >= 0){
                mc_option_list.push(answer.toString())
                console.log(mc_option_list)
              }
              if (question_title == '' && answer != ''){
                alert("\u2022Please include a question title for question " + (i + 1).toString() + '.\n\n' + '\u2022If you dont wan\'t to include the question in your survey then please DELETE the question options!')
                success = false
                break;
              }
              if(question_title != '' && answer == '' && mc_option_list.length == 0){
                alert("\u2022Please include at least two options for question " + (i + 1).toString() + '.\n\n' + '\u2022If you dont wan\'t to include the question in your survey then please DELETE the question title!')
                success = false
                break;
              } 
          }
          if (question_title != '' && mc_option_list.length != 0){
            q.push(mc_option_list)
            question_list.push(q)
          }
        }
      else{
        // let answer = document.getElementById((i.toString() + 'wr')).value
        if(question_title == ''){//have to create case for when user doesn't wants to delete question
          alert("\u2022 Please include a title for question " + (i + 1).toString() + ". \n\u2022 If you include a question title and do not select a question type, it will default to a written response question. \n\u2022 If you do not want to include the question, please select a question type and leave all the input fields blank for that question.")
          success = false
        }
        if (question_title.toString() != ""){
          q.push(null)
          question_list.push(q)
        }
      }
      }
    }
    if (count == 0){
      let q = []
      let question_id = 'Question_0'
      let question_title = document.getElementById(question_id).value
        if (question_title == '' && title != '' && question_type[0] == 'Multiple Choice'){
          alert("Please include a question title for question 1.")
          success = false;
        }
      q.push(question_title)
      q.push(question_type[0])
      if(question_type[0] == 'Multiple Choice'){
        let mc_option_list = []
        for(let i = 0; i < mc_options[0]; i++){
          let answer = document.getElementById(((i+1).toString() + count.toString()+'answer')).value
          if (answer == '' && i < 2 && question_title != '' && title != ''){
            alert("Please include at least two options for question 1.")
            success = false
            break;
          }
          if (answer != '' && i >= 0){
            mc_option_list.push(answer)
          }
        }
        q.push(mc_option_list)
        question_list.push(q)
      }
    if (question_type[0] == 'Short Response'){
      if(question_title == ''){
        alert("Please include question for written response question 1.")
        success = false
      }
      if (question_title.toString() != ""){
        q.push(null)
        question_list.push(q)
      }
    }
    }
  }

  if (success == true){
    const survey_data = {
                        'title':title,
                        'description':description,
                        'questions':question_list,
                        'expired_date': date,
                        'visibility': visible
                      }

    var xhr = new XMLHttpRequest();
    var url = "/submitSurvey";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            console.log(json.email + ", " + json.password);
        }
    };
    var data = JSON.stringify(survey_data);
    console.log(data)
    xhr.send(data);
    location.href = "creation_success"
  }

  else{
    question_list = []
    //alert('You are missing required fields.')
  }
}
