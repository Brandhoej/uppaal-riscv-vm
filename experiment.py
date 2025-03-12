import shutil
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
    def length(self) -> int:
        return sum(len(lines) for _, lines in self.__programs)

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
    
    @property
    def labels(self) -> List[Tuple[str, int]]:
        labels = []
        pc = 0
        for (label, lines) in self.programs:
            labels.append((label, pc))
            pc += len(lines)
        return labels

    def generated_program_length(self) -> str:
        # /* GENERATED: PROGRAM LENGTH */
        # Example: "const int32_t PROGRAM_LENGTH = 8;"
        return f'const int32_t PROGRAM_LENGTH = {self.length};'

    def generated_labels(self) -> str:
        # /* GENERATED: PC LABELS */
        # Example: "const pc_t L0 = 0;"
        # Example: "const pc_t verifyPIN() = 31;"
        labels: List[str] = []
        for (label, pc) in self.labels:
            labels.append(f'const pc_t {label} = {pc};')
        return '\n'.join(labels)

    def generated_global_symbols(self) -> str:
        # /* GENERATED: GLOBAL SYMBOLS */
        # Example: "const address_t g_authenticated = 0;"
        # Example: "const address_t g_authenticated = 2;"
        globals: List[str] = []
        offset = 0
        for (symbol, size, _) in self.symbols:
            globals.append(f'const address_t {symbol} = {offset};')
            offset += size
        return '\n'.join(globals)
    
    def generated_globals_initial(self) -> str:
        # TODO: initial memory for global symbols. Right now we just support zero.
        return ''

    def generated_program(self) -> str:
        # /* GENERATED: PROGRAM */
        # Example: "instruction_t line_0 = {ADDI_CODE, sp, sp, -32};"
        code_instructions: List[str] = []
        # Example: "program[0] = line_0;"
        code_assignments: List[str] = []

        line = 0
        for (symbol, instructions) in self.programs:
            for (i, (a, b, c, d)) in enumerate(instructions):
                line_identifier = f'line_{line}'
                code_instructions.append(f'instruction_t {line_identifier} = {{ {a}, {'0' if not b else b}, {'0' if not c else c}, {'0' if not d else d} }}; {f'// {symbol}' if i == 0 else ''}')
                code_assignments.append(f'program[{line}] = {line_identifier};')
                line += 1

        code_instructions.extend(code_assignments)
        return '\n'.join(code_instructions)

    def generated_sp_pc_init(self) -> str:
        return 'registers[sp] = MEMORY_LENGTH - 1;\npc = 0;'

    def fill_template(self, template: str):
        content = ''
        with open(template) as file:
            content = file.read()

        content = content.replace('/* GENERATED: LABELS */', self.generated_labels() + '\n')
        content = content.replace('/* GENERATED: GLOBAL SYMBOLS */', self.generated_global_symbols() + '\n')
        content = content.replace('/* GENERATED: PROGRAM LENGTH */', self.generated_program_length() + '\n')
        content = content.replace('/* GENERATED: PROGRAM */', self.generated_program() + '\n')

        with open(template, 'w') as file:
            file.write(content)
        
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

        operands = []
        if operand.startswith('%hi'):
            operand = operand.removeprefix('%hi')
            operands = re.findall(pattern, operand)
            operands[0] = f'symbol_high({operands[0]})'
            operands.reverse()
        elif operand.startswith('%lo'):
            operand = operand.removeprefix('%lo')
            operands = re.findall(pattern, operand)
            operands[0] = f'symbol_low({operands[0]})'
            operands.reverse()
        elif operand.startswith('(') or operand.endswith(')'):
            operands = re.findall(pattern, operand)
            operands.reverse()
        else:
            operands = [operand]

        for (i, operand) in enumerate(operands):
            # Remove '.' which is prefixes for label operands.
            operands[i] = operand.removeprefix('.')

            # Some operands are hexadecimals.
            if operand.startswith('0x'):
                operands[i] = str(int(operand, 0))


        return operands

    @staticmethod
    def parse_operands(values: List[str]) -> Tuple[str, str, str]:
        operands = [ operand for value in values for operand in RISCVProgram.parse_operand(value) ]
        if len(operands) > 3:
            # Too many operands
            raise SystemExit
        elif len(operands) < 3:
            operands.extend([''] * (3 - len(operands)))

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
        if len(lines) == 0:
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

        with open(path, 'r') as file:
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
                            raise SystemExit

                    # We remove ':' and '()' as some labels may end with it for some reason.
                    # Example: "verifyPIN():" -> "verifyPIN"
                    # Example: ".L4:" -> "L4"
                    segment = line.removesuffix(':').removesuffix('()').removeprefix('.')
                    segments.append((segment, []))
                    pass
                else:
                    # we found a line which does not start a segment. However,
                    # we are currently not inside a segment so where does this belong?
                    # This error is just handled by exiting because the assembly file is unsupported.
                    if segment is None:
                        raise SystemExit
                    
                    segments[len(segments) - 1][1].append(line)

        return segments

def main():
    parser = argparse.ArgumentParser(
        description="This script processes a RISC-V assembly file and generates an Uppaal model."
    )
    
    parser.add_argument(
        "file", type=str,
        help="Path to the RISC-V assembly file. This file will be processed by the script."
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

    # Copy the template at --template and save to --output.
    # Then fill the copied template with the generated code.
    shutil.copy(args.template, args.output)
    program.fill_template(args.output)

if __name__ == "__main__":
    main()