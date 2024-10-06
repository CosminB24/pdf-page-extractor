document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('extractorForm');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const errorDisplay = document.getElementById('error');

    fileInput.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name || 'No file selected';
        fileNameDisplay.textContent = fileName;
    });

    form.addEventListener('submit', (e) => {
        const file = fileInput.files[0];
        const pages = document.getElementById('pages').value;

        if (!file) {
            e.preventDefault();
            showError('Please select a PDF file.');
            return;
        }

        if (!pages) {
            e.preventDefault();
            showError('Please enter page numbers.');
            return;
        }

        // Clear any previous errors
        clearError();
    });

    function showError(message) {
        errorDisplay.textContent = message;
        errorDisplay.classList.add('show');
    }

    function clearError() {
        errorDisplay.textContent = '';
        errorDisplay.classList.remove('show');
    }
});