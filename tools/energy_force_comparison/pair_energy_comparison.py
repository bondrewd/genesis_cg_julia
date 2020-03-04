#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(cafefile, genefile, line_num, output_option, func_type, cafe_col, gene_col ):
    pair_dict_cafe = {}
    pair_dict_gene = {}

    iline = 0
    with open(cafefile, "r") as cafin:
        for line in cafin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j = int(words[1]), int(words[2])
            pair_dict_cafe[(i, j)] = float(words[cafe_col])

    iline = 0
    with open(genefile, "r") as genin:
        for line in genin:
            iline += 1
            if iline > line_num:
                break
            words = line.split()
            i, j = int(words[1]), int(words[2])
            pair_dict_gene[(i, j)] = float(words[gene_col])

    e_pair_cafe_all = []
    e_pair_gene_all = []
    e_pair_diff_all = []
    for pair, e_pair_cafe in pair_dict_cafe.items():
        e_pair_cafe_all.append(e_pair_cafe)
        if pair in pair_dict_gene:
            e_pair_gene = pair_dict_gene[pair]
        else:
            e_pair_gene = 0
        e_pair_gene_all.append(e_pair_gene)
        e_pair_diff_all.append(e_pair_cafe - e_pair_gene)
        

    # ===========
    # plotting...
    # ===========
    fig, ax  = plt.subplots(1, 1, figsize=(9, 5), constrained_layout=True, sharex=True)
    X = [i for i in range(len(e_pair_cafe_all))]
    ax.plot(X, e_pair_cafe_all, ls="-",  lw=2.0, c="g", alpha=0.3)
    ax.plot(X, e_pair_gene_all, ls="--",  lw=1.0, c="r")
    ax.plot(X, e_pair_diff_all, ls="-", lw=2.0, c="k", alpha=1.0)

    ax_x_ticks = ax.get_xticks()
    ax.set_xticklabels([ int(x) for x in ax_x_ticks ], fontsize=15)
    ax.set_xlabel("Pair index", fontsize=18)
    ax_y_ticks = ax.get_yticks()
    ax.set_yticklabels([ round(y, 2) for y in ax_y_ticks ], fontsize=15)
    ax.set_ylabel(r"$E_{{pair}}$ (kcal/mol)", fontsize=18)

    if output_option == 0:
        plt.show()
    elif output_option == 1:
        plt.savefig("pair_energy_comparison_{0}.png".format(func_type), dpi=150)

if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Compare energy/force output.')

        parser.add_argument('-c', '--cafemol', required=True, type=str)
        parser.add_argument('-g', '--genesis', required=True, type=str)
        parser.add_argument('-n', '--num',     required=True, type=int)
        parser.add_argument('-t', '--type',    required=False, type=str, default="pair")
        parser.add_argument('-i', '--col1',    required=True, type=int)
        parser.add_argument('-j', '--col2',    required=True, type=int)
        parser.add_argument('-o', '--out',     required=False, type=int, default=0)
        
        return parser.parse_args()

    args = parse_arguments()

    main(args.cafemol, args.genesis, args.num, args.out, args.type, args.col1, args.col2)
