#!/bin/zsh

# ===========================================
# gather all the simulation time information
# ===========================================

if [[ -f all_in_one.log ]] 
then
    rm -f all_in_one.log
fi

for f in ../../md?_run_??.log
do
    # echo Reading $f ...
    tail -n 32 $f >> all_in_one.log
done

# =================
# Define a function
# =================
function calc_average {
    
    t_cnt=0;
    t_sum=0; 
    t_avg=0;
    t_sds=0;
    t_std=0;

    for i in $( grep $1 all_in_one.log | awk "{ print \$$2; }" )
    do
        t_sum=$(echo $t_sum + $i | bc )
        ((t_cnt++))
    done
    t_avg=$(echo "scale=3; $t_sum / $t_cnt" | bc)

    for i in $( grep $1 all_in_one.log | awk "{ print \$$2; }" )
    do
        t_sds=$(echo "scale=3; $t_sds + ($i-$t_avg) ^ 2" | bc )
    done
    t_std=$(echo "scale=3; sqrt($t_sds/( $t_cnt - 1 ))" | bc)

    echo $1 " : " $t_avg " +- " $t_std
   
}

# ========================
# extract simulation times
# ========================
calc_average "total time" 4
calc_average "energy" 3
calc_average "integrator" 3
calc_average "pairlist" 3

echo " ------------------------------"

calc_average "bond" 3
calc_average "angle" 3
calc_average "dihedral" 3
calc_average "base stacking" 4
calc_average "nonbond" 3

echo " ------------------------------"
calc_average "CG DNA bp" 5
calc_average "CG DNA exv" 5
calc_average "CG ele" 4
calc_average "CG PWMcos" 4
