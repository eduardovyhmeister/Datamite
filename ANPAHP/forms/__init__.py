"""Package containing all the forms' code. Each form should have
its own Python file in order to keep things ordered, clean and 
easy to nagivate."""

# Enables imports in the form of 'from .forms import RegisterForm'
from .register import RegisterForm
from .anpahp import ANPAHPForm
from .notes import NotesForm
from .objectives import (ObjectiveSelectionForm,
                         CreateObjectiveForm,
                         DeleteObjectiveForm)
from .preferences import BSCPreferencesForm