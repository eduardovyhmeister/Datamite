import base64
from io import BytesIO
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
from pyanp import limitmatrix as lm


def get_graph(): 
    #this is a function to embed views with grapbhs automatically from database.
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def transform_list(original_list): 
    ''' Create a mapping from original number to the new smallest unique number'''
    unique_numbers = sorted(set(num for sublist in original_list for num in sublist))
    num_mapping = {num: i + 1 for i, num in enumerate(unique_numbers)}
    transformed_list = [[num_mapping[num] for num in sublist] for sublist in original_list]
    return transformed_list

def generate_pairs_as_lists(data):
    result = {}
    for key, value in data.items():
        result[key] = []
        for sublist in value:
            if len(sublist) > 1:
                pairs = list(combinations(sublist, 2))
                result[key].extend(list(pair) for pair in pairs)
            else:
                result[key].append(sublist)
    return result

def merge_unique_values(data):
    result = {}
    for key, value in data.items():
        unique_elements = set()
        for sublist in value:
            unique_elements.update(sublist)
        result[key] = [list(unique_elements)]
    return result

def ponder_and_normalize(list_of_lists, weighting_factors):
    # Initialize a list to store the pondered values
    pondered_values = []

    # Ponder each sublist by the corresponding weighting factor
    for sublist, weight in zip(list_of_lists, weighting_factors):
        pondered_sublist = [element * weight for element in sublist]
        pondered_values.append(pondered_sublist)

    # Calculate the total sum of all pondered values
    total_sum = sum(sum(sublist) for sublist in pondered_values)

    # Normalize the pondered values
    normalized_values = []
    for pondered_sublist in pondered_values:
        if total_sum == 0:
            normalized_values.append(pondered_sublist)  # Preserve the pondered values if total sum is zero
        else:
            normalized_values.append([element / total_sum for element in pondered_sublist])

    return normalized_values


def numerate_names(data):
    name_to_number = {}  # Dictionary to store name-number mapping
    next_number = 1  # Initial number to assign
    numerated_data = []  # List to store numerated lists
    for sublist in data:
        numerated_sublist = []  # List to store numerated sublist
        for name in sublist:
            if name not in name_to_number:
                name_to_number[name] = next_number
                next_number += 1
            numerated_sublist.append(name_to_number[name])
        numerated_data.append(numerated_sublist)
    return numerated_data

def make_radar_chart(stats,labels,plot_markers = None):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(5,5))
    attribute_labels=labels #List of names
    if plot_markers == None:
        plot_markers =[0,.2,0.4,0.6,0.8,1,]
    plot_str_markers=['0','0.2','0.4','0.6','0.8','1']
    angles = np.linspace(0, 2*np.pi, len(attribute_labels), endpoint=False)
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, attribute_labels)
    ax.tick_params(labelsize=8)
    plt.yticks(plot_markers)
    ax.set_title('ANP Results')
    ax.grid(True)
    graph = get_graph()
    return graph

def make_trend_chart(df,names,title,ticks):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax = df[names].plot(kind='box',title=title)
    ax.set_xticklabels(ticks)
    #plt.setp(ax, xticks=[np.random.normal(0, std, 100) for std in range(6, 10)], xticklabels=labels)
    graph = get_graph()
    return graph


def construct_matrix(selection,elements,dim=None):
    if len(selection)>1:
        matrix_size = dim if dim is not None else max(max(sublist) for sublist in elements)
        matrix = np.eye(matrix_size)
        
        for i in range(len(selection)):
            if selection[i]<0:
                value = 1/(abs(selection[i])+1)
            else:
                value = selection[i]+1
            
            matrix[elements[i][0]-1,elements[i][1]-1] = 1/value
            matrix[elements[i][1]-1,elements[i][0]-1] = value

    # eigenvalues and vectors
    elif len(selection) == 1:
        matrix = np.eye(2)
        value = 1 / (abs(selection[0]) + 1) if selection[0] < 0 else selection[0] + 1
        matrix[0,1] = value
        matrix[1,0] = 1/value

    else:
        matrix = np.array([[1]])
    print(elements)
    print(max(max(sublist) for sublist in elements))
    # eliminate rows and columns that contain 0,s
    #rows_to_keep = ~np.any(matrix == 0, axis=1)
    #columns_to_keep = ~np.any(matrix == 0, axis=0)
    #matrix = matrix[np.ix_(rows_to_keep, columns_to_keep)]
    #print(matrix)

    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    principal_eigenvalue_index = np.argmax(eigenvalues)
    principal_eigenvector = eigenvectors[:, principal_eigenvalue_index]
    normalized_eigenvector = np.abs(principal_eigenvector) / np.sum(np.abs(principal_eigenvector))
    eig_vec = normalized_eigenvector.real
    eig_val = eigenvalues.max().real
    try:
        inconcistency = (eig_val-len(eigenvalues))/(len(eigenvalues)-1)
    except:
        inconcistency = 0.0
    return matrix, eig_vec, inconcistency


def EXECUTE_ANALYSIS(ANPAHP):
    # ANPAHP is an Evaluation object
    try:
        supermatrix = eval(ANPAHP.supermatrix)
    except:
        supermatrix = ANPAHP.supermatrix
    supermatrix = np.array(supermatrix,dtype=float)
    columns_analysis = [1 if i == 0 else 0 for i in np.sum(supermatrix[:,1:5], axis=0)]
    if sum(columns_analysis) != 0:
        original = supermatrix[1:5,0]
        operated = [original[i] if k == 0 else 0 for (i,k) in enumerate(columns_analysis)]
        operated = np.abs(operated) / np.sum(np.abs(operated))
        supermatrix[1:5,0] = operated

    try:
        limitingmatrix = lm.calculus(supermatrix)
        hierarchy = lm.hiearhcy_formula(supermatrix)
        lista1 = limitingmatrix.tolist()
        lista2 = hierarchy.tolist()
    except:
        lista1 =[]
        lista2 = []
    return lista1,lista2, supermatrix
