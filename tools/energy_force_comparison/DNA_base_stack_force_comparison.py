#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(cafefile, genefile, line_num, output_option):
    base_dict_cafe = {}
    base_dict_gene = {}

    iline = 0
    with open(cafefile, "r") as cafin:
        for line in cafin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j = int(words[1]), int(words[2])
            local_forces = []
            for k in range(5, 22, 2):
                local_forces.append(float(words[k]))
            base_dict_cafe[(i, j)] = np.array( local_forces )

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j = int(words[1]), int(words[2])
            local_forces = []
            for k in range(5, 22, 2):
                local_forces.append(float(words[k]))
            base_dict_gene[(i, j)] = np.array( local_forces )

    f_base_cafe_all = []
    f_base_gene_all = []
    f_base_diff_all = []
    for base, f_base_cafe in base_dict_cafe.items():
        f_base_cafe_all.append(f_base_cafe)
        if base in base_dict_gene:
            f_base_gene = base_dict_gene[base]
        else:
            f_base_gene = np.zeros(9)

        f_base_gene_all.append(f_base_gene)
        f_base_diff_all.append(f_base_cafe - f_base_gene)
        
    f_base_cafe_arr = np.array(f_base_cafe_all)
    f_base_gene_arr = np.array(f_base_gene_all)
    f_base_diff_arr = np.array(f_base_diff_all)

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(3, 3, figsize=(20, 8), constrained_layout=True, sharex=True)
    X = [i for i in range(line_num)]
    for i in range(9):
        m, n = i // 3, i % 3
        ax[m, n].plot(X, f_base_cafe_arr[:, i], ls="-",  lw=2.0, c="g", alpha=0.3)
        ax[m, n].plot(X, f_base_gene_arr[:, i], ls="--", lw=1.0, c="r")
        ax[m, n].plot(X, f_base_diff_arr[:, i], ls="-",  lw=2.0, c="k", alpha=1.0)

        ax_x_ticks = ax[m, n].get_xticks()
        ax[m, n].set_xticklabels([ int(x) for x in ax_x_ticks ], fontsize=15)
        ax[m, n].set_xlabel("Base index", fontsize=18)
        ax_y_ticks = ax[m, n].get_yticks()
        ax[m, n].set_yticklabels([ round(y, 2) for y in ax_y_ticks ], fontsize=15)
        ax[m, n].set_ylabel(r"$F$", fontsize=18)

    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("base_stack_force_comparison.png", dpi=150)

if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Compare energy/force output.')

        parser.add_argument('-c', '--cafemol', required=True, type=str)
        parser.add_argument('-g', '--genesis', required=True, type=str)
        parser.add_argument('-n', '--num',     required=True, type=int)
        parser.add_argument('-t', '--functype',required=False, type=str, default="basestack")
        parser.add_argument('-o', '--out',     required=False, type=int, default=0)
        
        return parser.parse_args()

    args = parse_arguments()

    main(args.cafemol, args.genesis, args.num, args.out)
