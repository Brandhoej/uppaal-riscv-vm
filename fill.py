import shutil
import argparse
import re

from typing import Dict, List, Tuple, Optional

__verbose: bool = False

def v_print(text: str):
    global __verbose
    if __verbose:
        print(text)

def err_print(text: str):
    print(f'ERROR: {text}')

class RISCVProgram:
    __symbols: List[Tuple[str, List[str]]]
    """
    Ie. [(symbol, size, initialisation)]

    Example:
    symbols = [
        ('g_ptc',           ['.zero 1']),
        ('g_authenticated', ['.zero 1']),
        ('g_userPin',       ['.zero 4']),
        ('g_cardPin',       ['.zero 4']),
    ]
    """

    __programs: List[Tuple[str, List[Tuple[str, str, str, str]]]]
    """
    Ie. [(label, [(code, op1, op2, op3)])]
    
    Example:
    program = [
        ('verifyPIN', [
            # addi sp,sp,-32
            ('ADDI_CODE', 'sp', 'sp', '-32')
        ])
    ]
    
    """

    __assertions: List[Tuple[int, int, str]] = []
    """
    Ie. [(segment, instruction, assertion)]

    Example:
    assertions = [(0, 1, 'registers[sp] == 123')]
    """

    def __init__(
            self,
            symbols: List[Tuple[str, List[str]]],
            programs: List[Tuple[str, List[Tuple[str, str, str, str]]]],
            assertions: List[Tuple[int, int, str]] = []
        ):
        self.__symbols = symbols
        self.__programs = programs
        self.__assertions = assertions

    @property
    def length(self) -> int:
        return sum(len(lines) for _, lines in self.__programs)

    @property
    def symbols(self) -> List[Tuple[str, List[str]]]:
        """ Returns the symbols in sequence of declaration in the assembly file. """
        return self.__symbols

    @property
    def symbols_size(self) -> int:
        return sum(RISCVProgram.symbol_size(lines) for _, lines in self.__symbols)

    @property
    def memory(self) -> int:
        return self.__memory

    @property
    def max_flips(self) -> int:
        return self.__max_flips

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

    @property
    def assertions(self) -> List[Tuple[int, int, str]]:
        return self.__assertions

    def generated_max_flips(self, max_flips: int) -> str:
        # /* GENERATED: MAX_FLIPS */
        # Example: "const int32_t MAX_FLIPS = 1;"
        return f'const int32_t MAX_FLIPS = {max_flips};'

    def generated_program_length(self) -> str:
        # /* GENERATED: PROGRAM_LENGTH */
        # Example: "const int32_t PROGRAM_LENGTH = 8;"
        return f'const int32_t PROGRAM_LENGTH = {self.length};'

    def generated_global_symbols_size(self) -> str:
        # /* GENERATED: GLOBAL_SYMBOLS_SIZE */
        # Example: "const int32_t GLOBAL_SYMBOLS_SIZE = 8;"
        return f'const int32_t GLOBAL_SYMBOLS_SIZE = {self.symbols_size};'

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
        for (symbol, lines) in self.symbols:
            globals.append(f'const address_t {symbol} = {offset};')
            offset += RISCVProgram.symbol_size(lines)
        return '\n'.join(globals)
    
    def generated_memory_length(self, memory: int) -> str:
        # /* GENERATED: MEMORY_LENGTH */
        # Example: "const int32_t MEMORY_LENGTH = 64;"
        return f'const int32_t MEMORY_LENGTH = {memory};'

    def generated_initial_pc(self, initial_pc: str) -> str:
        # /* GENERATED: INITIAL_PC */
        # Example: "pc = verifyPIN;"
        return f'pc = {initial_pc};'

    def generated_cooldown(self, cooldown: int) -> str:
        # /* GENERATED: COOLDOWN */
        # Example: "attacker = Attacker(/* GENERATED: COOLDOWN */);"
        return f'{cooldown}'

    def generated_fault_models(self, fault_models: List[str]) -> str:
        # /* GENERATED: FAULT_MODELS */
        # Example: "system vm /* GENERATED: FAULT_MODELS */;"
        # After replacement: "system vm, attacker, rc, pcf, is, mc, sc, gc, oorc, orc;"

        if len(fault_models) > 0:
            fault_models.append('attacker')

        fault_models = list(map(str.lower, fault_models))
        network = ', '.join(fault_models)
        return f', {network}'

    def generated_memory_initialisation(self) -> str:
        # g_ptc:
        #         .word   32
        #         .word   0
        # g_authenticated:
        #         .byte   2
        # g_cardPin:
        #         .ascii  "\001\002\003\004"
        # g_userPin:
        #         .string "\001"
        #         .zero   2
        # g_ptc:
        #         .half   32
        # g_userPin:
        #         .string "\001\002\003"
        # OBS: Strings are zero escaped "\0" which accounts for a byte.

        generated: List[str] = []

        global_offset = 0
        for (symbol, lines) in self.symbols:
            local_offset = 0
            for line in lines:
                blob = RISCVProgram.data_bytes(line)
                for i in range(len(blob)):
                    generated.append(f'memory[{global_offset}] = {int(blob[i])}; // {local_offset}\'it byte of {symbol}')
                    local_offset += 1
                    global_offset += 1

        return '\n'.join(generated)

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

    def fill_template(
            self,
            template: str,
            initial_pc: str = '0',
            memory: int = 256,
            max_flips: int = 0,
            cooldown: int = 0,
            fault_models: List[str] = [],
        ):
        content = ''
        with open(template) as file:
            content = file.read()

        content = content.replace('/* GENERATED: LABELS */', self.generated_labels())
        content = content.replace('/* GENERATED: GLOBAL_SYMBOLS */', self.generated_global_symbols())
        content = content.replace('/* GENERATED: PROGRAM_LENGTH */', self.generated_program_length())
        content = content.replace('/* GENERATED: GLOBAL_SYMBOLS_SIZE */', self.generated_global_symbols_size())
        content = content.replace('/* GENERATED: PROGRAM */', self.generated_program())
        content = content.replace('/* GENERATED: MEMORY_INITIALISATION */', self.generated_memory_initialisation())
        content = content.replace('/* GENERATED: MEMORY_LENGTH */', self.generated_memory_length(memory))
        content = content.replace('/* GENERATED: MAX_FLIPS */', self.generated_max_flips(max_flips))
        content = content.replace('/* GENERATED: INITIAL_PC */', self.generated_initial_pc(initial_pc))
        content = content.replace('/* GENERATED: COOLDOWN */', self.generated_cooldown(initial_pc))
        content = content.replace('/* GENERATED: FAULT_MODELS */', self.generated_fault_models(fault_models))
        
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
    def data_size(line: str) -> int:
        return len(RISCVProgram.data_bytes(line))

    @staticmethod
    def data_bytes(line: str) -> bytes:
        [lhs, rhs] = line.split(' ')

        # Example: ".zero 2"
        if lhs == '.zero':
            return bytes(int(rhs))
        # Example ".ascii "\001\002\003\004""
        elif lhs == '.ascii':
            rhs = rhs.removeprefix('"').removesuffix('"')
            unescaped = rhs.encode('latin1').decode('unicode_escape')
            return unescaped.encode('latin1')
        # Example: ".string "\001""
        elif lhs == '.string':
            rhs = rhs.removeprefix('"').removesuffix('"')
            # Strings are zero escaped "\0" which accounts for a byte (+1).
            return rhs.encode('latin1') + b'\0'
        # Example: ".byte 2"
        elif lhs == '.byte':
            return int(rhs).to_bytes(1, 'little', signed=True)
        # Example: ".half 32"
        elif lhs == '.half':
            return int(rhs).to_bytes(2, 'little', signed=True)
        # Example: ".word 123"
        elif lhs == '.word':
            return int(rhs).to_bytes(4, 'little', signed=True)
        else:
            v_print(f'Unknwon global symbol initialisation type "{lhs}" with "{rhs}".')
            raise SystemExit

    @staticmethod
    def symbol_size(lines: List[str]) -> int:
        return sum(RISCVProgram.data_size(line) for line in lines)

    @staticmethod
    def parse(path: str) -> "RISCVProgram":
        # First we parse the file into segments which are seperated by an identifier such as "g_ptc"
        # or "verifyPIN:" - the pattern is that they all end with ":". The proceeding line as then
        # bundled into the segment which we then process later.
        (segments, assertions) = RISCVProgram.parse_segments(path)

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
        symbols: List[Tuple[str, List[str]]] = []
        for index in range(first_program):
            symbols.append(segments[index])

        # Fourth we parse the program segments.
        programs: List[Tuple[str, List[Tuple[str, str, str, str]]]] = []
        for index in range(first_program, len(segments)):
            program = RISCVProgram.parse_program(segments[index])
            programs.append(program)

        return RISCVProgram(symbols, programs, assertions)

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
            v_print(f'Too many instruction operands "{values}".')
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
            'call': 'CALL_CODE',
        }

        split = line.split(' ')

        # Instructions like "nop":
        if len(split) == 1:
            return (opcode_map[split[0]], '', '', '')
        
        if len(split) != 2:
            v_print(f'Unknown instruction layout: "{line}".')
            raise SystemExit

        (instruction, values) = split
        if instruction not in opcode_map:
            v_print(f'Unknown or unsupported instruction does not have an OP_CODE: "{instruction}".')
            raise SystemExit

        operands = RISCVProgram.parse_operands(values.split(','))

        return (opcode_map[instruction], operands[0], operands[1], operands[2])

    @staticmethod
    def parse_segments(path: str) -> Tuple[List[Tuple[str, List[str]]], List[Tuple[int, int, str]]]:
        """ Returns the segments which are the parts of a risc-v assembly seperated by identifier (postfixed ':'). """
        segments: List[Tuple[str, List[str]]] = []
        assertions: List[Tuple[int, int, str]] = []
        segment: Optional[str] = None

        with open(path, 'r') as file:
            for line in file:
                # Removes duplicate whitespace and pre- and post-fix whitespace.
                line = re.sub(r'\s+', ' ', line).strip()

                # We skip empty lines:
                if not line:
                    continue

                # It is possible to comment lines:
                if line.startswith(";"):
                    continue

                if line.endswith(':'):
                    # We try to add a new segment before we have added lines to the rpevious one.
                    # We assume that no segment can actually be empty.
                    if segment is not None:
                        (_, current_segment) = segments[len(segments) - 1]
                        if len(current_segment) == 0:
                            v_print(f'The segment "{current_segment}" is empty.')
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
                        v_print(f'The line "{line}" is not in a segment.')
                        raise SystemExit

                    segment_index = len(segments) - 1
                    
                    split = line.split(';')
                    if len(split) == 2:
                        (instruction, assertion) = (split[0].strip(), split[1].strip())
                        assertions.append((segment, len(segments[segment_index][1]), assertion))
                        segments[segment_index][1].append(instruction)
                    else:
                        segments[len(segments) - 1][1].append(line)

        return (segments, assertions)

