document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('description');
    const preview = document.getElementById('markdown-preview');

    textarea.addEventListener('input', function() {
        const markdownText = textarea.value;
        const html = marked(markdownText);
        preview.innerHTML = html;
    });
});
