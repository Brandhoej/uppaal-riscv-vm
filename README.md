# uppaal-riscv-vm

## Fill Template
```console
python3 ./fill.py -h
```

Example:
```console
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --memory 64 --flips 3 --template ./template.xml --output "./VerifyPIN_0.xml"
```

## Generating VerifyPIN Models
Requires _verifyta_ to be in the ``PATH``.
```console
./fill_templates.sh
```

## Test
Running the tests covers some of the parser and sanity checks for VerifyPIN examples.
```console
./test_linux.sh
```

## Experiments
VerifyTA must be a part of your PATH variable and set in the profile such that Python subprocess run can find the executable.
To run the experiments detached with a name one can run
```console
./experiments/nohup_run_experiment.sh <REQUIRED:EXPERIMENT_COMMAND> <OPTIONAL:PROCESS_NAME:DEFAULT("EXPERIMENT")> <OPTIONAL:LOG_OUTPUT_PATH> <$@:ADDITIONAL_EXPERIMENT_COMMAND_ARGS>

# Example (With loggin)
./experiments/nohup_run_experiment.sh "./experiments/run_smc_experiments_LARGE_ORC.sh" "SMC_LARGE" "SMC_LARGE.out" "./experiments/results/smc"
./experiments/nohup_run_experiment.sh "./experiments/run_symbolic_experiments.sh" "SYMBOLIC_EXPERIMENTS" "SYMBOLIC.out" "./experiments/results/symbolic"

# Example (Without logging)
./experiments/nohup_run_experiment.sh "./experiments/run_smc_experiments_LARGE_ORC.sh" "SMC_LARGE" "" "./experiments/results/smc"
```

If one wants to stop the experiment:
````console
./experiments/nohup_stop_experiment.sh <REQUIRED:EXPERIMENT_COMMAND>

# EXAMPLE
./experiments/nohup_stop_experiment.sh EXPERIMENT
```
