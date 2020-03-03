#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(cafefile, genefile, line_num, output_option):
    angle_dict_cafe = {}
    angle_dict_gene = {}

    iline = 0
    with open(cafefile, "r") as cafin:
        for line in cafin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j, k = int(words[2]), int(words[3]), int(words[4])
            local_forces = []
            for l in range(7, 23, 3):
                local_forces.append(-float(words[l]))
            angle_dict_cafe[(i, j, k)] = np.array( local_forces )

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j, k = int(words[2]), int(words[3]), int(words[4])
            local_forces = []
            for l in range(7, 14, 3):
                local_forces.append(float(words[l]))
            for l in range(25, 32, 3):
                local_forces.append(float(words[l]))
            angle_dict_gene[(i, j, k)] = np.array( local_forces )

    f_angle_cafe_all = []
    f_angle_gene_all = []
    f_angle_diff_all = []
    for pair, f_angle_cafe in angle_dict_cafe.items():
        f_angle_cafe_all.append(f_angle_cafe)
        f_angle_gene = angle_dict_gene[pair]
        f_angle_gene_all.append(f_angle_gene)
        f_angle_diff_all.append(f_angle_cafe - f_angle_gene)
        
    f_angle_cafe_arr = np.array(f_angle_cafe_all)
    f_angle_gene_arr = np.array(f_angle_gene_all)
    f_angle_diff_arr = np.array(f_angle_diff_all)

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(2, 3, figsize=(20, 8), constrained_layout=True, sharex=True)
    X = [i for i in range(line_num)]
    for i in range(6):
        m, n = i // 3, i % 3
        ax[m, n].plot(X, f_angle_cafe_arr[:, i], ls="-",  lw=2.0, c="g", alpha=0.3)
        ax[m, n].plot(X, f_angle_gene_arr[:, i], ls="--", lw=1.0, c="r")
        ax[m, n].plot(X, f_angle_diff_arr[:, i], ls="-",  lw=2.0, c="k", alpha=1.0)

        ax_x_ticks = ax[m, n].get_xticks()
        ax[m, n].set_xticklabels(ax_x_ticks, fontsize=15)
        ax[m, n].set_xlabel("Angle index", fontsize=18)
        ax_y_ticks = ax[m, n].get_yticks()
        ax[m, n].set_yticklabels(ax_y_ticks, fontsize=15)
        ax[m, n].set_ylabel("$F_{{angle}}$", fontsize=18)

    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("angle_force_comparison.png", dpi=150)

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
