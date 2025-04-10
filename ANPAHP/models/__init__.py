"""Package containing all the model definitions. Each model should have
its own Python file in order to keep things ordered and clean."""

# Enables imports in the form of 'from .models import Criterion'
from .bsc_family import BSCFamily, BSCSubfamily
from .criterion import Criterion
from .evaluation import Evaluation
from .kpi import KPI
from .objective import Objective
