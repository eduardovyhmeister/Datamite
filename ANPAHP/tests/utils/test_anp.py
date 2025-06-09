"""Unit test file for utils/anp.py."""

from copy import deepcopy
# import time
import random

from django.test import TestCase
import numpy as np

from ...utils import anp


class ANPTests(TestCase):
    """Testing class for ANP functions."""
    
    def test_build_matrix(self):
        """Tests that anp.build_matrix() returns the expected values (for both
        the keys and the matrix). The returned should correspond to a list of 
        columns."""
        prefs = {"m1": 50, "m2": 100}
        keys = ["m1", "m2"]
        retrieved_keys, matrix = anp.build_matrix(prefs, keys)
        self.assertEqual(retrieved_keys, keys)
        self.assertEqual(matrix, [[1, 0.5], [2, 1]])
        
        retrieved_keys, matrix = anp.build_matrix(prefs) # Unspecified order:
        self.assertEqual(set(retrieved_keys), set(keys))

        prefs = {"m1": 50, "m2": 100, "m3": 30}
        keys = ["m1", "m2", "m3"]
        retrieved_keys, matrix = anp.build_matrix(prefs, keys)
        self.assertEqual(retrieved_keys, keys)
        self.assertEqual(matrix, [[1, 50/100, 50/30], [100/50, 1, 100/30], [30/50, 30/100, 1]])

        retrieved_keys, matrix = anp.build_matrix(prefs) # Unspecified order:
        self.assertEqual(set(retrieved_keys), set(keys))
        
        
    def test_build_matrix_limit_preferences_considered(self):
        """Test that anp.build_matrix() can limit the number of preferences
        considered in the construction of the matrix by specifying a list of keys."""
        prefs = {"m1": 30, "m2": 50, "m3": 100, "m4": 10, "m5": 50}
        keys = ["m2", "m3"]
        retrieved_keys, matrix = anp.build_matrix(prefs, keys)
        
        self.assertEqual(len(matrix), 2)
        for column in matrix:
            self.assertEqual(len(column), 2)
        self.assertEqual(retrieved_keys, keys)
        self.assertEqual(matrix, [[1, 0.5], [2, 1]])
        
    
    def test_build_matrix_filters_out_0s(self):
        """Tests anp.build_matrix() to make sure it doesn't include
        preferences set to 0 in the final result."""
        prefs = {"m1": 0, "m2": 50, "m3": 100, "m4": 0, "m5": 0}
        keys = ["m2", "m3"]
        retrieved_keys, matrix = anp.build_matrix(prefs, keys)
        
        self.assertEqual(len(retrieved_keys), 2)
        self.assertEqual(len(matrix), 2)
        for column in matrix:
            self.assertEqual(len(column), 2)
        self.assertEqual(retrieved_keys, keys)
        self.assertEqual(matrix, [[1, 0.5], [2, 1]])
        
        # Should ignore m4 even though it is provided as a key:
        keys = ["m2", "m3", "m4"]
        retrieved_keys, matrix = anp.build_matrix(prefs, keys)
        
        self.assertEqual(len(retrieved_keys), 2)
        self.assertEqual(len(matrix), 2)
        for column in matrix:
            self.assertEqual(len(column), 2)
        self.assertNotIn("m4", retrieved_keys)
        self.assertEqual(matrix, [[1, 0.5], [2, 1]])
        
    
    def test_normalise_columns(self):
        """Tests that anp.normalise_columns() performs the normalisation like it
        should."""
        matrix = [[1, 2], [0.5, 1]]
        previous = deepcopy(matrix)
        normalised = anp.normalise_columns(matrix)
        # Check that the old matrix wasn't changed by normalise_matrix():
        self.assertEqual(previous, matrix)
        self.assertEqual(normalised, [[1/3, 2/3], [1/3, 2/3]])
        
        matrix = [[1, 50/100, 50/30],
                  [100/50, 1, 100/30],
                  [30/50, 30/100, 1]]
        previous = deepcopy(matrix)
        normalised = anp.normalise_columns(matrix)
        self.assertEqual(previous, matrix)
        self.assertEqual(normalised, [[300/950, 150/950, 150/285],
                                      [150/475, 150/950, 150/285],
                                      [300/950, 300/1900, 10/19]])
        
        
    def test_build_matrix_then_normalise(self):
        """Tests that anp.build_matrix() followed by normalise_columns() gives 
        the expected result of each column being identical."""
        # Build a random matrix:
        prefs = {f"m{i}": x for i, x in enumerate(random.choices(range(100), k = 100))}
        _, matrix = anp.build_matrix(prefs)
        normalised = anp.normalise_columns(matrix)
        
        # Check that all columns are identical:
        first_column = normalised[0]
        for column in normalised:
            for e1, e2 in zip(first_column, column):
                self.assertAlmostEqual(e1, e2) # Account for rounding errors
        
        
    def test_extract_principal_eigenvector(self):
        """Tests that anp.extract_principal_eigenvector() gives the expected
        results, if the matrix is a reciprocal matrix, then it returns the same
        as anp.normalise_columns(matrix)[0]."""
        matrix = [[1, 2], [0.5, 1]]
        eigenvector = anp.extract_principal_eigenvector(matrix)
        expected = [1/3, 2/3]
        for e1, e2 in zip(eigenvector, expected):
            self.assertAlmostEqual(e1, e2) # Account for rounding errors
        
        matrix = [[1, 50/100, 50/30], [100/50, 1, 100/30], [30/50, 30/100, 1]]
        eigenvector = anp.extract_principal_eigenvector(matrix)
        expected = [30/95, 15/95, 50/95]
        for e1, e2 in zip(eigenvector, expected):
            self.assertAlmostEqual(e1, e2) # Account for rounding errors


    def test_compute_limiting_matrix(self):
        """Tests that anp.build_limiting_matrix() gives the expected result."""
        matrix = [[1/3, 2/3], [1/3, 2/3]]
        power2 = anp.compute_limiting_matrix(matrix, max_iter=1)
        self.assertEqual(matrix, power2)
        
        # No dependencies between metrics (1 strategy, 4 BSC, 6 metrics):
        matrix = [
            [0, 1/3, 1/6, 1/3, 1/6] + [0] * 6,
            [0] * 5 + [1/6] * 6,
            [0] * 5 + [1/3] * 3 + [0] * 3,
            [0] * 5 + [0] * 3 + [1/3] * 3,
            [0] * 5 + [0] * 2 + [1/2] * 2 + [0] * 2     
        ]
        for i in range(6):
            column = [0] * 11
            column[5 + i] = 1
            matrix.append(column)
        
        limiting_matrix = anp.compute_limiting_matrix(matrix)
        # The only column that should have changed is the first one:
        expected_first_column = [0] * 5 + [1/9, 1/9, 1.75/9, 1/4, 1/6, 1/6]
        for value1, value2, in zip(limiting_matrix[0], expected_first_column):
            self.assertAlmostEqual(value1, value2)
        for column1, column2 in zip(limiting_matrix[1:], matrix[1:]):
            for value1, value2 in zip(column1, column2):
                self.assertAlmostEqual(value1, value2)
            
        # Circular dependencies: some metrics depend on the two next one:
        matrix = [
            [0, 1/3, 1/6, 1/3, 1/6] + [0] * 6,
            [0] * 5 + [1/6] * 6,
            [0] * 5 + [1/3] * 3 + [0] * 3,
            [0] * 5 + [0] * 3 + [1/3] * 3,
            [0] * 5 + [0] * 2 + [1/2] * 2 + [0] * 2     
        ]
        for i in range(3):
            column = [0] * 11
            column[5 + i] = 1
            matrix.append(column)
        for i in range(3):
            column = [0] * 11
            column[8 + (i+1) % 3] = 1/3
            column[8 + (i+2) % 3] = 2/3
            matrix.append(column)
        
        limiting_matrix = anp.compute_limiting_matrix(matrix)
        # Only the first column is important is this case:
        expected = [0] * 5 + [1/9] * 2 + [1.75/9] * 4
        for value1, value2 in zip(limiting_matrix[0], expected):
            self.assertAlmostEqual(value1, value2)

        
    ### TODO: test the construction of the supermatrix:
    ###  - Needs to setup a bunch of BSC families and subfamilies.
    ###  - Setup some KPIs
    ###  - Simulate the whole selection process.
    ###  - Check the build supermatrix is correct: correct columns and rows, correct values.
    ###      - A no dependency metric should depend on itself.
    ###      - A metric with dependencies should have itself as 0.
    ###      - The strategy should only depend on the BSC families.
    ###      - BSC families with no KPIs selected OR with preference set to 0 should NOT appear in it.
        
        
    
        