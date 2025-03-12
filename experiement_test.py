import unittest
import re

from experiment import RISCVProgram

class TestRISCVProgramParse(unittest.TestCase):
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

    def test_parse_operand(self):
        self.assertEqual(RISCVProgram.parse_operand(''), [''])
        self.assertEqual(RISCVProgram.parse_operand('ra'), ['ra'])
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
        path = "./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm"
        segments = RISCVProgram.parse_segments(path)
        self.assertEqual(len(segments), 12)

        self.assertEqual(segments[0][0], 'g_ptc')
        self.assertEqual(len(segments[0][1]), 1)
        self.assertEqual(segments[0][1][0], '.zero 1')

        self.assertEqual(segments[1][0], 'g_authenticated')
        self.assertEqual(len(segments[1][1]), 1)
        self.assertEqual(segments[1][1][0], '.zero 1')
        
        self.assertEqual(segments[2][0], 'g_userPin')
        self.assertEqual(len(segments[2][1]), 1)
        self.assertEqual(segments[2][1][0], '.zero 4')
        
        self.assertEqual(segments[3][0], 'g_cardPin')
        self.assertEqual(len(segments[3][1]), 1)
        self.assertEqual(segments[3][1][0], '.zero 4')

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
        self.assertEqual(len(segments[11][1]), 5)

    def test_parse_verify_pin_0(self):
        path = './FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm'
        program = RISCVProgram.parse(path)
    
        self.assertEqual(len(program.symbols), 4)

        (symbol, length, init) = program.symbols[0]
        self.assertEqual(symbol, 'g_ptc')
        self.assertEqual(length, 1)
        self.assertEqual(init, '.zero')

        (symbol, length, init) = program.symbols[1]
        self.assertEqual(symbol, 'g_authenticated')
        self.assertEqual(length, 1)
        self.assertEqual(init, '.zero')

        (symbol, length, init) = program.symbols[2]
        self.assertEqual(symbol, 'g_userPin')
        self.assertEqual(length, 4)
        self.assertEqual(init, '.zero')

        (symbol, length, init) = program.symbols[3]
        self.assertEqual(symbol, 'g_cardPin')
        self.assertEqual(length, 4)
        self.assertEqual(init, '.zero')

        self.assertEqual(program.symbols_memory, 10)

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
        self.assertEqual(len(program.programs[7][1]), 5)

    def test_generated_verify_pin_2(self):
        path = './FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm'
        program = RISCVProgram.parse(path)

        program_length = 'const int32_t PROGRAM_LENGTH = 84;'
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
        self.assertEqual(program.generated_globals(), globals)
        self.assertEqual(program.symbols_memory, 11)

        instructions = (
        )
        print(program.generated_program())
        self.assertEqual(program.generated_program(), instructions)

    def test_parse_verify_pins(self):
        files = [
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm', 4, 64 ),                          # VerifyPIN_0
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm', 5, 74 ),                       # VerifyPIN_1
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm', 5, 84 ),                   # VerifyPIN_2
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm', 5, 78 ),               # VerifyPIN_3
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm', 5, 121), # VerifyPIN_4
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm', 5, 139),           # VerifyPIN_5
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm', 5, 90 ),       # VerifyPIN_6
            ('./FISSC/INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm', 5, 186),    # VerifyPIN_7
        ]

        for (path, symbols, length) in files:
            program = RISCVProgram.parse(path)
            self.assertEqual(len(program.symbols), symbols)
            self.assertEqual(program.length, length)
    
if __name__ == '__main__':
    unittest.main()