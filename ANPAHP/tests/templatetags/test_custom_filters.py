from django.test import TestCase

from ...templatetags import custom_filters


class CustomFiltersTests(TestCase):
    """Testing class for custom filters."""
    
    
    def test_get_value_at_correct(self):
        """The function works with indexable objects when providing a correct index or key."""
        # Test for lists:
        l = list(range(10))
        for i in range(10):
            self.assertEqual(i, custom_filters.get_value_at(l, i))
            self.assertEqual(9 - i, custom_filters.get_value_at(l, -i-1))
            
        # Test for dicts:
        d = {str(i) : i for i in range(10)}
        for i in range(10):
            self.assertEqual(i, custom_filters.get_value_at(d, str(i)))
        
        # Test for strings:
        s = "".join([str(i) for i in range(10)])
        for i in range(10):
            self.assertEqual(str(i), custom_filters.get_value_at(s, i))
            self.assertEqual(str(9 - i), custom_filters.get_value_at(s, -i-1))
        
        
    def test_get_value_at_wrong_type(self):
        """The function returns 'None' when the provided object is not indexable (i.e.
        doesn't implement __get_item__())."""
        # Test with integers:
        self.assertEqual(custom_filters.get_value_at(12, 0), None)
        self.assertEqual(custom_filters.get_value_at(12, 1), None)
        self.assertEqual(custom_filters.get_value_at(12, 2), None)
        
        # Test with floats:
        self.assertEqual(custom_filters.get_value_at(1.2, 0), None)
        self.assertEqual(custom_filters.get_value_at(1.2, 1), None)
        self.assertEqual(custom_filters.get_value_at(1.2, 2), None)
        
        
    def test_get_value_at_wrong_index(self):
        """The function returns 'None' when the provided index is out of range."""
        l = list(range(10))
        for i in range(10, 20):
            self.assertEqual(custom_filters.get_value_at(l, i), None)
        for i in range (-20, -10):
            self.assertEqual(custom_filters.get_value_at(l, i), None)
            
        s = "".join([str(i) for i in range(10)])
        for i in range(10, 20):
            self.assertEqual(custom_filters.get_value_at(s, i), None)
        for i in range (-20, -10):
            self.assertEqual(custom_filters.get_value_at(s, i), None)
    
    
    def test_get_value_wrong_key(self):
        """The function returns 'None' when the provided key doesn't exist."""
        d = {str(i) : i for i in range(10)}
        for i in range(10, 20):
            self.assertEqual(custom_filters.get_value_at(d, i), None)
            self.assertEqual(custom_filters.get_value_at(d, str(i)), None)