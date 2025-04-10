from datetime import timedelta
import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models.kpi import KPI, NAME_MIN_LENGTH
from ...models.enumerations import BSCFamily

class KPIModelTest(TestCase):
    """Class to test model 'KPI' in the ANPAHP app."""
    
    
    def test_kpi_valid_basic_creation(self):
        """A KPI can be created and saved into the DB with a name and bsc_family
        and the 'last_update' field should be updated automatically."""
        new_KPI = KPI(name = "Test", bsc_family = list(BSCFamily)[0])
        new_KPI.save()
        
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 1)
        self.assertEqual(kpis[0].name, "Test")
        self.assertEqual(kpis[0].explanation, "") # Should be the default value
        self.assertLess(kpis[0].last_updated, timezone.now())
        self.assertGreater(kpis[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
        creation_time = timezone.now()
        self.assertLess(kpis[0].created, creation_time)
        
        time.sleep(0.3)
        
        # Modify it and check that the last_update field is updated accordingly:
        new_KPI.name = "NewName"
        new_KPI.save()
        
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 1)
        self.assertEqual(kpis[0].name, "NewName")
        self.assertLess(kpis[0].last_updated, timezone.now())
        self.assertGreater(kpis[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
        self.assertLess(kpis[0].created, creation_time)
        

    def test_kpi_missing_name(self):
        """A KPI cannot be created without a name, it should raise an exception."""
        new_KPI = KPI(bsc_family = list(BSCFamily)[0])
        with self.assertRaises(Exception):
            new_KPI.save()
    
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
    
    
    def test_kpi_missing_name(self):
        """Field 'name' should have a min length of NAME_MIN_LENGTH. Should 
        raise a ValidationError if not."""
        new_KPI = KPI(name = "a"*(NAME_MIN_LENGTH - 1), bsc_family = list(BSCFamily)[0])
        with self.assertRaises(ValidationError):
            new_KPI.save()
        
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
    
    
    def test_kpi_missing_bsc_family(self):
        """A KPI cannot be created without a bsc_family, it should raise an exception."""
        new_KPI = KPI(name = "Test")
        with self.assertRaises(Exception):
            new_KPI.save()
            
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
        
        
    def test_kpi_invalid_bsc_family(self):
        """The BSC family can only be selected from choices. Should fail if something
        unexpected is provided."""
        new_KPI = KPI(name = "Test", bsc_family = "ergbrdgqh")
        with self.assertRaises(Exception):
            new_KPI.save()
            
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
        
    