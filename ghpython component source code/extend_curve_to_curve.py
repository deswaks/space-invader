""" Extends curves until they hit another curve if there is one within
the distance threshold
Inputs:
    C   Wall curves
    t   Distance threshold
Outputs:
    C  Wall curves
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.components as gh
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

EPS = 1e-1


def extend_to_collision(curve, obstacles):
    extensions = []
    if curve.IsPolyline():
        #Start point ray
        pnt0 = curve.PointAtStart
        tan0 = curve.TangentAtStart
        tan0.Reverse()
        ray0 = rg.Line(pnt0, tan0, 1)
        _, dist0, i0 = gh.IsoVistRay(ray0, t, obstacles)
        if i0 != -1:
#            print(pnt0, tan0, ray0, dist0)
            extensions.append(rg.LineCurve(rg.Line(pnt0, tan0, dist0)))
        
        #End Point ray
        pnt1 = curve.PointAtEnd
        tan1 = curve.TangentAtEnd
        ray1 = rg.Line(pnt1, tan1, 1)
        _, dist1, i1 = gh.IsoVistRay(ray1, t, obstacles)
        if i1 != -1:
            print(pnt1, tan1, ray1, dist1)
            print(obstacles)
            extensions.append(rg.LineCurve(rg.Line(pnt1, tan1, dist1)))
    return extensions


def clean_obstacles(curve, other_curves):
    oc = []
    for other_curve in other_curves:
        distances = [gh.Distance(curve.PointAtStart, other_curve.PointAtStart),
                     gh.Distance(curve.PointAtStart, other_curve.PointAtEnd),
                     gh.Distance(curve.PointAtEnd, other_curve.PointAtStart),
                     gh.Distance(curve.PointAtEnd, other_curve.PointAtEnd)]
        close = [True if d<=EPS else False for d in distances]
        if not any(close):
            oc.append(other_curve)
    return oc

C.Flatten()
curves = ght.tree_to_list(C)
all_extensions = []
for i, curve in enumerate(curves):
    obstacles = clean_obstacles(curve, curves)
    print(i, len(obstacles),"/",len(curves))
    curve_extensions = extend_to_collision(curve, obstacles)
    all_extensions.extend(curve_extensions)
curves.extend(all_extensions)

C = ght.list_to_tree(curves)