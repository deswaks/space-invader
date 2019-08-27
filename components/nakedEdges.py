import ghpythonlib.components as ghComp
import ghpythonlib.parallel as par
import rhinoscriptsyntax as rs


# DelaunayMesh and get vertices and faces
mesh = ghComp.DelaunayMesh(points,rs.WorldXYPlane())
vertices,faces,_,_ = ghComp.DeconstructMesh(mesh)

# uses faces if max distance of edges are shorter than or equal to the given threshold(cell size ^2 + 2*cell size^2)
newMesh=[]
def face_distance(face):
    dist1=rs.Distance(points[face.A],points[face.B])
    dist2=rs.Distance(points[face.B],points[face.C])
    dist3=rs.Distance(points[face.C],points[face.A])
    maxDist=max(dist1,dist2,dist3)
    if(maxDist<=threshold):
        newMesh.append(face)
par.run(face_distance,faces)

# create final meshes and use naked edges for boundary
finalMesh=ghComp.ConstructMesh(vertices,newMesh)
nakedEdges = finalMesh.GetNakedEdges()