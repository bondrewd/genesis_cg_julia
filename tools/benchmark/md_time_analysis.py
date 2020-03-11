#!/usr/bin/env python

import glob
import argparse
import numpy as np

def main(log_dir, verbose):
    if verbose:
        print("Geting information from ", log_dir)

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
                    run_pairlist_time_all.append(float(words[2]))
                elif words[0] == "bond" and words[1] == "=":
                    run_bond_time_all.append(float(words[2]))
                elif words[0] == "angle" and words[1] == "=":
                    run_angle_time_all.append(float(words[2]))
                elif words[0] == "dihedral" and words[1] == "=":
                    run_dihedral_time_all.append(float(words[2]))
                elif line[7:20] == "base stacking" and words[2] == "=":
                    run_base_stacking_time_all.append(float(words[3]))
                elif words[0] == "nonbond" and words[1] == "=":
                    run_nonbond_time_all.append(float(words[2]))
                elif line[7:16] == "CG DNA bp" and words[3] == "=":
                    run_CG_DNA_bp_time_all.append(float(words[4]))
                elif line[7:17] == "CG DNA exv" and words[3] == "=":
                    run_CG_DNA_exv_time_all.append(float(words[4]))
                elif line[7:13] == "CG ele" and words[2] == "=":
                    run_CG_ele_time_all.append(float(words[3]))
                elif line[7:16] == "CG PWMcos" and words[2] == "=":
                    run_CG_PWMcos_time_all.append(float(words[3]))
                else:
                    pass
            # local simulation time estimation
            if tot_time == 0:
                print("WARNING: ", filename, " total simulation time == 0!!!")
            else:
                sim_time_per_day = ( time_step / 1000 ) * md_steps / tot_time * 86400
                sim_time_per_day_all.append(sim_time_per_day)

    # ====================================
    # compute averages and standard errors
    # ====================================
    def calc_averages(data_arr):
        if len(data_arr) > 0:
            arra = np.array(data_arr)
            arra_mean = np.mean(arra)
            arra_std  = np.std(arra)
            return (arra_mean, arra_std)
        else:
            return (0, 0)

    print("============================================================")
    total_time_mean , total_time_std = calc_averages(run_total_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(total_time_mean, total_time_std, "Total"))
    energy_time_mean , energy_time_std = calc_averages(run_energy_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(energy_time_mean, energy_time_std, "Energy"))
    integrator_time_mean , integrator_time_std = calc_averages(run_integrator_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(integrator_time_mean, integrator_time_std, "Integrator"))
    pairlist_time_mean , pairlist_time_std = calc_averages(run_pairlist_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(pairlist_time_mean, pairlist_time_std, "Pairlist"))

    print("------------------------------------------------------------")
    bond_time_mean , bond_time_std = calc_averages(run_bond_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(bond_time_mean, bond_time_std, "Bond"))
    angle_time_mean , angle_time_std = calc_averages(run_angle_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(angle_time_mean, angle_time_std, "Angle"))
    dihedral_time_mean , dihedral_time_std = calc_averages(run_dihedral_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(dihedral_time_mean, dihedral_time_std, "Dihedral"))
    base_stacking_time_mean , base_stacking_time_std = calc_averages(run_base_stacking_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(base_stacking_time_mean, base_stacking_time_std, "BStacking"))
    print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    nonbond_time_mean , nonbond_time_std = calc_averages(run_nonbond_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(nonbond_time_mean, nonbond_time_std, "Nonbond"))
    CG_DNA_bp_time_mean , CG_DNA_bp_time_std = calc_averages(run_CG_DNA_bp_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(CG_DNA_bp_time_mean, CG_DNA_bp_time_std, "CG_DNA_Bp"))
    CG_DNA_exv_time_mean , CG_DNA_exv_time_std = calc_averages(run_CG_DNA_exv_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(CG_DNA_exv_time_mean, CG_DNA_exv_time_std, "CG_DNA_Exv"))
    CG_ele_time_mean , CG_ele_time_std = calc_averages(run_CG_ele_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(CG_ele_time_mean, CG_ele_time_std, "CG_ele"))
    CG_PWMcos_time_mean , CG_PWMcos_time_std = calc_averages(run_CG_PWMcos_time_all)
    print("{2:>12s} time = {0:>18.3f} +- {1:>12.3f} ".format(CG_PWMcos_time_mean, CG_PWMcos_time_std, "CG_PWMcos"))
    print("------------------------------------------------------------")


    print("------------------------------------------------------------")
    stpd_m, stpd_s = calc_averages(sim_time_per_day_all)
    print(" Estimated computational efficiency: {0:>8.3f} +- {1:>4.3f} ns/day.".format(stpd_m, stpd_s))
    print("============================================================")


if __name__ == '__main__':
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Analyze MD simulation time from GENESIS log files.')
        parser.add_argument('log_dir', type=str, help="Directory of the log files.")
        parser.add_argument('-v', '--verbose', help="Output more information", action="store_true")
        return parser.parse_args()

    args = parse_arguments()
    main(args.log_dir, args.verbose)
