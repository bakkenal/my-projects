let current_data = ""
let weapons = []

fetch('items/manifest.json')
  .then((response) => response.json())
  .then(manifest => {
    for(file of manifest.files) {
      fetch(`items/${file}.json`)
      .then(response => response.json())
      .then(weapon_data => {
        document.querySelector("weapon-box").innerHTML += `
        <div class="row">
        <div class="col l1"></div>
        <button id = "${weapon_data.item}" class = "weapon btn-large light-blue accent-4 waves-effect col l10 center" type = "button" onclick = "weapon_click('${weapon_data.item}')" value = "0">
        ${weapon_data.item}
        </button>
        </div>
        `

        weapons.push(weapon_data)
      })
    }
  })

  window.onload = function() {
    document.getElementById("username").innerHTML += localStorage.getItem("curr");
  }

const weapon_click = (ev_id) =>{
  let weapon_elements = document.getElementsByClassName("weapon");
  for(i = 0; i<weapon_elements.length; i++){
    weapon_elements[i].value = "0";
  }

  for (weapon of weapons) {
    if (weapon.item == ev_id) {
      data = weapon
    }
  }

  const weapon_box = document.getElementById(ev_id);
  const weapon_info = document.getElementById("info");
  if(weapon_box.value == "0"){
    button = document.getElementById("add");
    weapon_info.innerHTML = "";
    weapon_box.value = "1";
    weapon_info.style = "display:normal";

    let weapon_card = ``
    weapon_card += `
    <div class="card blue-grey lighten-5">
    <div class="card-image">
      <img src=${data.image_url} style="max-height:200px; width:auto;" class="right">
    </div>
    <div class="card-content" style="min-height:200px;">
    <span class="card-title">${data.item}</span>`

    weapon_card += `
    <p>${"Damage:  " + data.damage}</p>
    `;

    Object.keys(data.properties).forEach(function (p) {
      weapon_card += `
      <div weapon = "attribute">
        <b>${data.properties[p].name}</b>
        <p>${data.properties[p].value}</p>
      </div>
      `
    });

    weapon_card += `
    </div>`

    weapon_info.innerHTML += weapon_card;
    current_data = weapon_card;
    weapon_card += `
    <div class="card-action">
    <a href="#" onclick = "add_to_pad()" class = "light-blue-text accent-1">Add to Notepad</a>`
    weapon_info.innerHTML = weapon_card
  }
}

const add_to_pad = () =>{
  let user = localStorage.getItem("curr");

  localStorage.setItem(user + "weapon", current_data);
  localStorage.setItem(user + "track-weapon", "1");
  if(localStorage.getItem(user + "done") != "1" && localStorage.getItem(user + "track-race") == "1" && localStorage.getItem(user + "track-class") == "1" && localStorage.getItem(user + "track-spell") == "1"){
    alert("Character creation achievement earned! \nYou have created your very first character. See your profile page for more details.");
    localStorage.setItem(user + "done", "1");
  }
  alert("Added to notepad");
}

const notepad = () =>{
  window.location.href = "http://0.0.0.0:8000/notepad.html";
}
