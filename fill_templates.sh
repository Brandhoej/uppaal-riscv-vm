#!/bin/bash
set -e

python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --pc 'verifyPIN' --memory 128 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm" --pc 'verifyPIN' --memory 128 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml"
python3 ./fill.py "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml"

python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml"
python3 ./fill.py "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm" --pc 'verifyPIN' --memory 64 --flips 0 --template ./template.xml --output "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml"

verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "./tests/done.q" > /dev/null

verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "./tests/done.q" > /dev/null
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "./tests/done.q" > /dev/null