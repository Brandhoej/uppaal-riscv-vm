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
        lui     a5,%hi(g_ptc)
        lbu     a5,%lo(g_ptc)(a5)
        sb      a5,-29(s0)
        lui     a5,%hi(g_authenticated)
        li      a4,85
        sb      a4,%lo(g_authenticated)(a5)
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        ble     a5,zero,.L2
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        lb      a4,-29(s0)
        beq     a4,a5,.L3
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L3:
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        andi    a5,a5,0xff
        addi    a5,a5,-1
        andi    a5,a5,0xff
        slli    a4,a5,24
        srai    a4,a4,24
        lui     a5,%hi(g_ptc)
        sb      a4,%lo(g_ptc)(a5)
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        mv      a4,a5
        lb      a5,-29(s0)
        addi    a5,a5,-1
        beq     a4,a5,.L4
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L4:
        lb      a5,-29(s0)
        andi    a5,a5,0xff
        addi    a5,a5,-1
        andi    a5,a5,0xff
        sb      a5,-29(s0)
        li      a5,85
        sb      a5,-21(s0)
        li      a5,85
        sb      a5,-22(s0)
        sw      zero,-28(s0)
        sw      zero,-20(s0)
        j       .L5
.L7:
        lui     a5,%hi(g_userPin)
        addi    a4,a5,%lo(g_userPin)
        lw      a5,-20(s0)
        add     a5,a4,a5
        lbu     a4,0(a5)
        lui     a5,%hi(g_cardPin)
        addi    a3,a5,%lo(g_cardPin)
        lw      a5,-20(s0)
        add     a5,a3,a5
        lbu     a5,0(a5)
        beq     a4,a5,.L6
        li      a5,-86
        sb      a5,-22(s0)
.L6:
        lw      a5,-28(s0)
        addi    a5,a5,1
        sw      a5,-28(s0)
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
.L5:
        lw      a4,-20(s0)
        li      a5,3
        ble     a4,a5,.L7
        lw      a4,-28(s0)
        li      a5,4
        beq     a4,a5,.L8
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L8:
        lw      a4,-20(s0)
        li      a5,4
        beq     a4,a5,.L9
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L9:
        lbu     a4,-22(s0)
        li      a5,85
        bne     a4,a5,.L10
        li      a5,-86
        sb      a5,-21(s0)
        j       .L11
.L10:
        li      a5,85
        sb      a5,-21(s0)
.L11:
        lbu     a4,-21(s0)
        li      a5,170
        bne     a4,a5,.L2
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        lb      a4,-29(s0)
        beq     a4,a5,.L12
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L12:
        lui     a5,%hi(g_ptc)
        li      a4,3
        sb      a4,%lo(g_ptc)(a5)
        lui     a5,%hi(g_authenticated)
        li      a4,-86
        sb      a4,%lo(g_authenticated)(a5)
        li      a5,170
        j       .L13
.L2:
        li      a5,85
.L13:
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
;        jr      ra