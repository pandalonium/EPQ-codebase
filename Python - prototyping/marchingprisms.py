import numpy as np
import pyperclip as ppc
from itertools import chain


# 
#         0
#   (0) / | \ (1)
#     1 -(2)- 2
#     |   |<--|--- (3)
#    (5)  3  (4)
# (6)-|>/   \<|-(7)
#     4 -(8)- 5
# 



# EXECUTIVE DECISION: always prioritise connectedness of the inner (above-threshold) region.

prismlookup = [                                 # 0 1 2 3 4 5
                                            #  ================ (0 means below, 1 means above threshold)
    [],                                         # 0 0 0 0 0 0 - none
    [(8,7,4)],                                  # 0 0 0 0 0 1 - triangle around outlier
    [(5,6,8)],                                  # 0 0 0 0 1 0 - triangle around outlier
    [(5,6,7),(4,5,7)],                          # 0 0 0 0 1 1 - quad (2 x triangle) across midpoints
    [(7,6,3)],                                  # 0 0 0 1 0 0 - triangle around outlier
    [(3,6,8),(8,4,3)],                          # 0 0 0 1 0 1 - quad (2 x triangle) across midpoints
    [(8,5,3),(3,7,8)],                          # 0 0 0 1 1 0 - quad (2 x triangle) across midpoints
    [(3,4,5)],                                  # 0 0 0 1 1 1 - triangle on vertical midpoints
    [(1,2,4)],                                  # 0 0 1 0 0 0 - triangle around outlier
    [(8,7,2),(1,2,7)],                          # 0 0 1 0 0 1 - quad (2 x triangle) across midpoints
    [(6,5,1),(5,2,1)],                          # 0 0 1 0 1 0 - tunnel between above vertices
    [(1,6,7),(1,2,6),(2,5,6)],                  # 0 0 1 0 1 1 - triangulated wall across above and below regions 2,1,6,7,5
    [],                                         # 0 0 1 1 0 0 - tunnel between above vertices
    [(2,8,6),(6,2,1),(1,3,6)],                  # 0 0 1 1 0 1 - triangulated wall across above and below regions
    [(4,7,8),(1,2,5),(1,2,3)],                  # 0 0 1 1 1 0 - triangle around lone below vertex and quad across pair of below vertices
    [(1,2,5),(1,2,3)],                          # 0 0 1 1 1 1 - quad (2 x triangle) across midpoints
    [(5,2,0)],                                  # 0 1 0 0 0 0 - triangle around outlier
    [],                                         # 0 1 0 0 0 1 - tunnel between above vertices
    [(8,2,0),(0,6,8)],                          # 0 1 0 0 1 0 - quad (2 x triangle) across midpoints
    [(0,7,6),(0,2,7),(2,4,7)],                                         # 0 1 0 0 1 1 - triangulated wall across above and below regions
    [],                                         # 0 1 0 1 0 0 - tunnel between above vertices
    [(5,2,0),(3,6,8),(8,4,3)],                  # 0 1 0 1 0 1 - triangle around lone below vertex and quad across pair of below vertices
    [],                                         # 0 1 0 1 1 0 - triangulated wall across above and below regions
    [(3,2,0),(2,3,4)],                          # 0 1 0 1 1 1 - quad (2 x triangle) across midpoints
    [(5,4,0),(4,1,0)],                          # 0 1 1 0 0 0 - quad (2 x triangle) across midpoints
    [],                                         # 0 1 1 0 0 1 - triangulated wall across above and below regions
    [],                                         # 0 1 1 0 1 0 - triangulated wall across above and below regions
    [(0,1,6),(1,6,7)],                          # 0 1 1 0 1 1 - quad (2 x triangle) across midpoints
    [(7,6,3),(5,4,0),(4,1,0)],                  # 0 1 1 1 0 0 - triangle around lone below vertex and quad across pair of below vertices
    [(3,1,0),(8,6,5)],                          # 0 1 1 1 0 1 - two separate triangles around outliers
    [(3,1,0),(4,7,8)],                          # 0 1 1 1 1 0 - two separate triangles around outliers
    [(3,1,0)],                                  # 0 1 1 1 1 1 - triangle around outlier
    [(0,1,3)],                                  # 1 0 0 0 0 0 - triangle around outlier
    [],                                         # 1 0 0 0 0 1 - tunnel between above vertices
    [],                                         # 1 0 0 0 1 0 - tunnel between above vertices
    [(3,6,7),(5,4,0),(4,1,0)],                  # 1 0 0 0 1 1 - triangle around lone below vertex and quad across pair of below vertices
    [(6,1,0),(7,6,1)],                          # 1 0 0 1 0 0 - quad (2 x triangle) across midpoints
    [(0,1,6),(1,8,6),(1,4,8)],                                         # 1 0 0 1 0 1 - triangulated wall across above and below regions
    [],                                         # 1 0 0 1 1 0 - triangulated wall across above and below regions
    [(0,4,5),(0,1,1)],                          # 1 0 0 1 1 1 - quad (2 x triangle) across midpoints
    [(0,2,3),(4,3,2)],                          # 1 0 1 0 0 0 - quad (2 x triangle) across midpoints
    [],                                         # 1 0 1 0 0 1 - triangulated wall across above and below regions
    [(0,2,5),(8,6,3),(3,4,8)],                  # 1 0 1 0 1 0 - triangle around lone below vertex and quad across pair of below vertices
    [(0,2,5),(3,6,7)],                          # 1 0 1 0 1 1 - two separate triangles around outliers
    [(6,7,0),(7,2,0),(7,4,2)],                  # 1 0 1 1 0 0 - triangulated wall across above and below regions
    [(0,2,8),(8,6,0)],                          # 1 0 1 1 0 1 - quad (2 x triangle) across midpoints
    [],                                         # 1 0 1 1 1 0 - triangulated wall across above and below regions
    [(0,2,5)],                                  # 1 0 1 1 1 1 - triangle around outlier
    [(5,2,1),(1,3,5)],                          # 1 1 0 0 0 0 - quad (2 x triangle) across midpoints
    [(4,2,1),(3,5,8),(8,7,3)],                  # 1 1 0 0 0 1 - triangle around lone below vertex and quad across pair of below vertices
    [(6,8,2),(1,2,6),(6,3,1)],                  # 1 1 0 0 1 0 - triangulated wall across above and below regions
    [(4,2,1),(3,6,7)],                          # 1 1 0 0 1 1 - two separate triangles around outliers
    [(7,6,1),(6,2,1),(6,5,2)],                  # 1 1 0 1 0 0 - triangulated wall across above and below regions
    [(4,2,1),(8,6,5)],                          # 1 1 0 1 0 1 - two separate triangles around outliers
    [(2,7,8),(1,2,7)],                          # 1 1 0 1 1 0 - quad (2 x triangle) across midpoints
    [(4,2,1)],                                  # 1 1 0 1 1 1 - triangle around outlier
    [(5,4,3)],                                  # 1 1 1 0 0 0 - triangle on vertical midpoints
    [(3,5,8),(8,7,3)],                          # 1 1 1 0 0 1 - quad (2 x triangle) across midpoints
    [(8,6,3),(3,4,8)],                          # 1 1 1 0 1 0 - quad (2 x triangle) across midpoints
    [(3,6,7)],                                  # 1 1 1 0 1 1 - triangle around outlier
    [(7,6,5),(7,5,4)],                          # 1 1 1 1 0 0 - quad (2 x triangle) across midpoints
    [(8,6,5)],                                  # 1 1 1 1 0 1 - triangle around outlier
    [(4,7,8)],                                  # 1 1 1 1 1 0 - triangle around outlier
    [],                                         # 1 1 1 1 1 1 - none
]

