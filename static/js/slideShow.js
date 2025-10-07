"use strict";
let slides = document.querySelectorAll(".slide");

for(let i=0; i < slides.length; i++){
    slides[i].addEventListener("click", ()=>{
        activeClassis();
        slides[i].classList.add("active");
    })
}
function activeClassis(){
    for(let i=0; i < slides.length; i++){
        slides[i].classList.remove("active");
    }
}