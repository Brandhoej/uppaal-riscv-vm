import argparse
import re

from typing import Dict, List, Tuple, Optional

class RISCVProgram:
    __symbols: List[Tuple[str, int, str]]
    """Dictionary mapping global symbol identifiers to memory offsets and size.
    
    Ie. [(symbol, size, initialisation)]

    Example:
    symbols = [
        ('g_ptc',           1, '.zero 1'),
        ('g_authenticated', 1, '.zero 1'),
        ('g_userPin',       4, '.zero 4'),
        ('g_cardPin',       4, '.zero 4'),
    ]
    """

    __programs: List[Tuple[str, List[Tuple[str, str, str, str]]]]
    """Dictionary mapping a label to a list of instructions.

    Ie. [(label, [(code, op1, op2, op3)])]
    
    Example:
    program = [
        ('verifyPIN', [
            # addi sp,sp,-32
            ('ADDI_CODE', 'sp', 'sp', '-32')
        ])
    ]
    
    """

    def __init__(
            self,
            symbols: List[Tuple[str, int, str]],
            programs: List[Tuple[str, List[Tuple[str, str, str, str]]]],
        ):
        self.__symbols = symbols
        self.__programs = programs

    @property
    def symbols(self) -> List[Tuple[str, int, str]]:
        """ Returns the symbols in sequence of declaration in the assembly file. """
        return self.__symbols

    @property
    def symbols_memory(self) -> int:
        """ Returns the number of bytes the global symbols require in memory. """
        return sum(size for _, size, _ in self.__symbols)

    @property
    def programs(self) -> List[Tuple[str, List[Tuple[str, str, str, str]]]]:
        return self.__programs

    @staticmethod
    def is_instruction(line: str) -> bool:
        # For now I believe it is sufficient to check if it starts with a '.' or not.
        # Example 1: 'addi sp,sp,-32' - clearly no '.'
        # Example 2: '.zero 1' - clearly has a '.' (From 'BOOL g_authenticated;').
        # Example 3: '.byte 123' - clearly has a '.' (From 'SBYTE g_ptc = 123;')
        # Example 4: '.ascii "\001\002\003\004"' - clearly has a '.' (From 'UBYTE g_cardPin[PIN_SIZE] = {1, 2, 3, 4};')
        return not line.startswith('.')

    @staticmethod
    def parse(path: str) -> "RISCVProgram":
        # First we parse the file into segments which are seperated by an identifier such as "g_ptc"
        # or "verifyPIN:" - the pattern is that they all end with ":". The proceeding line as then
        # bundled into the segment which we then process later.
        segments = RISCVProgram.parse_segments(path)

        # Second we try to figure out when the program starts and the global symbols end.
        # When this has been figured out then we can start constructing the global and program segments.
        # I assume that it is much more prone to find invalid files if we first find where the global symbols end.
        # Then in other processes where we take the "program" segments and encunter an error then we
        # know this is most likely the place to look. The index of the first "program" segment:
        first_program = 0
        for (index, (_, lines)) in enumerate(segments):
            if RISCVProgram.is_instruction(lines[0]):
                first_program = index
                break
        
        # Third we parse the global symbols.
        symbols: List[Tuple[str, int, str]] = []
        for index in range(first_program):
            symbol = RISCVProgram.parse_global_symbol(segments[index])
            symbols.append(symbol)

        # Fourth we parse the program segments.
        programs: List[Tuple[str, List[Tuple[str, str, str, str]]]] = []
        for index in range(first_program, len(segments)):
            program = RISCVProgram.parse_program(segments[index])
            programs.append(program)

        return RISCVProgram(symbols, programs)

    @staticmethod
    def parse_program(segment: Tuple[str, List[str]]) -> Tuple[str, List[Tuple[str, str, str, str]]]:
        (identifier, lines) = segment
        return (identifier, [ RISCVProgram.parse_instruction(line) for line in lines ])

    @staticmethod
    def parse_operand(operand: str) -> List[str]:
        # Example: 'ra'             -> ['-32']
        # Example: '-32'            -> ['-32']
        # Example: '(-20)sp'        -> ['sp', '-20']
        # Example: '-24(s0)'        -> ['s0', '-24']
        # Example: '%hi(g_cardPin)' -> ['symbol_high(g_cardPin)']
        # Example: '%lo(g_ptc)(a5)' -> ['a5', 'symbol_low(g_ptc)']

        # This pattern extracts groups like '%lo(g_ptc)(a5)' into ['g_ptc', 'a5']
        # And also seperates the non grouped in an element in the array.
        pattern = r"\(?([+-]?\d+|[a-zA-Z_]\w*)\)?"

        if operand.startswith('%hi'):
            operand = operand.removeprefix('%hi')
            groups = re.findall(pattern, operand)
            groups[0] = f'symbol_high({groups[0]})'
            groups.reverse()
            return groups
        elif operand.startswith('%lo'):
            operand = operand.removeprefix('%lo')
            groups = re.findall(pattern, operand)
            groups[0] = f'symbol_low({groups[0]})'
            groups.reverse()
            return groups
        elif operand.startswith('(') or operand.endswith(')'):
            groups = re.findall(pattern, operand)
            groups.reverse()
            return groups

        return [operand]

    @staticmethod
    def parse_operands(values: List[str]) -> Tuple[str, str, str]:
        operands = [ operand for value in values for operand in RISCVProgram.parse_operand(value) ]
        if len(operands) > 3:
            # Too many operands
            raise SystemExit
        elif len(operands) < 3:
            operands.extend([""] * (3 - len(operands)))

        return tuple(operands)

    @staticmethod
    def parse_instruction(line: str) -> Tuple[str, str, str, str]:
        opcode_map: Dict[str, str] = {
            'addi': 'ADDI_CODE',
            'sw': 'SW_CODE',
            'lw': 'LW_CODE',
            'lui': 'LUI_CODE',
            'sb': 'SB_CODE',
            'j': 'J_CODE',
            'li': 'LI_CODE',
            'lb': 'LB_CODE',
            'ble': 'BLE_CODE',
            'beq': 'BEQ_CODE',
            'nop': 'NOP_CODE',
            'andi': 'ANDI_CODE',
            'slli': 'SLLI_CODE',
            'srai': 'SRAI_CODE',
            'add': 'ADD_CODE',
            'lbu': 'LBU_CODE',
            'bne': 'BNE_CODE',
            'mv': 'MV_CODE',
            'jr': 'JR_CODE',
            'seqz': 'SEQZ_CODE',
            'blt': 'BLT_CODE',
        }

        split = line.split(' ')

        # Instructions like "nop":
        if len(split) == 1:
            return (opcode_map[split[0]], '', '', '')
        
        if len(split) != 2:
            # Unknown or unsupported instruction
            raise SystemExit

        (instruction, values) = split
        if instruction not in opcode_map:
            # Unknown or unsupported instruction
            raise SystemExit

        operands = RISCVProgram.parse_operands(values.split(','))

        return (opcode_map[instruction], operands[0], operands[1], operands[2])

    @staticmethod
    def parse_global_symbol(segment: Tuple[str, List[str]]) -> Tuple[str, int, str]:
        # g_ptc:     .zero 1
        # g_ptc:     .byte 123
        # g_ptc:     .word 123
        # g_cardPin: .ascii "\001\002\003\004"
        (symbol, lines) = segment

        # Multi-line initialisation of global variables are unsupported.
        if len(lines) is 0:
            raise SystemExit

        [lhs, rhs] = lines[0].split(' ')
        if lhs == '.zero':
            return (symbol, int(rhs), lhs)
        elif lhs == '.word':
            #  We assume 32-bit and therefore a word i four bytes.
            return (symbol, 4, rhs)
        elif lhs == '.ascii':
            # We assume that an ascii character is one byte lone.
            characters = rhs.count('\\')
            rhs = rhs.removeprefix('"').removesuffix('"')
            return (symbol, characters, rhs)
        
        # Unknown global symbol
        raise SystemExit

    @staticmethod
    def parse_segments(path: str) -> List[Tuple[str, List[str]]]:
        """ Returns the segments which are the parts of a risc-v assembly seperated by identifier (postfixed ':'). """
        segments: List[Tuple[str, List[str]]] = []
        segment: Optional[str] = None

        file = open(path, 'r')
        for line in file:
            # Removes duplicate whitespace and pre- and post-fix whitespace.
            line = re.sub(r'\s+', ' ', line).strip()

            # We skip empty lines:
            if not line:
                continue

            if line.endswith(':'):
                # We try to add a new segment before we have added lines to the rpevious one.
                # We assume that no segment can actually be empty.
                if segment is not None:
                    (_, current_segment) = segments[len(segments) - 1]
                    if len(current_segment) == 0:
                        file.close()
                        raise SystemExit

                segment = line.removesuffix(':')
                segments.append((segment, []))
                pass
            else:
                # we found a line which does not start a segment. However,
                # we are currently not inside a segment so where does this belong?
                # This error is just handled by exiting because the assembly file is unsupported.
                if segment is None:
                    file.close()
                    raise SystemExit
                
                segments[len(segments) - 1][1].append(line)

        file.close()
        return segments

def main():
    parser = argparse.ArgumentParser(
        description="This script processes a RISC-V assembly file and generates an Uppaal model."
    )

    RISCVProgram.__symbols
    
    parser.add_argument(
        "file", type=str,
        help="Path to the RISC-V assembly file. This file will be processed by the script."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose output for debugging or detailed logging."
    )
    parser.add_argument(
        "-t", "--template", type=str, default="./template.xml",
        help="Path to the Uppaal template file (default: './template.xml')."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="./",
        help="Directory or file path where the Uppaal model will be saved (default: './')."
    )
    
    args = parser.parse_args()

    program = RISCVProgram.parse(args.file)

if __name__ == "__main__":
    main()