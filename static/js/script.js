
// функция к картинкам на главной странице
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


// функция для очистки поиска
function clearSearch() {
    console.log('clearSearch called!');
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.value = '';
        searchInput.form.submit();
    }
}

// функция для показа/скрытия крестика
function toggleClearButton() {
    const searchInput = document.getElementById('search-input');
    const clearBtn = document.getElementById('clear-search');
    
    if (searchInput && clearBtn) {
        if (searchInput.value.trim() !== '') {
            clearBtn.style.display = 'block';
        } else {
            clearBtn.style.display = 'none';
        }
    }
}

// назначение обработчиков после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    
    if (searchInput) {
        searchInput.addEventListener('input', toggleClearButton);
        searchInput.addEventListener('keyup', toggleClearButton);
        // проверка начального состояния
        toggleClearButton();
    }
});