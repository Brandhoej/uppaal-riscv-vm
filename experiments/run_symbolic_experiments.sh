# Example: ./experiments/run_symbolic_experiments.sh "./experiments/results/symbolic"

#!/bin/bash
set -e

OUTPUT_DIR=$1
COOLDOWN=100
MEMORY=64

for FLIPS in 1 2 3 4 5; do
    for FAULT_MODEL in "ORC" "IS" "SC"; do
        BASE_DIRECTORY="$OUTPUT_DIR/VerifyPIN_0"
        QUERY_OUTPUT="$BASE_DIRECTORY/VerifyPIN_0--F$FLIPS-C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--query.q"
        LOG_OUTPUT="$BASE_DIRECTORY/VerifyPIN_0--F$FLIPS-C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--verifyta.log"
        MODEL_PATH="$BASE_DIRECTORY/VerifyPIN_0--F$FLIPS-C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL.xml"

        python3 ./fill.py "./FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --memory $MEMORY --flips $FLIPS --template ./experiments/1111_template.xml --output $MODEL_PATH --fault_models $FAULT_MODEL --cooldown $COOLDOWN
        python3 ./experiments/experiment_symbolic.py "./experiments/symbolic/VerifyPIN_0.q" --model $MODEL_PATH --query-output $QUERY_OUTPUT --log-output $LOG_OUTPUT

        for PROGRAM in \
            "VerifyPIN_1_HB" \
            "VerifyPIN_2_HB+FTL" \
            "VerifyPIN_3_HB+FTL+INL" \
            "VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC" \
            "VerifyPIN_5_HB+FTL+DPTC+DC" \
            "VerifyPIN_6_HB+FTL+INL+DPTC+DT" \
            "VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC"; do
            BASE_DIRECTORY="$OUTPUT_DIR/$PROGRAM"
            QUERY_OUTPUT="$BASE_DIRECTORY/$PROGRAM--F$FLIPS--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--query.q"
            LOG_OUTPUT="$BASE_DIRECTORY/$PROGRAM--F$FLIPS--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL--verifyta.log"
            MODEL_PATH="$BASE_DIRECTORY/$PROGRAM--F$FLIPS--C$COOLDOWN--T$TIME--N$SIMULATIONS--$FAULT_MODEL.xml"
            python3 ./fill.py "./FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/$PROGRAM.asm" --memory $MEMORY --flips $FLIPS --template ./experiments/1111_template.xml --output $MODEL_PATH --fault_models $FAULT_MODEL --cooldown $COOLDOWN
            python3 ./experiments/experiment_symbolic.py "./experiments/symbolic/VerifyPIN_1_2_3_4_5_6_7.q" --model $MODEL_PATH --query-output $QUERY_OUTPUT --log-output $LOG_OUTPUT
        done
    done
done
