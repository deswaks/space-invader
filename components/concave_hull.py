import ghpythonlib.components as ghComp
import rhinoscriptsyntax as rs

# mesh and faces
mesh = ghComp.DelaunayMesh(pts)
vertices,faces,colours,normals = ghComp.DeconstructMesh(mesh)

# max distance of edges of all faces
maxDists=[]
for face in faces:
    dist1=rs.Distance(pts[face.A],pts[face.B])
    dist2=rs.Distance(pts[face.B],pts[face.C])
    dist3=rs.Distance(pts[face.C],pts[face.A])
    maxDist=max(dist1,dist2,dist3)
    maxDists.append(maxDist)

# median 
sortedDists = sorted(maxDists)
medIndex = int(len(sortedDists)/2)
median = sortedDists[medIndex]

# keep faces with edges within treshold
distTreshold=median*(1.0+factor)
newMesh=[]
i = 0
for face in faces:
    if(maxDists[i]<distTreshold):
        newMesh.append(face)
    i+=1

# create final meshes and outlines
finalMesh=ghComp.ConstructMesh(vertices,newMesh)
concaveHull = rs.MeshOutline(finalMesh)
