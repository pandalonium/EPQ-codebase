import numpy as np
import pyperclip as pc

def gen_latex_3d(points):
    ptstring = ""
    ptstring += r"\left["
    for pt in points:
        ptstring += f"\\left({pt[0]:.3f},{pt[1]:.3f},{pt[2]:.3f}\\right),"
    ptstring = ptstring[:-1] + r"\right]"
    return ptstring

class Simulator:
    def __init__(self, points : np.ndarray, edges : np.ndarray):
        self.points = points
        self.edges = edges
        self.velocities = np.zeros(self.points.shape)

    def projectToSphere(self):
        magnitudes = np.sqrt(np.sum(np.square(self.points),axis=1))
        self.points = np.divide(self.points,magnitudes)

rng = np.random.default_rng()
testpoints = rng.random((10000,3))
print(testpoints)

testsim = Simulator(testpoints,np.array([0,0,0]))
testsim.projectToSphere()
pc.copy(gen_latex_3d(testsim.points))