def main():
    parser = argparse.ArgumentParser(
        description="This script processes a RISC-V assembly file and generates an Uppaal model.",
        formatter_class=argparse.RawTextHelpFormatter,
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
    parser.add_argument(
        '-m', '--memory', type=int, default=256,
        help="The memory allocated for the program."
    )
    parser.add_argument(
        '-f', '--flips', type=int, default=0,
        help="The number of flips an attacker can perform."
    )
    parser.add_argument(
        '-p', '--pc', type=str, default='0',
        help="The initial PC of the simulation."
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable verbose mode: print detailed step-by-step output to the terminal.'
    )
    parser.add_argument(
        '-cd', '--cooldown', type=int, default=0,
        help='The cooldown performed by the attacker'
    )

    fault_model_descriptions = {
        "RC": "RegisterCorruption: Bit-flips in arbritary CPU registers.",
        "PCF": "PCFlip: Bit-flips in the Program Counter (PC).",
        "IS": "InstructionSkip: Skips an instruction after execution by incrementing C by one.",
        "MC": "MemoryCorruption: Bit-flips in arbritary memory.",
        "SC": "StackCorruption: Bit-flips in the memory segment that is the stack at current time.",
        "GC": "GlobalsCorruption: Bit-flips in the memory segment containing the global variables.",
        "ORC": "OptimisedRegisterCorruption: Bit-flips on registers where an effect is guaranteed.",
        "OORC": "ObsOptimisedRegisterCorruption: Bit-flips on write lie ORC but uses write to memory as observable actions.",
    }
    fault_model_help_text = "Select the type of fault models:\n" + "\n".join(
        f"    {key} - {desc}" for key, desc in fault_model_descriptions.items()
    )
    parser.add_argument(
        '-fm', '--fault_models', nargs='+', type=str,
        choices=fault_model_descriptions.keys(),
        help=fault_model_help_text,
    )
    
    args = parser.parse_args()

    # For now the verbose printing flag is globally set.
    global __verbose
    __verbose = args.verbose

    if args.flips > 0 and (args.fault_models is None or len(args.fault_models) == 0):
        err_print(f"{args.flips} flip(s) requested, but no fault models were specified. Please provide at least one fault model.")
        return

    if args.fault_models is not None and len(args.fault_models) > 0 and args.flips == 0:
        err_print(f"Fault model(s) specified ({args.fault_models}), but the number of flips is set to 0. Please set a positive number for flips.")
        return

    if args.cooldown > 0 and args.flips == 0:
        err_print(f'Cooldown for the attacker specified ({args.cooldown}), but the number of flips is set to 0. Please set a positive number for flips.')
        return

    program = RISCVProgram.parse(args.file)

    # Copy the template at --template and save to --output.
    # Then fill the copied template with the generated code.
    shutil.copy(args.template, args.output)
    program.fill_template(
        args.output,
        memory=args.memory,
        max_flips=args.flips,
        initial_pc=args.pc,
        cooldown=args.cooldown,
        fault_models=args.fault_models,
    )

if __name__ == "__main__":
    main()