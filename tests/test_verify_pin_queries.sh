#!/bin/bash
set -e

# None of the models has attacks and therefore all should end in vm.DONE.
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "./tests/done.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "./tests/done.q" --nosummary