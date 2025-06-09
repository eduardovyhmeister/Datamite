"""A module for computing the ANP-AHP operations. Mostly for matrix computations."""


import numpy as np

from ..models import BSCFamily, KPI


def build_matrix(preferences, keys=None):
    """Builds a matrix based on the provided preferences.
    
    The matrix is built such that matrix[1][2] = 1 / matrix[2][1], i.e. a12 is
    the reciprocal value of a21.
    Objects with a preference set as 0 will be excluded from the matrix,
    reducing the size of the resulting matrix.
    Because dictionaries can return a random order for keys of the preferences,
    an order is set and returned with the built matrix (or can be set through
    the `keys` parameter).
    
    Args:
        preferences (dict[obj: int/float]): The preferences expressed by a user.
            Any object is valid as key. The values need to be a positive number.
            Any 0 will be ignored for the construction of the matrix.
        keys (iter[obj]): An ordered iterable in specifying in which order
            the keys should be considered. If set to `None`, the `.keys()`
            of `preferences` is simply cast to a list. Can also be used to 
            specify which objects should be considered for the construction of
            the matrix, e.g. you can have loads of preferences but force the 
            construction to consider only a few of them. The provided keys should
            be valid. (Defaults to `None`)
            
    Returns:
        (list[obj], list[list[int/float]]) - A tuple containing 1) the objects
        used, in the order in which they were used, and the matrix as a list of
        lists of values (a list of columns).
    """
    matrix = []
    # Make sure to get the preferences in the same order
    objects = keys if keys else list(preferences.keys())
    # Get rid of the 0s in the expressed preferences, to prevent dividing by 0:
    preferences = {x:y for x,y in preferences.items() if y != 0 and x in objects}
    objects = [o for o in objects if o in preferences]
    
    for i, pref1 in enumerate(objects):
        matrix.append([])
        for j, pref2 in enumerate(objects):
            matrix[i].append(preferences[pref1] / preferences[pref2])

    return (objects, matrix)


def normalise_columns(matrix):
    """Normalises the columns of the matrix so that every column sums to 1 (except
    if the sum of the column is 0, then it stays this way).
    
    If normalising a matrix built using `build_matrix()`, then all the columns
    will have the same value which gives you the importance (in [0; 1]) of each 
    object.
    
    Args:
        matrix (list[list[int/float]]): The matrix to normalise, provided as
            a list of columns.
        
    Returns:
        list[list[int/float]] - A new matrix which is the normalised 
        version of the provided one.
    """
    normalised_matrix = []
    for column in matrix:
        total = sum(column)
        if total == 0:
            normalised_matrix.append([0] * len(matrix[0]))
        else:
            normalised_matrix.append([x/total for x in column])
    return normalised_matrix


def extract_principal_eigenvector(matrix):
    """Extracts the principal eigenvector of the provided matrix. That vector
    will be normalised.
    
    If the matrix is reciprocal, then it's just a slow version of `normalise_columns()`.
    
    Args:
        matrix (list[list[int/float]]): The matrix to extract the eigen
            vector for, provided as a list of columns.
    
    Returns:
        list[value] - The normalised principal eigenvector of the matrix.
    """
    # Transpose the matrix because numpy considers a matrix as an array of lines:
    eigenvalues, eigenvectors = np.linalg.eig(np.transpose(np.asarray(matrix)))
    principal_eigenvalue_index = np.argmax(eigenvalues)
    principal_eigenvector = eigenvectors[:, principal_eigenvalue_index]
    normalised_eigenvector = np.abs(principal_eigenvector) / np.sum(np.abs(principal_eigenvector))
    return normalised_eigenvector.tolist()


