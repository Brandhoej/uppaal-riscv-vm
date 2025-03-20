g_ptc:
        .byte   3
g_authenticated:
        .zero   1
g_userPin:
        .zero   4
g_cardPin:
        .ascii  "\001\002\003\004"
byteArrayCompare:
        addi    sp,sp,-48
        sw      ra,44(sp)
        sw      s0,40(sp)
        addi    s0,sp,48
        sw      a0,-36(s0)
        sw      a1,-40(s0)
        mv      a5,a2
        sb      a5,-41(s0)
        sw      zero,-20(s0)
        j       .L2
.L5:
        lw      a5,-20(s0)
        lw      a4,-36(s0)
        add     a5,a4,a5
        lbu     a4,0(a5)
        lw      a5,-20(s0)
        lw      a3,-40(s0)
        add     a5,a3,a5
        lbu     a5,0(a5)
        beq     a4,a5,.L3
        li      a5,0
        j       .L4
.L3:
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
.L2:
        lbu     a5,-41(s0)
        lw      a4,-20(s0)
        blt     a4,a5,.L5
        li      a5,1
.L4:
        mv      a0,a5
        lw      ra,44(sp)
        lw      s0,40(sp)
        addi    sp,sp,48
        jr      ra
verifyPIN:
        addi    sp,sp,-16
        sw      ra,12(sp)
        sw      s0,8(sp)
        addi    s0,sp,16
        lui     a5,%hi(g_authenticated)
        sb      zero,%lo(g_authenticated)(a5)
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        ble     a5,zero,.L7
        li      a2,4
        lui     a5,%hi(g_cardPin)
        addi    a1,a5,%lo(g_cardPin)
        lui     a5,%hi(g_userPin)
        addi    a0,a5,%lo(g_userPin)
        call    byteArrayCompare
        mv      a5,a0
        mv      a4,a5
        li      a5,1
        bne     a4,a5,.L8
        lui     a5,%hi(g_ptc)
        li      a4,3
        sb      a4,%lo(g_ptc)(a5)
        lui     a5,%hi(g_authenticated)
        li      a4,1
        sb      a4,%lo(g_authenticated)(a5)
        li      a5,1
        j       .L9
.L8:
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        andi    a5,a5,0xff
        addi    a5,a5,-1
        andi    a5,a5,0xff
        slli    a4,a5,24
        srai    a4,a4,24
        lui     a5,%hi(g_ptc)
        sb      a4,%lo(g_ptc)(a5)
        li      a5,0
        j       .L9
.L7:
        li      a5,0
.L9:
        mv      a0,a5
        lw      ra,12(sp)
        lw      s0,8(sp)
        addi    sp,sp,16
        jr      ra