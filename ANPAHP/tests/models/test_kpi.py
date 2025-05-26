"""Tests for module 'models.kpi'."""

from datetime import timedelta
import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models.kpi import KPI, NAME_MIN_LENGTH
from ...models import BSCFamily, BSCSubfamily

class KPIModelTest(TestCase):
    """Class to test model 'KPI' in the ANPAHP app."""
    
    def setUp(self):
        """Method called before each test."""
        # Create 4 BSC families, and 3 subfamilies for each one of them:
        for i in range(4):
            new_BSCFamily = BSCFamily(name = f"Test Family {i}",
                                    short_name = f"TestFam{i}",
                                    short_definition = f"This is the test family #{1}.",
                                    explanation = f"This a longer explanation of the fact that it is the test family #{i}.")
            new_BSCFamily.save()
        
            for j in range(3):
                new_subfamily = BSCSubfamily(name = f"Test subfamily {i*3 + j}",
                                             bsc_family = new_BSCFamily,
                                             short_definition = f"This is the test subfamily #{i*3 + i}.",
                                             explanation = f"his a longer explanation of the fact that it is the test subfamily #{i*3 + i}.")
                new_subfamily.save()
                
                
    def tearDown(self):
        """Method called after each test."""
        pass
    
    
    def test_kpi_valid_basic_creation(self):
        """A KPI can be created and saved into the DB with a name
        and the 'last_update' field should be updated automatically."""
        new_KPI = KPI(name = "Test")#, alternative_names = [])
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
        # This bugs because of a stupid bug in Django with non-basic primary keys.
        # new_KPI.name = "NewName"
        # new_KPI.save()
        new_KPI.explanation = "Blablabla"
        new_KPI.save()
        
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 1)
        self.assertEqual(kpis[0].explanation, "Blablabla")
        self.assertLess(kpis[0].last_updated, timezone.now())
        self.assertGreater(kpis[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
        self.assertLess(kpis[0].created, creation_time)
        

    def test_kpi_missing_name(self):
        """A KPI cannot be created without a name, it should raise an exception."""
        new_KPI = KPI()
        with self.assertRaises(Exception):
            new_KPI.save()
    
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
    
    
    def test_kpi_min_length_name(self):
        """Field 'name' should have a min length of NAME_MIN_LENGTH. Should 
        raise a ValidationError if not."""
        new_KPI = KPI(name = "a"*(NAME_MIN_LENGTH - 1))
        with self.assertRaises(ValidationError):
            new_KPI.save()
        
        kpis = KPI.objects.all()
        self.assertEqual(len(kpis), 0)
        
        
    def test_kpi_get_bsc_families(self):
        """Test for the get_bsc_families() method which should return the right family names."""
        bsc_subfamilies = [BSCSubfamily.objects.first(), BSCSubfamily.objects.last()]
        bsc_families = [sub.bsc_family for sub in bsc_subfamilies]
        
        new_KPI = KPI(name = "Test")
        new_KPI.save()
        new_KPI.bsc_subfamilies.set(bsc_subfamilies)
        new_KPI.save()
        
        self.assertEqual(new_KPI.get_bsc_families(), bsc_families)
        
    
    def test_kpi_shares_same_family(self):
        """Test for the shares_same_family() method which should return True the two KPIs
        have at least 1 BSC family in common."""
        KPI1, KPI2 = KPI(name = "Test1"), KPI(name = "Test2")
        KPI1.save()
        KPI2.save()
        bsc_subfamilies = list(BSCSubfamily.objects.all())
        
        # Share all families:
        KPI1.bsc_subfamilies.set(bsc_subfamilies)
        KPI2.bsc_subfamilies.set(bsc_subfamilies)
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI1.shares_same_family(KPI2))
        self.assertTrue(KPI2.shares_same_family(KPI1))
        
        # Share same family from different subfamilies:
        KPI1.bsc_subfamilies.set([bsc_subfamilies[0]])
        KPI2.bsc_subfamilies.set([bsc_subfamilies[2]])
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI1.shares_same_family(KPI2))
        self.assertTrue(KPI2.shares_same_family(KPI1))
        
        # Share only 1 family out of the two they have:
        KPI1.bsc_subfamilies.set(bsc_subfamilies[1:3])
        KPI2.bsc_subfamilies.set(bsc_subfamilies[2:4])
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI1.shares_same_family(KPI2))
        self.assertTrue(KPI2.shares_same_family(KPI1))
        
        # Share no family:
        KPI1.bsc_subfamilies.set(bsc_subfamilies[1:3])
        KPI2.bsc_subfamilies.set(bsc_subfamilies[6:8])
        KPI1.save()
        KPI2.save()
        self.assertFalse(KPI1.shares_same_family(KPI2))
        self.assertFalse(KPI2.shares_same_family(KPI1))
        
        
    def test_kpi_share_a_family(self):
        """Test for the share_a_family() static method which should return True the two KPIs
        have at least 1 BSC family in common."""
        KPI1, KPI2 = KPI(name = "Test1"), KPI(name = "Test2")
        KPI1.save()
        KPI2.save()
        bsc_subfamilies = list(BSCSubfamily.objects.all())
        
        # Share all families:
        KPI1.bsc_subfamilies.set(bsc_subfamilies)
        KPI2.bsc_subfamilies.set(bsc_subfamilies)
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI.share_a_family(KPI1, KPI2))
        self.assertTrue(KPI.share_a_family(KPI2, KPI1))
        
        # Share same family from different subfamilies:
        KPI1.bsc_subfamilies.set([bsc_subfamilies[0]])
        KPI2.bsc_subfamilies.set([bsc_subfamilies[2]])
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI.share_a_family(KPI1, KPI2))
        self.assertTrue(KPI.share_a_family(KPI2, KPI1))
        
        # Share only 1 family out of the two they have:
        KPI1.bsc_subfamilies.set(bsc_subfamilies[1:3])
        KPI2.bsc_subfamilies.set(bsc_subfamilies[2:4])
        KPI1.save()
        KPI2.save()
        self.assertTrue(KPI.share_a_family(KPI1, KPI2))
        self.assertTrue(KPI.share_a_family(KPI2, KPI1))
        
        # Share no family:
        KPI1.bsc_subfamilies.set(bsc_subfamilies[1:3])
        KPI2.bsc_subfamilies.set(bsc_subfamilies[6:8])
        KPI1.save()
        KPI2.save()
        self.assertFalse(KPI.share_a_family(KPI1, KPI2))
        self.assertFalse(KPI.share_a_family(KPI2, KPI1))