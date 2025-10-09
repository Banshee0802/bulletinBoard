"use strict";

import { adAction } from "./utils.js";

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#comment-form');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const url = form.dataset.url;
    const advertisementId = form.querySelector('input[name="advertisement_id"]').value;
    const text = form.querySelector('textarea[name="text"]').value.trim();

    if (!text) {
      alert('Текст комментария не может быть пустым');
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
      console.error('Ошибка при добавлении комментария:', error);
      alert('Произошла ошибка при отправке комментария.');
    }
  });
});

// удаление комментария в реалтайме
document.addEventListener('click', async function(e) {
    if (!e.target.classList.contains('delete-comment-btn')) return;

    const btn = e.target;
    const url = btn.dataset.url;

    if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) return;

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
      console.error('Ошибка при удалении комментария:', err);
      alert('Произошла ошибка при удалении комментария.');
    }
  });
