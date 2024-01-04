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
  