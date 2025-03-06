import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

phi = (1 + np.sqrt(5)) / 2 #gplden ratio

def subdivide(triangles):
    '''
    Divides given triangles into 2 or 3 triangles.
    triangles is a list of tuples (color, a, b, c).
    
    color=0 indicates a pink ('small') triangle with sides in ratio 1:1:(1/phi), 
    color=1 indicates a blue ('large') triangle with sides in ratio 1:1:phi.

    a, b, c are numpy arrays [x, y], x and y are the coordinates of the vertices, 
    a and c are vertices at the equal base angles and b is s at the vertex angle.
    
    '''
    
    result = [] 
    for triangle in triangles:
        color, a, b, c = triangle
        if color == 0:
            p = b + (a - b) / phi
            result += [(0, p, c, a), (1, c, p, b)]
        elif color == 1:
            q = a + (b - a) / phi
            r = a + (c - a) / phi
            result += [(1, c, r, b), (1, r, q, a), (0, q, r, b)]
            
    return result


def Penrose_gen(N, plot_tiling = False):
    '''
    Generates penrose tiling of type 3 with generation depth N and plots it if needed.
    Returns a list of coordinates of each point of the tiling.
    '''

    if plot_tiling:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        
    #generation of initial pink triangles around the origin
    triangles = []
    beta = np.pi / 10
    alpha = np.pi / 5
    b = np.array([0, 0])
    for i in range(10):
        a = np.array([np.sin(beta), np.cos(beta)])
        c = np.array([np.sin(beta+alpha), np.cos(beta+alpha)])
        if i % 2 == 0:
            a, c = c, a
        if i == 9:
            c = (np.sin(np.pi / 10), np.cos(np.pi / 10))
        triangles.append((0, a, b, c))
        beta += alpha

    #generation of Penrose tiling
    for i in range(N):
        triangles = subdivide(triangles)

    points = [] #list contains numpy arrays of coordinates of each point
    for triangle in triangles:
        color, a, b, c = triangle
        points += [a, b, c]
        if plot_tiling:
            if color == 0:
                poly = plt.Polygon([a, b, c], closed=False, facecolor='pink', edgecolor='black', linewidth=2)
            elif color == 1:
                poly = plt.Polygon([a, b, c], closed=False, facecolor='skyblue', edgecolor='black', linewidth=2)
            ax.add_patch(poly)
    points = tuple(map(tuple, points))
    points = list(set(points))

    if plot_tiling:
        ax.axis('off')
        plt.show

    return points, triangles