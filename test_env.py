import sys
import pymesh
import timeit
import numpy as np
from mesh_utils import *
# from greedy_remesh_remesh import gre_remesh
# from variational_remesh import var_remesh
from incremental_remesh import inc_remesh

mesh = pymesh.load_mesh(str(sys.argv[1]))

# mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100)
# mesh = pymesh.resolve_self_intersection(mesh)
# mesh, __ = pymesh.remove_duplicated_faces(mesh)
# mesh = pymesh.compute_outer_hull(mesh)
# mesh, __ = pymesh.remove_duplicated_faces(mesh)
# mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
# mesh, __ = pymesh.remove_isolated_vertices(mesh)

mesh, __ = pymesh.remove_duplicated_faces(mesh)
mesh, __ = pymesh.remove_isolated_vertices(mesh)

mesh.enable_connectivity()

edges = get_edges(mesh)

check_mesh(mesh)

start = timeit.default_timer()
mesh = equalize_valences(mesh)
stop = timeit.default_timer()
print('Time: ', stop - start)

# mesh = tangential_relaxation(mesh)
# edges = get_edges(mesh)
# check_mesh(mesh)
