function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initializeFavorites() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const adId = this.getAttribute('data-ad-id');
            const heart = this.querySelector('.heart');
            const textSpan = this.querySelector('.favorite-text');
            
            this.disabled = true;
            
            fetch("/toggle-favorite/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    ad_id: adId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    heart.classList.toggle('active', data.is_favorite);
                    
                    if (textSpan) {
                        textSpan.textContent = data.is_favorite ? 'В избранном' : 'В избранное';
                    }
                } else {
                    alert('Ошибка: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка');
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', initializeFavorites);