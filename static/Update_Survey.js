var count = 0
var options = ['c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)','y)','z)','aa)','ab)','ac)']
var static_options = ['c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)','u)','v)','w)','x)','y)','z)','aa)','ab)','ac)']
var added_options = ['a', 'b']
var question_type = []
var option_count = []
var mc_options = {}
var visible = 'public'
//final data should be in the form of {questionType-(questionNumber-1)-options: [question title, question type, question options.length, [options a-ac] ]}
var final_data = {}

function load_survey(data){
    let survey_data = JSON.parse(data);
    console.log(Array.isArray(survey_data));
    console.log("Incoming data: ", survey_data)
    let counter = 0
    for (dictionary = 3; dictionary < survey_data.length; dictionary++){
      
        let survey_info = survey_data[dictionary];
        console.log("This is the survey info: ", survey_info)
        let survey_values = Object.values(survey_info);
        console.log("This is the current survey values: ", survey_values)
        let question_number = Object.keys(survey_info)[0];
        console.log("This is the current questions number: ", question_number)
        
        let question_title = survey_values[0][0];
        console.log("This is the current survey question title: ", question_title)
        let question_type = survey_values[0][1];
        console.log("This is the current question type: ", question_type)
        let quesiton_options = survey_values[0][2];
        console.log("This is the current question options: ", quesiton_options)
        
        if (question_number.toString() != 'question_1'){
          // Add the existing question title
          add_exisitng_question_title(question_title);
        }
        if (question_type == 'Multiple Choice'){
            // Add the key to the current question for the final data
            final_data['mc-'+counter.toString()+'-options'] = []
            // Add the correct values for the current question
            let final_data_values = final_data['mc-'+counter.toString()+'-options']
            final_data_values[0] = question_title
            final_data_values[1] = question_type
            final_data_values[2] = quesiton_options.length
            final_data_values[3] = static_options
            final_data['mc-'+counter.toString()+'-options'] = final_data_values
            console.log("This is the final data so far: ", final_data)

            // Start the main loop to add all of the data into the Survey editor 
            // Add the first two options of the Multiple Choice question
            add_first_two_existing_mc_options(quesiton_options[0], quesiton_options[1], quesiton_options.length)
            // Loop through the rest of the data (if any) to add to the survey.
            for (let i = 2; i < quesiton_options.length; i++){
                console.log("Current mc question option: ", quesiton_options[i])
                add_exisitng_mc_option(quesiton_options[i], counter, i)
            }
        }
        counter++
            
    }
    
  
}

function add_first_two_existing_mc_options(option1, option2, total_options){
    console.log("current count: ", count)
    document.getElementById("mc").remove();
    // document.getElementById("wr").remove();
  
    const subject = document.querySelector('#question_type');
  
    let question_id = count.toString() + "answer name='mc'><br></form>"

    subject.insertAdjacentHTML("beforeend", "<div id='mc-" + count.toString() + "-options'></div>")

    const current_mc_question = document.querySelector("#mc-" + count.toString() + "-options");
  
    current_mc_question.insertAdjacentHTML("beforeend", "<label for='mc' id=1" + count + ">a)</label>")
  
    current_mc_question.insertAdjacentHTML("beforeend", ("<form onsubmit='return false;'> <input type='text' value=" + option1 + " id=1" + question_id))
  
    current_mc_question.insertAdjacentHTML("beforeend", ("<label id=2" + count.toString() + ">b)<form onsubmit='return false;'> <input type='text' value=" + option2 + " id=2" + question_id + "</label>"))
  
    if (total_options == 2){
      // current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-delete-mc' id='mc-" + count.toString() + "-delete-option' onclick='delete_option(this.id)' role='button'>-</button>")

      current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + count.toString() + "-add-option' onclick='add_option(this.id)' role='button'>+</button>")

      current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>")
    }
    
    
    
    mc_options[count] = 2
    question_type.push('Multiple Choice') ;
}


