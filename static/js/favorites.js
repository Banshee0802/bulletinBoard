import { adAction } from "/static/js/utils.js";

const adsContainer = document.getElementById('adsContainer') || document.body;

adsContainer.addEventListener('click', async (event) => {
    const btn = event.target.closest('.favoriteBtn');
    if (!btn) return;

    try {
        const icon = btn.querySelector('.favoriteIcon');
        const count = btn.nextElementSibling;
        const url = btn.dataset.url;
        const adId = btn.dataset.adId;

        const data = await adAction(url, { advertisement_id: adId });

        if (data.is_favorite) {
            icon.classList.replace('bi-bookmark', 'bi-bookmark-fill');
        } else {
            icon.classList.replace('bi-bookmark-fill', 'bi-bookmark');
            
            if (window.location.pathname.includes('favorites')) {
                const adCard = btn.closest('.adCard');
                if (adCard) {
                    adCard.remove();
                    
                    const remainingAds = document.querySelectorAll('.adCard');
                    if (remainingAds.length === 0) {
                        const container = document.querySelector('.container');
                        if (container) {
                            container.innerHTML = '<p>Пусто</p>';
                        }
                    }
                }
            }
        }

        count.textContent = data.favorites_count;

    } catch (err) {
        console.error("Ошибка при работе кнопки избранного:", err);
    }
});
