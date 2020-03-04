#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(cafefile, genefile, line_num, output_option, dih_type):
    dihedral_dict_cafe = {}
    dihedral_dict_gene = {}

    iline = 0
    with open(cafefile, "r") as cafin:
        for line in cafin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j, k, l = int(words[2]), int(words[3]), int(words[4]), int(words[5])
            dihedral_dict_cafe[(i, j, k, l)] = float(words[17])

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j, k, l = int(words[2]), int(words[3]), int(words[4]), int(words[5])
            dihedral_dict_gene[(i, j, k, l)] = float(words[17])

    e_dihedral_cafe_all = []
    e_dihedral_gene_all = []
    e_dihedral_diff_all = []
    for pair, e_dihedral_cafe in dihedral_dict_cafe.items():
        e_dihedral_cafe_all.append(e_dihedral_cafe)
        e_dihedral_gene = dihedral_dict_gene[pair]
        e_dihedral_gene_all.append(e_dihedral_gene)
        e_dihedral_diff_all.append(e_dihedral_cafe - e_dihedral_gene)
        

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(1, 1, figsize=(9, 5), constrained_layout=True, sharex=True)
    X = [i for i in range(len(e_dihedral_cafe_all))]
    ax.plot(X, e_dihedral_cafe_all, ls="-",  lw=2.0, c="g", alpha=0.3)
    ax.plot(X, e_dihedral_gene_all, ls="--",  lw=1.0, c="r")
    ax.plot(X, e_dihedral_diff_all, ls="-", lw=2.0, c="k", alpha=1.0)

    ax_x_ticks = ax.get_xticks()
    ax.set_xticklabels([int( x ) for x in ax_x_ticks ], fontsize=15)
    ax.set_xlabel("Dihedral index", fontsize=18)
    ax_y_ticks = ax.get_yticks()
    ax.set_yticklabels([round(y, 2) for y in ax_y_ticks ], fontsize=15)
    ax.set_ylabel(r"$E_{{dihedral}}$ (kcal/mol)", fontsize=18)

    if dih_type == 1:
        ditype = "periodic"
    elif dih_type == 2:
        ditype = "Gaussian"
    elif dih_type == 3:
        ditype = "flexible"
    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("dihedral_energy_comparison_{0}.png".format(ditype), dpi=150)

if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Compare energy/force output.')

        parser.add_argument('-c', '--cafemol', required=True, type=str)
        parser.add_argument('-g', '--genesis', required=True, type=str)
        parser.add_argument('-n', '--num',     required=True, type=int)
        parser.add_argument('-t', '--type', required=False, type=int, help="1: periodic; 2: Gaussian; 3: flexible")
        parser.add_argument('-o', '--out',     required=False, type=int, default=0)
        
        return parser.parse_args()

    args = parse_arguments()

    main(args.cafemol, args.genesis, args.num, args.out, args.type)
