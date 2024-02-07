
        org     8000h

        adc     a, b
        add     a, 3

        and     c
        and     5
        and     (hl)
        and     (ix+1)
        and     (iy-1)
        sub     5
        sub     (hl)
        sub     (ix+1)
        sub     (iy-1)
        bit     3, a
        call    123
        call    nz, 124
        ccf
        scf
        cp      a
        cp      5
        cp      (hl)
        cp      (ix - 2)
        cp      (iy + 3)
        cpd
        cpdr
        cpi
        cpir
        daa
        inc     b
        dec     d
        inc     (hl)
        dec     (hl)
        inc     (ix - 2)
        dec     (ix + 12)
        inc     (iy + 122)
        dec     (iy - 29)
        di
        ei
        djnz    -12
        ex      de, hl
        ex      af, af'
        ex      (sp), hl
        ex      (sp), ix
        ex      (sp), iy
        exx
        ind
        indr
        ini
        inir
        jp      2980
        jp      pe, 223
        jp      (hl)
        jp      (ix)
        jp      (iy)
        jr      -123
        jr      c, 12
        jr      nc, -99
        jr      z, 13
        jr      nz, -88
        ldi
        ldir
        ldd
        lddr
;       ld
        neg
        nop                 ; nop instruction
        or      (hl)
        or      c
        or      128
        or      (ix - 2)
        or      (iy+2)
        otdr
        otir
        outd
        outi
        push    af
        push    hl
        push    bc
        push    de
        push    ix
        push    iy
        pop     iy
        pop     ix
        pop     de
        pop     bc
        pop     hl
        pop     af
        reti
        retn
        ret
        ret     nc
        ret     c
        ret     z
        ret     nz
        ret     p
        ret     pe
        ret     po
        ret     m
        rl      a
        rl      (hl)
        rl      (ix+1)
        rl      (iy-1)
        rr      b
        rr      (hl)
        rr      (ix+1)
        rr      (iy-1)
        rlc     c
        rlc     (hl)
        rlc     (ix+1)
        rlc     (iy-1)
        rrc     d
        rrc     (hl)
        rrc     (ix+1)
        rrc     (iy-1)
        rla
        rlca
        rld
        rra
        rrca
        rst     08h
        sbc     a, b
        sbc     a, 55
        sbc     a, (hl)
        sbc     a, (ix+5)
        sbc     a, (iy-6)
        sub      (hl)
        sub      c
        sub      128
        sub      (ix - 2)
        sub      (iy+2)
        add     hl, bc
        add     hl, de
        add     hl, hl
        add     hl, sp
        adc     hl, bc
        adc     hl, de
        adc     hl, hl
        adc     hl, sp
        add     ix, bc
        add     ix, de
        add     ix, ix
        add     ix, sp
        add     iy, bc
        add     iy, de
        add     iy, iy
        add     iy, sp
        adc     hl, bc
        sbc     hl, de
        sbc     hl, hl
        sbc     hl, sp
        im      0
        im      1
        im      2
        out     (255), a
        out     (c), l
        in      a, (255)
        in      h, (c)

        ld      b, c
        ld      d, 123
        ld      d, (hl)
        ld      e, (ix+2)
        ld      h, (iy-2)
        ld      (hl), l
        ld      (ix+5), b
        ld      (iy-9), c
        ld      (hl), 29
        ld      (ix-4), 28
        ld      (iy+4), 27
        ld      a, (bc)
        ld      a, (de)
        ld      a, (12345)
        ld      (bc), a
        ld      (de), a
        ld      (12347), a
        ld      a, i
        ld      a, r
        ld      i, a
        ld      r, a
        ld      bc, 12345
        ld      de, 12346
        ld      hl, 12347
        ld      sp, 12348
        ld      ix, 12348
        ld      iy, 12349
        ld      hl, (12345)
        ld      bc, (12346)
        ld      de, (12347)
        ld      hl, (12348)
        ld      sp, (12349)
        ld      ix, (12351)
        ld      iy, (12352)
        ld      (12300), hl
        ld      (12301), bc
        ld      (12302), de
        ld      (12303), hl
        ld      (12304), sp
        ld      (12305), ix
        ld      (12306), iy
        ld      sp, hl
        ld      sp, ix
        ld      sp, iy
