var count = 0
var options = ['d)','e)','f)','g)','h)','i)','j)']
var added_options = ['a', 'b', 'c']
var question_type = []
var option_count = []
var mc_options = {}

function mc(){
  document.getElementById("mc").remove();
  document.getElementById("wr").remove();

  const subject = document.querySelector('#question_type');

  let question_id = count.toString() + "answer' name='mc'><br></form>"

  subject.insertAdjacentHTML("beforeend", "<label for='mc'>a)</label>")

  subject.insertAdjacentHTML("beforeend", ("<form><input type='text' id='1" + question_id))

  subject.insertAdjacentHTML("beforeend", ("<label>b)<form><input type='text' id='2" + question_id + "</label>"))

  subject.insertAdjacentHTML("beforeend", ("<label>c)<form><input type='text' id='3" + question_id + "</label>"))

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>")
  
  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>")
  
  mc_options[count] = 3
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

  const subject = document.querySelector('#question_type');
  mc_options[count] += 1
  let to_add = mc_options[count] 
  let op = "<label>".concat(options.shift())
  op += "<form><input type='text' id='" + to_add.toString() + count.toString() + "answer' name='mc'><br></form></label>"
  subject.insertAdjacentHTML("beforeend", op)

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' onclick='add_option()' id='add-mc' role='button'>+</button>");

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>");  

  }

function add_question(){
  document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();
  count++

  const subject = document.querySelector('#question_type');
  var head = "<h5>Question(s):</h5><form><input type='text' id='Question_"+count.toString()+"'" + "name='fname'><br></form>"

  subject.insertAdjacentHTML("beforeend", head)

  subject.insertAdjacentHTML("beforeend", "<button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>")

  subject.insertAdjacentHTML("beforeend", "<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>")

  added_options = ['a', 'b', 'c']
  options = ['d)','e)','f)','g)','h)','i)','j)']
}

async function publish(){
  let success = true
  const title = document.getElementById('Title').value
  console.log(title)
  if(title == ''){
    success = false;
  }
  const description = document.getElementById('Description').value
  var date=document.getElementById('expiredDate').value
  let question_list = []
  if (question_type.length == 0){
    success = false
  }
  else{
    if (count > 0){
      let q = []
      for(let i = 0; i <= count ;i++){
        let question_id = 'Question' + '_' + i.toString()
        let question_title = document.getElementById(question_id).value
        if (question_title == ''){
          success = false;
        }
        q.push(question_type[i])
        q.push(question_title)
        let mc_option_list = []
        for(let v = 0; v < mc_options[count]; v++){
          let answer = document.getElementById(((v+1).toString() + i.toString()+'answer')).value
          if (answer == ''){
            success = false
          }
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
      for(let i = 0; i < mc_options[0]; i++){
        let answer = document.getElementById(((i+1).toString() + count.toString()+'answer')).value
        mc_option_list.push(answer)
      }
      q.push(mc_option_list)
      question_list.push(q)
    }
  }
  if (success == true){
    const survey_data = {
                        'title':title,
                        'description':description,
                        'questions':question_list,
                        'expired_date': date,
                        'visibility': 'public'
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
    xhr.send(data);
    location.href = "creation_success"
  }

  else if(question_type.length == 0){
    alert('You have not created any questions!')
  }

  else{
    question_list = []
    alert('You left some fields blank')
  }
}
