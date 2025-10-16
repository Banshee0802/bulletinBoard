"use strict";

import { adAction } from "./utils.js";
import { formatDate } from "./format-dates.js";

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#comment-form');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const url = form.dataset.url;
    const advertisementId = form.querySelector('input[name="advertisement_id"]').value;
    const text = form.querySelector('textarea[name="text"]').value.trim();

    if (!text) {
      alert('Текст отзыва не может быть пустым');
      return;
    }

    try {
      const data = await adAction(url, {
        advertisement_id: advertisementId,
        text: text,
      });

      if (data.success) {
        const container = document.querySelector('#comments-container');
        container.insertAdjacentHTML('afterbegin', data.comment_html);
        document.querySelector('#comments-count').textContent = data.comments_count;
        form.reset();
      } else if (data.error) {
        alert(data.error);
      }
    } catch (error) {
      console.error('Ошибка при добавлении отзыва:', error);
      alert('Произошла ошибка при отправке отзыва.');
    }
  });
});

// удаление комментария в реалтайме
document.addEventListener('click', async function(e) {
    if (!e.target.classList.contains('delete-comment-btn')) return;

    const btn = e.target;
    const url = btn.dataset.url;

    if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) return;

    try {
      const data = await adAction(url, {});

      if (data.success) {
        const commentDiv = document.querySelector(`#comment-${data.comment_id}`);
        if (commentDiv) commentDiv.remove();

        const countElem = document.querySelector('#comments-count');
        if (countElem) countElem.textContent = parseInt(countElem.textContent) - 1;
      } else if (data.error) {
        alert(data.error);
      }
    } catch (err) {
      console.error('Ошибка при удалении отзыва:', err);
      alert('Произошла ошибка при удалении отзыва.');
    }
  });


// Ответы на комментарии
class ReplyManager {
  constructor() {
    this.init();
  }
  init() {
    document.addEventListener('click', (event) => {
      if (event.target.closest('.reply-btn')) {
        this.handleReplyClick(event.target.closest('.reply-btn'));
      }

      if (event.target.closest('.cancel-reply')) {
        this.handleCancelReply(event.target.closest('.cancel-reply'))
      }
    });
    document.addEventListener('submit', (event) => {
      if (event.target.closest('.reply-form')) {
        event.preventDefault();
        this.handleReplySubmit(event.target.closest('.reply-form'));
      }
    })
  }
  handleReplyClick(replyBtn) {
    const commentId = replyBtn.dataset.commentId;
    const replyForm = document.getElementById(`replyFormContainer${commentId}`);

    document.querySelectorAll('.reply-form-container').forEach(form => {
      form.classList.add('d-none');
    })

    replyForm.classList.remove('d-none');
    replyForm.querySelector('textarea').focus();
  }

  handleCancelReply(cancelBtn) {
    const replyForm = cancelBtn.closest('.reply-form-container');
    replyForm.classList.add('d-none');
    replyForm.querySelector('textarea').value = '';
  }

  async handleReplySubmit(form) {
    const textarea = form.querySelector('textarea');
    const text = textarea.value.trim();
    if (!text) {
      alert('Введите текст ответа');
      return;
    }
    const advertisementId = form.dataset.advertisementId;
    const parentId = form.dataset.parentId;
    const url = `/ads/${advertisementId}/comments/add/`;

    const requestData = {
      advertisement_id: advertisementId,
      text,
      parentId
    };

    try {
      const data = await adAction(url, requestData);

    if (data.success) {
      textarea.value = '';
      form.closest('.reply-form-container').classList.add('d-none');

      const commentContainer = form.closest('.comment-container');
      let repliesContainer = commentContainer.querySelector('.replies');

      if (!repliesContainer) {
        repliesContainer = document.createElement('div');
        repliesContainer.classList.add('mt-3', 'ms-3', 'border-start', 'ps-3', 'replies');
        commentContainer.appendChild(repliesContainer);
      }

      repliesContainer.insertAdjacentHTML('beforeend', data.comment_html);

      const newReply = repliesContainer.lastElementChild;
      const dateElement = newReply.querySelector('.date-field');
      formatDate(dateElement);

      const commentsCountElement = document.querySelector('#comments-count');
        if (commentsCountElement) {
          commentsCountElement.textContent = data.comments_count;
        }
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error('Ошибка при отправке ответа:', error);
      alert('Произошла ошибка при отправке ответа.');
    }
  }
}

new ReplyManager();