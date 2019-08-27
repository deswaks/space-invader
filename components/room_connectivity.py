import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as ght

connectivity = []

reparametrize = rg.Interval(0,1)
global_Z = rg.Vector3d(0,0,1)

def create_outside_points(segment):
    # Create a point mid-curve outside the region
    points = []
    n_pts = int(segment.GetLength()/pt_dist)
    curve_points, tangents, _ = ghc.DivideCurve(segment, n_pts, False)
    if n_pts > 1:
        for curve_point in curve_points[1:-1]:
            normal = ghc.CrossProduct(tangents[0], global_Z, True)
            curve_point, _ = ghc.Move(curve_point, normal[0]*move_dist)
            points.append(curve_point)
        return points

all_pts = []
all_sgmts = []
for room in srf:
    _, segments, _ = ghc.DeconstructBrep(room)
    all_sgmts.append(segments)
    for segment in segments:
        points = create_outside_points(segment)
        all_pts.append(points)

all_sgmts = ght.list_to_tree(all_sgmts)
all_pts = ght.list_to_tree(all_pts)