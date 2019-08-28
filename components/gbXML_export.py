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


def brep_area(brep, plane):
    section_curve = ghc.BrepXPlane(brep,plane)[0]
    area = ghc.Area(section_curve)[0]
    return area

def get_spatial_data(rooms):
    spatial_data = {"area":[],"volume":[]}
    for i, room_brep in enumerate(rooms):
        # Get volume
        room_volume, room_centroid = ghc.Volume(room_brep)
        spatial_data["volume"].append(int(room_volume))
        # Get Area
        room_area = brep_area(room_brep, ghc.XYPlane(room_centroid))
        spatial_data["area"].append(int(room_area))
    return spatial_data
spatial_data = get_spatial_data(rooms)



polyloops = []
for room_brep in rooms:
    faces = ghc.DeconstructBrep(room_brep)[0]
    for face in faces:
        edges = ghc.DeconstructBrep(face)[1]
        polyline = ghc.JoinCurves(edges, False)
        vertices = ghc.Explode(polyline)[1]
        a.append(vertices)


gbXML_txt = '''<Campus id="cmps-1">
    <Building id="bldg-1" buildingType="Office">
        <Area>15811.390974</Area>
        <Space id="sp-1-Open" zoneIdRef="zone-Default">
            <Name>1 Open</Name>
            <Area>3997.5</Area>
            <Volume>44055.8</Volume>
            <ShellGeometry id="sg-sp-1-Open" unit="Feet">
                <ClosedShell>
                    <PolyLoop>
                        <CartesianPoint>...</CartesianPoint>
                        <CartesianPoint>...</CartesianPoint>
                        <CartesianPoint>...</CartesianPoint>
                        <CartesianPoint>...</CartesianPoint>
                    </PolyLoop>
                    <PolyLoop>...</PolyLoop>
                    <PolyLoop>...</PolyLoop>
                    <PolyLoop>...</PolyLoop>
                    <PolyLoop>...</PolyLoop>
                    <PolyLoop>...</PolyLoop>
                </ClosedShell>
                <AnalyticalShell>...</AnalyticalShell>
            </ShellGeometry>
        </Space>
    </Building>
</Campus>'''


# Convert outputs to trees
a = ght.list_to_tree(a)