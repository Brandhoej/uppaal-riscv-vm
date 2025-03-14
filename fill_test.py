import unittest
import re
import subprocess

from fill import RISCVProgram

class TestRISCVProgramParse(unittest.TestCase):
    def test_symbol_size(self):
        self.assertEqual(RISCVProgram.symbol_size(['.zero 2']), 2)
        self.assertEqual(RISCVProgram.symbol_size(['.byte 2']), 1)
        self.assertEqual(RISCVProgram.symbol_size(['.half 32']), 2)
        self.assertEqual(RISCVProgram.symbol_size(['.word 5']), 4)
        self.assertEqual(RISCVProgram.symbol_size(['.word 32', '.word 0']), 8)
        self.assertEqual(RISCVProgram.symbol_size(['.string "\001\002\003"']), 4)
        self.assertEqual(RISCVProgram.symbol_size(['.string "\001\002"', '.zero 1']), 4)

    def test_is_instruction(self):
        self.assertTrue(RISCVProgram.is_instruction('addi sp,sp,-32'))
        self.assertFalse(RISCVProgram.is_instruction('.zero 1'))
        self.assertFalse(RISCVProgram.is_instruction('.byte 123'))
        self.assertFalse(RISCVProgram.is_instruction('.ascii "\001\002\003\004"'))

    def test_operand_pattern(self):
        pattern = r"\(?([+-]?\d+|[a-zA-Z_]\w*)\)?"
        
        groups = re.findall(pattern, '(g_authenticated)(a5)')
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0], 'g_authenticated')
        self.assertEqual(groups[1], 'a5')
        
        groups = re.findall(pattern, '(-20)sp')
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0], '-20')
        self.assertEqual(groups[1], 'sp')
        
        groups = re.findall(pattern, '-24(s0)')
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0], '-24')
        self.assertEqual(groups[1], 's0')

    def test_generated_memory_initialisation(self):
        program = RISCVProgram([('g_ptc', ['.word 32'])], [], 0)
        generated_memory_initialisation = (
            'memory[0] = 32; // 0\'it byte of g_ptc',
            'memory[1] = 0; // 1\'it byte of g_ptc',
            'memory[2] = 0; // 2\'it byte of g_ptc',
            'memory[3] = 0; // 3\'it byte of g_ptc',
        )
        self.assertEqual(program.generated_memory_initialisation(), '\n'.join(generated_memory_initialisation))

        program = RISCVProgram([('g_ptc', ['.word -1430532899'])], [])
        generated_memory_initialisation = (
            'memory[0] = 221; // 0\'it byte of g_ptc',
            'memory[1] = 204; // 1\'it byte of g_ptc',
            'memory[2] = 187; // 2\'it byte of g_ptc',
            'memory[3] = 170; // 3\'it byte of g_ptc',
        )
        self.assertEqual(program.generated_memory_initialisation(), '\n'.join(generated_memory_initialisation))

        program = RISCVProgram([('g_ptc', ['.ascii "\001\002\003\004"'])], [])
        generated_memory_initialisation = (
            'memory[0] = 1; // 0\'it byte of g_ptc',
            'memory[1] = 2; // 1\'it byte of g_ptc',
            'memory[2] = 3; // 2\'it byte of g_ptc',
            'memory[3] = 4; // 3\'it byte of g_ptc',
        )
        self.assertEqual(program.generated_memory_initialisation(), '\n'.join(generated_memory_initialisation))

        program = RISCVProgram([
            ('g_ptc', ['.word 32', '.word 0']),
            ('g_authenticated', ['.byte 2']),
            ('g_cardPin', ['.ascii "\001\002\003\004"']),
            ('g_userPin', ['.string "\001"', '.zero 2']),
            ('g_ptc', ['.half 1000']),
            ('g_userPin', ['.string "\001\002\003"']),
        ], [])
        generated_memory_initialisation = (
            'memory[0] = 32; // 0\'it byte of g_ptc',
            'memory[1] = 0; // 1\'it byte of g_ptc',
            'memory[2] = 0; // 2\'it byte of g_ptc',
            'memory[3] = 0; // 3\'it byte of g_ptc',
            'memory[4] = 0; // 4\'it byte of g_ptc',
            'memory[5] = 0; // 5\'it byte of g_ptc',
            'memory[6] = 0; // 6\'it byte of g_ptc',
            'memory[7] = 0; // 7\'it byte of g_ptc',
            'memory[8] = 2; // 0\'it byte of g_authenticated',
            'memory[9] = 1; // 0\'it byte of g_cardPin',
            'memory[10] = 2; // 1\'it byte of g_cardPin',
            'memory[11] = 3; // 2\'it byte of g_cardPin',
            'memory[12] = 4; // 3\'it byte of g_cardPin',
            'memory[13] = 1; // 0\'it byte of g_userPin',
            'memory[14] = 0; // 1\'it byte of g_userPin',
            'memory[15] = 0; // 2\'it byte of g_userPin',
            'memory[16] = 0; // 3\'it byte of g_userPin',
            'memory[17] = 232; // 0\'it byte of g_ptc',
            'memory[18] = 3; // 1\'it byte of g_ptc',
            'memory[19] = 1; // 0\'it byte of g_userPin',
            'memory[20] = 2; // 1\'it byte of g_userPin',
            'memory[21] = 3; // 2\'it byte of g_userPin',
            'memory[22] = 0; // 3\'it byte of g_userPin',
        )
        self.assertEqual(program.generated_memory_initialisation(), '\n'.join(generated_memory_initialisation))

    def test_parse_operand(self):
        self.assertEqual(RISCVProgram.parse_operand(''), [''])
        self.assertEqual(RISCVProgram.parse_operand('ra'), ['ra'])
        self.assertEqual(RISCVProgram.parse_operand('0xff'), ['255'])
        self.assertEqual(RISCVProgram.parse_operand('-32'), ['-32'])
        self.assertEqual(RISCVProgram.parse_operand('(-20)sp'), ['sp', '-20'])
        self.assertEqual(RISCVProgram.parse_operand('%lo(g_authenticated)(a5)'), ['a5', 'symbol_low(g_authenticated)'])

    def test_parse_operands(self):
        self.assertEqual(RISCVProgram.parse_operands([]), ('', '', ''))
        self.assertEqual(RISCVProgram.parse_operands(['sp', 'sp', '-32']), ('sp', 'sp', '-32'))
        self.assertEqual(RISCVProgram.parse_operands(['zero', '%lo(g_authenticated)(a5)']), ('zero', 'a5', 'symbol_low(g_authenticated)'))
        self.assertEqual(RISCVProgram.parse_operands(['a5', '-24(s0)']), ('a5', 's0', '-24'))

    def test_parse_instruction(self):
        self.assertEqual(RISCVProgram.parse_instruction('j .L3'), ('J_CODE', 'L3', '', ''))

    def test_parse_segments_verify_pin_0(self):
        path = "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm"
        (segments, assertions) = RISCVProgram.parse_segments(path)
        self.assertEqual(len(segments), 12)
        self.assertEqual(len(assertions), 0)

        self.assertEqual(segments[0][0], 'g_ptc')
        self.assertEqual(len(segments[0][1]), 1)
        self.assertEqual(segments[0][1][0], '.byte 3')

        self.assertEqual(segments[1][0], 'g_authenticated')
        self.assertEqual(len(segments[1][1]), 1)
        self.assertEqual(segments[1][1][0], '.zero 1')
        
        self.assertEqual(segments[2][0], 'g_userPin')
        self.assertEqual(len(segments[2][1]), 1)
        self.assertEqual(segments[2][1][0], '.zero 4')
        
        self.assertEqual(segments[3][0], 'g_cardPin')
        self.assertEqual(len(segments[3][1]), 1)
        self.assertEqual(segments[3][1][0], '.ascii "\\001\\002\\003\\004"')

        self.assertEqual(segments[4][0], 'verifyPIN')
        self.assertEqual(len(segments[4][1]), 19)
        
        self.assertEqual(segments[5][0], 'L6')
        self.assertEqual(len(segments[5][1]), 11)
        
        self.assertEqual(segments[6][0], 'L4')
        self.assertEqual(len(segments[6][1]), 3)
        
        self.assertEqual(segments[7][0], 'L3')
        self.assertEqual(len(segments[7][1]), 4)
        
        self.assertEqual(segments[8][0], 'L5')
        self.assertEqual(len(segments[8][1]), 10)
        
        self.assertEqual(segments[9][0], 'L7')
        self.assertEqual(len(segments[9][1]), 11)
        
        self.assertEqual(segments[10][0], 'L2')
        self.assertEqual(len(segments[10][1]), 1)
        
        self.assertEqual(segments[11][0], 'L8')
        # We have commented the jr at the end ("- 1").
        self.assertEqual(len(segments[11][1]), 5 - 1)

    def test_parse_verify_pin_0(self):
        path = './FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm'
        program = RISCVProgram.parse(path, 0, 0)
    
        self.assertEqual(len(program.symbols), 4)

        (symbol, lines) = program.symbols[0]
        self.assertEqual(symbol, 'g_ptc')
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], '.byte 3')

        (symbol, lines) = program.symbols[1]
        self.assertEqual(symbol, 'g_authenticated')
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], '.zero 1')

        (symbol, lines) = program.symbols[2]
        self.assertEqual(symbol, 'g_userPin')
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], '.zero 4')

        (symbol, lines) = program.symbols[3]
        self.assertEqual(symbol, 'g_cardPin')
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], '.ascii "\\001\\002\\003\\004"')

        self.assertEqual(program.programs[0][0], 'verifyPIN')
        self.assertEqual(len(program.programs[0][1]), 19)

        self.assertEqual(program.programs[1][0], 'L6')
        self.assertEqual(len(program.programs[1][1]), 11)

        self.assertEqual(program.programs[2][0], 'L4')
        self.assertEqual(len(program.programs[2][1]), 3)

        self.assertEqual(program.programs[3][0], 'L3')
        self.assertEqual(len(program.programs[3][1]), 4)

        self.assertEqual(program.programs[4][0], 'L5')
        self.assertEqual(len(program.programs[4][1]), 10)

        self.assertEqual(program.programs[5][0], 'L7')
        self.assertEqual(len(program.programs[5][1]), 11)

        self.assertEqual(program.programs[6][0], 'L2')
        self.assertEqual(len(program.programs[6][1]), 1)

        self.assertEqual(program.programs[7][0], 'L8')
        # We have commented the jr at the end ("- 1").
        self.assertEqual(len(program.programs[7][1]), 5 - 1)

    def test_generated_verify_pin_2(self):
        path = './FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm'
        program = RISCVProgram.parse(path, 0, 0)

        program_length = 'const int32_t PROGRAM_LENGTH = 83;'
        self.assertEqual(program.generated_program_length(), program_length)

        labels = (
            "const pc_t verifyPIN = 0;\n"
            "const pc_t L5 = 24;\n"
            "const pc_t L4 = 35;\n"
            "const pc_t L3 = 38;\n"
            "const pc_t L6 = 48;\n"
            "const pc_t L7 = 54;\n"
            "const pc_t L8 = 56;\n"
            "const pc_t L10 = 67;\n"
            "const pc_t L2 = 78;\n"
            "const pc_t L11 = 79;"
        )
        self.assertEqual(program.generated_labels(), labels)

        globals = (
            "const address_t g_countermeasure = 0;\n"
            "const address_t g_ptc = 1;\n"
            "const address_t g_authenticated = 2;\n"
            "const address_t g_userPin = 3;\n"
            "const address_t g_cardPin = 7;"
        )
        self.assertEqual(program.generated_global_symbols(), globals)

        generated_memory_initialisation = (
            'memory[0] = 0; // 0\'it byte of g_countermeasure',
            'memory[1] = 3; // 0\'it byte of g_ptc',
            'memory[2] = 0; // 0\'it byte of g_authenticated',
            'memory[3] = 0; // 0\'it byte of g_userPin',
            'memory[4] = 0; // 1\'it byte of g_userPin',
            'memory[5] = 0; // 2\'it byte of g_userPin',
            'memory[6] = 0; // 3\'it byte of g_userPin',
            'memory[7] = 1; // 0\'it byte of g_cardPin',
            'memory[8] = 2; // 1\'it byte of g_cardPin',
            'memory[9] = 3; // 2\'it byte of g_cardPin',
            'memory[10] = 4; // 3\'it byte of g_cardPin',
        )
        self.assertEqual(program.generated_memory_initialisation(), '\n'.join(generated_memory_initialisation))

        instructions = (
            "instruction_t line_0 = { ADDI_CODE, sp, sp, -32 }; // verifyPIN",
            "instruction_t line_1 = { SW_CODE, ra, sp, 28 }; ",
            "instruction_t line_2 = { SW_CODE, s0, sp, 24 }; ",
            "instruction_t line_3 = { ADDI_CODE, s0, sp, 32 }; ",
            "instruction_t line_4 = { LUI_CODE, a5, symbol_high(g_authenticated), 0 }; ",
            "instruction_t line_5 = { LI_CODE, a4, 85, 0 }; ",
            "instruction_t line_6 = { SB_CODE, a4, a5, symbol_low(g_authenticated) }; ",
            "instruction_t line_7 = { LUI_CODE, a5, symbol_high(g_ptc), 0 }; ",
            "instruction_t line_8 = { LB_CODE, a5, a5, symbol_low(g_ptc) }; ",
            "instruction_t line_9 = { BLE_CODE, a5, zero, L2 }; ",
            "instruction_t line_10 = { LUI_CODE, a5, symbol_high(g_userPin), 0 }; ",
            "instruction_t line_11 = { ADDI_CODE, a5, a5, symbol_low(g_userPin) }; ",
            "instruction_t line_12 = { SW_CODE, a5, s0, -20 }; ",
            "instruction_t line_13 = { LUI_CODE, a5, symbol_high(g_cardPin), 0 }; ",
            "instruction_t line_14 = { ADDI_CODE, a5, a5, symbol_low(g_cardPin) }; ",
            "instruction_t line_15 = { SW_CODE, a5, s0, -24 }; ",
            "instruction_t line_16 = { LI_CODE, a5, 4, 0 }; ",
            "instruction_t line_17 = { SB_CODE, a5, s0, -25 }; ",
            "instruction_t line_18 = { LI_CODE, a5, 85, 0 }; ",
            "instruction_t line_19 = { SB_CODE, a5, s0, -26 }; ",
            "instruction_t line_20 = { LI_CODE, a5, 85, 0 }; ",
            "instruction_t line_21 = { SB_CODE, a5, s0, -27 }; ",
            "instruction_t line_22 = { SW_CODE, zero, s0, -32 }; ",
            "instruction_t line_23 = { J_CODE, L3, 0, 0 }; ",
            "instruction_t line_24 = { LW_CODE, a5, s0, -32 }; // L5",
            "instruction_t line_25 = { LW_CODE, a4, s0, -20 }; ",
            "instruction_t line_26 = { ADD_CODE, a5, a4, a5 }; ",
            "instruction_t line_27 = { LBU_CODE, a4, a5, 0 }; ",
            "instruction_t line_28 = { LW_CODE, a5, s0, -32 }; ",
            "instruction_t line_29 = { LW_CODE, a3, s0, -24 }; ",
            "instruction_t line_30 = { ADD_CODE, a5, a3, a5 }; ",
            "instruction_t line_31 = { LBU_CODE, a5, a5, 0 }; ",
            "instruction_t line_32 = { BEQ_CODE, a4, a5, L4 }; ",
            "instruction_t line_33 = { LI_CODE, a5, -86, 0 }; ",
            "instruction_t line_34 = { SB_CODE, a5, s0, -27 }; ",
            "instruction_t line_35 = { LW_CODE, a5, s0, -32 }; // L4",
            "instruction_t line_36 = { ADDI_CODE, a5, a5, 1 }; ",
            "instruction_t line_37 = { SW_CODE, a5, s0, -32 }; ",
            "instruction_t line_38 = { LBU_CODE, a5, s0, -25 }; // L3",
            "instruction_t line_39 = { LW_CODE, a4, s0, -32 }; ",
            "instruction_t line_40 = { BLT_CODE, a4, a5, L5 }; ",
            "instruction_t line_41 = { LBU_CODE, a5, s0, -25 }; ",
            "instruction_t line_42 = { LW_CODE, a4, s0, -32 }; ",
            "instruction_t line_43 = { BEQ_CODE, a4, a5, L6 }; ",
            "instruction_t line_44 = { LUI_CODE, a5, symbol_high(g_countermeasure), 0 }; ",
            "instruction_t line_45 = { LI_CODE, a4, 1, 0 }; ",
            "instruction_t line_46 = { SB_CODE, a4, a5, symbol_low(g_countermeasure) }; ",
            "instruction_t line_47 = { NOP_CODE, 0, 0, 0 }; ",
            "instruction_t line_48 = { LBU_CODE, a4, s0, -27 }; // L6",
            "instruction_t line_49 = { LI_CODE, a5, 85, 0 }; ",
            "instruction_t line_50 = { BNE_CODE, a4, a5, L7 }; ",
            "instruction_t line_51 = { LI_CODE, a5, -86, 0 }; ",
            "instruction_t line_52 = { SB_CODE, a5, s0, -26 }; ",
            "instruction_t line_53 = { J_CODE, L8, 0, 0 }; ",
            "instruction_t line_54 = { LI_CODE, a5, 85, 0 }; // L7",
            "instruction_t line_55 = { SB_CODE, a5, s0, -26 }; ",
            "instruction_t line_56 = { LBU_CODE, a4, s0, -26 }; // L8",
            "instruction_t line_57 = { LI_CODE, a5, 170, 0 }; ",
            "instruction_t line_58 = { BNE_CODE, a4, a5, L10 }; ",
            "instruction_t line_59 = { LUI_CODE, a5, symbol_high(g_ptc), 0 }; ",
            "instruction_t line_60 = { LI_CODE, a4, 3, 0 }; ",
            "instruction_t line_61 = { SB_CODE, a4, a5, symbol_low(g_ptc) }; ",
            "instruction_t line_62 = { LUI_CODE, a5, symbol_high(g_authenticated), 0 }; ",
            "instruction_t line_63 = { LI_CODE, a4, -86, 0 }; ",
            "instruction_t line_64 = { SB_CODE, a4, a5, symbol_low(g_authenticated) }; ",
            "instruction_t line_65 = { LI_CODE, a5, 170, 0 }; ",
            "instruction_t line_66 = { J_CODE, L11, 0, 0 }; ",
            "instruction_t line_67 = { LUI_CODE, a5, symbol_high(g_ptc), 0 }; // L10",
            "instruction_t line_68 = { LB_CODE, a5, a5, symbol_low(g_ptc) }; ",
            "instruction_t line_69 = { ANDI_CODE, a5, a5, 255 }; ",
            "instruction_t line_70 = { ADDI_CODE, a5, a5, -1 }; ",
            "instruction_t line_71 = { ANDI_CODE, a5, a5, 255 }; ",
            "instruction_t line_72 = { SLLI_CODE, a4, a5, 24 }; ",
            "instruction_t line_73 = { SRAI_CODE, a4, a4, 24 }; ",
            "instruction_t line_74 = { LUI_CODE, a5, symbol_high(g_ptc), 0 }; ",
            "instruction_t line_75 = { SB_CODE, a4, a5, symbol_low(g_ptc) }; ",
            "instruction_t line_76 = { LI_CODE, a5, 85, 0 }; ",
            "instruction_t line_77 = { J_CODE, L11, 0, 0 }; ",
            "instruction_t line_78 = { LI_CODE, a5, 85, 0 }; // L2",
            "instruction_t line_79 = { MV_CODE, a0, a5, 0 }; // L11",
            "instruction_t line_80 = { LW_CODE, ra, sp, 28 }; ",
            "instruction_t line_81 = { LW_CODE, s0, sp, 24 }; ",
            "instruction_t line_82 = { ADDI_CODE, sp, sp, 32 }; ",
            "program[0] = line_0;",
            "program[1] = line_1;",
            "program[2] = line_2;",
            "program[3] = line_3;",
            "program[4] = line_4;",
            "program[5] = line_5;",
            "program[6] = line_6;",
            "program[7] = line_7;",
            "program[8] = line_8;",
            "program[9] = line_9;",
            "program[10] = line_10;",
            "program[11] = line_11;",
            "program[12] = line_12;",
            "program[13] = line_13;",
            "program[14] = line_14;",
            "program[15] = line_15;",
            "program[16] = line_16;",
            "program[17] = line_17;",
            "program[18] = line_18;",
            "program[19] = line_19;",
            "program[20] = line_20;",
            "program[21] = line_21;",
            "program[22] = line_22;",
            "program[23] = line_23;",
            "program[24] = line_24;",
            "program[25] = line_25;",
            "program[26] = line_26;",
            "program[27] = line_27;",
            "program[28] = line_28;",
            "program[29] = line_29;",
            "program[30] = line_30;",
            "program[31] = line_31;",
            "program[32] = line_32;",
            "program[33] = line_33;",
            "program[34] = line_34;",
            "program[35] = line_35;",
            "program[36] = line_36;",
            "program[37] = line_37;",
            "program[38] = line_38;",
            "program[39] = line_39;",
            "program[40] = line_40;",
            "program[41] = line_41;",
            "program[42] = line_42;",
            "program[43] = line_43;",
            "program[44] = line_44;",
            "program[45] = line_45;",
            "program[46] = line_46;",
            "program[47] = line_47;",
            "program[48] = line_48;",
            "program[49] = line_49;",
            "program[50] = line_50;",
            "program[51] = line_51;",
            "program[52] = line_52;",
            "program[53] = line_53;",
            "program[54] = line_54;",
            "program[55] = line_55;",
            "program[56] = line_56;",
            "program[57] = line_57;",
            "program[58] = line_58;",
            "program[59] = line_59;",
            "program[60] = line_60;",
            "program[61] = line_61;",
            "program[62] = line_62;",
            "program[63] = line_63;",
            "program[64] = line_64;",
            "program[65] = line_65;",
            "program[66] = line_66;",
            "program[67] = line_67;",
            "program[68] = line_68;",
            "program[69] = line_69;",
            "program[70] = line_70;",
            "program[71] = line_71;",
            "program[72] = line_72;",
            "program[73] = line_73;",
            "program[74] = line_74;",
            "program[75] = line_75;",
            "program[76] = line_76;",
            "program[77] = line_77;",
            "program[78] = line_78;",
            "program[79] = line_79;",
            "program[80] = line_80;",
            "program[81] = line_81;",
            "program[82] = line_82;"
        )
        self.assertEqual(program.generated_program(), '\n'.join(instructions))

    def test_parse_test_example_verify_pin_0(self):
        path = './test_examples/VerifyPIN_0.asm'
        program = RISCVProgram.parse(path, 0, 0)
        self.assertEqual(len(program.assertions), 1)

    def test_parse_verify_pins(self):
        files = [
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm', 4, 64 - 1),                             # VerifyPIN_0
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm', 5, 74 - 1),                          # VerifyPIN_1
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm', 5, 84 - 1),                      # VerifyPIN_2
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm', 5, 78 - 1 ),                 # VerifyPIN_3
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm', 5, 121 - 1),   # VerifyPIN_4
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm', 5, 139 - 1),             # VerifyPIN_5
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm', 5, 90 - 1),          # VerifyPIN_6
            ('./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm', 5, 186 - 1),      # VerifyPIN_7
        ]

        for (path, symbols, length) in files:
            program = RISCVProgram.parse(path, 0, 0)
            self.assertEqual(len(program.symbols), symbols)
            self.assertEqual(program.length, length)
    
    def test_fill_templates(self):
        subprocess.run('./fill_templates.sh')
        subprocess.run('./fill_test_examples.sh')

if __name__ == '__main__':
    unittest.main()