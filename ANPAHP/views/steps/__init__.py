"""Package containing all the views' code for the various steps of the ANP-AHP
process. Each complex view should have its own Python file in order to keep 
things ordered, clean and easy to nagivate."""

# Enables imports in the form of 'from .views.steps import step1'
from .step1 import step1_view
from .step2 import step2_view
from .step3 import step3_view
from .step4 import step4_view
from .step5 import step5_view
from .step6 import step6_view