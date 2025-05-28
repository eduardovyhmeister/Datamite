// Make a whole selectable when it contains a radio button, preventing
// having to click on the radio button itself.

// HOW TO:
// Define your row as follows:
// <tr class="radio-row" data-radio-id="radio-{{ obj.pk }}">
// Inside your row, have a radiobutton defined as follows:
// <input type="radio" id="radio-{{ obj.pk }}" name=...>
// Now the whole row can be clicked instead of just the radiobutton.

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