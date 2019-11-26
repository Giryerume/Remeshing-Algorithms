#!/usr/bin/env python

"""
Greedy surface meshing algorithm used for isotropic remeshing of smooth surfaces
"""

import argparse
import numpy as np
from numpy.linalg import norm

import pymesh

# def dual(facet):

# def intersection(dual, s):

# def delaunay_triang(points):

def gre_remesh(mesh, detail="normal"):
    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 5e-3
    elif detail == "high":
        target_len = diag_len * 2.5e-3
    elif detail == "low":
        target_len = diag_len * 1e-2
    print("Target resolution: {} mm".format(target_len))

    # -- pseudocódigo --
    # while L is not empty
    #     pop one bad facet f from L
    #     cf = dual(f) ∩ S
    #     insert cf to P
    #     update Del(P)
    #     update DelS (P)
    #     update L, i.e.,
    #       remove facets of L that are no longer facets of DelS (P)
    #       add new bad facets of DelS (P) to L

    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100)
    num_vertices = mesh.num_vertices

    p = mesh.vertices #conjunto P de pontos da malha
    del_p, dels_p, bad_facets = delaunay_triang(p)# triagulação de Delauney
    l = bad_facets #lista L de faceta ruins de Dels(P)

    while True:
        if len(l)==0: break
        f = l.pop()
        cf = intersection(dual(f), mesh)
        p.append(cf)
        del_p, dels_p, bad_facets = delaunay_triang(p)
        l = bad_facets

        num_vertices = mesh.num_vertices
        print("#v: {}".format(num_vertices))

    # mesh = pymesh.resolve_self_intersection(mesh)
    # mesh, __ = pymesh.remove_duplicated_faces(mesh)
    # mesh = pymesh.compute_outer_hull(mesh)
    # mesh, __ = pymesh.remove_duplicated_faces(mesh)
    # mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5)
    # mesh, __ = pymesh.remove_isolated_vertices(mesh)

    return mesh

def parse_args():
    parser = argparse.ArgumentParser(
            description=__doc__)
    parser.add_argument("--timing", help="print timing info",
            action="store_true")
    parser.add_argument("--detail", help="level of detail to preserve",
            choices=["low", "normal", "high"], default="normal")
    parser.add_argument("in_mesh", help="input mesh")
    parser.add_argument("out_mesh", help="output mesh")
    return parser.parse_args()

def main():
    args = parse_args()
    mesh = pymesh.meshio.load_mesh(args.in_mesh)

    mesh = gre_remesh(mesh, detail = args.detail)

    pymesh.meshio.save_mesh(args.out_mesh, mesh)

    if args.timing:
        pymesh.timethis.summarize()

if __name__ == "__main__":
    main();
