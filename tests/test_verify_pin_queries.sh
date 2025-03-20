#!/bin/bash
set -e

# Run simple checks when user pin is incorrect:
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "u0000 VerifyPIN_0.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "u0000 VerifyPIN_7.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.xml" "u0000 VerifyPIN_0.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.xml" "u0000 VerifyPIN_1_2_3_4_5_6.q" --nosummary
verifyta "./FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.xml" "u0000 VerifyPIN_7.q" --nosummary