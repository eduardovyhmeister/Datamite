// Function to validate preferences. To be used in combination with 
// PreferencesSelectionForm (ANPAHP/forms/preferences.py). Will look
// for the slider elements and check that they are consistent.

// HOW TO:
// Use <form method='POST' onsubmit="return validatePreferences()"> 
// on your form to check the validity of the preferences.

function validatePreferences() {
    //Use to validate the preferences:
    // - If none are 0, then everything is okay.
    // - If at least 1 is 0, show a warning and ask for confirmation.
    // - If all are equal, raise a warning and ask for confirmation.
    // - If all are 0, raise an error.
    const inputs = document.querySelectorAll('.slider');
    const values = Array.from(inputs).map(input => parseInt(input.value || "0"));
    const allZero = values.every(v => v === 0);
    const someZero = values.some(v => v === 0);
    const allEqual = values.every(v => v === values[0]);
    const messageDiv = document.getElementById('preferenceMessage');

    messageDiv.classList.remove('d-none', 'alert-danger', 'alert-warning');

    if (allZero) {
        messageDiv.textContent = "⚠️ You cannot set all preferences to zero. Please adjust at least one value.";
        messageDiv.classList.add('alert-danger');
        return false; // Prevent submission
    }

    if (someZero) {
        const confirmProceed = confirm("Some preferences are set to 0. This will prevent you from selecting any KPI/metric from the concerned BSC families. Do you want to continue?");
        if (!confirmProceed) {
            messageDiv.textContent = "Preferences submission cancelled. Please adjust your inputs.";
            messageDiv.classList.add('alert-warning');
            return false;
        }
    }

    if (allEqual) {
        const confirmEqual = confirm("All preference values are equal. Are you sure this is intentional? This would mean that no family of KPIs/metrics will have a larger weight in the ANP-AHP analysis.");
        if (!confirmEqual) {
            messageDiv.textContent = "Submission cancelled. Please adjust your inputs.";
            messageDiv.classList.add('alert-warning');
            return false;
        }
    }

    return true; // All good
}