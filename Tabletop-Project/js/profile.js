window.onload = function() {
    document.getElementById("username").innerHTML += localStorage.getItem("curr");
}

document.getElementById("userbox").innerHTML = `<font size="6" class="blue-grey-text text-lighten-4"><b>${localStorage.getItem("curr")}</b></font>`

const user = localStorage.getItem("curr");

if (localStorage.getItem(user + "race")) {
    document.getElementById("raceCheck").className = "far fa-check-square"
}

if (localStorage.getItem(user + "class")) {
    document.getElementById("classCheck").className = "far fa-check-square"
}

if (localStorage.getItem(user + "weapon")) {
    document.getElementById("weaponCheck").className = "far fa-check-square"
}

if (localStorage.getItem(user + "spell")) {
    document.getElementById("spellCheck").className = "far fa-check-square"
}

if(localStorage.getItem(user + "race") && localStorage.getItem(user + "class") && localStorage.getItem(user + "weapon") && localStorage.getItem(user + "spell")){
  document.getElementById("achievement").innerHTML = "You have created a character!";
}
