// Function to toggle the visibility of the logout menu
function toggleLogoutMenu() {
  var logoutMenu = document.getElementById("logout-menu");
  if (logoutMenu.style.display === "block") {
    logoutMenu.style.display = "none";
  } else {
    logoutMenu.style.display = "block";
  }
}

// Assuming you have the user's token stored in a variable named 'userToken'

// Function to handle logout
function logout() {
  // Clear or invalidate the stored token
  clearToken();

  // Optionally, redirect to the login page or perform other logout-related actions
  window.location.href = "login.html"; // Update the URL
}

// Function to clear or invalidate the stored token
function clearToken() {
  // Clear the token securely (e.g., remove from an HTTP-only cookie or local storage)
  // For example, using localStorage:
  localStorage.removeItem("accessToken");
}

// Attach the logout function to the "Logout" link
$("#logout-menu a").on("click", function (event) {
  event.preventDefault();
  logout();
});

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

function buttonClick() {
  document.getElementById("fileID").click();
}
let fileName;

async function handleFileUpload(files) {
  const tableBody = $("#pdfTable tbody");

  let fileName; // Declare fileName variable

  for (const file of files) {
    fileName = file.name; // Set fileName inside the loop

    const row = $("<tr>");
    const fileNameCell = $("<td>").text(file.name);
    const fileSizeCell = $("<td>").text((file.size / 1024).toFixed(2));
    const optionsCell = $("<td>").append(createOptionsMenu());
    row.append(fileNameCell, fileSizeCell, optionsCell);
    tableBody.append(row);
  }

  if (files.length > 0) {
    const file = files[0];

    // Assuming your API endpoint is http://your-api-endpoint/upload-pdf
    const apiUrl = "http://localhost:8002/upload-pdf/";

    // Retrieve the stored token
    const userToken = retrieveToken();

    // Create FormData and append the file to it
    const formData = new FormData();
    formData.append("file", file);

    $.ajax({
      url: apiUrl,
      type: "POST",
      headers: {
        Authorization: `Bearer ${userToken}`,
      },
      data: formData,
      processData: false, // Don't process the data, let FormData handle it
      contentType: false, // Don't set content type (FormData will automatically set it as multipart/form-data)
    
      success: function (responseData) {
        console.log("File uploaded successfully to the API");
        console.log("File path:", responseData.file_path);
        const filepath = responseData.file_path;
        sendFilePathToAPI(filepath);
        setTimeout(() => {
          window.location.href = `chat.html?file=${encodeURIComponent(fileName)}`;
        }, 200);
      },
    
      error: function (xhr, status, error) {
        console.error("Failed to upload file to the API");
        console.error("Error details:", error);
        // Handle error (e.g., show an error message to the user)
      }
    });
  }
}

    

  //   try {
  //     const response = await fetch(apiUrl, {
  //       method: "POST",
  //       headers: {
  //         Authorization: `Bearer ${userToken}`, // Include the stored token in the headers
  //         // "Content-Type": "multipart/form-data", // Set the Content-Type header
  //       },

  //       body: formData,
  //     });
  //     // console.log(formData);

  //     if (response.ok) {
  //       const responseData = await response.json();
  //       console.log("File uploaded successfully to the API");
  //       console.log("File path:", responseData.file_path);
  //       const filepath = responseData.file_path;
  //       sendFilePathToAPI(filepath);
  //       setTimeout(() => {
  //         window.location.href = `chat.html?file=${encodeURIComponent(
  //           fileName
  //         )}`;
  //       }, 200);
  //     } else {
  //       console.error("Failed to upload file to the API");
  //     }
  //   } catch (error) {
  //     console.error("Error during file upload to the API:", error);
  //     // Handle error (e.g., show an error message to the user)
  //   }
  // }


// Function to send filePath to another API on port 8001
async function sendFilePathToAPI(filepath) {
  const secondApiUrl = "http://localhost:8001/process_pdf";

  try {
    const secondApiResponse = await fetch(secondApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Set the Content-Type header
      },
      body: JSON.stringify({ path: filepath }),
    });

    if (secondApiResponse.ok) {
      // Redirect to another HTML page after both API calls are successful
      // window.location.assign(`chat.html?file=${encodeURIComponent(fileName)}`);
    } else {
      console.error("Failed to send file path to the second API");
      // Handle failure for the second API call
    }
  } catch (error) {
    console.error("Error during sending file path to the second API:", error);
    // Handle error for the second API call
  }
}
// Function to retrieve the stored token
function retrieveToken() {
  // Retrieve the token securely (e.g., from an HTTP-only cookie or local storage)
  // For example, using localStorage:
  return localStorage.getItem("accessToken");
}

$(function () {
  // URL form submission handling
  $("#urlForm").submit(function (e) {
    e.preventDefault();
    const url = $("#url").val();
    // Save the URL to local storage
    localStorage.setItem("chatUrl", url);
    addToTable(url, "N/A");
    // Clear the input field after adding to the table
    $("#url").val("");
    sendUrlToServer(url);

    // Redirect to chat.html with the specified URL as a query parameter
    // window.location.href = `chat.html?url=${encodeURIComponent(url)}`;
  });

  function sendUrlToServer(url) {
    // Make sure to replace 'http://localhost:8000' with the actual URL of your server
    const serverUrl = "http://localhost:8000";

    // Create an object with the data you want to send to the server
    const data = {
      url: url,
    };

    // Use jQuery's AJAX function to send a POST request to the server
    $.ajax({
      url: `${serverUrl}/process_url`, // Replace 'your-server-endpoint' with the actual endpoint on your server
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        console.log("URL sent to server successfully:", response);
        // Handle the server response if needed
        window.location.href = `chat.html?url=${encodeURIComponent(url)}`;

      },
      error: function (error) {
        console.error("Error sending URL to server:", error);
        // Handle the error if needed
      },
    });
  }

  // Function to add PDF or URL to the table
  function addToTable(name, size) {
    const tableBody = $("#pdfTable tbody");
    const row = $("<tr>");
    const nameCell = $("<td>").text(name);
    const sizeCell = $("<td>").text(size);
    const optionsCell = $("<td>").append(createOptionsMenu());
    row.append(nameCell, sizeCell, optionsCell);
    tableBody.append(row);
  }
});
// Function to create the options menu
function createOptionsMenu() {
  const optionsMenu = $("<div class='options-menu'>");
  const optionsBtn = $("<div class='options-btn'>").html(
    "<span>&#8942;</span>"
  );

  const optionsContent = $("<div class='options-content'>");
  const openToChat = $("<a href='#'>").text("Open to Chat");
  const deleteOption = $("<a href='#'>").text("Delete");

  optionsContent.append(openToChat, deleteOption);
  optionsMenu.append(optionsBtn, optionsContent);

  return optionsMenu;
}
// Show/hide options menu on button click
$(document).on("click", ".options-btn", function () {
  const optionsContent = $(this).siblings(".options-content");
  optionsContent.toggle();
});

// Close options menu when clicking outside
$(document).on("click", function (event) {
  if (!$(event.target).closest(".options-menu").length) {
    $(".options-content").hide();
  }
});
