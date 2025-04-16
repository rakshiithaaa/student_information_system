<<<<<<< HEAD
/*document.getElementById('loginForm').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent form submission

  // Get input values
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Simple validation (replace with actual backend validation)
});*/

// Handle Edit Button
document.getElementById('editButton').addEventListener('click', function () {
  const selectedStudent = document.querySelector('input[name="student"]:checked');
  if (selectedStudent) {
      window.location.href = `/edit_student/${selectedStudent.value}`;
  } else {
      alert("Please select a student to edit.");
  }
});

function deleteStudent() {
  if (confirm("Are you sure you want to delete this student?")) {
    const button = document.querySelector(".delete-button");
    button.innerHTML = "Deleting...";  // Update button text
    button.disabled = true;  // Disable button

    fetch(`/delete_student/${studentId}`, { method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete");
        return response.json();
      })
      .then((data) => {
        alert("Student deleted successfully!");
        window.location.href = "/dashboard";
      })
      .catch((error) => {
        alert("Error: " + error.message);
        button.innerHTML = "Delete Data";  // Reset button
        button.disabled = false;
      });
  }
}
=======
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission
  
    // Get input values
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Simple validation (replace with actual backend validation)
    if (username === "admin" && password === "1234") {
      window.location.href = "/dashboard"; // Redirect to dashboard
    } else {
      alert("Invalid Username or Password, Check Again");
    }
  });
  
  // Handle Edit and Delete Buttons
  document.getElementById('editButton').addEventListener('click', function () {
    const selectedStudent = document.querySelector('input[name="student"]:checked');
    if (selectedStudent) {
        window.location.href = `/edit_student/${selectedStudent.value}`;
    } else {
        alert("Please select a student to edit.");
    }
});

document.getElementById('deleteButton').addEventListener('click', function () {
  const selectedStudent = document.querySelector('input[name="student"]:checked');
  if (selectedStudent) {
      if (confirm("Are you sure you want to delete this student?")) {
          window.location.href = `/delete_student/${selectedStudent.value}`;
      }
  } else {
      alert("Please select a student to delete.");
  }
});
>>>>>>> 67d6d9b36165ed5fcc488e5c28d2527fca8275b1
