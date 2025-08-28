function ToggleReplies(commentId) {
    let toggleLabel = document.getElementById(`toggle-replies-${commentId}`);
    let repliesContainer = document.getElementById(`replies-for-${commentId}`);
    let replyCountSpan = document.getElementById(`hidden-reply-count-${commentId}`);

    let contentTypeId = toggleLabel.dataset.contentTypeId;
    let objectId = toggleLabel.dataset.objectId;
    let url = `/comments/reply-count/${contentTypeId}/${objectId}/${commentId}/`

    if (!repliesContainer || !replyCountSpan || !toggleLabel) {
        console.error("Ошибка: Один из элементов не найден.");
        return;
    }

    let computedStyles = window.getComputedStyle(repliesContainer);

    if (computedStyles.display === 'none') {
        repliesContainer.style.display = 'block';
        toggleLabel.innerHTML = '&#9650; Скрыть';
    } else {
        repliesContainer.style.display = 'none';
        replyCountSpan = htmx.ajax('GET', url, {target: `#toggle-replies-${commentId}`, swap: 'innerHTML'});
        toggleLabel.textContent = replyCountSpan.innerHTML;
    }
}

document.addEventListener('click', function(event) {
    const toggleButton = event.target.closest('[id^="toggle-replies-"]');

    if (toggleButton) {
        const commentId = toggleButton.dataset.commentId ||
                         toggleButton.id.replace('toggle-replies-', '');
        if (commentId) {
            ToggleReplies(commentId);
        }
    }
});


// --- Добавление значения к счетчику ответа на комментарии через htmx ---
document.body.addEventListener('htmx:afterRequest', (event) => {
    const form = event.target.closest('.reply-form');
    if (!form) return;

    const { contentTypeId, objectId, commentId } = form.dataset;
    if (!contentTypeId || !objectId || !commentId) {
        console.error("Нет данных для обновления счётчика.");
        return;
    }

    form.remove();

    htmx.ajax('GET', `/comments/reply-count/${contentTypeId}/${objectId}/${commentId}/`, {
        target: `#toggle-replies-${commentId}`,
        swap: 'innerHTML'
    });
});
