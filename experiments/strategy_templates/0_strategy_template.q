strategy Access = control: A<> vm.DONE && mem_u8(g_authenticated) == 1 && remaining_flips < MAX_FLIPS
saveStrategy("<<PATH>>/<<MODEL>>-strategy-access", Access)