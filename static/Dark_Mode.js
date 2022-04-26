
var isDark = window.localStorage.getItem("theme");

var toggle = document.getElementById("toggle");

if (isDark === "dark") document.body.classList.add("dark");



function setDarkMode(){
    console.log("here");
    document.body.classList.toggle("dark");
   if (isDark === "dark") {
     window.localStorage.setItem("theme", null);
     console.log("hello")
   } else {
       window.localStorage.setItem("theme", "dark");
       console.log("hi")
   }
   window.location.reload();
}