strategy UndetectedAccess = control: A<> vm.DONE && mem_u8(g_countermeasure) == 0 && mem_u8(g_authenticated) == 170 && remaining_flips < MAX_FLIPS
