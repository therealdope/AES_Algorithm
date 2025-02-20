// clear.js
document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            // Reset the form fields
            const form = this.closest('form');
            if (form) {
                form.reset();
            }
            // Clear the result display area
            const resultDiv = document.getElementById('resultDiv');
            if (resultDiv) {
                resultDiv.innerHTML = '<p class="text-gray-500">Results will appear here</p>';
            }
        });
    }
});