// Register new user
function registerUser() {
  let username = document.getElementById("username").value;
  if (!username) {
    alert("Please enter a name!");
    return;
  }

  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: username })
  })
  .then(response => response.json())
  .then(data => alert(data.message))
  .catch(err => console.error(err));
}

// Take attendance
function takeAttendance() {
  fetch("http://127.0.0.1:5000/attendance")
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(err => console.error(err));
}

// View report
function viewReport() {
  fetch("http://127.0.0.1:5000/report")
    .then(response => response.text())
    .then(csv => {
      document.getElementById("report").textContent = csv;
    })
    .catch(err => console.error(err));
}
