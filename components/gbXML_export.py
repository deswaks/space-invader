""" Export rooms to gbXML
Input:
    rooms [brep] - Solid of the rooms to export
    path [path] - Place to save the gbXML
"""
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as ght

# Convert brep to polylines
room_segments = [ghc.DeconstructBrep(room)[1] for room in rooms]
room_polylines = [ghc.JoinCurves(segments, False) for segments in room_segments]



# Convert outputs to trees
a = ght.list_to_tree(a)