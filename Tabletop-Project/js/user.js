const signin = () =>{
  window.location.href = "signin.html";
}

const signup = () =>{
  window.location.href = "signup.html";
}

const new_account = () =>{
  let email = document.getElementById("new_email").value
  let password = document.getElementById("new_password").value
  let password_repeat = document.getElementById("password_repeat").value

  if(email == "" || password == "" || password_repeat == ""){
    alert("Please fill in the required fields.");
  }

  else if(localStorage.getItem(email) != null){
    alert("This account already exists.");
  }

  else if(password != password_repeat){
    alert("Passwords do not match.");
  }

  else if(email.length > 10){
    alert("Username is more than 10 characters.");
  }

  else{
    localStorage.setItem(email, password);
    localStorage.setItem("curr", email);
    window.location.href = "races.html";
  }
}

const old_account = () =>{
  let email = document.getElementById("old_email").value
  let password = document.getElementById("old_password").value

  if(email == "" || password == ""){
    alert("Please fill in the required fields.");
  }

  else if(localStorage.getItem(email) == null){
    alert("This account does not exist.");
  }

  else if(localStorage.getItem(email) != password){
    alert("Incorrect password. Try again.");
  }

  else{
    localStorage.setItem("curr", email);
      window.location.href = "races.html";
  }

  document.getElementById("username").innerHTML = email;
}
