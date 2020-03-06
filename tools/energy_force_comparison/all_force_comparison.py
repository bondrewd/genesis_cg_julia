#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(cafefile, genefile, line_num, output_option):
    all_dict_cafe = {}
    all_dict_gene = {}

    iline = 0
    with open(cafefile, "r") as cafin:
        for line in cafin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i = int(words[1])
            local_forces = []
            for k in [4, 7, 10]:
                local_forces.append(float(words[k]))
            all_dict_cafe[i] = np.array( local_forces )

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i = int(words[1])
            local_forces = []
            for k in [4, 7, 10]:
                local_forces.append(float(words[k]))
            all_dict_gene[i] = np.array( local_forces )

    f_all_cafe_all = []
    f_all_gene_all = []
    f_all_diff_all = []
    for pair, f_all_cafe in all_dict_cafe.items():
        f_all_cafe_all.append(f_all_cafe)
        f_all_gene = all_dict_gene[pair]
        f_all_gene_all.append(f_all_gene)
        f_all_diff_all.append(f_all_cafe - f_all_gene)
        
    f_all_cafe_arr = np.array(f_all_cafe_all)
    f_all_gene_arr = np.array(f_all_gene_all)
    f_all_diff_arr = np.array(f_all_diff_all)

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(3, 1, figsize=(10, 12), constrained_layout=True, sharex=True)
    X = [i for i in range(line_num)]
    for i in range(3):
        ax[i].plot(X, f_all_cafe_arr[:, i], ls="-",  lw=2.0, c="g", alpha=0.3)
        ax[i].plot(X, f_all_gene_arr[:, i], ls="--", lw=1.0, c="r")
        ax[i].plot(X, f_all_diff_arr[:, i], ls="-",  lw=2.0, c="k", alpha=1.0)

        ax_x_ticks = ax[i].get_xticks()
        ax[i].set_xticklabels([ int(x) for x in ax_x_ticks ], fontsize=15)
        ax[i].set_xlabel("All index", fontsize=18)
        ax[i].set_ylim(-10.0, 10.0)
        ax_y_ticks = ax[i].get_yticks()
        ax[i].set_yticklabels([ round(y, 2) for y in ax_y_ticks ], fontsize=15)
        ax[i].set_ylabel("$F_{{all}}$", fontsize=18)

    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("all_force_comparison.png", dpi=150)

if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Compare energy/force output.')

        parser.add_argument('-c', '--cafemol', required=True, type=str)
        parser.add_argument('-g', '--genesis', required=True, type=str)
        parser.add_argument('-n', '--num',     required=True, type=int)
        parser.add_argument('-o', '--out',     required=False, type=int, default=0)
        
        return parser.parse_args()

    args = parse_arguments()

    main(args.cafemol, args.genesis, args.num, args.out)
