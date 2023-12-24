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







function buttonClick() {
  document.getElementById("fileID").click();
}

function handleFileUpload(files) {
  const tableBody = $("#pdfTable tbody");

  for (const file of files) {
    const row = $("<tr>");
    const fileNameCell = $("<td>").text(file.name);
    const fileSizeCell = $("<td>").text((file.size / 1024).toFixed(2));
    const optionsCell = $("<td>").append(createOptionsMenu());
    row.append(fileNameCell, fileSizeCell, optionsCell);
    tableBody.append(row);
  }
}

$(function(){
  // URL form submission handling
  $("#urlForm").submit(function(e) {
    e.preventDefault();
    const url = $("#url").val();
    addToTable(url, "N/A");
    // Clear the input field after adding to the table
    $("#url").val("");
  });

  // Function to add PDF or URL to the table
  function addToTable(name, size) {
    const tableBody = $("#pdfTable tbody");
    const row = $("<tr>");
    const nameCell = $("<td>").text(name);
    const sizeCell = $("<td>").text(size);
    const optionsCell = $("<td>").append(createOptionsMenu());
    row.append(nameCell, sizeCell,optionsCell);
    tableBody.append(row);
  }
});

 // Function to create the options menu
 function createOptionsMenu() {
  const optionsMenu = $("<div class='options-menu'>");
  const optionsBtn = $("<div class='options-btn'>").html("<span>&#8942;</span>");

  const optionsContent = $("<div class='options-content'>");
  const openToChat = $("<a href='#'>").text("Open to Chat");
  const deleteOption = $("<a href='#'>").text("Delete");

  optionsContent.append(openToChat, deleteOption);
  optionsMenu.append(optionsBtn, optionsContent);

  return optionsMenu;
}
// Show/hide options menu on button click
$(document).on("click", ".options-btn", function() {
  const optionsContent = $(this).siblings(".options-content");
  optionsContent.toggle();
});

// Close options menu when clicking outside
$(document).on("click", function(event) {
  if (!$(event.target).closest(".options-menu").length) {
    $(".options-content").hide();
  }
});
