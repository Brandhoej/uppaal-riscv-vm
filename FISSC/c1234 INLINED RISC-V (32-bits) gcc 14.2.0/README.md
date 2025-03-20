# RISC-V (32-bits) gcc 14.2.0
The compilations assmeblies can all be found in [godbolt](https://godbolt.org/z/xsMKToGf8). The exact command can be found following the link. Omitting the specific paths we get the command:

```console
-g -o output.s -fno-verbose-asm -S -fdiagnostics-color=always verify_pin.cpp
```

## Changes to FISSC
The VerifyPIN programs have all been inlined with ``always_inline`` attribute.