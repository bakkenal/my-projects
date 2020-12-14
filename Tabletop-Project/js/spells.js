let current_data = ""
let spells = []

fetch('spells/manifest.json')
  .then((response) => response.json())
  .then(manifest => {
    for(file of manifest.files) {
      fetch(`spells/${file}.json`)
      .then(response => response.json())
      .then(spell_data => {
        document.querySelector("spell-box").innerHTML += `
        <div class="row">
        <div class="col l1"></div>
        <button id = "${spell_data.spell}" class = "spell btn-large light-blue accent-4 waves-effect col l10 center" type = "button" onclick = "spell_click('${spell_data.spell}')" value = "0">
        ${spell_data.spell}
        </button>
        </div>
        `

        spells.push(spell_data)
      })
    }
  })

  window.onload = function() {
    document.getElementById("username").innerHTML += localStorage.getItem("curr");
  }

const spell_click = (ev_id) =>{
  let spell_elements = document.getElementsByClassName("spell");
  for(i = 0; i<spell_elements.length; i++){
    spell_elements[i].value = "0";
  }

  for (spell of spells) {
    if (spell.spell == ev_id) {
      data = spell
    }
  }

  const spell_box = document.getElementById(ev_id);
  const spell_info = document.getElementById("info");
  if(spell_box.value == "0"){
    button = document.getElementById("add");
    spell_info.innerHTML = "";
    spell_box.value = "1";
    spell_info.style = "display:normal";

    let spell_card = ``
    spell_card += `
    <div class="card blue-grey lighten-5">
    <div class="card-image">
      <img src=${data.image_url} style="max-height:200px; width:auto;" class="right">
    </div>
    <div class="card-content" style="min-height:200px;">
    <span class="card-title">${data.spell}</span>`

    spell_card += `
    <p>${"Level: " + data.level}</p>
    `;

    Object.keys(data.properties).forEach(function (p) {
      spell_card += `
      <div class = "property">
        <b>${data.properties[p].name}</b>
        <p>${data.properties[p].value}</p>
      </div>
      `
    });

    spell_card += `
    <p>${"Description: " + data.description}</p>
    `;



    spell_card += `
    </div>`

    spell_info.innerHTML += spell_card;
    current_data = spell_card;
    spell_card += `
    <div class="card-action">
    <a href="#" onclick = "add_to_pad()" class = "light-blue-text accent-1">Add to Notepad</a>`
    spell_info.innerHTML = spell_card
  }
}

const add_to_pad = () =>{
  let user = localStorage.getItem("curr");

  localStorage.setItem(user + "spell", current_data);
  localStorage.setItem(user + "track-spell", "1");
  if(localStorage.getItem(user + "done") != "1" && localStorage.getItem(user + "track-class") == "1" && localStorage.getItem(user + "track-spell") == "1" && localStorage.getItem(user + "track-race") == "1"){
    alert("Character creation achievement earned! \nYou have created your very first character. See your profile page for more details.");
    localStorage.setItem(user + "done", "1");
  }
  alert("Added to notepad");
}

const notepad = () =>{
  window.location.href = "http://0.0.0.0:8000/notepad.html";
}
