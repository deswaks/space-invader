""" Find the adjacent rooms for each room
Input:
    rooms [brep] - Surfaces of the rooms to analyze
    distance [value] - Distance from the room to check for other rooms
    sample [value] - Distance between sample points (lower = more points)
Returns:
    connectivity [index] - Nested Lists of indices of adjacent rooms
"""
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as ght

# Create output Lists
room_polylines = []
room_points = []
connectivity = []

# Define global tool objects
global_Z = rg.Vector3d(0,0,1)

def create_outside_points(segment):
    # Create a point mid-curve outside the region
    points = []
    n_pts = int(segment.GetLength()/sample)
    curve_points, tangents, _ = ghc.DivideCurve(segment, n_pts, False)
    if n_pts > 1:
        for curve_point in curve_points[1:-1]:
            normal = ghc.CrossProduct(tangents[0], global_Z, True)
            curve_point, _ = ghc.Move(curve_point, normal[0]*distance)
            points.append(curve_point)
        return points


# Convert brep to polylines
room_segments = [ghc.DeconstructBrep(room)[1] for room in rooms]
room_polylines = [ghc.JoinCurves(segments, False) for segments in room_segments]

# Main script
for i, room_polyline in enumerate(room_polylines):
    connect = set()
    for segment in room_segments[i]:
        points = create_outside_points(segment)
        if type(points) in [list, tuple]:
            for p in points:
                for j, pl in enumerate(room_polylines):
                    if j not in connect:
                        relation, _ = ghc.PointInCurve(p, pl)
                        if relation > 0:
                            connect.add(j)
    connectivity.append(list(connect))


# Convert outputs to trees
connectivity = ght.list_to_tree(connectivity)