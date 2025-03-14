# uppaal-riscv-vm

## Fill Template
```console
python3 ./fill.py -h
```

Example:
```console
python3 ./fill.py "./FISSC/u0000 INLINED RISC-V (32-bits) gcc 14.2.0/VerifyPIN_0.asm" --memory 64 --flips 3 --template ./template.xml --output "./VerifyPIN_0.xml"
```

## Generating VerifyPIN Models
Requires _verifyta_ to be in the ``PATH``.
```console
./fill_templates.sh
```

## Test
Running the tests covers some of the parser and sanity checks for VerifyPIN examples.
```console
./test_linux.sh
```