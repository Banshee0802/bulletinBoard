
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

// функция для спиннера
class InfiniteScroll {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.offset = Number(this.container.dataset.initialOffset);
        this.url = this.container.dataset.url;
        this.hasMore = this.container.dataset.hasMore === 'true';
        this.loading = false;
        this.paginateBy = 6;

        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            if ((window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 1)) {
                this.loadMoreAds();
            }
        });
    }

    async loadMoreAds() {
        if (this.loading || !this.hasMore) return;

        this.loading = true;
        this.showLoadingSpinner();

        try {
            const response = await fetch(`${this.url}?offset=${this.offset}`);
            const data = await response.json();

            this.container.insertAdjacentHTML('beforeend', data.html);
            this.offset += this.paginateBy;
            this.hasMore = data.has_more;
        } catch (error) {
            console.error('Ошибка загрузки:', error);
        } finally {
            this.loading = false;
            this.hideLoadingSpinner();
        }
    }

    showLoadingSpinner() {
        document.getElementById('loadingSpinner')?.classList.remove('d-none');
    }

    hideLoadingSpinner() {
        document.getElementById('loadingSpinner')?.classList.add('d-none');
    }
}

    new InfiniteScroll('adsContainer');
