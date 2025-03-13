#!/bin/bash
set -e

# UserPIN=0000
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml"
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm" --template ./template.xml --output "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml"

# UserPIN=1234
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml"
python3 ./fill.py "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm" --template ./template.xml --output "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml"


# Run verifyta tautology on them for sanity check (output only error)
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "tautology.q"  > /dev/null
verifyta "./FISSC/u1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "tautology.q"  > /dev/null