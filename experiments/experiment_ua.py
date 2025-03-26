import subprocess

from pathlib import Path
from typing import Dict, Tuple, List

verifyta = 'verifyta'
python = 'python3'
fill_path = './fill.py'
template_path = './experiments/template.xml'
strategy_templates_base = './experiments/strategy_templates'

cooldown: int = 10
fault_models: List[str] = [
    "ORC", "IS", "OORC", "GC", "SC", "PCF", "RC", "MC"
]

models: Dict[str, Tuple[str, str]] = {
    # Inlined:
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm': ('INL', f'{strategy_templates_base}/0_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm': ('INL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    # Not inline (CALL Instruction):
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm': ('CALL', f'{strategy_templates_base}/0_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
    './FISSC/c1111 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm': ('CALL', f'{strategy_templates_base}/1_2_3_4_5_6_7_ua_strategy_template.q'),
}

for flips in [1, 2, 3]:
    for fault_model in fault_models:

        for riscv, (prefix, query) in models.items():
            program = Path(riscv).stem

            # Create identifiers and outputs.
            output_directory = f'./experiments/{prefix}-{program}'
            output_stem = f'{program}---{fault_model}---'
            output_path = f'{output_directory}/{output_stem}.xml'
            
            # Create the template.
            fill_code = subprocess.call([
                python, fill_path, riscv,
                '--template', template_path,
                '--output', output_path,
                '--cooldown', str(cooldown),
                '--flips', str(flips),
                '--fault_models', f'{fault_model}',
            ])

            # Check if creating the template failed.
            if fill_code != 0:
                print(f'ERROR: Fill failed: {fill_code}; {riscv}; {query}; {fault_model}')
                continue

            # Read the query file.
            content = ''
            with open(query) as file:
                content = file.read()

            # Replace the query tags with the unique id for the model.
            content = content.replace('<<PATH>>', output_directory)
            content = content.replace('<<MODEL>>', output_stem)

            # Write the new query file.
            query_file = f'{output_directory}/{output_stem}-query.q'
            with open(query_file, 'w') as file:
                file.write(content)

            # Run VerifyTA to synthesis the strategies.
            verifyta_code = subprocess.call([
                verifyta, output_path, query_file,
                '--silence-progress', '--summary',
            ])

            # Check if creating running the queries failed.
            if verifyta_code != 0:
                print(f'ERROR: VerifyTA failed: {verifyta_code}; {riscv}; {query}; {fault_model}')
                continue
