// login
let container = document.getElementById("container");

toggle = () => {
  container.classList.toggle("sign-in");
  container.classList.toggle("sign-up");
};

setTimeout(() => {
  container.classList.add("sign-in");
}, 200);

// signup api call

async function signup() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // Check for empty fields
  if (!username || !email || !password || !confirmPassword) {
    displayErrorMessage("All fields must be filled");
    return;
  }

  // Validate password length
  if (password.length < 8) {
    displayErrorMessage("Password must be at least 8 characters long");
    return;
  }
  // Validate password and confirmPassword
  if (password !== confirmPassword) {
    displayErrorMessage("Passwords do not match");
    return;
  }

  // Validate email format
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    displayErrorMessage("Invalid email format");
    return;
  }

  // Your backend API endpoint (update the URL accordingly)
  const apiUrl = "http://localhost:8000/create_user";

  // Data to be sent to the server
  const data = {
    username: username,
    email: email,
    hashed_password: password,
  };

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Signup failed");
    }

    // Handle successful signup
    // You can customize this part
    showCookiePopup();

    // Reset the form or redirect to the login page
    document.getElementById("username").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password").value = "";
    document.getElementById("confirmPassword").value = "";
    document.getElementById("errorMessage").innerText = "";
  } catch (error) {
    // Handle errors
    console.error("Signup failed:", error.message);
    document.getElementById("errorMessage").innerText = error.message;
  }
}

function displayErrorMessage(message) {
  const errorMessageElement = document.getElementById("errorMessage");
  errorMessageElement.innerText = message;
}

// signin api call

document.addEventListener("DOMContentLoaded", function () {
  // Hide the popup initially
  closeCookiePopup();
});

async function signin() {
  const username = document.getElementById("signin-username").value;
  const password = document.getElementById("signin-password").value;

  // Check if username and password are provided
  if (!username || !password) {
    document.getElementById("signin-error-message").innerText =
      "Username and password are required.";
    return;
  }

  // Your backend API endpoint for signin (update the URL accordingly)
  const apiUrl = "http://localhost:8000/token"; // Update the URL

  // Data to be sent to the server
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded", // Set the correct Content-Type
      },
      body: data,
    });

    if (response.ok) {
      // Successful signin
      const responseData = await response.json();

      // Store the token securely (e.g., in an HTTP-only cookie or local storage)
      storeToken(responseData.access_token);

      // Redirect to the user_upload page
      window.location.href = "user_upload.html"; // Update the URL
    } else if (response.status === 401) {
      // Unauthorized - Incorrect credentials
      document.getElementById("signin-error-message").innerText =
        "Incorrect username or password.";
    } else {
      // Handle other errors
      const errorData = await response.json();
      if (errorData.detail && Array.isArray(errorData.detail)) {
        // Display the first validation error message to the user
        document.getElementById("signin-error-message").innerText =
          errorData.detail[0].msg;
      } else if (errorData.detail) {
        // Display a single validation error message to the user
        document.getElementById("signin-error-message").innerText =
          errorData.detail.msg;
      } else {
        // Display a generic error message to the user
        document.getElementById("signin-error-message").innerText =
          "Signin failed";
      }
    }
  } catch (error) {
    // Handle other errors
    console.error("Signin failed:", error.message);
    document.getElementById("signin-error-message").innerText = "Signin failed";
  }
}

function storeToken(token) {
  // Store the token securely (e.g., in an HTTP-only cookie or local storage)
  // For example, using localStorage:
  localStorage.setItem("accessToken", token);
}

// You can call this function when the signin form is submitted
// document.getElementById("signin-form").addEventListener("submit", function (event) {
//   event.preventDefault();
//   signin();
// });

function showCookiePopup() {
  var popup = document.getElementById("cookiesPopup");
  popup.style.display = "block";
  // alert("Signup successful! Show your popup here.");
}

function closeCookiePopup() {
  var popup = document.getElementById("cookiesPopup");
  popup.style.display = "none";
}