function add_exisitng_question_title(data){
    // document.getElementById("add-mc").remove();
    document.getElementById("add-question").remove();
    count++

    const subject = document.querySelector('#question_type');
    var head = "<h5>Question " + (count + 1).toString() + ":</h5><form onsubmit='return false;'><input type='text' id='Question_"+ count.toString() + "'name='fname' value='"+ data.toString() +"'><br></form>"

    subject.insertAdjacentHTML("beforeend", head)

    subject.insertAdjacentHTML("beforeend", "<button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>")

    // subject.insertAdjacentHTML("beforeend", "<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>")

    added_options = ['a', 'b']
    options = ['c)','d)','e)','f)','g)','h)','i)','j)']

}

function add_exisitng_mc_option(option, question_num, current_option){

    let subject = document.querySelector("#mc-" + question_num.toString() + "-options");

    let curr_number_of_options = final_data['mc-'+question_num.toString()+'-options']
    let updated_curr_question_number_of_options = curr_number_of_options[2]
    console.log("This is the updated curr question number of options: ", updated_curr_question_number_of_options)
    mc_options[count] += 1

    console.log("Line 125 updted xurr question number of options: ", updated_curr_question_number_of_options)
    console.log("Current question number: ", question_num)
    console.log("This is the current option so far: ", current_option)
    
    let op = "<label id='" + mc_options[count].toString() + question_num.toString() +  "'>".concat(options.shift())
    op += "<form onsubmit='return false;'> <input type='text' id='" + (current_option+1).toString() + question_num.toString() + "answer' value="+ option + " name='mc'><br></form></label>"
    subject.insertAdjacentHTML("beforeend", op)

    if (updated_curr_question_number_of_options == (current_option+1)){

      subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + question_num.toString() + "-delete-option' onclick='delete_option(this.id)' role='button'>-</button>")

      subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + question_num.toString() + "-add-option' onclick='add_option(this.id)' role='button'>+</button>");

      subject = document.querySelector('#question_type');

      subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' id='add-question' onclick='add_question()' role='button'>Add question</button>");

    }
    
    }














function mc(){
  document.getElementById("mc").remove();
  // document.getElementById("wr").remove();

  let question_id = count.toString() + "answer' name='mc'><br></form>"

  const subject = document.querySelector('#question_type');

  subject.insertAdjacentHTML("beforeend", "<div id='mc-" + count.toString()+ "-options'></div>")

  const current_mc_question = document.querySelector("#mc-" + count.toString() + "-options");

  current_mc_question.insertAdjacentHTML("beforeend", "<label for='mc' id='1" + count.toString() + "'>a)</label>")

  current_mc_question.insertAdjacentHTML("beforeend", ("<form onsubmit='return false;'> <input type='text' id='1" + question_id))

  current_mc_question.insertAdjacentHTML("beforeend", ("<label id='2" + count.toString() + "'>b)<form onsubmit='return false;'> <input type='text' id='2" + question_id + "'</label>"))

  // current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + count.toString() + "-delete-option' onclick='delete_option(this.id)' role='button'>-</button>")

  current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + count.toString() + "-add-option' onclick='add_option(this.id)' role='button'>+</button>")
  
  current_mc_question.insertAdjacentHTML("beforeend", "<button class='button-add-question' onclick='add_question()' id='add-question' role='button'>Add question</button>")
  
  // Add the new data to final_data
  final_data['mc-'+(count).toString()+'-options'] = []
  final_data['mc-'+(count).toString()+'-options'][0] = ''
  final_data['mc-'+(count).toString()+'-options'][1] = ''
  final_data['mc-'+(count).toString()+'-options'][2] = 2
  final_data['mc-'+(count).toString()+'-options'][3] = static_options

  mc_options[count] = 2
  question_type.push('Multiple Choice') ;
}
  

function private(){
  visible = 'private'
  alert('This survey will be private')
}

function public(){
  visible = 'public'
  alert('This survey will be public')
}
// function wr(){
//   document.getElementById("mc").remove();
//   document.getElementById("wr").remove();
//   question_type.push('Short Response');
//   }

