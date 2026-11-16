import math
import numpy as np
import pyperclip


def gen_latex_3d(points):
  ptstring = ""
  ptstring += r"\left["
  for pt in points:
    ptstring += f"\\left({pt[0]:.3f},{pt[1]:.3f},{pt[2]:.3f}\\right),"
  ptstring = ptstring[:-1] + r"\right]"
  return ptstring



# Icosahedron
vertices = [
  np.array([0,-0.5,-0.8090169943749475]),
  np.array([0,0.5,-0.8090169943749475]),
  np.array([0,-0.5,0.8090169943749475]),
  np.array([0,0.5,0.8090169943749475]),
  np.array([-0.8090169943749475,0,-0.5]),
  np.array([-0.8090169943749475,0,0.5]),
  np.array([0.8090169943749475,0,-0.5]),
  np.array([0.8090169943749475,0,0.5]),
  np.array([-0.5,-0.8090169943749475,0]),
  np.array([0.5,-0.8090169943749475,0]),
  np.array([-0.5,0.8090169943749475,0]),
  np.array([0.5,0.8090169943749475,0])
]

triangles = [
  [0,1,4],
  [0,1,6],
  [0,4,8],
  [0,6,9],
  [0,8,9],
  [1,4,10],
  [1,6,11],
  [1,10,11],
  [2,3,5],
  [2,3,7],
  [2,5,8],
  [2,7,9],
  [2,8,9],
  [3,5,10],
  [3,7,11],
  [3,10,11],
  [4,5,8],
  [4,5,10],
  [6,7,9],
  [6,7,11]
]

def subdivide(p_a,p_b,p_c, n):
  fractions = [x/n for x in range(n+1)]
  # Step one: subdivide AB and AC
  ab_pts = [(1-t)*p_a + t*p_b for t in fractions]
  ac_pts = [(1-t)*p_a + t*p_c for t in fractions]
  output = []
  # Step two: loop through each 'layer' of the triangle
  for i in range(n+1):
    # Establish the layer using our subdivided points
    start = ab_pts[i]
    end = ac_pts[i]
    # Split up the layer into more subdivided points
    subfractions = [x/i for x in range(i+1)] if i > 0 else [1]
    rowpoints = [t*end + (1-t)*start for t in subfractions]
    # Append the new points to the output
    output += rowpoints
  return output

def subdivide_edges(p_a,p_b,p_c, n):
  fractions = [x/n for x in range(n+1)]
  # Step one: subdivide AB and AC
  ab_pts = [(1-t)*p_a + t*p_b for t in fractions]
  ac_pts = [(1-t)*p_a + t*p_c for t in fractions]
  output = []
  for i in range(n+1):
    start = ab_pts[i]
    end = ac_pts[i]
    subfractions = [x/i for x in range(i+1)] if i > 0 else [1]
    rowpoints = [t*end + (1-t)*start for t in subfractions]
    output += rowpoints
  return output



pts = []
for tri in triangles:
  pts += subdivide(
  vertices[tri[0]],
  vertices[tri[1]],
  vertices[tri[2]],
  50)

ptsnorm = [np.divide(pt,np.sqrt(np.sum(np.square(pt)))) for pt in pts]

for window in range(0,len(ptsnorm),10000):
  subpts = ptsnorm[window:window+10000]
  pyperclip.copy(gen_latex_3d(subpts))
  input(window)



