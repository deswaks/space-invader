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
    """ Computes plane area of a brep"""
    section_curve = ghc.BrepXPlane(brep,plane)[0]
    area = ghc.Area(section_curve)[0]
    return area

def get_spatial_data(breps):
    """ Creates a dictionary with volume and area of the breps"""
    spatial_data = {"area":[],"volume":[]}
    for i, room_brep in enumerate(breps):
        # Get volume
        room_volume, room_centroid = ghc.Volume(room_brep)
        spatial_data["volume"].append(int(room_volume))
        # Get Area
        room_area = brep_area(room_brep, ghc.XYPlane(room_centroid))
        spatial_data["area"].append(int(room_area))
    return spatial_data

def brep_polyloops(brep):
    """ Returns the polyloop of all faces for a brep"""
    faces = ghc.DeconstructBrep(brep)[0]
    polyloops = []
    for face in faces:
        edges = ghc.DeconstructBrep(face)[1]
        polyline = ghc.JoinCurves(edges, False)
        vertices = ghc.Explode(polyline, recursive=True)[1]
        polyloops.append(vertices)
    return polyloops

def room_xml_string(room_brep, i):
    # Header for string concatenation
    XML_room_header = '''\n        <Space id="sp-%i-Open" zoneIdRef="zone-Default">
            <Name>%i Open</Name>
            <Area>%i</Area>
            <Volume>%i</Volume>
            <ShellGeometry id="sg-sp-%i-Open" unit="mm">
                <ClosedShell>''' %(i,i,spatial_data["area"][i],spatial_data["volume"][i],i)
    
    # Goemetry strings for string concatenation
    XML_room_polyloops = ""
    polyloops = brep_polyloops(room_brep)
    for polyloop in polyloops:
        XML_room_polyloops += "\n\t\t\t\t\t<PolyLoop>"
        for point in polyloop:
            XML_room_polyloops += "\n"+"\t"*6+"<CartesianPoint>"
            for coordinate in point:
                XML_room_polyloops += "\n"+"\t"*7+"<Coordinate>%i<Coordinate>" %int(coordinate)
            XML_room_polyloops += "\n"+"\t"*6+"</CartesianPoint>"
        XML_room_polyloops += "\n\t\t\t\t\t</PolyLoop>"
    
    # Footer for string concatenation
    XML_room_footer = '''</ClosedShell>
                <AnalyticalShell>
                </AnalyticalShell>
            </ShellGeometry>
        </Space>'''
    return XML_room_header + XML_room_polyloops + XML_room_footer


# Open file and create list to write
xml = open(path, "w")

# Get volume and area
spatial_data = get_spatial_data(rooms)

# Write header and open tags
XML_header = '''<Campus id="cmps-1">
    <Building id="bldg-1" buildingType="Office">
        <Area>%i</Area>''' % sum(spatial_data["area"])
xml.write(XML_header)

# Write rooms
for i, room_brep in enumerate(rooms):
    xml.write(room_xml_string(room_brep, i))

# Write Close tags
XML_footer = '''</Building>\n</Campus>'''
xml.write(XML_footer)

# close file
xml.close()