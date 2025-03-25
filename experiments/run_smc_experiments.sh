# Example: ./experiments/run_smc_experiments.sh "./experiments/results/smc"

#!/bin/bash
set -e
set -x

OUTPUT_DIR=$1
TIME=10000
SIMULATIONS=2500000
COOLDOWN=10

for FAULT_MODEL in "IS" "SC"; do
    BASE_DIRECTORY="./$OUTPUT_DIR/VerifyPIN_0"
    QUERY_OUTPUT="$BASE_DIRECTORY/VerifyPIN_0--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--query.q"
    LOG_OUTPUT="$BASE_DIRECTORY/VerifyPIN_0--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--verifyta.log"
    MODEL_PATH="$BASE_DIRECTORY/$PROGRAM--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL.xml"

    python3 ./fill.py "./FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --memory 64 --flips 1 --template ./experiments/1111_template.xml --output $MODEL_PATH --fault_models $FAULT_MODEL --cooldown $COOLDOWN
    python3 ./experiments/experiment_smc.py "./experiments/smc/pr_VerifyPIN_0.q" --model $MODEL_PATH --time $TIME --simulations $SIMULATIONS --query-output $QUERY_OUTPUT --log-output $LOG_OUTPUT

    for PROGRAM in \
        "VerifyPIN_1_HB" \
        "VerifyPIN_2_HB+FTL" \
        "VerifyPIN_3_HB+FTL+INL" \
        "VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC" \
        "VerifyPIN_5_HB+FTL+DPTC+DC" \
        "VerifyPIN_6_HB+FTL+INL+DPTC+DT" \
        "VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC"; do
        BASE_DIRECTORY="./$OUTPUT_DIR/$PROGRAM"
        QUERY_OUTPUT="$BASE_DIRECTORY/$PROGRAM--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--query.q"
        LOG_OUTPUT="$BASE_DIRECTORY/$PROGRAM--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--verifyta.log"
        MODEL_PATH="$BASE_DIRECTORY/$PROGRAM--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL.xml"
        python3 ./fill.py "./FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/$PROGRAM.asm" --memory 64 --flips 1 --template ./experiments/1111_template.xml --output $MODEL_PATH --fault_models $FAULT_MODEL --cooldown $COOLDOWN
        python3 ./experiments/experiment_smc.py "./experiments/smc/pr_VerifyPIN_1_2_3_4_5_6_7.q" --model $MODEL_PATH --time $TIME --simulations $SIMULATIONS --query-output $QUERY_OUTPUT --log-output $LOG_OUTPUT
    done
done
