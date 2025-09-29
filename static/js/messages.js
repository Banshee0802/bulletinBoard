document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.close-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const message = this.closest('.alert');
            message.style.transform = 'translateX(100%)';
            message.style.opacity = '0';
            setTimeout(function() {
                if (message.parentNode) {
                    message.remove();
                }
            }, 300);
        });
    });
    
    document.querySelectorAll('.message-item').forEach(function(message) {
        setTimeout(function() {
            if (message.parentNode) {
                message.style.transform = 'translateX(100%)';
                message.style.opacity = '0';
                setTimeout(function() {
                    if (message.parentNode) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
});