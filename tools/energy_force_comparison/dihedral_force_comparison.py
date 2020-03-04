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
            local_forces = []
            for m in range(8, 42, 3):
                local_forces.append(-float(words[m]))
            dihedral_dict_cafe[(i, j, k, l)] = np.array( local_forces )

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j, k, l = int(words[2]), int(words[3]), int(words[4]), int(words[5])
            local_forces = []
            for m in range(8, 42, 3):
                local_forces.append(-float(words[m]))
            dihedral_dict_gene[(i, j, k, l)] = np.array( local_forces )

    f_dihedral_cafe_all = []
    f_dihedral_gene_all = []
    f_dihedral_diff_all = []
    for pair, f_dihedral_cafe in dihedral_dict_cafe.items():
        f_dihedral_cafe_all.append(f_dihedral_cafe)
        if pair in dihedral_dict_gene.keys():
            f_dihedral_gene = dihedral_dict_gene[pair]
        else:
            f_dihedral_gene = np.zeros(12)
        f_dihedral_gene_all.append(f_dihedral_gene)
        f_dihedral_diff_all.append(f_dihedral_cafe - f_dihedral_gene)
        
    f_dihedral_cafe_arr = np.array(f_dihedral_cafe_all)
    f_dihedral_gene_arr = np.array(f_dihedral_gene_all)
    f_dihedral_diff_arr = np.array(f_dihedral_diff_all)

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(4, 3, figsize=(20, 12), constrained_layout=True, sharex=True, sharey=True)
    X = [i for i in range(line_num)]
    for i in range(12):
        m, n = i // 3, i % 3
        ax[m, n].plot(X, f_dihedral_cafe_arr[:, i], ls="-",  lw=2.0, c="g", alpha=0.3)
        ax[m, n].plot(X, f_dihedral_gene_arr[:, i], ls="--", lw=1.0, c="r")
        ax[m, n].plot(X, f_dihedral_diff_arr[:, i], ls="-",  lw=2.0, c="k", alpha=1.0)

        ax_x_ticks = ax[m, n].get_xticks()
        if m == 3:
            ax[m, n].set_xticklabels([int(x) for x in ax_x_ticks ], fontsize=15)
            ax[m, n].set_xlabel("Dihedral index", fontsize=18)
        ax_y_ticks = ax[m, n].get_yticks()
        if n == 0:
            ax[m, n].set_yticks(ax_y_ticks)
            ax[m, n].set_yticklabels([round(y, 2) for y in ax_y_ticks ], fontsize=15)
            ax[m, n].set_ylabel("$F_{{dihedral}}$", fontsize=18)

    if dih_type == 1:
        ditype = "periodic"
    elif dih_type == 2:
        ditype = "Gaussian"
    elif dih_type == 3:
        ditype = "flexible"
    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("dihedral_force_comparison_{0}.png".format(ditype), dpi=150)

if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Compare energy/force output.')

        parser.add_argument('-c', '--cafemol', required=True, type=str)
        parser.add_argument('-g', '--genesis', required=True, type=str)
        parser.add_argument('-n', '--num',     required=True, type=int)
        parser.add_argument('-t', '--type',    required=True, type=int)
        parser.add_argument('-o', '--out',     required=False, type=int, default=0)
        
        return parser.parse_args()

    args = parse_arguments()

    main(args.cafemol, args.genesis, args.num, args.out, args.type)