function add_option(option_id){

  const split_id = option_id.split("-")
  let current_question_number = split_id[1]
  console.log("This is teh currnt question line 198: ", current_question_number)
  const subject = document.querySelector("#mc-" + current_question_number.toString() + "-options");
  console.log("This is the subject: ", subject)

  let number_of_question_options = final_data['mc-'+current_question_number+'-options']
  let updated_number_of_question_options = number_of_question_options[2] + 1
  console.log("Updated number of question options: ", updated_number_of_question_options)
  // Add 1 to the current questions number of options
  final_data['mc-'+current_question_number+'-options'][2] += 1


  if (number_of_question_options[2] > 3){
    console.log("Line 230")
      document.getElementById('mc-'+current_question_number+'-delete-option').remove()
  }

  new_option = final_data['mc-'+current_question_number+'-options'][2] - 3
  let op = "<label id=" + updated_number_of_question_options.toString() + current_question_number.toString() + ">".concat(final_data['mc-'+current_question_number+'-options'][3][new_option])
  op += "<form onsubmit='return false;'> <input type='text' id='" + updated_number_of_question_options.toString() + current_question_number.toString() + "answer' name='mc'><br></form></label>"
  subject.insertAdjacentHTML("beforeend", op)

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + current_question_number.toString() + "-delete-option' onclick='delete_option(this.id)' role='button'>-</button>")

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-mc' id='mc-" + current_question_number.toString() + "-add-option' onclick='add_option(this.id)' role='button'>+</button>");

  subject.insertAdjacentHTML("beforeend", "<button class='button-add-question' id='add-question' role='button' onclick='add_question()'>Add question</button>");

  document.getElementById(option_id).remove();
  document.getElementById("add-question").remove();

  mc_options[current_question_number] += 1
  }

function delete_option(option_id){
  //final data should be in the form of {questionType-(questionNumber-1)-options: [question title, question type, question options.length, [options a-ac] ]}
  const split_id = option_id.split("-")
  let current_question_number = split_id[1]
  final_data['mc-'+current_question_number+'-options'][2] -= 1
  mc_options[current_question_number] -= 1
  // Get the latest number of options for the specific question
  let number_of_question_options = final_data['mc-'+current_question_number+'-options'][2] + 1

  if (number_of_question_options > 2){
    // Select the specific option label and remove it
    document.getElementById(number_of_question_options.toString() + current_question_number.toString()).remove();
  }
  if (number_of_question_options == 3){
    document.getElementById('mc-'+current_question_number+'-delete-option').remove()
  }
}

function add_question(){
  // document.getElementById("add-mc").remove();
  document.getElementById("add-question").remove();
  count++

  const subject = document.querySelector('#question_type');
  var head = "<h5>Question " + (count + 1).toString() + ":</h5><form onsubmit='return false;'> <input type='text' id='Question_"+count.toString()+"'" + "name='fname'><br></form>"

  subject.insertAdjacentHTML("beforeend", head)

  subject.insertAdjacentHTML("beforeend", "<button class='button-mc' onclick='mc()' role='button' id='mc'>MC</button>")

  // subject.insertAdjacentHTML("beforeend", "<button class='button-wr' onclick='wr()' role='button' onclick='mc()' id='wr'>WR</button>")

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
        let mc_option_list = []
        
        for(let v = 0; v < mc_options[i]; v++){
          console.log("This is V: ", v)
          console.log("This is i: ", i)
          console.log("MC options: ", mc_options)
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
    }
    if (count == 0){
      let q = []
      let question_id = 'Question_0'
      let question_title = document.getElementById(question_id).value
        if (question_title == '' && title != ''){
          alert("Please include a question title for question 1.")
          success = false;
        }
      q.push(question_title)
      q.push(question_type[0])
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
  }
  if (success == true){
    const survey_data = {
                        'title':title,
                        'description':description,
                        'questions':question_list,
                        'expired_date': date,
                        'visibility': visible
    }

    var surveys_id = window.location.pathname
    surveys_id = surveys_id.split("/")[2]
    var xhr = new XMLHttpRequest();
    var url = "/survey/modify/" + surveys_id.toString();
    xhr.open("PUT", url, true);
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
    
    location.href = "/update_success/"+surveys_id

  }

  else{
    question_list = []
    //alert('You are missing required fields.')
  }
}