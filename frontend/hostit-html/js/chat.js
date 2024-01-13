// Function to toggle the visibility of the logout menu
function toggleLogoutMenu() {
  var logoutMenu = document.getElementById("logout-menu");
  if (logoutMenu.style.display === "block") {
    logoutMenu.style.display = "none";
  } else {
    logoutMenu.style.display = "block";
  }
}

// Close the logout menu when clicking outside of it
document.addEventListener("click", function (event) {
  var logoutMenu = document.getElementById("logout-menu");
  var avatarContainer = document.getElementById("avatar-container");

  if (
    event.target !== avatarContainer &&
    !avatarContainer.contains(event.target)
  ) {
    logoutMenu.style.display = "none";
  }
});

// Function to toggle the visibility of the exit chat menu
function toggleExitChatMenu() {
  var exitChatMenu = document.getElementById("exitChatMenu");
  if (exitChatMenu.style.display === "block") {
    exitChatMenu.style.display = "none";
  } else {
    exitChatMenu.style.display = "block";
  }
}

// Close the exit chat menu when clicking outside of it
document.addEventListener("click", function (event) {
  var exitChatMenu = document.getElementById("exitChatMenu");
  var optionContainer = document.getElementById("optioncontainer");

  if (
    event.target !== optionContainer &&
    !optionContainer.contains(event.target)
  ) {
    exitChatMenu.style.display = "none";
  }
});

// Get the file name from the query parameter
const urlParams = new URLSearchParams(window.location.search);
const fileName = urlParams.get('file');
const url = urlParams.get('url');

// Specify the folder where the PDFs are stored
const pdfFolder = 'pdfs';
// Retrieve the URL from localStorage

// Set the src attribute of the iframe based on the available data
if (fileName) {
  // Handle the case where a file is specified in the query parameter
  document.getElementById('pdfViewer').src = `${pdfFolder}/${encodeURIComponent(fileName)}`;
} else if (url) {
  // Handle the case where a URL is stored in localStorage
  document.getElementById('pdfViewer').src = url;
} else {
  // Handle the case where neither a file nor a URL is specified
  console.error('No file or URL specified.');
}

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = [
"Hi, how are you?",
"Ohh... I can't understand what you trying to say. Sorry!",
"I like to play games... But I don't know how to play!",
"Sorry if my answers are not relevant. :))",
"I feel sleepy! :("];


// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "images/chaticon.png";
const PERSON_IMG = "images/userlogo.png";
const BOT_NAME = "ChatPad AI";
const PERSON_NAME = "Me";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  ;
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(data) {

  const msgText = "response";
  const delay = msgText.split(" ").length * 100;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  }, delay);
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}



// Function to send a message to the server
function sendMessage(message) {
  fetch('http://127.0.0.1:8000/usermsg', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({message: message})
  })
  .then(response => response.json())
  .then(data => {
      // Handle the response data here
      console.log(data);
      botResponse(data);
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

// Assuming you have a form with an input field with id 'messageInput' and a 'send' button
document.getElementById('send').addEventListener('click', function() {
  var message = document.getElementById('messageInput').value;
  sendMessage(message);
});
