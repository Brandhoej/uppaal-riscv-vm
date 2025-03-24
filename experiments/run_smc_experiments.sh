# Example: ./experiments/run_smc_experiments.sh "./experiments/results/smc"

#!/bin/bash
set -e

OUTPUT_DIR=$1
TIME=10000
SIMULATIONS=100000

for FAULT_MODEL in "ORC"; do
    BASE_DIRECTORY=$OUTPUT_DIR/VerifyPIN_0
    python3 ./fill.py "./FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --memory 64 --flips 1 --template ./experiments/1111_template.xml --output "$BASE_DIRECTORY/VerifyPIN_0-$FAULT_MODEL.xml" --fault_models $FAULT_MODEL
    python3 ./experiments/experiment_smc.py "./experiments/smc/pr_VerifyPIN_0.q" --model "$BASE_DIRECTORY/VerifyPIN_0-$FAULT_MODEL.xml" --output $BASE_DIRECTORY --time $TIME --simulations $SIMULATIONS

    for PROGRAM in \
        "VerifyPIN_1_HB" \
        "VerifyPIN_2_HB+FTL" \
        "VerifyPIN_3_HB+FTL+INL" \
        "VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC" \
        "VerifyPIN_5_HB+FTL+DPTC+DC" \
        "VerifyPIN_6_HB+FTL+INL+DPTC+DT" \
        "VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC"; do
        BASE_DIRECTORY=$OUTPUT_DIR/$PROGRAM
        python3 ./fill.py "./FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/$PROGRAM.asm" --memory 64 --flips 1 --template ./experiments/1111_template.xml --output "$BASE_DIRECTORY/$PROGRAM-$FAULT_MODEL.xml" --fault_models $FAULT_MODEL
        python3 ./experiments/experiment_smc.py "./experiments/smc/pr_VerifyPIN_1_2_3_4_5_6_7.q" --model "$BASE_DIRECTORY/$PROGRAM-$FAULT_MODEL.xml" --output $BASE_DIRECTORY --time $TIME --simulations $SIMULATIONS
    done
done