SQRT_3 = 3**0.5



midpointLookup = [
    (0,1),
    (0,2),
    (1,2),
    (0,3),
    (2,5),
    (1,4),
    (3,4),
    (3,5),
    (4,5)
]

def triangulatePrism(coords: list[np.ndarray], values: list[float]):
    signs = [value > 0 for value in values]
    index = ((signs[0] << 5) 
             + (signs[1] << 4)
             + (signs[2] << 3)
             + (signs[3] << 2)
             + (signs[4] << 1)
             + (signs[5])
             )
    triangles = prismlookup[index]
    midpointCache = dict()
    output = []
    debugIndices = []
    for triangle in triangles:
        if triangle[0] in midpointCache:
            vertex0 = midpointCache[triangle[0]]
        else:
            startInd = midpointLookup[triangle[0]][0]
            endInd = midpointLookup[triangle[0]][1]
            lerp = abs(values[startInd])/(abs(values[startInd]) + abs(values[endInd]))
            vertex0 = (1-lerp)*coords[startInd] + lerp*coords[endInd]
            midpointCache[triangle[0]] = vertex0

        if triangle[1] in midpointCache:
            vertex1 = midpointCache[triangle[1]]
        else:
            startInd = midpointLookup[triangle[1]][0]
            endInd = midpointLookup[triangle[1]][1]
            lerp = abs(values[startInd])/(abs(values[startInd]) + abs(values[endInd]))
            vertex1 = (1-lerp)*coords[startInd] + lerp*coords[endInd]
            midpointCache[triangle[1]] = vertex1

        if triangle[2] in midpointCache:
            vertex2 = midpointCache[triangle[2]]
        else:
            startInd = midpointLookup[triangle[2]][0]
            endInd = midpointLookup[triangle[2]][1]
            lerp = abs(values[startInd])/(abs(values[startInd]) + abs(values[endInd]))
            vertex2 = (1-lerp)*coords[startInd] + lerp*coords[endInd]
            midpointCache[triangle[2]] = vertex2

        output.append((vertex0,vertex1,vertex2))
        debugIndices.append(index)
    return (output,debugIndices)

