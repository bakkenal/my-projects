window.onload = function() {
  let user = localStorage.getItem("curr");

  document.getElementById("username").innerHTML += localStorage.getItem("curr");

  document.getElementById("race").innerHTML = `<font size="6" class="blue-grey-text text-lighten-4"><b>Race</b></font>`
  if (localStorage.getItem(user + "race")) {
    document.getElementById("race").innerHTML += localStorage.getItem(user + "race");
  }

  document.getElementById("class").innerHTML = `<font size="6" class="blue-grey-text text-lighten-4"><b>Class</b></font>`
  if (localStorage.getItem(user + "class")) {
    document.getElementById("class").innerHTML += localStorage.getItem(user + "class");
  }

  document.getElementById("weapon").innerHTML = `<font size="6" class="blue-grey-text text-lighten-4"><b>Weapon</b></font>`
  if (localStorage.getItem(user + "weapon")) {
    document.getElementById("weapon").innerHTML += localStorage.getItem(user + "weapon");
  }

  document.getElementById("spell").innerHTML = `<font size="6" class="blue-grey-text text-lighten-4"><b>Spell</b></font>`
  if (localStorage.getItem(user + "spell")) {
    document.getElementById("spell").innerHTML += localStorage.getItem(user + "spell");
  }
}
