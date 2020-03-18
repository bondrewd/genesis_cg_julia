#!/usr/bin/env python

import glob
import argparse
import numpy as np
import os
import re
import matplotlib.pyplot as plt

def main(log_dir, verbose):
    if verbose:
        print("Geting information from ", log_dir)

    run_simu_name = []
    run_simu_name_index = []
    
    run_simulation_time     = []
    run_total_time_all      = []
    run_energy_time_all     = []
    run_integrator_time_all = []
    run_pairlist_time_all   = []

    run_bond_time_all          = []
    run_angle_time_all         = []
    run_dihedral_time_all      = []
    run_base_stacking_time_all = []
    run_nonbond_time_all       = []
    run_CG_DNA_bp_time_all     = []
    run_CG_DNA_exv_time_all    = []
    run_CG_ele_time_all        = []
    run_CG_PWMcos_time_all     = []

    sim_time_per_day_all = []

    for filename in glob.glob(log_dir + "*.log"):
        if verbose:
            print("Analyzing ", filename, " ...")
        m = re.search(r"mpi([0-9]*)_r([0-9]{2})", filename)
        mpinum = int(m[1])
        runnum = int(m[2])
        run_simu_name.append("m{0:0>2d}-r{1:0>2d}".format(mpinum, runnum))
        run_simu_name_index.append(100*mpinum + runnum)
        with open(filename, "r") as fin:
            time_step = 0
            md_steps = 0
            tot_time = 0
            for line in fin:
                words = line.split()
                if len(words) < 2:
                    continue
                if line.startswith("INFO:") and words[1] != "STEP":
                    md_steps = int(words[1])
                if words[0] == "dynamics" and words[1] == "=":
                    tot_time = float(words[2])
                    run_total_time_all.append(tot_time)
                elif words[0] == "timestep" and words[1] == "=":
                    time_step = float(words[2])
                elif words[0] == "energy" and words[1] == "=":
                    run_energy_time_all.append(float(words[2]))
                elif words[0] == "integrator" and words[1] == "=" and len(words) == 3:
                    run_integrator_time_all.append(float(words[2]))
                elif words[0] == "pairlist" and words[1] == "=":
                    run_pairlist_time_all.append( (float(words[2]), float(words[4][:-1]), float(words[5][:-1])) )
                elif words[0] == "bond" and words[1] == "=":
                    run_bond_time_all.append( (float(words[2]), float(words[4][:-1]), float(words[5][:-1])) )
                elif words[0] == "angle" and words[1] == "=":
                    run_angle_time_all.append( (float(words[2]), float(words[4][:-1]), float(words[5][:-1])) )
                elif words[0] == "dihedral" and words[1] == "=":
                    run_dihedral_time_all.append( (float(words[2]), float(words[4][:-1]), float(words[5][:-1])) )
                elif line[4:17] == "base stacking" and words[2] == "=":
                    run_base_stacking_time_all.append( (float(words[3]), float(words[5][:-1]), float(words[6][:-1])) )
                elif words[0] == "nonbond" and words[1] == "=":
                    run_nonbond_time_all.append( (float(words[2]), float(words[4][:-1]), float(words[5][:-1])) )
                elif line[6:15] == "CG DNA bp" and words[3] == "=":
                    run_CG_DNA_bp_time_all.append( (float(words[4]), float(words[6][:-1]), float(words[7][:-1])) )
                elif line[6:16] == "CG DNA exv" and words[3] == "=":
                    run_CG_DNA_exv_time_all.append( (float(words[4]), float(words[6][:-1]), float(words[7][:-1])) )
                elif line[6:12] == "CG ele" and words[2] == "=":
                    run_CG_ele_time_all.append( (float(words[3]), float(words[5][:-1]), float(words[6][:-1])) )
                elif line[6:15] == "CG PWMcos" and words[2] == "=":
                    run_CG_PWMcos_time_all.append( (float(words[3]), float(words[5][:-1]), float(words[6][:-1])) )
                else:
                    pass
            # local simulation time estimation
            if tot_time == 0:
                print("WARNING: ", filename, " total simulation time == 0!!!")
            else:
                sim_time_per_day = ( time_step / 1000 ) * md_steps / tot_time * 86400
                sim_time_per_day_all.append(sim_time_per_day)
                run_simulation_time.append(md_steps)


    # =====================
    # pick out output terms
    # =====================
    termnames = ["run", "total",
                 "energy", "integrat",
                 "pairlist ( min , max )",
                 "bond ( min , max )",
                 "angle ( min , max )",
                 "dihedral ( min , max )"]
    data_all_in_one = [run_total_time_all, run_energy_time_all, run_integrator_time_all, run_pairlist_time_all,
                       run_bond_time_all, run_angle_time_all, run_dihedral_time_all]
    if sum(run_base_stacking_time_all[0]) > 0:
        termnames.append("bs ( min , max )")
        data_all_in_one.append(run_base_stacking_time_all)
    if sum(run_nonbond_time_all[0]) > 0:
        termnames.append("nonbond ( min , max )")
        data_all_in_one.append(run_nonbond_time_all)
    if sum(run_CG_DNA_bp_time_all[0]) > 0:
        termnames.append("bp ( min , max )")
        data_all_in_one.append(run_CG_DNA_bp_time_all)
    if sum(run_CG_DNA_exv_time_all[0]) > 0:
        termnames.append("DNA_exv ( min , max )")
        data_all_in_one.append(run_CG_DNA_exv_time_all)
    if sum(run_CG_ele_time_all[0]) > 0:
        termnames.append("ele ( min , max )")
        data_all_in_one.append(run_CG_ele_time_all)
    if sum(run_CG_PWMcos_time_all[0]) > 0:
        termnames.append("PWMcos ( min , max )")
        data_all_in_one.append(run_CG_PWMcos_time_all)
    termnames.append("estimate")
    data_all_in_one.append(sim_time_per_day_all)

    # ======
    # output
    # ======
    of = open("benchmark_list.md", "w")
    of.write("|")
    for name in termnames[:4]:
        of.write(" {0:8s} |".format(name))
    for name in termnames[4:-1]:
        of.write(" {0:32s} |".format(name))
    of.write(" {0:8s} |".format("estimate"))
    of.write("\n")
    of.write("|")
    for name in termnames[:4]:
        of.write("----------|")
    for name in termnames[4:-1]:
        of.write("----------------------------------|")
    of.write("----------|")
    of.write("\n")

    for run_name_index in sorted( run_simu_name_index ):
        i = run_simu_name_index.index(run_name_index)
        of.write("| {0:8s} |".format(run_simu_name[i]))
        for data in data_all_in_one[:3]:
            of.write(" {0:8.3f} |".format(data[i]))
        for data in data_all_in_one[3:-1]:
            of.write(" {0:8.3f} ( {1:8.3f} , {2:8.3f} ) |".format(data[i][0], data[i][1], data[i][2]))
        of.write(" {0:8.3f} |".format(data_all_in_one[-1][i]))
        of.write("\n")

    of.close()

    # ===========
    # Plotting...
    # ===========
    num_subfigs = len(data_all_in_one) - 1

    # determine MPI number list
    mpi_num_list = []
    for n in sorted( run_simu_name_index ):
        mn = n // 100
        if mn not in mpi_num_list:
            mpi_num_list.append(mn)

    # find the best profile
    plot_run_index = []
    for m in mpi_num_list:
        indx_list = []
        time_list = []
        for i, n in enumerate(  run_simu_name_index ):
            if n // 100 == m :
                indx_list.append(i)
                time_list.append(sim_time_per_day_all[i])
        z = [x for _, x in sorted(zip(time_list, indx_list))]
        plot_run_index.append(z[2])

    # make figure
    fig, axes = plt.subplots(num_subfigs // 2, 2, figsize=(9, 2 * num_subfigs // 2), constrained_layout=True, sharex=True, sharey=False)
    X = mpi_num_list[:]

    # energy and integrator
    for i in [0, 1]:
        Y = []
        for j in plot_run_index:
            Y.append(data_all_in_one[i+1][j])
        axes[i//2, i%2].plot(X, Y, ls="--", marker="o", lw=1.0)
        axes[i//2, i%2].set_title(termnames[i+2])

    # Detailed energy terms
    for i in range(2, num_subfigs - 1):
        Y = []
        y_min = []
        y_max = []
        for j in plot_run_index:
            Y.append(data_all_in_one[i+1][j][0])
            y_min.append(data_all_in_one[i+1][j][0] - data_all_in_one[i+1][j][1])
            y_max.append(data_all_in_one[i+1][j][2] - data_all_in_one[i+1][j][0])
        y_err = np.array([y_min, y_max])
        axes[i//2, i%2].errorbar(X, Y, yerr=y_err, ls="--", marker="o", capsize=5, lw=1.0)
        axes[i//2, i%2].set_title(termnames[i+2])

    # estimated time
    Y = []
    for j in plot_run_index:
        Y.append(sim_time_per_day_all[j])
    i = num_subfigs - 1
    axes[i//2, i%2].plot(X, Y, ls="--", marker="o", lw=1.0)

    for i in range(num_subfigs):
        yticks = axes[i//2, i%2].get_yticks()
        axes[i//2, i%2].set_xscale("log")
        axes[i//2, i%2].set_xticks(X)
        axes[i//2, i%2].set_xticklabels(X, fontsize=12)
        axes[i//2, i%2].set_yticklabels([round( y, 3 ) for y in yticks], fontsize=12)
        axes[i//2, i%2].set_ylabel("cpu time (s)", fontsize=14)
        axes[i//2, i%2].grid(axis="y", ls="-", color="black", alpha=0.2)
    i = num_subfigs - 1
    axes[i//2, i%2].set_ylabel("speed (ns/day)", fontsize=14)

    plt.savefig("benchmark_plots.png", dpi=150)


if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Analyze MD simulation time from GENESIS log files.')
        parser.add_argument('log_dir', type=str, help="Directory of the log files.")
        parser.add_argument('-v', '--verbose', help="Output more information", action="store_true")
        return parser.parse_args()

    args = parse_arguments()
    main(args.log_dir, args.verbose)
