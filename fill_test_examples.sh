#!/bin/bash
set -e

python3 ./fill.py "./test_examples/VerifyPIN_0.asm" --template ./template.xml --output "./test_examples/VerifyPIN_0.xml"

# Run verifyta tautology on them for sanity check (output only error)
verifyta "./test_examples/VerifyPIN_0.xml" "tautology.q"  > /dev/null