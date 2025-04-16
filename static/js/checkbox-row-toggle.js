// Make a whole row checkable, preventing having to click exactly
// on the checkbox for it to be checked.

// HOW TO:
// Define your row as follows:
// <tr class="checkable-row" data-checkbox-id="checkbox-{{ obj.pk }}">
// Inside your row, have a checkbox defined as follows:
// <input type="checkbox" id="checkbox-{{ obj.pk }}" name=...>
// Now the whole row can be clicked instead of just the checkbox.

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.checkable-row').forEach(row => {
        row.addEventListener('click', function (e) {
            if (e.target.tagName.toLowerCase() === 'input') return;
            const checkboxId = this.dataset.checkboxId;
            const checkbox = document.getElementById(checkboxId);
            if (checkbox) checkbox.checked = !checkbox.checked;
        });
    });
});