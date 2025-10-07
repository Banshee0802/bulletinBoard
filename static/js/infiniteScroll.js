
// функция для бесконечного скролла
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