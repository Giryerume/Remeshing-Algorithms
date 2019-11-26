import numpy as np

import pymesh

def equalize_valences(mesh):
    edges = get_edges(mesh)
    for e in range(len(edges)):
        if e>=len(edges):
            break

        # if is_border(edges[e][0],mesh) and is_border(edges[e][1],mesh):
        #     continue

        v, _ = vertices_triangles_adjacent(e, edges, mesh)
        if len(v)!= 4 :
            continue

        print(e, end="\r")
        deviation_pre = deviation(v, mesh)
        new_mesh = flip_edge(e, edges, mesh)
        deviation_post = deviation(v, new_mesh)

        if deviation_pre > deviation_post:
            mesh = new_mesh
            edges = get_edges(mesh)

    mesh = pymesh.compute_outer_hull(mesh)
    return mesh

def tangential_relaxation(mesh):
    q = np.zeros(shape=(mesh.num_vertices,3))
    p = np.zeros(shape=(mesh.num_vertices,3))
    n = np.zeros(shape=(mesh.num_vertices,3))
    mesh.add_attribute("vertex_normal")
    for v in range(len(mesh.vertices)):
        print(v, end="\r")
        q[v] = barycenter(v, mesh)# the barycenter of v’s neighbor vertices
    for v in range(len(mesh.vertices)):
        p[v] = mesh.vertices[v] # position of v
        n[v] = mesh.get_vertex_attribute("vertex_normal")[v] # normal of v
        p[v] = np.add(q[v],np.dot(np.dot(n[v],np.subtract(p[v],q[v])),n[v]))

    return pymesh.form_mesh(p, mesh.faces)

def deviation(v, mesh):
    return abs(valence(v[0], mesh)-target_val(v[0], mesh))
    + abs(valence(v[1], mesh)-target_val(v[1], mesh))
    + abs(valence(v[2], mesh)-target_val(v[2], mesh))
    + abs(valence(v[3], mesh)-target_val(v[3], mesh))

def barycenter(vertex, mesh):
    mesh.enable_connectivity()
    nbs = mesh.get_vertex_adjacent_vertices(vertex)
    nbsv = np.array([mesh.vertices[x] for x in nbs])
    b = nbsv.mean(0)
    return b

def get_edges(mesh):
    mesh.enable_connectivity();
    edges = []
    for i in range(mesh.num_vertices):
        nbs = mesh.get_vertex_adjacent_vertices(i)
        for v in nbs:
            edges.append((i,v))
    edges = set(tuple(sorted(l)) for l in edges)
    return np.array(list(edges))

# def get_edges(mesh):
#     edges = []
#     for i in range(mesh.num_faces):
#         edges.append((mesh.faces[i][0],mesh.faces[i][1]))
#         edges.append((mesh.faces[i][0],mesh.faces[i][2]))
#         edges.append((mesh.faces[i][1],mesh.faces[i][2]))
#     edges = set(tuple(sorted(l)) for l in edges)
#     return np.array(list(edges))
#
# def get_edges(mesh):
#     edges = [[mesh.faces[i][0],mesh.faces[i][1],mesh.faces[i][0],mesh.faces[i][2],mesh.faces[i][1],mesh.faces[i][2]] for i in range(mesh.num_faces)]
#     edges = np.array(edges)
#     edges = np.reshape(edges,(-1,2))
#     edges = set(tuple(sorted(l)) for l in edges)
#     return np.array(list(edges))

# def vertices_triangles_adjacent(edge, edges, mesh):
#     faces = []
#     x = edges[edge][0]
#     y = edges[edge][1]
#
#     for i in range(len(mesh.faces)):
#         if x in mesh.faces[i] and y in mesh.faces[i]:
#             faces.append(i)
#
#     vertices = list(set(list(mesh.faces[faces[0]]) + list(mesh.faces[faces[1]])))
#     return vertices, faces

def vertices_triangles_adjacent(edge, edges, mesh):
    faces = []
    x = edges[edge][0]
    y = edges[edge][1]

    xi = set(np.where(mesh.faces==x)[0])
    yi = set(np.where(mesh.faces==y)[0])

    faces = list(xi.intersection(yi))
    if len(faces)!=2 : return [], faces

    vertices = list(set(list(mesh.faces[faces[0]]) + list(mesh.faces[faces[1]])))
    return vertices, faces

def valence(vertex, mesh):
    mesh.enable_connectivity();
    return len(mesh.get_vertex_adjacent_vertices(vertex))

def target_val(vertex, mesh):
    if is_border(vertex, mesh): return 4
    return 6

def is_border(vertex, mesh):
    if valence(vertex, mesh) <= 4: return True
    return False

def flip_edge(edge, edges, mesh):
    faces = mesh.faces
    old_edge = [edges[edge][0],edges[edge][1]]

    v, f = vertices_triangles_adjacent(edge, edges, mesh)

    new_faces = np.delete(faces,f,0)
    new_edge = list(np.setdiff1d(v,old_edge))

    f1 = new_edge + [old_edge[0]]
    f2 = new_edge + [old_edge[1]]

    new_faces = np.vstack([new_faces, f1])
    new_faces = np.vstack([new_faces, f2])

    new_mesh = pymesh.form_mesh(mesh.vertices, new_faces)
    return new_mesh

def check_mesh(mesh):
    edges = get_edges(mesh)
    print()
    print("| vertices : "+str(mesh.num_vertices))
    print("|    faces : "+str(mesh.num_faces))
    print("|    edges : "+str(len(edges)))
    print()
