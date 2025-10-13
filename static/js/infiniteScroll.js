import { adAction } from "/static/js/utils.js";
import { formatDatesHTML } from "/static/js/format-dates.js";

// функция для бесконечного скролла
class InfiniteScroll {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.offset = Number(this.container.dataset.initialOffset);
        this.url = this.container.dataset.url;
        this.hasMore = this.container.dataset.hasMore === 'true';
        this.triggerType = this.container.dataset.triggerType;
        this.loading = false;
        this.paginateBy = 6;

        this.init();
    }

    init() {
        if (this.triggerType === 'scroll') {
          window.addEventListener('scroll', () => {
            if ((window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 1)) {
                this.loadMore();
            }
        });
    } else if (this.triggerType === 'button') {
        this.loadMoreBtn = document.getElementById(this.container.dataset.loadMoreBtn);
        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => {
                this.loadMore()
            })
        }
    }
}
    async loadMore() {
        if (this.loading || !this.hasMore) return;

        this.loading = true;
        this.showLoadingSpinner();
        if (this.triggerType === 'button') {
            this.hideLoadMoreButton();
        }

        try {
            const response = await fetch(`${this.url}?offset=${this.offset}`);
            const data = await response.json();

            const formattedHTML = formatDatesHTML(data.html);

            this.container.insertAdjacentHTML('beforeend', formattedHTML);
            this.offset += this.paginateBy;
            this.hasMore = data.has_more;

            if (this.triggerType === 'button' && this.hasMore) {
                this.showLoadMoreButton();
            }
        } catch (error) {
            console.error('Ошибка загрузки:', error);

            if (this.triggerType === 'button') {
                this.showLoadMoreButton();
            }
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

    showLoadMoreButton() {
        this.loadMoreBtn.classList.remove('d-none');
    }

    hideLoadMoreButton() {
        this.loadMoreBtn.classList.add('d-none');
    }
}

document.addEventListener('DOMContentLoaded', () => {
  const adsContainer = document.getElementById('adsContainer');
  if (adsContainer) new InfiniteScroll('adsContainer');

  const commentsContainer = document.getElementById('comments-container');
  if (commentsContainer) new InfiniteScroll('comments-container');
});

