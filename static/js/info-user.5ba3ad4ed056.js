// Get the userBox
let userBox = document.getElementById("myUserBox");

// Get the button that opens the userBox
let userBtn = document.getElementById("myUserBtn");

// Get the <userSpan> element that closes the userBox
let userSpan = document.getElementsByClassName("closeWindow")[0];

// When the user clicks on the button, open the userBox
userBtn.onclick = function() {
  userBox.style.display = "block";
}

// When the user clicks on <userSpan> (x), close the userBox
userSpan.onclick = function() {
  userBox.style.display = "none";
}

// When the user clicks anywhere outside of the userBox, close it
window.addEventListener("click", function(event) {
    if (event.target == userBox) {
        userBox.style.display = "none"
}})
