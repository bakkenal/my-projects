let current_data = ""
let races = []

fetch('races/manifest.json')
  .then((response) => response.json())
  .then(manifest => {
    for(file of manifest.files) {
      fetch(`races/${file}.json`)
      .then(response => response.json())
      .then(race_data => {
        document.querySelector("race-box").innerHTML += `
        <div class="row">
        <div class="col l1"></div>
        <button id = "${race_data.race}" class = "race btn-large light-blue accent-4 waves-effect col l10 center" type = "button" onclick = "race_click('${race_data.race}')" value = "0">
        ${race_data.race}
        </button>
        </div>
        `

        races.push(race_data)
      })
    }
  })

window.onload = function() {
  document.getElementById("username").innerHTML += localStorage.getItem("curr");
}

const race_click = (ev_id) =>{
  let race_elements = document.getElementsByClassName("race");
  for(i = 0; i<race_elements.length; i++){
    race_elements[i].value = "0";
  }

  for (race of races) {
    if (race.race == ev_id) {
      data = race
    }
  }

  const race_box = document.getElementById(ev_id);
  const race_info = document.getElementById("info");
  if(race_box.value == "0"){
    button = document.getElementById("add");
    race_info.innerHTML = "";
    race_box.value = "1";
    race_info.style = "display:normal";

    let race_card = ``
    race_card += `
    <div class="card blue-grey lighten-5">
    <div class="card-image">
      <img src=${data.image_url} style="max-height:200px; width:auto;" class="right">
    </div>
    <div class="card-content" style="min-height:200px;">
    <span class="card-title">${data.race}</span>`

    race_card += "Statistics".bold()

    Object.keys(data.stats).forEach(function (key) {
      race_card += `
      <p>${data.stats[key]} </p>`;
    });

    Object.keys(data.attributes).forEach(function (attribute) {
      race_card += `
      <div class = "attribute">
        <b>${data.attributes[attribute].name}</b>
        <p>${data.attributes[attribute].description}</p>
      </div>`
    });

    race_card += `
    </div>`

    race_info.innerHTML += race_card;
    current_data = race_card;
    race_card += `
    <div class="card-action">
    <a href="#" onclick = "add_to_pad()" class = "light-blue-text accent-1">Add to Notepad</a>`
    race_info.innerHTML = race_card
  }
}

const add_to_pad = () =>{
  let user = localStorage.getItem("curr");

  localStorage.setItem(user + "track-race", "1");
  if(localStorage.getItem(user + "done") != "1" && localStorage.getItem(user + "track-class") == "1" && localStorage.getItem(user + "track-weapon") == "1" && localStorage.getItem(user + "track-spell") == "1"){
    alert("Character creation achievement earned! \nYou have created your very first character. See your profile page for more details.");
    localStorage.setItem(user + "done", "1");
  }
  localStorage.setItem(user + "race", current_data);
  alert("Added to notepad");
}

const notepad = () =>{
  window.location.href = "http://localhost:8000/notepad.html";
}
