""" Export rooms to gbXML
Input:
    rooms [brep] - Solid of the rooms to export
    path [path] - Place to save the gbXML
"""
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as ght


room_polylines = [ghc.JoinCurves(segments, False) for segments in room_segments]

a = []
for room_brep in rooms:
    faces = ghc.DeconstructBrep(room_brep)[0]
    for face in faces:
        edges = ghc.DeconstructBrep(face)[1]
        polyline = ghc.JoinCurves(edges, False)
        vertices = ghc.Explode(polyline)[1]
        a.append(vertices)





# Convert outputs to trees
a = ght.list_to_tree(a)