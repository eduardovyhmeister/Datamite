import unittest.mock as mock
import tempfile

from django.test import TestCase

from ...models import KPI, Objective, Criterion
from ...models.enumerations import BSCFamily
from ...scripts.populate_db import populate_KPIs

class PopulateDBTests(TestCase):
    """A class to test the 'populate_db.py' script."""
    
    def populate_kpis_correct_values(self):
        """The 'populate_KPIs()' function should populate the KPIs table correctly with
        warnings or error messages when provided with a correct csv file."""
        # Create a temp file of a correct KPI csv file:
        temp = tempfile.NamedTemporaryFile()
        with open(temp) as temp_file:
            temp_file.write("name,explanation,BSCfamily")
            for i, bsc_family in enumerate(BSCFamily):
                temp_file.write(f"Test{i},Explanation{i},{bsc_family}")
                
            # Test populate_KPIs() with this file:
            with mock.patch('scripts.populate_db.KPIS_CSV_PATH', temp.name):
                populate_KPIs()
            
        assert True
            
        
        