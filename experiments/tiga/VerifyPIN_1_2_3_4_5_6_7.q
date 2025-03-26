strategy Undetected = control: A[] mem_u8(g_countermeasure) == 0 && ((vm.DONE || vm.ERR) imply remaining_flips < MAX_FLIPS)
strategy Access = control: A<> vm.DONE && mem_u8(g_authenticated) == 170 && remaining_flips < MAX_FLIPS
strategy UndetectedAccess = control: A<> vm.DONE && mem_u8(g_countermeasure) == 0 && mem_u8(g_authenticated) == 170 && remaining_flips < MAX_FLIPS
strategy NoCrash = control: A<> !vm.ERR