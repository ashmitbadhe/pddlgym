(define (problem Perestroika-problem-9-3)
(:domain Perestroika)
(:objects l1 l2 l3 l4 l5 - lvl
r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 r16 r17 r18 r19 r20 r21 r22 r23 r24 r25 r26 r27 r28 r29 r30 r31 r32 r33 r34 r35 r36 r37 r38 r39 r40 r41 r42 r43 - resource
l-1-1 l-1-2 l-1-3 l-1-4 l-1-5 l-1-6 l-1-7 l-1-8 l-1-9 l-2-1 l-2-2 l-2-3 l-2-4 l-2-5 l-2-6 l-2-7 l-2-8 l-2-9 l-3-1 l-3-2 l-3-3 l-3-4 l-3-5 l-3-6 l-3-7 l-3-8 l-3-9 l-4-1 l-4-2 l-4-3 l-4-4 l-4-5 l-4-6 l-4-7 l-4-8 l-4-9 l-5-1 l-5-2 l-5-3 l-5-4 l-5-5 l-5-6 l-5-7 l-5-8 l-5-9 l-6-1 l-6-2 l-6-3 l-6-4 l-6-5 l-6-6 l-6-7 l-6-8 l-6-9 l-7-1 l-7-2 l-7-3 l-7-4 l-7-5 l-7-6 l-7-7 l-7-8 l-7-9 l-8-1 l-8-2 l-8-3 l-8-4 l-8-5 l-8-6 l-8-7 l-8-8 l-8-9 l-9-1 l-9-2 l-9-3 l-9-4 l-9-5 l-9-6 l-9-7 l-9-8 l-9-9 - location)
(:init (alive) (at-agent l-1-1) (level-min l1)
(next l1 l2)
(next l2 l3)
(next l3 l4)
(next l4 l5)
(connected l-1-1 l-2-1)
(connected l-2-1 l-1-1)
(connected l-1-1 l-1-2)
(connected l-1-2 l-1-1)
(free l-1-2)
(connected l-1-2 l-2-2)
(connected l-2-2 l-1-2)
(connected l-1-2 l-1-3)
(connected l-1-3 l-1-2)
(free l-1-3)
(connected l-1-3 l-2-3)
(connected l-2-3 l-1-3)
(connected l-1-3 l-1-4)
(connected l-1-4 l-1-3)
(free l-1-4)
(connected l-1-4 l-2-4)
(connected l-2-4 l-1-4)
(connected l-1-4 l-1-5)
(connected l-1-5 l-1-4)
(free l-1-5)
(connected l-1-5 l-2-5)
(connected l-2-5 l-1-5)
(connected l-1-5 l-1-6)
(connected l-1-6 l-1-5)
(free l-1-6)
(connected l-1-6 l-2-6)
(connected l-2-6 l-1-6)
(connected l-1-6 l-1-7)
(connected l-1-7 l-1-6)
(free l-1-7)
(connected l-1-7 l-2-7)
(connected l-2-7 l-1-7)
(connected l-1-7 l-1-8)
(connected l-1-8 l-1-7)
(free l-1-8)
(connected l-1-8 l-2-8)
(connected l-2-8 l-1-8)
(connected l-1-8 l-1-9)
(connected l-1-9 l-1-8)
(free l-1-9)
(connected l-1-9 l-2-9)
(connected l-2-9 l-1-9)
(free l-2-1)
(connected l-2-1 l-3-1)
(connected l-3-1 l-2-1)
(connected l-2-1 l-2-2)
(connected l-2-2 l-2-1)
(free l-2-2)
(connected l-2-2 l-3-2)
(connected l-3-2 l-2-2)
(connected l-2-2 l-2-3)
(connected l-2-3 l-2-2)
(free l-2-3)
(connected l-2-3 l-3-3)
(connected l-3-3 l-2-3)
(connected l-2-3 l-2-4)
(connected l-2-4 l-2-3)
(free l-2-4)
(connected l-2-4 l-3-4)
(connected l-3-4 l-2-4)
(connected l-2-4 l-2-5)
(connected l-2-5 l-2-4)
(free l-2-5)
(connected l-2-5 l-3-5)
(connected l-3-5 l-2-5)
(connected l-2-5 l-2-6)
(connected l-2-6 l-2-5)
(free l-2-6)
(connected l-2-6 l-3-6)
(connected l-3-6 l-2-6)
(connected l-2-6 l-2-7)
(connected l-2-7 l-2-6)
(free l-2-7)
(connected l-2-7 l-3-7)
(connected l-3-7 l-2-7)
(connected l-2-7 l-2-8)
(connected l-2-8 l-2-7)
(free l-2-8)
(connected l-2-8 l-3-8)
(connected l-3-8 l-2-8)
(connected l-2-8 l-2-9)
(connected l-2-9 l-2-8)
(free l-2-9)
(connected l-2-9 l-3-9)
(connected l-3-9 l-2-9)
(free l-3-1)
(connected l-3-1 l-4-1)
(connected l-4-1 l-3-1)
(connected l-3-1 l-3-2)
(connected l-3-2 l-3-1)
(free l-3-2)
(connected l-3-2 l-4-2)
(connected l-4-2 l-3-2)
(connected l-3-2 l-3-3)
(connected l-3-3 l-3-2)
(free l-3-3)
(connected l-3-3 l-4-3)
(connected l-4-3 l-3-3)
(connected l-3-3 l-3-4)
(connected l-3-4 l-3-3)
(free l-3-4)
(connected l-3-4 l-4-4)
(connected l-4-4 l-3-4)
(connected l-3-4 l-3-5)
(connected l-3-5 l-3-4)
(free l-3-5)
(connected l-3-5 l-4-5)
(connected l-4-5 l-3-5)
(connected l-3-5 l-3-6)
(connected l-3-6 l-3-5)
(free l-3-6)
(connected l-3-6 l-4-6)
(connected l-4-6 l-3-6)
(connected l-3-6 l-3-7)
(connected l-3-7 l-3-6)
(free l-3-7)
(connected l-3-7 l-4-7)
(connected l-4-7 l-3-7)
(connected l-3-7 l-3-8)
(connected l-3-8 l-3-7)
(free l-3-8)
(connected l-3-8 l-4-8)
(connected l-4-8 l-3-8)
(connected l-3-8 l-3-9)
(connected l-3-9 l-3-8)
(free l-3-9)
(connected l-3-9 l-4-9)
(connected l-4-9 l-3-9)
(free l-4-1)
(connected l-4-1 l-5-1)
(connected l-5-1 l-4-1)
(connected l-4-1 l-4-2)
(connected l-4-2 l-4-1)
(free l-4-2)
(connected l-4-2 l-5-2)
(connected l-5-2 l-4-2)
(connected l-4-2 l-4-3)
(connected l-4-3 l-4-2)
(free l-4-3)
(connected l-4-3 l-5-3)
(connected l-5-3 l-4-3)
(connected l-4-3 l-4-4)
(connected l-4-4 l-4-3)
(free l-4-4)
(connected l-4-4 l-5-4)
(connected l-5-4 l-4-4)
(connected l-4-4 l-4-5)
(connected l-4-5 l-4-4)
(free l-4-5)
(connected l-4-5 l-5-5)
(connected l-5-5 l-4-5)
(connected l-4-5 l-4-6)
(connected l-4-6 l-4-5)
(free l-4-6)
(connected l-4-6 l-5-6)
(connected l-5-6 l-4-6)
(connected l-4-6 l-4-7)
(connected l-4-7 l-4-6)
(free l-4-7)
(connected l-4-7 l-5-7)
(connected l-5-7 l-4-7)
(connected l-4-7 l-4-8)
(connected l-4-8 l-4-7)
(free l-4-8)
(connected l-4-8 l-5-8)
(connected l-5-8 l-4-8)
(connected l-4-8 l-4-9)
(connected l-4-9 l-4-8)
(free l-4-9)
(connected l-4-9 l-5-9)
(connected l-5-9 l-4-9)
(free l-5-1)
(connected l-5-1 l-6-1)
(connected l-6-1 l-5-1)
(connected l-5-1 l-5-2)
(connected l-5-2 l-5-1)
(free l-5-2)
(connected l-5-2 l-6-2)
(connected l-6-2 l-5-2)
(connected l-5-2 l-5-3)
(connected l-5-3 l-5-2)
(free l-5-3)
(connected l-5-3 l-6-3)
(connected l-6-3 l-5-3)
(connected l-5-3 l-5-4)
(connected l-5-4 l-5-3)
(free l-5-4)
(connected l-5-4 l-6-4)
(connected l-6-4 l-5-4)
(connected l-5-4 l-5-5)
(connected l-5-5 l-5-4)
(free l-5-5)
(connected l-5-5 l-6-5)
(connected l-6-5 l-5-5)
(connected l-5-5 l-5-6)
(connected l-5-6 l-5-5)
(free l-5-6)
(connected l-5-6 l-6-6)
(connected l-6-6 l-5-6)
(connected l-5-6 l-5-7)
(connected l-5-7 l-5-6)
(free l-5-7)
(connected l-5-7 l-6-7)
(connected l-6-7 l-5-7)
(connected l-5-7 l-5-8)
(connected l-5-8 l-5-7)
(free l-5-8)
(connected l-5-8 l-6-8)
(connected l-6-8 l-5-8)
(connected l-5-8 l-5-9)
(connected l-5-9 l-5-8)
(free l-5-9)
(connected l-5-9 l-6-9)
(connected l-6-9 l-5-9)
(free l-6-1)
(connected l-6-1 l-7-1)
(connected l-7-1 l-6-1)
(connected l-6-1 l-6-2)
(connected l-6-2 l-6-1)
(free l-6-2)
(connected l-6-2 l-7-2)
(connected l-7-2 l-6-2)
(connected l-6-2 l-6-3)
(connected l-6-3 l-6-2)
(free l-6-3)
(connected l-6-3 l-7-3)
(connected l-7-3 l-6-3)
(connected l-6-3 l-6-4)
(connected l-6-4 l-6-3)
(free l-6-4)
(connected l-6-4 l-7-4)
(connected l-7-4 l-6-4)
(connected l-6-4 l-6-5)
(connected l-6-5 l-6-4)
(free l-6-5)
(connected l-6-5 l-7-5)
(connected l-7-5 l-6-5)
(connected l-6-5 l-6-6)
(connected l-6-6 l-6-5)
(free l-6-6)
(connected l-6-6 l-7-6)
(connected l-7-6 l-6-6)
(connected l-6-6 l-6-7)
(connected l-6-7 l-6-6)
(free l-6-7)
(connected l-6-7 l-7-7)
(connected l-7-7 l-6-7)
(connected l-6-7 l-6-8)
(connected l-6-8 l-6-7)
(free l-6-8)
(connected l-6-8 l-7-8)
(connected l-7-8 l-6-8)
(connected l-6-8 l-6-9)
(connected l-6-9 l-6-8)
(free l-6-9)
(connected l-6-9 l-7-9)
(connected l-7-9 l-6-9)
(free l-7-1)
(connected l-7-1 l-8-1)
(connected l-8-1 l-7-1)
(connected l-7-1 l-7-2)
(connected l-7-2 l-7-1)
(free l-7-2)
(connected l-7-2 l-8-2)
(connected l-8-2 l-7-2)
(connected l-7-2 l-7-3)
(connected l-7-3 l-7-2)
(free l-7-3)
(connected l-7-3 l-8-3)
(connected l-8-3 l-7-3)
(connected l-7-3 l-7-4)
(connected l-7-4 l-7-3)
(free l-7-4)
(connected l-7-4 l-8-4)
(connected l-8-4 l-7-4)
(connected l-7-4 l-7-5)
(connected l-7-5 l-7-4)
(free l-7-5)
(connected l-7-5 l-8-5)
(connected l-8-5 l-7-5)
(connected l-7-5 l-7-6)
(connected l-7-6 l-7-5)
(free l-7-6)
(connected l-7-6 l-8-6)
(connected l-8-6 l-7-6)
(connected l-7-6 l-7-7)
(connected l-7-7 l-7-6)
(free l-7-7)
(connected l-7-7 l-8-7)
(connected l-8-7 l-7-7)
(connected l-7-7 l-7-8)
(connected l-7-8 l-7-7)
(free l-7-8)
(connected l-7-8 l-8-8)
(connected l-8-8 l-7-8)
(connected l-7-8 l-7-9)
(connected l-7-9 l-7-8)
(free l-7-9)
(connected l-7-9 l-8-9)
(connected l-8-9 l-7-9)
(free l-8-1)
(connected l-8-1 l-9-1)
(connected l-9-1 l-8-1)
(connected l-8-1 l-8-2)
(connected l-8-2 l-8-1)
(free l-8-2)
(connected l-8-2 l-9-2)
(connected l-9-2 l-8-2)
(connected l-8-2 l-8-3)
(connected l-8-3 l-8-2)
(free l-8-3)
(connected l-8-3 l-9-3)
(connected l-9-3 l-8-3)
(connected l-8-3 l-8-4)
(connected l-8-4 l-8-3)
(free l-8-4)
(connected l-8-4 l-9-4)
(connected l-9-4 l-8-4)
(connected l-8-4 l-8-5)
(connected l-8-5 l-8-4)
(free l-8-5)
(connected l-8-5 l-9-5)
(connected l-9-5 l-8-5)
(connected l-8-5 l-8-6)
(connected l-8-6 l-8-5)
(free l-8-6)
(connected l-8-6 l-9-6)
(connected l-9-6 l-8-6)
(connected l-8-6 l-8-7)
(connected l-8-7 l-8-6)
(free l-8-7)
(connected l-8-7 l-9-7)
(connected l-9-7 l-8-7)
(connected l-8-7 l-8-8)
(connected l-8-8 l-8-7)
(free l-8-8)
(connected l-8-8 l-9-8)
(connected l-9-8 l-8-8)
(connected l-8-8 l-8-9)
(connected l-8-9 l-8-8)
(free l-8-9)
(connected l-8-9 l-9-9)
(connected l-9-9 l-8-9)
(free l-9-1)
(connected l-9-1 l-9-2)
(connected l-9-2 l-9-1)
(free l-9-2)
(connected l-9-2 l-9-3)
(connected l-9-3 l-9-2)
(free l-9-3)
(connected l-9-3 l-9-4)
(connected l-9-4 l-9-3)
(free l-9-4)
(connected l-9-4 l-9-5)
(connected l-9-5 l-9-4)
(free l-9-5)
(connected l-9-5 l-9-6)
(connected l-9-6 l-9-5)
(free l-9-6)
(connected l-9-6 l-9-7)
(connected l-9-7 l-9-6)
(free l-9-7)
(connected l-9-7 l-9-8)
(connected l-9-8 l-9-7)
(free l-9-8)
(connected l-9-8 l-9-9)
(connected l-9-9 l-9-8)
(free l-9-9)
(solid l-1-1)
(accessible l-1-1)
(level-max l-1-2 l4)
(level l-1-2 l2)
(accessible l-1-2)
(solid l-1-3)
(accessible l-1-3)
(at-res r1 l-1-3)
(solid l-1-4)
(accessible l-1-4)
(at-res r2 l-1-4)
(level-max l-1-5 l5)
(level l-1-5 l2)
(accessible l-1-5)
(level-max l-1-6 l4)
(level l-1-6 l4)
(accessible l-1-6)
(solid l-1-7)
(accessible l-1-7)
(at-res r3 l-1-7)
(solid l-1-8)
(accessible l-1-8)
(at-res r4 l-1-8)
(solid l-1-9)
(accessible l-1-9)
(at-res r5 l-1-9)
(level-max l-2-1 l5)
(level l-2-1 l1)
(accessible l-2-1)
(level-max l-2-2 l1)
(level l-2-2 l1)
(accessible l-2-2)
(solid l-2-3)
(accessible l-2-3)
(at-res r6 l-2-3)
(solid l-2-4)
(accessible l-2-4)
(at-res r7 l-2-4)
(solid l-2-5)
(accessible l-2-5)
(at-res r8 l-2-5)
(solid l-2-6)
(accessible l-2-6)
(at-res r9 l-2-6)
(level-max l-2-7 l5)
(level l-2-7 l3)
(accessible l-2-7)
(level-max l-2-8 l3)
(level l-2-8 l2)
(accessible l-2-8)
(solid l-2-9)
(accessible l-2-9)
(at-res r10 l-2-9)
(solid l-3-1)
(accessible l-3-1)
(at-res r11 l-3-1)
(level-max l-3-2 l3)
(level l-3-2 l2)
(accessible l-3-2)
(solid l-3-3)
(accessible l-3-3)
(at-res r12 l-3-3)
(level-max l-3-4 l4)
(level l-3-4 l2)
(accessible l-3-4)
(level-max l-3-5 l3)
(none l-3-5)
(solid l-3-6)
(accessible l-3-6)
(at-res r13 l-3-6)
(level-max l-3-7 l2)
(none l-3-7)
(solid l-3-8)
(accessible l-3-8)
(at-res r14 l-3-8)
(solid l-3-9)
(accessible l-3-9)
(at-res r15 l-3-9)
(level-max l-4-1 l4)
(level l-4-1 l1)
(accessible l-4-1)
(solid l-4-2)
(accessible l-4-2)
(at-res r16 l-4-2)
(level-max l-4-3 l1)
(none l-4-3)
(level-max l-4-4 l1)
(none l-4-4)
(solid l-4-5)
(accessible l-4-5)
(at-res r17 l-4-5)
(level-max l-4-6 l2)
(level l-4-6 l1)
(accessible l-4-6)
(solid l-4-7)
(accessible l-4-7)
(at-res r18 l-4-7)
(level-max l-4-8 l3)
(level l-4-8 l2)
(accessible l-4-8)
(solid l-4-9)
(accessible l-4-9)
(at-res r19 l-4-9)
(level-max l-5-1 l2)
(level l-5-1 l2)
(accessible l-5-1)
(solid l-5-2)
(accessible l-5-2)
(at-res r20 l-5-2)
(solid l-5-3)
(accessible l-5-3)
(at-res r21 l-5-3)
(solid l-5-4)
(accessible l-5-4)
(at-res r22 l-5-4)
(level-max l-5-5 l1)
(none l-5-5)
(level-max l-5-6 l4)
(none l-5-6)
(solid l-5-7)
(accessible l-5-7)
(at-res r23 l-5-7)
(level-max l-5-8 l5)
(level l-5-8 l5)
(accessible l-5-8)
(solid l-5-9)
(accessible l-5-9)
(at-res r24 l-5-9)
(solid l-6-1)
(accessible l-6-1)
(at-res r25 l-6-1)
(level-max l-6-2 l2)
(level l-6-2 l1)
(accessible l-6-2)
(solid l-6-3)
(accessible l-6-3)
(at-res r26 l-6-3)
(level-max l-6-4 l4)
(level l-6-4 l2)
(accessible l-6-4)
(level-max l-6-5 l4)
(level l-6-5 l2)
(accessible l-6-5)
(level-max l-6-6 l5)
(level l-6-6 l3)
(accessible l-6-6)
(level-max l-6-7 l5)
(level l-6-7 l1)
(accessible l-6-7)
(solid l-6-8)
(accessible l-6-8)
(at-res r27 l-6-8)
(level-max l-6-9 l5)
(level l-6-9 l1)
(accessible l-6-9)
(level-max l-7-1 l4)
(none l-7-1)
(solid l-7-2)
(accessible l-7-2)
(at-res r28 l-7-2)
(solid l-7-3)
(accessible l-7-3)
(at-res r29 l-7-3)
(solid l-7-4)
(accessible l-7-4)
(at-res r30 l-7-4)
(level-max l-7-5 l2)
(level l-7-5 l1)
(accessible l-7-5)
(solid l-7-6)
(accessible l-7-6)
(at-res r31 l-7-6)
(level-max l-7-7 l2)
(level l-7-7 l1)
(accessible l-7-7)
(level-max l-7-8 l1)
(level l-7-8 l1)
(accessible l-7-8)
(solid l-7-9)
(accessible l-7-9)
(at-res r32 l-7-9)
(level-max l-8-1 l1)
(none l-8-1)
(solid l-8-2)
(accessible l-8-2)
(at-res r33 l-8-2)
(level-max l-8-3 l5)
(none l-8-3)
(solid l-8-4)
(accessible l-8-4)
(at-res r34 l-8-4)
(level-max l-8-5 l3)
(level l-8-5 l3)
(accessible l-8-5)
(solid l-8-6)
(accessible l-8-6)
(at-res r35 l-8-6)
(solid l-8-7)
(accessible l-8-7)
(at-res r36 l-8-7)
(solid l-8-8)
(accessible l-8-8)
(at-res r37 l-8-8)
(level-max l-8-9 l2)
(none l-8-9)
(solid l-9-1)
(accessible l-9-1)
(at-res r38 l-9-1)
(solid l-9-2)
(accessible l-9-2)
(at-res r39 l-9-2)
(level-max l-9-3 l1)
(level l-9-3 l1)
(accessible l-9-3)
(solid l-9-4)
(accessible l-9-4)
(at-res r40 l-9-4)
(solid l-9-5)
(accessible l-9-5)
(at-res r41 l-9-5)
(solid l-9-6)
(accessible l-9-6)
(at-res r42 l-9-6)
(level-max l-9-7 l4)
(level l-9-7 l2)
(accessible l-9-7)
(solid l-9-8)
(accessible l-9-8)
(at-res r43 l-9-8)
(level-max l-9-9 l4)
(level l-9-9 l2)
(accessible l-9-9)
)
(:goal (and (alive)
(taken r1)
(taken r2)
(taken r3)
(taken r4)
(taken r5)
(taken r6)
(taken r7)
(taken r8)
(taken r9)
(taken r10)
(taken r11)
(taken r12)
(taken r13)
(taken r14)
(taken r15)
(taken r16)
(taken r17)
(taken r18)
(taken r19)
(taken r20)
(taken r21)
(taken r22)
(taken r23)
(taken r24)
(taken r25)
(taken r26)
(taken r27)
(taken r28)
(taken r29)
(taken r30)
(taken r31)
(taken r32)
(taken r33)
(taken r34)
(taken r35)
(taken r36)
(taken r37)
(taken r38)
(taken r39)
(taken r40)
(taken r41)
(taken r42)
(taken r43)
))
)
