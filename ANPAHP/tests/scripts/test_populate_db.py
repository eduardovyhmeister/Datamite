import logging
import unittest.mock as mock
import tempfile

from django.test import TestCase
import testfixtures

from ...models import KPI, Objective, Criterion
from ...models.enumerations import BSCFamily
from ...scripts.populate_db import populate_KPIs
from utils.custom_logger import get_logger


class PopulateDBTests(TestCase):
    """A class to test the 'populate_db.py' script."""
    
    def setUp(self):
        """Method called before each test."""
        # Changes the logger to prevent logging from printing in stdout:
        self.temp_logger_file = tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False)
        self.handler = logging.FileHandler(self.temp_logger_file.name)
        self.logger = get_logger(__name__, level = logging.INFO, handler = self.handler)
        
    def tearDown(self):
        """Method called after each test."""
        # Clean up the temporary logger mess:
        self.handler.close()
        self.logger.removeHandler(self.handler)
        self.logger = None
        self.temp_logger_file.close()
        
    
    def test_populate_kpis_correct_values(self):
        """'populate_KPIs()' should populate the KPIs table correctly with no
        warnings or error messages when provided with a correct csv file."""
        # Create a temp file of a correct KPI csv file:
        with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
            temp.write(b"name,explanation,BSCfamily\n")
            for i, bsc_family in enumerate(BSCFamily):
                temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
            temp.close()
            
            # Test populate_KPIs() with the file:
            with testfixtures.LogCapture() as logs:
                with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
                    with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
                        populate_KPIs()
            
                # Only info logs, one generic info and one per KPI:
                self.assertEqual(len(logs), len(BSCFamily) + 1)
                for record in logs:
                    self.assertEqual(record[1], "INFO")
            
            # Checks that the right amount of KPIs where inserted, with the right values:
            kpis = KPI.objects.all()
            self.assertEqual(len(kpis), len(BSCFamily))
            for i, kpi in enumerate(kpis):
                self.assertEqual(kpi.name, f"Test{i}")
                self.assertEqual(kpi.explanation, f"Explanation{i}")
                self.assertEqual(kpi.BSCfamily, list(BSCFamily)[i])
    
    
    def test_populate_kpis_incorrect_bsc_family(self):
        """'populate_KPIs()' should not insert KPIs that have an
        invalid BSCfamily and log an error for each one."""
        with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
            temp.write(b"name,explanation,BSCfamily\n")
            for i, bsc_family in enumerate(BSCFamily):
                temp.write(f"Test{i},Explanation{i},{bsc_family}_error\n".encode())
            temp.close()
        
            # Test populate_KPIs() with the file:
            with testfixtures.LogCapture() as logs:
                with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
                    with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
                        populate_KPIs()
            
                # Check logs, one INFO and the rest errors:
                self.assertEqual(len(logs), len(BSCFamily) + 1)
                msg_types = [record[1] for record in logs]
                self.assertEqual(msg_types[0], "INFO") # The first message is always at the INFO level.
                for log_type in msg_types[1:]:
                    self.assertEqual(log_type, "ERROR")
            
            # Should not have inserted anything:
            kpis = KPI.objects.all()
            self.assertEqual(len(kpis), 0)
                    
    
    def test_populate_kpis_too_many_columns(self):
        """'populate_KPIs() should not populate anything with a file containing too many
        columns AND log a critical message."""
        with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
            temp.write(b"name,explanation,BSCfamily,extra_column\n")
            for i, bsc_family in enumerate(BSCFamily):
                temp.write(f"Test{i},Explanation{i},{bsc_family},extra{i}\n".encode())
            temp.close()
        
            # Test populate_KPIs() with the file:
            with testfixtures.LogCapture() as logs:
                with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
                    with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
                        populate_KPIs()
            
                self.assertEqual(len(logs), 2)
                self.assertEqual(logs[0][1], "INFO")
                self.assertEqual(logs[1][1], "CRITICAL")
        
            # Should not have inserted anything:
            kpis = KPI.objects.all()
            self.assertEqual(len(kpis), 0)
            

    def test_populate_kpis_too_few_columns(self):
        """'populate_KPIs() should not populate anything with a file containing too few
        columns AND log a critical message."""
        with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
            temp.write(b"name,BSCfamily\n")
            for i, bsc_family in enumerate(BSCFamily):
                temp.write(f"Test{i},{bsc_family}\n".encode())
            temp.close()
        
            # Test populate_KPIs() with the file:
            with testfixtures.LogCapture() as logs:
                with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
                    with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
                        populate_KPIs()
            
                self.assertEqual(len(logs), 2)
                self.assertEqual(logs[0][1], "INFO")
                self.assertEqual(logs[1][1], "CRITICAL")
        
            # Should not have inserted anything:
            kpis = KPI.objects.all()
            self.assertEqual(len(kpis), 0)
            
    
    def test_populate_kpis_duplicates(self):
        """'populate_KPIs()' should not add duplicates to the database AND log an error
        for every duplicate."""
        with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
            temp.write(b"name,explanation,BSCfamily\n")
            for i, bsc_family in enumerate(BSCFamily):
                temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
                temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
            temp.close()
            
            # Test populate_KPIs() with the file:
            with testfixtures.LogCapture() as logs:
                with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
                    with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
                        populate_KPIs()
            
                # Only info logs, one generic info and one per KPI:
                self.assertEqual(len(logs), 2*len(BSCFamily) + 1)
                msg_types = [record[1] for record in logs]
                self.assertEqual(msg_types[0], "INFO")
                # Every other entry is a duplicate:
                for i, msg in enumerate(msg_types[1:]):
                    if i%2 == 0: self.assertEqual(msg, "INFO")
                    else: self.assertEqual(msg, "ERROR")
                    
            # Checks that the right amount of KPIs where inserted, with the right values:
            kpis = KPI.objects.all()
            self.assertEqual(len(kpis), len(BSCFamily))
            for i, kpi in enumerate(kpis):
                self.assertEqual(kpi.name, f"Test{i}")
                self.assertEqual(kpi.explanation, f"Explanation{i}")
                self.assertEqual(kpi.BSCfamily, list(BSCFamily)[i])
    