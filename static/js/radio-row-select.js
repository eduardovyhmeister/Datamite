// Make a whole selectable when it contains a radio button, preventing
// having to click on the radio button itself.

// HOW TO:
//

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.radio-row').forEach(row => {
        row.addEventListener('click', function (e) {
            if (e.target.tagName.toLowerCase() === 'input') return;
            const radioId = this.dataset.radioId;
            const radio = document.getElementById(radioId);
            if (radio) radio.checked = true;
        });
    });
});