def genPrismLattice(minx, miny, minz, n_x, n_y, n_z, step, field = None):
    lattice = []
    if field: values = []
    for i in range(n_z):
        z = minz + i*step*SQRT_3*0.333333333
        plane = []
        if field: valuesplane = []
        for j in range(n_y):
            y = miny + j*step*SQRT_3*0.5
            row = []
            if field: valuesrow = []
            for k in range(n_x):
                x = minx + k*step + (j % 2) * 0.5
                if field: valuesrow.append(field(np.array([x,y,z])))
                row.append(np.array([x,y,z]))
            plane.append(row)
            if field: valuesplane.append(valuesrow)
        lattice.append(plane)
        if field: values.append(valuesplane)
    if field: return (lattice,values)
    else: return lattice

def marchingPrismsLattice(lattice, values):
    triangles = []
    debugIndices = []
    for i in range(len(lattice)-1):
        for j in range(len(lattice[0])-1):
            for k in range(len(lattice[0][0])-1):
                if (j % 2) == 0:
                    prism1coords = [lattice[i][j][k],lattice[i][j][k+1],lattice[i][j+1][k],lattice[i+1][j][k],lattice[i+1][j][k+1],lattice[i+1][j+1][k]]
                    prism1values = [values[i][j][k],values[i][j][k+1],values[i][j+1][k],values[i+1][j][k],values[i+1][j][k+1],values[i+1][j+1][k]]

                    prism2coords = [lattice[i][j][k+1],lattice[i][j+1][k],lattice[i][j+1][k+1],lattice[i+1][j][k+1],lattice[i+1][j+1][k],lattice[i+1][j+1][k+1]]
                    prism2values = [values[i][j][k+1],values[i][j+1][k],values[i][j+1][k+1],values[i+1][j][k+1],values[i+1][j+1][k],values[i+1][j+1][k+1]]
                else:
                    prism1coords = [lattice[i][j][k],lattice[i][j+1][k],lattice[i][j+1][k+1],lattice[i+1][j][k],lattice[i+1][j+1][k],lattice[i+1][j+1][k+1]]
                    prism1values = [values[i][j][k],values[i][j+1][k],values[i][j+1][k+1],values[i+1][j][k],values[i+1][j+1][k],values[i+1][j+1][k+1]]

                    prism2coords = [lattice[i][j][k],lattice[i][j+1][k+1],lattice[i][j][k+1],lattice[i+1][j][k],lattice[i+1][j+1][k+1],lattice[i+1][j][k+1]]
                    prism2values = [values[i][j][k],values[i][j+1][k+1],values[i][j][k+1],values[i+1][j][k],values[i+1][j+1][k+1],values[i+1][j][k+1]]

                newTriangles, newIndices = triangulatePrism(prism1coords,prism1values)
                triangles += newTriangles
                debugIndices += newIndices
                newTriangles, newIndices = triangulatePrism(prism2coords,prism2values)
                triangles += newTriangles
                debugIndices += newIndices
    return (triangles,debugIndices)

def gen_latex_scalar(values):
    ptstring = ""
    ptstring += r"\left["
    for val in values:
        ptstring += f"{val}," # make .3f when floats needed
    ptstring = ptstring[:-1] + r"\right]"
    return ptstring

def gen_latex_3d(points):
    ptstring = ""
    ptstring += r"\left["
    for pt in points:
        ptstring += f"\\left({pt[0]:.4f},{pt[1]:.4f},{pt[2]:.4f}\\right),"
    ptstring = ptstring[:-1] + r"\right]"
    return ptstring

def gen_latex_triangle(triangles):
    latex = ""
    latex += "\\left["
    for tri in triangles:
        latex += f"\\begin{{bmatrix}}{tri[0][0]:.4f}&{tri[0][1]:.4f}&{tri[0][2]:.4f}\\\\{tri[1][0]:.4f}&{tri[1][1]:.4f}&{tri[1][2]:.4f}\\\\{tri[2][0]:.4f}&{tri[2][1]:.4f}&{tri[2][2]:.4f}\\end{{bmatrix}},"
    latex = latex[:-1] + "\\right]"
    return latex

        
testCoords = [
    np.array([-1,0,SQRT_3]),
    np.array([0.5,0.5*SQRT_3,SQRT_3]),
    np.array([0.5,-0.5*SQRT_3,SQRT_3]),
    np.array([-1,0,0]),
    np.array([0.5,0.5*SQRT_3,0]),
    np.array([0.5,-0.5*SQRT_3,0]),
]

testLattice,testvalues = genPrismLattice(-5,-5,-5,10,20,10,1, lambda p: np.sum(np.square(p)) - 16)

triangles, indices = marchingPrismsLattice(testLattice,testvalues)

# t1,t2,t3 = tuple(zip(*triangles))

# ppc.copy(gen_latex_3d(t1))
# input("t1")

# ppc.copy(gen_latex_3d(t2))
# input("t2")

# ppc.copy(gen_latex_3d(t3))
# input("t3")

ppc.copy(gen_latex_triangle(triangles))
input("triangles")

ppc.copy(gen_latex_3d([x for plane in testLattice for row in plane for x in row]))
input("lattice")

ppc.copy(gen_latex_scalar(indices))