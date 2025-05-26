import logging
import unittest.mock as mock
import tempfile

from django.test import TestCase
import testfixtures

# from ...models import KPI, Objective, Criterion
# from ...models.enumerations import BSCFamily
# from ...scripts.populate_db import populate_KPIs, populate_objectives, populate_criteria
# from utils.custom_logger import get_logger


class PopulateDBTests(TestCase):
    """A class to test the 'populate_db.py' script."""
    
    # def setUp(self):
    #     """Method called before each test."""
    #     # Changes the logger to prevent logging from printing in stdout while still enabling logging:
    #     self.temp_logger_file = tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False)
    #     self.handler = logging.FileHandler(self.temp_logger_file.name)
    #     self.logger = get_logger(__name__, level = logging.INFO, handler = self.handler)
        
    # def tearDown(self):
    #     """Method called after each test."""
    #     # Clean up the temporary logger mess:
    #     self.handler.close()
    #     self.logger.removeHandler(self.handler)
    #     self.logger = None
    #     self.temp_logger_file.close()
        
    
    # def test_populate_kpis_correct_values(self):
    #     """'populate_KPIs()' should populate the KPIs table correctly with no
    #     warnings or error messages when provided with a correct csv file."""
    #     # Create a temp file of a correct KPI csv file:
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,bsc_family\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
    #         temp.close()
            
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             # Only info logs, one generic info and one per KPI:
    #             self.assertEqual(len(logs), len(BSCFamily) + 1)
    #             for record in logs:
    #                 self.assertEqual(record[1], "INFO")
            
    #         # Checks that the right amount of KPIs where inserted, with the right values:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), len(BSCFamily))
    #         for i, kpi in enumerate(kpis):
    #             self.assertEqual(kpi.name, f"Test{i}")
    #             self.assertEqual(kpi.explanation, f"Explanation{i}")
    #             self.assertEqual(kpi.bsc_family, list(BSCFamily)[i])

    
    # def test_populate_kpis_incorrect_bsc_family(self):
    #     """'populate_KPIs()' should not insert KPIs that have an
    #     invalid bsc_family and log an error for each one."""
    #     with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,bsc_family\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},Explanation{i},{bsc_family}_error\n".encode())
    #         temp.close()
        
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             # Check logs, one INFO and the rest errors:
    #             self.assertEqual(len(logs), len(BSCFamily) + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO") # The first message is always at the INFO level.
    #             for log_type in msg_types[1:]:
    #                 self.assertEqual(log_type, "ERROR")
            
    #         # Should not have inserted anything:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), 0)
            

    # def test_populate_kpis_kpi_already_exists_in_db(self):
    #     """'populate_KPIs()' should not add a KPI already registered in the DB and log a
    #     WARNING message."""
    #     # Add a KPI to the DB
    #     existing_kpi = KPI(name = "Test0", explanation = "AlreadyExplained", bsc_family = BSCFamily.choices[-1][0])
    #     existing_kpi.save()
        
    #     # This should have the first KPI as duplicate:
    #     with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,bsc_family\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
    #         temp.close()
            
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             # Check logs: one INFO, one WARNING, the rest INFO
    #             self.assertEqual(len(logs), len(BSCFamily) + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             self.assertEqual(msg_types[1], "WARNING")
    #             for msg_type in msg_types[2:]:
    #                 self.assertEqual(msg_type, "INFO")
                    
    #         # Check the right number of KPIs where loaded into the DB:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), len(BSCFamily))
    #         self.assertEqual(kpis[0].name, existing_kpi.name)
    #         self.assertEqual(kpis[0].explanation, existing_kpi.explanation)
    #         self.assertEqual(kpis[0].bsc_family, existing_kpi.bsc_family)
    #         for i, kpi in enumerate(kpis[1:], 1):
    #             self.assertEqual(kpi.name, f"Test{i}")
    #             self.assertEqual(kpi.explanation, f"Explanation{i}")
    #             self.assertEqual(kpi.bsc_family, list(BSCFamily)[i])
            
    
    # def test_populate_kpis_too_many_columns(self):
    #     """'populate_KPIs() should not populate anything with a file containing too many
    #     columns AND log a critical message."""
    #     with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,bsc_family,extra_column\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},Explanation{i},{bsc_family},extra{i}\n".encode())
    #         temp.close()
        
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
        
    #         # Should not have inserted anything:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), 0)
            

    # def test_populate_kpis_too_few_columns(self):
    #     """'populate_KPIs() should not populate anything with a file containing too few
    #     columns AND log a critical message."""
    #     with tempfile.NamedTemporaryFile(delete_on_close = False) as temp:
    #         temp.write(b"name,bsc_family\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},{bsc_family}\n".encode())
    #         temp.close()
        
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
        
    #         # Should not have inserted anything:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), 0)
            
    
    # def test_populate_kpis_duplicates(self):
    #     """'populate_KPIs()' should not add duplicates to the database AND log an error
    #     for every duplicate."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,bsc_family\n")
    #         for i, bsc_family in enumerate(BSCFamily):
    #             temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
    #             temp.write(f"Test{i},Explanation{i},{bsc_family}\n".encode())
    #         temp.close()
            
    #         # Test populate_KPIs() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.KPIS_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_KPIs()
            
    #             # Only info logs, one generic info and one per KPI:
    #             self.assertEqual(len(logs), 2*len(BSCFamily) + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             # Every other entry is a duplicate:
    #             for i, msg in enumerate(msg_types[1:]):
    #                 if i%2 == 0: self.assertEqual(msg, "INFO")
    #                 else: self.assertEqual(msg, "ERROR")
                    
    #         # Checks that the right amount of KPIs where inserted, with the right values:
    #         kpis = KPI.objects.all()
    #         self.assertEqual(len(kpis), len(BSCFamily))
    #         for i, kpi in enumerate(kpis):
    #             self.assertEqual(kpi.name, f"Test{i}")
    #             self.assertEqual(kpi.explanation, f"Explanation{i}")
    #             self.assertEqual(kpi.bsc_family, list(BSCFamily)[i])
    
    
    # def test_populate_objectives_correct_values(self):
    #     """'populate_objectives()' populate the objectives AND log INFO only messages."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_objectives = 10
    #         for i in range(nb_objectives):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.OBJECTIVES_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_objectives()
                
    #             # Only info logs, one generic info and one per objective:
    #             self.assertEqual(len(logs), nb_objectives + 1)
    #             for record in logs:
    #                 self.assertEqual(record[1], "INFO")
                
    #         # Check that the right amount of objectives where inserted with the right values:
    #         objectives = Objective.objects.all()
    #         self.assertEqual(len(objectives), nb_objectives)
    #         for i, objective in enumerate(objectives):
    #             self.assertEqual(objective.name, f"Test{i}")
    #             self.assertEqual(objective.explanation, f"Explanation{i}")

    
    # def test_populate_objectives_objective_already_exists_in_db(self):
    #     """'populate_objective()' should not add an objective already in the DB AND
    #     log a WARNING message."""
    #     existing_objective = Objective(name = "Test0", explanation = "AlreadyExplained")
    #     existing_objective.save()
        
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_objectives = 10
    #         for i in range(nb_objectives):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.OBJECTIVES_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_objectives()
                
    #             # One generic info log, one warning, the rest info:
    #             self.assertEqual(len(logs), nb_objectives + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             self.assertEqual(msg_types[1], "WARNING")
    #             for msg_type in msg_types[2:]:
    #                 self.assertEqual(msg_type, "INFO")
                
    #         # Check that the right amount of objectives where inserted with the right values:
    #         objectives = Objective.objects.all()
    #         self.assertEqual(len(objectives), nb_objectives)
    #         self.assertEqual(objectives[0].name, existing_objective.name)
    #         self.assertEqual(objectives[0].explanation, existing_objective.explanation)
    #         for i, objective in enumerate(objectives[1:], 1):
    #             self.assertEqual(objective.name, f"Test{i}")
    #             self.assertEqual(objective.explanation, f"Explanation{i}")
    
    
    # def test_populate_objectives_too_many_columns(self):
    #     """'populate_objectives()' populate the objectives AND log INFO only messages."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,extra_column\n")
    #         nb_objectives = 10
    #         for i in range(nb_objectives):
    #             temp.write(f"Test{i},Explanation{i},Extra{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.OBJECTIVES_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_objectives()
                
    #             # Only two logs, one generic INFO and one CRITICAL:
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
                
    #         # Check that no objectives were input:
    #         objectives = Objective.objects.all()
    #         self.assertEqual(len(objectives), 0)
            
            
    # def test_populate_objectives_too_few_columns(self):
    #     """'populate_objectives()' populate the objectives AND log INFO only messages."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name\n")
    #         nb_objectives = 10
    #         for i in range(nb_objectives):
    #             temp.write(f"Test{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.OBJECTIVES_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_objectives()
                
    #             # Only two logs, one generic INFO and one CRITICAL:
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
                
    #         # Check that no objectives were input:
    #         objectives = Objective.objects.all()
    #         self.assertEqual(len(objectives), 0)
            
    
    # def test_populate_objectives_duplicates(self):
    #     """'populate_objectives()' should not input duplicate objectives AND
    #     log an ERROR message for each duplicate."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_objectives = 10
    #         for i in range(nb_objectives):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.OBJECTIVES_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_objectives()
                
    #             # One generic info, then alternating info and error:
    #             self.assertEqual(len(logs), 2*nb_objectives + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             for i, msg_type in enumerate(msg_types[1:]):
    #                 if i%2 == 0: self.assertEqual(msg_type, "INFO")
    #                 else: self.assertEqual(msg_type, "ERROR")
                
    #         # Check that the right amount of objectives where inserted with the right values:
    #         objectives = Objective.objects.all()
    #         self.assertEqual(len(objectives), nb_objectives)
    #         for i, objective in enumerate(objectives):
    #             self.assertEqual(objective.name, f"Test{i}")
    #             self.assertEqual(objective.explanation, f"Explanation{i}")
                
                
    # def test_populate_criteria_correct_values(self):
    #     """'populate_criteria()' should populate the criteria AND log only INFO."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_criteria = 10
    #         for i in range(nb_criteria):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_criteria() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.CRITERIA_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_criteria()
                
    #             # Only info logs, one generic info and one per criterion:
    #             self.assertEqual(len(logs), nb_criteria + 1)
    #             for record in logs:
    #                 self.assertEqual(record[1], "INFO")
                
    #         # Check that the right amount of criteria where inserted with the right values:
    #         criteria = Criterion.objects.all()
    #         self.assertEqual(len(criteria), nb_criteria)
    #         for i, criterion in enumerate(criteria):
    #             self.assertEqual(criterion.name, f"Test{i}")
    #             self.assertEqual(criterion.explanation, f"Explanation{i}")
                
                
    # def test_populate_criteria_criterion_already_exists_in_db(self):
    #     """'populate_criteria()' should not add a criterion already in the DB AND
    #     log a WARNING message."""
    #     existing_criterion = Criterion(name = "Test0", explanation = "AlreadyExplained")
    #     existing_criterion.save()
        
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_criteria = 10
    #         for i in range(nb_criteria):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_criteria() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.CRITERIA_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_criteria()
                
    #             # One generic info, one warning, and the rest info:
    #             self.assertEqual(len(logs), nb_criteria + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             self.assertEqual(msg_types[1], "WARNING")
    #             for msg_type in msg_types[2:]:
    #                 self.assertEqual(msg_type, "INFO")
                
    #         # Check that the right amount of criteria where inserted with the right values:
    #         criteria = Criterion.objects.all()
    #         self.assertEqual(len(criteria), nb_criteria)
    #         self.assertEqual(criteria[0].name, existing_criterion.name)
    #         self.assertEqual(criteria[0].explanation, existing_criterion.explanation)
    #         for i, criterion in enumerate(criteria[1:], 1):
    #             self.assertEqual(criterion.name, f"Test{i}")
    #             self.assertEqual(criterion.explanation, f"Explanation{i}")
                
                
    # def test_populate_criteria_too_many_columns(self):
    #     """'populate_criteria()' shoud not populate with any criterion and log
    #     a CRITICAL message if the file is invalid."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation,extra_column\n")
    #         nb_criteria = 10
    #         for i in range(nb_criteria):
    #             temp.write(f"Test{i},Explanation{i},Extra{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.CRITERIA_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_criteria()
                
    #             # Only two logs, one generic INFO and one CRITICAL:
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
                
    #         # Check that no objectives were input:
    #         criteria = Criterion.objects.all()
    #         self.assertEqual(len(criteria), 0)
            
            
    # def test_populate_criteria_too_few_columns(self):
    #     """'populate_criteria()' shoud not populate with any criterion and log
    #     a CRITICAL message if the file is invalid."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name\n")
    #         nb_criteria = 10
    #         for i in range(nb_criteria):
    #             temp.write(f"Test{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_objectives() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.CRITERIA_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_criteria()
                
    #             # Only two logs, one generic INFO and one CRITICAL:
    #             self.assertEqual(len(logs), 2)
    #             self.assertEqual(logs[0][1], "INFO")
    #             self.assertEqual(logs[1][1], "CRITICAL")
                
    #         # Check that no objectives were input:
    #         criteria = Criterion.objects.all()
    #         self.assertEqual(len(criteria), 0)
            
    
    # def test_populate_criteria_duplicates(self):
    #     """'populate_criteria()' should not input duplicate criteria AND
    #     log an ERROR message for each duplicate."""
    #     with tempfile.NamedTemporaryFile(dir = '.', delete_on_close = False) as temp:
    #         temp.write(b"name,explanation\n")
    #         nb_criteria = 10
    #         for i in range(nb_criteria):
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #             temp.write(f"Test{i},Explanation{i}\n".encode())
    #         temp.close()
            
    #         # Test populate_criteria() with the file:
    #         with testfixtures.LogCapture() as logs:
    #             with mock.patch('ANPAHP.scripts.populate_db.CRITERIA_CSV_PATH', temp.name):
    #                 with mock.patch('ANPAHP.scripts.populate_db.logger', self.logger):
    #                     populate_criteria()
                
    #             # One generic info, then alternating info and error:
    #             self.assertEqual(len(logs), 2*nb_criteria + 1)
    #             msg_types = [record[1] for record in logs]
    #             self.assertEqual(msg_types[0], "INFO")
    #             for i, msg_type in enumerate(msg_types[1:]):
    #                 if i%2 == 0: self.assertEqual(msg_type, "INFO")
    #                 else: self.assertEqual(msg_type, "ERROR")
                
    #         # Check that the right amount of criteria where inserted with the right values:
    #         criteria = Criterion.objects.all()
    #         self.assertEqual(len(criteria), nb_criteria)
    #         for i, criterion in enumerate(criteria):
    #             self.assertEqual(criterion.name, f"Test{i}")
    #             self.assertEqual(criterion.explanation, f"Explanation{i}")