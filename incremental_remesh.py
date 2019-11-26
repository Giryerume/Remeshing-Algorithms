#!/usr/bin/env python

"""
Incremental remeshing algorithm that produces isotropic triangle meshes
"""

import argparse
import numpy as np
from numpy.linalg import norm
from mesh_utils import *

import pymesh

def inc_remesh(mesh, detail="normal"):
    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 5e-3
    elif detail == "high":
        target_len = diag_len * 2.5e-3
    elif detail == "low":
        target_len = diag_len * 2.5e-2
    print("Target resolution: {} mm".format(target_len))

    count = 1;

    #
    # mesh = pymesh.resolve_self_intersection(mesh)
    mesh, __ = pymesh.remove_duplicated_faces(mesh)
    # mesh = pymesh.compute_outer_hull(mesh)
    # mesh, __ = pymesh.remove_duplicated_faces(mesh)

    mesh, __ = pymesh.remove_isolated_vertices(mesh)

    num_vertices = mesh.num_vertices

    low = 4/5 * target_len
    high = 4/3 * target_len

    while True:
        print()
        print("[iteration "+str(count)+"]")
        # mesh, __ = pymesh.split_long_edges(mesh, high)
        # print("<split_long_edges> :      DONE")
        # mesh, __ = pymesh.collapse_short_edges(mesh, low, preserve_feature=True)
        # print("<collapse_short_edges> :  DONE")
        check_mesh(mesh)
        mesh = equalize_valences(mesh)
        print("<equalize_valences> :     DONE")
        # mesh = tangential_relaxation(mesh)
        # print("<tangential_relaxation> : DONE")

        if mesh.num_vertices == num_vertices: break

        num_vertices = mesh.num_vertices
        print("#v: {}".format(num_vertices))
        count += 1
        if count > 10: break

    # mesh = pymesh.resolve_self_intersection(mesh)
    # mesh, __ = pymesh.remove_duplicated_faces(mesh)
    # mesh = pymesh.compute_outer_hull(mesh)
    # mesh, __ = pymesh.remove_duplicated_faces(mesh)
    # mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
    # mesh, __ = pymesh.remove_isolated_vertices(mesh)

    check_mesh(mesh)

    return mesh;

def parse_args():
    parser = argparse.ArgumentParser(
            description=__doc__)
    parser.add_argument("--timing", help="print timing info",
            action="store_true")
    parser.add_argument("--detail", help="level of detail to preserve",
            choices=["low", "normal", "high"], default="low")
    parser.add_argument("in_mesh", help="input mesh")
    parser.add_argument("out_mesh", help="output mesh")
    return parser.parse_args()

def main():
    args = parse_args()
    mesh = pymesh.meshio.load_mesh(args.in_mesh)

    mesh = inc_remesh(mesh, detail = args.detail)

    pymesh.meshio.save_mesh(args.out_mesh, mesh)

    if args.timing:
        pymesh.timethis.summarize()

if __name__ == "__main__":
    main()
