g_countermeasure:
        .zero   1
g_ptc:
        .byte   3
g_authenticated:
        .zero   1
g_userPin:
        .ascii  "\001\002\003\004"
g_cardPin:
        .ascii  "\001\002\003\004"
verifyPIN():
        addi    sp,sp,-32
        sw      ra,28(sp)
        sw      s0,24(sp)
        addi    s0,sp,32
        sw      zero,-20(s0)
        lui     a5,%hi(g_authenticated)
        li      a4,85
        sb      a4,%lo(g_authenticated)(a5)
        lui     a5,%hi(g_ptc)
        lb      a5,%lo(g_ptc)(a5)
        ble     a5,zero,.L2
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,1
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
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,2
        beq     a4,a5,.L4
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L4:
        li      a5,85
        sb      a5,-25(s0)
        li      a5,85
        sb      a5,-26(s0)
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,3
        beq     a4,a5,.L5
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L5:
        sw      zero,-24(s0)
        j       .L6
.L9:
        lui     a5,%hi(g_userPin)
        addi    a4,a5,%lo(g_userPin)
        lw      a5,-24(s0)
        add     a5,a4,a5
        lbu     a4,0(a5)
        lui     a5,%hi(g_cardPin)
        addi    a3,a5,%lo(g_cardPin)
        lw      a5,-24(s0)
        add     a5,a3,a5
        lbu     a5,0(a5)
        beq     a4,a5,.L7
        li      a5,-86
        sb      a5,-26(s0)
.L7:
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a5,-24(s0)
        addi    a5,a5,4
        lw      a4,-20(s0)
        beq     a4,a5,.L8
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L8:
        lw      a5,-24(s0)
        addi    a5,a5,1
        sw      a5,-24(s0)
.L6:
        lw      a4,-24(s0)
        li      a5,3
        ble     a4,a5,.L9
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,8
        beq     a4,a5,.L10
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L10:
        lw      a4,-24(s0)
        li      a5,4
        beq     a4,a5,.L11
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L11:
        lbu     a4,-26(s0)
        li      a5,85
        bne     a4,a5,.L12
        lbu     a4,-26(s0)
        li      a5,85
        bne     a4,a5,.L13
        li      a5,-86
        sb      a5,-25(s0)
        j       .L14
.L13:
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        j       .L14
.L12:
        li      a5,85
        sb      a5,-25(s0)
.L14:
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,9
        beq     a4,a5,.L15
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L15:
        lbu     a4,-25(s0)
        li      a5,170
        bne     a4,a5,.L16
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,10
        beq     a4,a5,.L17
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L17:
        lbu     a4,-25(s0)
        li      a5,170
        bne     a4,a5,.L18
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,11
        beq     a4,a5,.L19
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L19:
        lui     a5,%hi(g_ptc)
        li      a4,3
        sb      a4,%lo(g_ptc)(a5)
        lw      a5,-20(s0)
        addi    a5,a5,1
        sw      a5,-20(s0)
        lw      a4,-20(s0)
        li      a5,12
        beq     a4,a5,.L20
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L20:
        lui     a5,%hi(g_authenticated)
        li      a4,-86
        sb      a4,%lo(g_authenticated)(a5)
        li      a5,170
        j       .L21
.L18:
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        j       .L2
.L16:
        lui     a5,%hi(g_countermeasure)
        li      a4,1
        sb      a4,%lo(g_countermeasure)(a5)
        nop
.L2:
        li      a5,85
.L21:
        mv      a0,a5
        lw      ra,28(sp)
        lw      s0,24(sp)
        addi    sp,sp,32
;        jr      ra