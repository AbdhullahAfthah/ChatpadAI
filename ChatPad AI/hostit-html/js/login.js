// login
let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)



// signup api call

// signup.js
function signup() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Check if passwords match
    if (password !== confirmPassword) {
		displayErrorMessage("Passwords do not match");
        console.log("Passwords do not match");
        return;
    }

    const userData = {
        username: username,
        email: email,
        password: password
    };

    // Make a POST request to the backend API
    fetch('http://127.0.0.1:8000/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Signup failed');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Redirect or show success message
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle error, show error message, etc.
    });
}

function displayErrorMessage(message) {
    const errorMessageElement = document.getElementById('errorMessage');
    errorMessageElement.innerText = message;
}