def build_supermatrix(bsc_prefs, kpi_prefs, intermetrics_relationships = None):
    """Build the supermatrix for the AHP.
    
    If intermetrics_relationships create cycles in the dependency graph, then 
    you should find the limiting matrix using `compute_limiting_matrix()`.
    
    Args:
        bsc_prefs (dict[name: value]): The preferences in terms of BSC families.
            Corresponds to `Evaluation.bsc_preferences`.
        kpi_prefs (dict[name: value]): The preferences in terms of KPIs/metrics.
            Will be separated into the separated BSC families to compute the
            matrices separately.
            Corresponds to `models.Evaluation.kpis_preferences`.
        intermetrics_relationships (dict[kpi_name: dict[kpi_name: value]]): the 
            dictionary of intermetrics relationships (for each kpi/metric, a
            dictionary of dependencies and their importance is provided).
            (Defaults to `None`, e.g. if the user didn't specify any of them).
            Corresponds to `models.Evaluation.intermetric_preferences`.
        
    Returns:
        (list[str], list[list[float]]) - A tuple (names of the columns, matrix)
        with the matrix being the supermatrix of the hierarchy (the AHP). The 
        matrix is given as a list of columns.
    """
    # Extract the KPI preferences per family:
    kpi_preferences = __separate_family_preferences(kpi_prefs)
    
    # Filter out BSC families with a preference of 0 OR no KPI selected:
    bsc_keys = [key for key in bsc_prefs.keys() if bsc_prefs[key] != 0 and kpi_preferences[key] != {}]
    kpi_keys = list(kpi_prefs.keys()) 
    
    # 1st column = strategy
    # Following columns = BSC families
    # Last columns = KPIs/metrics
    matrix_size = 1 + len(bsc_keys) + len(kpi_prefs)
    supermatrix = []
    
    # Construct the first column for the strategy:
    # The strategy depends on the BSC Families selected.
    # It uses the expressed preferences in terms of BSC families (the pairwise comparisons).
    bsc_weights = normalise_columns(build_matrix(bsc_prefs, keys = bsc_keys)[1])[0]
    supermatrix.append([0] + bsc_weights + [0] * len(kpi_keys))
    
    # Construct the columns for the BSC families:
    # Each family depends on the KPIs/metrics it contains.
    # It uses the expressed preferences in terms of KPIs (the pairwise comparison).
    for bsc_family in bsc_keys:
        keys, pref_matrix = build_matrix(kpi_preferences[bsc_family])
        kpi_weights = normalise_columns(pref_matrix)[0]
        quick_access = {name: value for name, value in zip(keys, kpi_weights)}
        column = [0] * (1 + len(bsc_keys)) + [quick_access.get(key, 0) for key in kpi_keys]
        supermatrix.append(column)
    
    # Construct the columns for all the metrics:
    for kpi in kpi_keys:
        # No dependencies, metric depends only on itself:
        if kpi not in intermetrics_relationships:
            kpi_column = [0] * matrix_size
            kpi_column[1 + len(bsc_keys) + kpi_keys.index(kpi)] = 1
            supermatrix.append(kpi_column)
            continue
        
        # There are dependencies, compute the weights:
        keys, importance_matrix = build_matrix(intermetrics_relationships[kpi])
        kpi_weights = normalise_columns(importance_matrix)[0]
        quick_access = {name: value for name, value in zip(keys, kpi_weights)}
        column = [0] * (1 + len(bsc_keys)) + [quick_access.get(key, 0) for key in kpi_keys]
        supermatrix.append(column)
    
    keys = ["strategy"] + bsc_keys + kpi_keys
    return (keys, supermatrix)


def compute_limiting_matrix(matrix, max_iter=1000, error=1e-6, rounding=6):
    """Computes the limiting matrix of the provided matrix by raising to a power
    until it converges. The matrix has to be a square matrix.
    
    Convergence can be defined as:
        - The maximum number of iterations (`max_iter`) has been reached.
        - The average distance between the values before and after an iteration
          is lower than `error`.
    
    Args:
        matrix (list[list[float]]): The matrix to compute the limiting matrix for, as
            a list of columns.
        max_iter (int): The maximum number of iterations in the process. (Defaults to 1000)
        error (float): The error used to compute if the process has converged.
        rounding (int): The number of decimals to keep in the rounding process. (Defaults to 6)
        
    Returns:
        list[list[float]] - The limiting matrix as a list of columns.
    """
    base_matrix = np.transpose(np.asarray(matrix))
    previous_matrix = base_matrix
    
    for i in range(max_iter):
        new_matrix = np.matmul(previous_matrix, base_matrix)
        distance = np.sum(np.abs(np.subtract(previous_matrix, new_matrix)))
        if distance < error: break
        previous_matrix = new_matrix
    
    return np.around(np.transpose(new_matrix), rounding).tolist()


# -----------------------------------------------------------------------------
# Private functions:

def __separate_family_preferences(kpi_prefs):
    """Separates the KPIs from the different families from all the preferences
    expressed in the KPI preference step.
    
    Args:
        kpi_prefs (dict[name: value]): The dictionary of preferences as expressed
            by the user in terms of importance of KPIs.
            
    Returns:
        dict[bsc_family_name: dict[name : value]] - A dictionary which for each BSC
        family stores a dictionary of the preferences expressed by the user for the
        KPIs of that family.
    """
    preferences = {}
    for bsc_family in BSCFamily.objects.all():
        preferences[bsc_family.name] = {}
        
    for kpi in KPI.objects.filter(name__in = kpi_prefs.keys()):
        families = kpi.get_bsc_families()
        for family in families:
            preferences[family.name][kpi.name] = kpi_prefs[kpi.name]
            
    return preferences