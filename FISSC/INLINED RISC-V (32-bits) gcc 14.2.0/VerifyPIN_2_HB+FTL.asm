g_countermeasure:
        .zero   1
g_ptc:
        .zero   1
g_authenticated:
        .zero   1
g_userPin:
        .zero   4
g_cardPin:
        .ascii  "\001\002\003\004"
verifyPIN:
        addi    sp,sp,-32
        sw      ra,28(sp)
        sw      s0,24(sp)
        addi    s0,sp,32
        lui     a5,%hi(g_authenticated)
        li      a4,85
        sb      a4,%lo(g_authenticated)(a5)
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        ble     a5,zero,.L2
        lui     a5,%hi(g_userPin)
        addi    a5,a5,%lo(g_userPin)
        sw      a5,-20(s0)
        lui     a5,%hi(g_cardPin)
        addi    a5,a5,%lo(g_cardPin)
        sw      a5,-24(s0)
        li      a5,4
        sb      a5,-25(s0)
        li      a5,85
        sb      a5,-26(s0)
        li      a5,85
        sb      a5,-27(s0)
        sw      zero,-32(s0)
        j       .L3
.L5:
        lw      a5,-32(s0)
        lw      a4,-20(s0)
        add     a5,a4,a5
        lbu     a4,0(a5)
        lw      a5,-32(s0)
        lw      a3,-24(s0)
        add     a5,a3,a5
        lbu     a5,0(a5)
        beq     a4,a5,.L4
        li      a5,-86
        sb      a5,-27(s0)
.L4:
        lw      a5,-32(s0)
        addi    a5,a5,1
        sw      a5,-32(s0)
.L3:
        lbu     a5,-25(s0)
        lw      a4,-32(s0)
        blt     a4,a5,.L5
        lbu     a5,-25(s0)
        lw      a4,-32(s0)
        beq     a4,a5,.L6
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L6:
        lbu     a4,-27(s0)
        li      a5,85
        bne     a4,a5,.L7
        li      a5,-86
        sb      a5,-26(s0)
        j       .L8
.L7:
        li      a5,85
        sb      a5,-26(s0)
.L8:
        lbu     a4,-26(s0)
        li      a5,170
        bne     a4,a5,.L10
        lui     a5,%hi(g_ptc)
        li      a4,3
        sb      a4,%lo(g_ptc)(a5)
        lui     a5,%hi(g_authenticated)
        li      a4,-86
        sb      a4,%lo(g_authenticated)(a5)
        li      a5,170
        j       .L11
.L10:
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        andi    a5,a5,0xff
        addi    a5,a5,-1
        andi    a5,a5,0xff
        slli    a4,a5,24
        srai    a4,a4,24
        lui     a5,%hi(g_ptc)
        sb      a4,%lo(g_ptc)(a5)
        li      a5,85
        j       .L11
.L2:
        li      a5,85
.L11:
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
;        jr      ra