import System
import clr
clr.AddReference("Grasshopper")
import rhinoscriptsyntax as rs
from Grasshopper import DataTree
import Rhino.Geometry as rg
import ghpythonlib.components as ghc
import ghpythonlib.treehelpers as ght

a = []
# Checks whether the input geometry is brep, mesh or curve
# If it is a brep or mesh, the input height is used to create the contour, in 
# the given height
# Curves are then projected onto world xy-plane
for i in range (len(geometry)):
    if (geometry[i].ToString().split(".")[-1]).Contains("Brep"):
        a.append(geometry[i].CreateContourCurves(geometry[i],rs.MovePlane(rs.WorldXYPlane(),[0,0,height])))
    elif (geometry[i].ToString().split(".")[-1]).Contains("Mesh"):
        a.append(geometry[i].CreateContourCurves(geometry[i],rs.MovePlane(rs.WorldXYPlane(),[0,0,height])))
    elif (geometry[i].ToString().split(".")[-1]).Contains("Curve"):
        a.append(geometry[i].ProjectToPlane(geometry[i],rs.WorldXYPlane()))

a = ght.list_to_tree(a)
a.Flatten()