import subprocess

from pathlib import Path
from typing import Dict, List

verifyta = 'verifyta'
python = 'python3'
fill_path = './fill.py'
template_path = './experiments/template.xml'
strategy_templates_base = './experiments/strategy_templates'

cooldown: int = 10
fault_models: List[str] = [
    "RC", "PCF", "IS", "MC", "SC", "GC", "ORC", "OORC"
]

models: Dict[str, str] = {
    # Inlined:
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm': f'{strategy_templates_base}/0_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    # Not inline (CALL Instruction):
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm': f'{strategy_templates_base}/0_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_1_HB.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_2_HB+FTL.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_3_HB+FTL+INL.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_4_HB+FTL+INL+DPTC+PTCBK+LC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_5_HB+FTL+DPTC+DC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_6_HB+FTL+INL+DPTC+DT.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
    './FISSC/c1234 RISC-V (32-bits) gcc 14.2.0/VerifyPIN_7_HB+FTL+INL+DPTC+DT+SC.asm': f'{strategy_templates_base}/1_2_3_4_5_6_7_strategy_template.q',
}

for riscv, query in models.items():
    program = Path(riscv).stem

    for fault_model in fault_models:
        # Create identifiers and outputs.
        output_directory = f'./experiments/{program}'
        output_stem = f'{program}-{fault_model}'
        output_path = f'{output_directory}/{output_stem}.xml'
        
        # Create the template.
        fill_code = subprocess.call([
            python, fill_path, riscv,
            '--template', template_path,
            '--output', output_path,
            '--cooldown', str(cooldown),
            '--flips', str(1),
            '--fault_models', f'{fault_model}'
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
        verifyta_code = subprocess.call([ verifyta, output_path, query_file ])

        # Check if creating running the queries failed.
        if verifyta_code != 0:
            print(f'ERROR: VerifyTA failed: {verifyta_code}; {riscv}; {query}; {fault_model}')
            continue