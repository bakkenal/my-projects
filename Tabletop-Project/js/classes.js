let current_data = ""
let classes = []

fetch('classes/manifest.json')
  .then((response) => response.json())
  .then(manifest => {
    for(file of manifest.files) {
      fetch(`classes/${file}.json`)
      .then(response => response.json())
      .then(class_data => {
        document.querySelector("class-box").innerHTML += `
        <div class="row">
        <div class="col l1"></div>
        <button id = "${class_data.class}" class = "class btn-large light-blue accent-4 waves-effect col l10 center" type = "button" onclick = "class_click('${class_data.class}')" value = "0">
        ${class_data.class}
        </button>
        </div>
        `

        classes.push(class_data)
      })
    }
  })

window.onload = function() {
  document.getElementById("username").innerHTML += localStorage.getItem("curr");
}

const class_click = (ev_id) =>{
  let class_elements = document.getElementsByClassName("class");
  for(i = 0; i<class_elements.length; i++){
    class_elements[i].value = "0";
  }

  for (c of classes) {
    if (c.class == ev_id) {
      data = c
    }
  }

  const class_box = document.getElementById(ev_id);
  const class_info = document.getElementById("info");
  if(class_box.value == "0"){
    button = document.getElementById("add");
    class_info.innerHTML = "";
    class_box.value = "1";
    class_info.style = "display:normal";

    let class_card = ``
    class_card += `
    <div class="card blue-grey lighten-5">
    <div class="card-image">
      <img src=${data.image_url} style="max-height:200px; width:auto;" class="right">
    </div>
    <div class="card-content" style="min-height:200px;">
    <span class="card-title">${data.class}</span>`

    class_card += `
     <p>${"HP:  " + data.hp}</p>
     `;

     Object.keys(data.proficiencies).forEach(function (key) {
       if(data.proficiencies[key].length != 0){
         class_card += `
         <p>${key.charAt(0).toUpperCase() + key.slice(1) + ":  " + data.proficiencies[key]}</p>
         `;
       }
       else{
         class_card += `
         <p>${key.charAt(0).toUpperCase() + key.slice(1) + ":  " + "none"}</p>
         `;
       }
     });

     class_card +=  'Equip options:  ';

     for(i in data['equip-options']){
       if(i == data['equip-options'].length-1){
         class_card +=  data['equip-options'][i];
       }
       else{
         class_card +=  data['equip-options'][i] + ", ";
       }
     }

     class_card += `
     <p>${"Spells".bold().fontsize(5)}</p>
     `;



     if(isEmpty(data.spells)){
       class_card += `
       <p>${"none"}</p>
       `
     }

    else{
     Object.keys(data.spells).forEach(function (s) {
       class_card += `
       <div class = "feature">
         <b>${s}</b>
         <p>${data.spells[s]}</p>
       </div>
       `
     });
   }

     class_card += `
     <p>${"Features".bold().fontsize(5)}</p>
     `;

     Object.keys(data.features).forEach(function (feature) {
       class_card += `
       <div class = "feature">
         <b>${data.features[feature].name}</b>
         <p>${data.features[feature].description}</p>
       </div>
       `
     });

    class_card += `
    </div>`

    class_info.innerHTML += class_card;
    current_data = class_card;
    class_card += `
    <div class="card-action">
    <a href="#" onclick = "add_to_pad()" class = "light-blue-text accent-1">Add to Notepad</a>`
    class_info.innerHTML = class_card
  }
}

const add_to_pad = () =>{
  let user = localStorage.getItem("curr");

  localStorage.setItem(user + "track-class", "1");
  if(localStorage.getItem(user + "done") != "1" && localStorage.getItem(user + "track-class") == "1" && localStorage.getItem(user + "track-weapon") == "1" && localStorage.getItem(user + "track-spell") == "1"){
    alert("Character creation achievement earned! \nYou have created your very first character. See your profile page for more details.");
    localStorage.setItem(user + "done", "1");
  }
  localStorage.setItem(user + "class", current_data);
  alert("Added to notepad");
}

const notepad = () =>{
  window.location.href = "http://localhost:8000/notepad.html";
}

const isEmpty = (obj) =>{
  for(var s in obj) {
      if(obj.hasOwnProperty(s))
          return false;
  }
  return true;
}
