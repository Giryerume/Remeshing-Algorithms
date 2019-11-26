#!/usr/bin/env python

"""
Variational surface remeshing technique based on Lloyd relaxation
"""

import argparse
import numpy as np
from numpy.linalg import norm

import pymesh

def var_remesh(mesh, detail="normal"):
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
    # conformal paramerization of M
    # compute density function
    # perform in parameter space
    #     random sampling in accordance to the density function
    #     repeat until convergence
    #         Voronoi diagram
    #         relocate sites to Voronoi cell centroids
    # lift 2D Delaunay triangulation to 3D

    # count = 0;
    # mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100);
    # mesh, __ = pymesh.split_long_edges(mesh, target_len);
    # num_vertices = mesh.num_vertices;

    # mesh = pymesh.resolve_self_intersection(mesh);
    # mesh, __ = pymesh.remove_duplicated_faces(mesh);
    # mesh = pymesh.compute_outer_hull(mesh);
    # mesh, __ = pymesh.remove_duplicated_faces(mesh);
    # mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5);
    # mesh, __ = pymesh.remove_isolated_vertices(mesh);

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

    mesh = var_remesh(mesh, detail = args.detail)

    pymesh.meshio.save_mesh(args.out_mesh, mesh)

    if args.timing:
        pymesh.timethis.summarize()

if __name__ == "__main__":
    main()
