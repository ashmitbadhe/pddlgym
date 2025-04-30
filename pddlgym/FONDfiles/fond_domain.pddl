(define (domain auv)
(:requirements :non-deterministic)

(:predicates 
             (selected-move-ship-free_s1_l-2-2_l-2-1)
             (enab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (notsel-move-ship-free_s1_l-2-2_l-2-1)
             (wenab-move-ship-free_s1_l-2-2_l-2-1)
             (selected-move-ship-free_s1_l-2-2_l-2-3)
             (enab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (notsel-move-ship-free_s1_l-2-2_l-2-3)
             (wenab-move-ship-free_s1_l-2-2_l-2-3)
             (selected-move-ship-free_s1_l-2-1_l-2-2)
             (enab-move-ship-free_s1_l-2-1_l-2-2)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (notsel-move-ship-free_s1_l-2-1_l-2-2)
             (wenab-move-ship-free_s1_l-2-1_l-2-2)
             (selected-move-ship-free_s1_l-2-3_l-2-2)
             (enab-move-ship-free_s1_l-2-3_l-2-2)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (notsel-move-ship-free_s1_l-2-3_l-2-2)
             (wenab-move-ship-free_s1_l-2-3_l-2-2)
             (selected-move-ship-auv_s1_l-2-2_l-2-1_a)
             (enab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (notsel-move-ship-auv_s1_l-2-2_l-2-1_a)
             (wenab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (selected-move-ship-auv_s1_l-2-2_l-2-3_a)
             (enab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (notsel-move-ship-auv_s1_l-2-2_l-2-3_a)
             (wenab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (selected-move-ship-auv_s1_l-2-1_l-2-2_a)
             (enab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (notsel-move-ship-auv_s1_l-2-1_l-2-2_a)
             (wenab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (selected-move-ship-auv_s1_l-2-3_l-2-2_a)
             (enab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (notsel-move-ship-auv_s1_l-2-3_l-2-2_a)
             (wenab-move-ship-auv_s1_l-2-3_l-2-2_a)
             
             (free_l-2-3)
             (free_l-2-1)
             (at_a_l-1-2)
             (free_l-1-1)
             (at_a_l-2-2)
             (free_l-3-1)
             (at_a_l-1-3)
             (at_a_l-3-2)
             (at_a_l-2-1)
             (operational_a)
             (free_l-3-3)
             (at_s1_l-2-2)
             (free_l-1-2)
             (sampled_r1)
             (free_l-1-3)
             (at_a_l-2-3)
             (free_l-3-2)
             (at_s1_l-2-3)
             (free_l-2-2)
             (at_a_l-3-1)
             (at_a_l-1-1)
             (at_s1_l-2-1)
             (at_a_l-3-3)
             (act-turn)
             (ev-turn)
             (ev-turn2)
)



(:action move_a_l-1-2_l-1-1
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-1-1)
                    (at_a_l-1-2)
              )
:effect (and 
             (ev-turn)
             (free_l-1-2)
             (at_a_l-1-1)
             (not (act-turn))
             (not (free_l-1-1))
             (not (at_a_l-1-2)))
)

(:action move_a_l-1-2_l-1-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-1-3)
                    (at_a_l-1-2)
              )
:effect (and 
             (ev-turn)
             (at_a_l-1-3)
             (free_l-1-2)
             (not (act-turn))
             (not (free_l-1-3))
             (not (at_a_l-1-2)))
)

(:action move_a_l-1-1_l-2-1
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-2-1)
                    (at_a_l-1-1)
              )
:effect (and 
             (ev-turn)
             (at_a_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (free_l-1-1)
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (not (act-turn))
             (not (free_l-2-1))
             (not (at_a_l-1-1))
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-1_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-1_a))))
             )
)

(:action move_a_l-1-1_l-1-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (operational_a)
                    (free_l-1-2)
                    (at_a_l-1-1)
              )
:effect (and 
             (ev-turn)
             (free_l-1-1)
             (at_a_l-1-2)
             (not (act-turn))
             (not (free_l-1-2))
             (not (at_a_l-1-1)))
)

(:action move_a_l-1-3_l-2-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-2-3)
                    (at_a_l-1-3)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (at_a_l-2-3)
             (free_l-1-3)
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (act-turn))
             (not (free_l-2-3))
             (not (at_a_l-1-3))
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-3_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-3_a))))
             )
)

(:action move_a_l-1-3_l-1-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-1-3)
                    (free_l-1-2)
              )
:effect (and 
             (ev-turn)
             (free_l-1-3)
             (at_a_l-1-2)
             (not (act-turn))
             (not (at_a_l-1-3))
             (not (free_l-1-2)))
)

(:action move_a_l-1-2_l-2-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-2-2)
                    (at_a_l-1-2)
              )
:effect (and 
             (at_a_l-2-2)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (ev-turn)
             (free_l-1-2)
             (not (act-turn))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (at_a_l-1-2))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (free_l-2-2))
             (when (and (operational_a) (at_s1_l-2-1))
                   (and (enab-move-ship-auv_s1_l-2-1_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-1_l-2-2_a))))
             
             (when (and (operational_a) (at_s1_l-2-3))
                   (and (enab-move-ship-auv_s1_l-2-3_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-3_l-2-2_a))))
             )
)

(:action move_a_l-2-1_l-1-1
:parameters ()
:precondition (and 
                    (at_a_l-2-1)
                    (act-turn)
                    (operational_a)
                    (free_l-1-1)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (free_l-2-1)
             (at_a_l-1-1)
             (not (at_a_l-2-1))
             (not (act-turn))
             (not (free_l-1-1))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-1) (not (disab-move-ship-free_s1_l-2-2_l-2-1))))
             )
)

(:action move_a_l-2-1_l-3-1
:parameters ()
:precondition (and 
                    (at_a_l-2-1)
                    (act-turn)
                    (operational_a)
                    (free_l-3-1)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (at_a_l-3-1)
             (free_l-2-1)
             (not (at_a_l-2-1))
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (free_l-3-1))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-1) (not (disab-move-ship-free_s1_l-2-2_l-2-1))))
             )
)

(:action move_a_l-2-1_l-2-2
:parameters ()
:precondition (and 
                    (at_a_l-2-1)
                    (act-turn)
                    (operational_a)
                    (free_l-2-2)
              )
:effect (and 
             (at_a_l-2-2)
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (free_l-2-1)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (ev-turn)
             (not (at_a_l-2-1))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (act-turn))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (free_l-2-2))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-1) (not (disab-move-ship-free_s1_l-2-2_l-2-1))))
             
             (when (and (operational_a) (at_s1_l-2-1))
                   (and (enab-move-ship-auv_s1_l-2-1_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-1_l-2-2_a))))
             
             (when (and (operational_a) (at_s1_l-2-3))
                   (and (enab-move-ship-auv_s1_l-2-3_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-3_l-2-2_a))))
             )
)

(:action move_a_l-2-3_l-1-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-2-3)
                    (free_l-1-3)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (free_l-2-3)
             (at_a_l-1-3)
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (at_a_l-2-3))
             (not (free_l-1-3))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-3) (not (disab-move-ship-free_s1_l-2-2_l-2-3))))
             )
)

(:action move_a_l-2-3_l-3-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-2-3)
                    (free_l-3-3)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (free_l-2-3)
             (at_a_l-3-3)
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (at_a_l-2-3))
             (not (free_l-3-3))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-3) (not (disab-move-ship-free_s1_l-2-2_l-2-3))))
             )
)

(:action move_a_l-2-3_l-2-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-2-3)
                    (free_l-2-2)
              )
:effect (and 
             (at_a_l-2-2)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (ev-turn)
             (free_l-2-3)
             (not (act-turn))
             (not (at_a_l-2-3))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (free_l-2-2))
             (when (and (at_s1_l-2-2))
                   (and (enab-move-ship-free_s1_l-2-2_l-2-3) (not (disab-move-ship-free_s1_l-2-2_l-2-3))))
             
             (when (and (operational_a) (at_s1_l-2-1))
                   (and (enab-move-ship-auv_s1_l-2-1_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-1_l-2-2_a))))
             
             (when (and (operational_a) (at_s1_l-2-3))
                   (and (enab-move-ship-auv_s1_l-2-3_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-3_l-2-2_a))))
             )
)

(:action move_a_l-2-2_l-2-1
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (operational_a)
                    (act-turn)
                    (free_l-2-1)
              )
:effect (and 
             (at_a_l-2-1)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (ev-turn)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (not (at_a_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (free_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (when (and (at_s1_l-2-1))
                   (and (enab-move-ship-free_s1_l-2-1_l-2-2) (not (disab-move-ship-free_s1_l-2-1_l-2-2))))
             
             (when (and (at_s1_l-2-3))
                   (and (enab-move-ship-free_s1_l-2-3_l-2-2) (not (disab-move-ship-free_s1_l-2-3_l-2-2))))
             
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-1_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-1_a))))
             )
)

(:action move_a_l-2-2_l-2-3
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (operational_a)
                    (act-turn)
                    (free_l-2-3)
              )
:effect (and 
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (at_a_l-2-3)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (not (at_a_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (free_l-2-3))
             (when (and (at_s1_l-2-1))
                   (and (enab-move-ship-free_s1_l-2-1_l-2-2) (not (disab-move-ship-free_s1_l-2-1_l-2-2))))
             
             (when (and (at_s1_l-2-3))
                   (and (enab-move-ship-free_s1_l-2-3_l-2-2) (not (disab-move-ship-free_s1_l-2-3_l-2-2))))
             
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-3_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-3_a))))
             )
)

(:action move_a_l-2-2_l-3-2
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (operational_a)
                    (act-turn)
                    (free_l-3-2)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (at_a_l-3-2)
             (not (at_a_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (free_l-3-2))
             (when (and (at_s1_l-2-1))
                   (and (enab-move-ship-free_s1_l-2-1_l-2-2) (not (disab-move-ship-free_s1_l-2-1_l-2-2))))
             
             (when (and (at_s1_l-2-3))
                   (and (enab-move-ship-free_s1_l-2-3_l-2-2) (not (disab-move-ship-free_s1_l-2-3_l-2-2))))
             )
)

(:action move_a_l-2-2_l-1-2
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (operational_a)
                    (act-turn)
                    (free_l-1-2)
              )
:effect (and 
             (at_a_l-1-2)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (ev-turn)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (not (at_a_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (act-turn))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (free_l-1-2))
             (when (and (at_s1_l-2-1))
                   (and (enab-move-ship-free_s1_l-2-1_l-2-2) (not (disab-move-ship-free_s1_l-2-1_l-2-2))))
             
             (when (and (at_s1_l-2-3))
                   (and (enab-move-ship-free_s1_l-2-3_l-2-2) (not (disab-move-ship-free_s1_l-2-3_l-2-2))))
             )
)

(:action move_a_l-3-1_l-2-1
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-3-1)
                    (free_l-2-1)
              )
:effect (and 
             (ev-turn)
             (at_a_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (free_l-3-1)
             (not (act-turn))
             (not (at_a_l-3-1))
             (not (free_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-1_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-1_a))))
             )
)

(:action move_a_l-3-1_l-3-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-3-1)
                    (free_l-3-2)
              )
:effect (and 
             (ev-turn)
             (free_l-3-1)
             (at_a_l-3-2)
             (not (act-turn))
             (not (at_a_l-3-1))
             (not (free_l-3-2)))
)

(:action move_a_l-3-3_l-2-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-2-3)
                    (at_a_l-3-3)
              )
:effect (and 
             (ev-turn)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (at_a_l-2-3)
             (free_l-3-3)
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (act-turn))
             (not (free_l-2-3))
             (not (at_a_l-3-3))
             (when (and (operational_a) (at_s1_l-2-2))
                   (and (enab-move-ship-auv_s1_l-2-2_l-2-3_a) (not (disab-move-ship-auv_s1_l-2-2_l-2-3_a))))
             )
)

(:action move_a_l-3-3_l-3-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-3-2)
                    (at_a_l-3-3)
              )
:effect (and 
             (ev-turn)
             (at_a_l-3-2)
             (free_l-3-3)
             (not (free_l-3-2))
             (not (act-turn))
             (not (at_a_l-3-3)))
)

(:action move_a_l-3-2_l-3-1
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-3-1)
                    (at_a_l-3-2)
              )
:effect (and 
             (ev-turn)
             (at_a_l-3-1)
             (free_l-3-2)
             (not (free_l-3-1))
             (not (act-turn))
             (not (at_a_l-3-2)))
)

(:action move_a_l-3-2_l-3-3
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-3-2)
                    (free_l-3-3)
              )
:effect (and 
             (ev-turn)
             (free_l-3-2)
             (at_a_l-3-3)
             (not (act-turn))
             (not (at_a_l-3-2))
             (not (free_l-3-3)))
)

(:action move_a_l-3-2_l-2-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (free_l-2-2)
                    (at_a_l-3-2)
              )
:effect (and 
             (at_a_l-2-2)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (ev-turn)
             (free_l-3-2)
             (not (act-turn))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (free_l-2-2))
             (not (at_a_l-3-2))
             (when (and (operational_a) (at_s1_l-2-1))
                   (and (enab-move-ship-auv_s1_l-2-1_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-1_l-2-2_a))))
             
             (when (and (operational_a) (at_s1_l-2-3))
                   (and (enab-move-ship-auv_s1_l-2-3_l-2-2_a) (not (disab-move-ship-auv_s1_l-2-3_l-2-2_a))))
             )
)

(:action sample_a_r1_l-3-2
:parameters ()
:precondition (and 
                    (operational_a)
                    (act-turn)
                    (at_a_l-3-2)
              )
:effect (and 
             (ev-turn)
             (sampled_r1)
             (not (act-turn)))
)


;;;;;;;;;;;
;;; noop
;;;;;;;;;;;

(:action noop
:parameters ()
:precondition (and (act-turn))
:effect (and
             (not (act-turn))
             (ev-turn)
        )
)

;;;;;;;;;;;
;;; selector
;;;;;;;;;;;

(:action selector
:parameters ()
:precondition (and (ev-turn))
:effect (oneof (and (not (ev-turn))(act-turn))
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-auv_s1_l-2-2_l-2-3_a))
                    (selected-move-ship-auv_s1_l-2-2_l-2-3_a)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-auv_s1_l-2-1_l-2-2_a))
                    (selected-move-ship-auv_s1_l-2-1_l-2-2_a)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-auv_s1_l-2-2_l-2-1_a))
                    (selected-move-ship-auv_s1_l-2-2_l-2-1_a)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-free_s1_l-2-2_l-2-3))
                    (selected-move-ship-free_s1_l-2-2_l-2-3)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-free_s1_l-2-3_l-2-2))
                    (selected-move-ship-free_s1_l-2-3_l-2-2)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-free_s1_l-2-2_l-2-1))
                    (selected-move-ship-free_s1_l-2-2_l-2-1)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-free_s1_l-2-1_l-2-2))
                    (selected-move-ship-free_s1_l-2-1_l-2-2)
                    )
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    (not (notsel-move-ship-auv_s1_l-2-3_l-2-2_a))
                    (selected-move-ship-auv_s1_l-2-3_l-2-2_a)
                    )
               )
)

;;;;;;;;;;;
;;; events
;;;;;;;;;;;


(:action move-ship-free_s1_l-2-2_l-2-1
:parameters ()
:precondition (and 
                    (selected-move-ship-free_s1_l-2-2_l-2-1)
                    (enab-move-ship-free_s1_l-2-2_l-2-1)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (at_s1_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (wenab-move-ship-free_s1_l-2-1_l-2-2)
             (notsel-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (free_l-2-2)
             (not (wenab-move-ship-free_s1_l-2-2_l-2-3))
             (not (selected-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-1))
             (not (at_s1_l-2-2))
             (not (free_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (when (and (at_s1_l-2-3))
                   (and (wenab-move-ship-free_s1_l-2-3_l-2-2)))
             
             (when (and (at_a_l-2-2) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-1_l-2-2_a)))
             )
)

(:action move-ship-free_s1_l-2-2_l-2-3
:parameters ()
:precondition (and 
                    (enab-move-ship-free_s1_l-2-2_l-2-3)
                    (selected-move-ship-free_s1_l-2-2_l-2-3)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (wenab-move-ship-free_s1_l-2-3_l-2-2)
             (at_s1_l-2-3)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (notsel-move-ship-free_s1_l-2-2_l-2-3)
             (free_l-2-2)
             (not (wenab-move-ship-free_s1_l-2-2_l-2-3))
             (not (selected-move-ship-free_s1_l-2-2_l-2-3))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-1))
             (not (at_s1_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (free_l-2-3))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (when (and (at_s1_l-2-1))
                   (and (wenab-move-ship-free_s1_l-2-1_l-2-2)))
             
             (when (and (at_a_l-2-2) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-3_l-2-2_a)))
             )
)

(:action move-ship-free_s1_l-2-1_l-2-2
:parameters ()
:precondition (and 
                    (enab-move-ship-free_s1_l-2-1_l-2-2)
                    (selected-move-ship-free_s1_l-2-1_l-2-2)
              )
:effect (and 
             (wenab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (at_s1_l-2-2)
             (free_l-2-1)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (notsel-move-ship-free_s1_l-2-1_l-2-2)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-3_l-2-2))
             (not (at_s1_l-2-1))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (wenab-move-ship-free_s1_l-2-1_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (selected-move-ship-free_s1_l-2-1_l-2-2))
             (not (free_l-2-2))
             (when (and (free_l-2-3))
                   (and (wenab-move-ship-free_s1_l-2-2_l-2-3)))
             
             (when (and (at_a_l-2-1) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-1_a)))
             
             (when (and (operational_a) (at_a_l-2-3))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-3_a)))
             )
)

(:action move-ship-free_s1_l-2-3_l-2-2
:parameters ()
:precondition (and 
                    (selected-move-ship-free_s1_l-2-3_l-2-2)
                    (enab-move-ship-free_s1_l-2-3_l-2-2)
              )
:effect (and 
             (wenab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (at_s1_l-2-2)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (notsel-move-ship-free_s1_l-2-3_l-2-2)
             (free_l-2-3)
             (not (wenab-move-ship-free_s1_l-2-3_l-2-2))
             (not (at_s1_l-2-3))
             (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (selected-move-ship-free_s1_l-2-3_l-2-2))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (wenab-move-ship-free_s1_l-2-1_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (free_l-2-2))
             (when (and (free_l-2-1))
                   (and (wenab-move-ship-free_s1_l-2-2_l-2-1)))
             
             (when (and (at_a_l-2-1) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-1_a)))
             
             (when (and (operational_a) (at_a_l-2-3))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-3_a)))
             )
)

(:action move-ship-auv_s1_l-2-2_l-2-1_a
:parameters ()
:precondition (and 
                    (selected-move-ship-auv_s1_l-2-2_l-2-1_a)
                    (enab-move-ship-auv_s1_l-2-2_l-2-1_a)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (at_s1_l-2-1)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (wenab-move-ship-free_s1_l-2-1_l-2-2)
             (notsel-move-ship-auv_s1_l-2-2_l-2-1_a)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (not (operational_a))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-3))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (at_s1_l-2-2))
             (not (selected-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (free_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (when (and (at_s1_l-2-3))
                   (and (wenab-move-ship-free_s1_l-2-3_l-2-2)))
             
             (when (and (at_a_l-2-2) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-1_l-2-2_a)))
             )
)

(:action move-ship-auv_s1_l-2-2_l-2-3_a
:parameters ()
:precondition (and 
                    (selected-move-ship-auv_s1_l-2-2_l-2-3_a)
                    (enab-move-ship-auv_s1_l-2-2_l-2-3_a)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (notsel-move-ship-auv_s1_l-2-2_l-2-3_a)
             (wenab-move-ship-free_s1_l-2-3_l-2-2)
             (at_s1_l-2-3)
             (disab-move-ship-free_s1_l-2-2_l-2-3)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (free_l-2-2)
             (not (selected-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (operational_a))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-3))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (at_s1_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-free_s1_l-2-2_l-2-1))
             (not (enab-move-ship-free_s1_l-2-2_l-2-3))
             (not (free_l-2-3))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (when (and (at_s1_l-2-1))
                   (and (wenab-move-ship-free_s1_l-2-1_l-2-2)))
             
             (when (and (at_a_l-2-2) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-3_l-2-2_a)))
             )
)

(:action move-ship-auv_s1_l-2-1_l-2-2_a
:parameters ()
:precondition (and 
                    (enab-move-ship-auv_s1_l-2-1_l-2-2_a)
                    (selected-move-ship-auv_s1_l-2-1_l-2-2_a)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (notsel-move-ship-auv_s1_l-2-1_l-2-2_a)
             (wenab-move-ship-free_s1_l-2-2_l-2-1)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (at_s1_l-2-2)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (free_l-2-1)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (operational_a))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-3_l-2-2))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (at_s1_l-2-1))
             (not (wenab-move-ship-free_s1_l-2-1_l-2-2))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (selected-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (free_l-2-2))
             (when (and (free_l-2-3))
                   (and (wenab-move-ship-free_s1_l-2-2_l-2-3)))
             
             (when (and (at_a_l-2-1) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-1_a)))
             
             (when (and (operational_a) (at_a_l-2-3))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-3_a)))
             )
)

(:action move-ship-auv_s1_l-2-3_l-2-2_a
:parameters ()
:precondition (and 
                    (enab-move-ship-auv_s1_l-2-3_l-2-2_a)
                    (selected-move-ship-auv_s1_l-2-3_l-2-2_a)
              )
:effect (and 
             (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
             (wenab-move-ship-free_s1_l-2-2_l-2-3)
             (notsel-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
             (disab-move-ship-free_s1_l-2-1_l-2-2)
             (at_s1_l-2-2)
             (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
             (disab-move-ship-free_s1_l-2-3_l-2-2)
             (free_l-2-3)
             (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (operational_a))
             (not (enab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (selected-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-3_l-2-2))
             (not (at_s1_l-2-3))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-1_a))
             (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (wenab-move-ship-free_s1_l-2-1_l-2-2))
             (not (enab-move-ship-free_s1_l-2-3_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
             (not (enab-move-ship-auv_s1_l-2-3_l-2-2_a))
             (not (enab-move-ship-free_s1_l-2-1_l-2-2))
             (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (enab-move-ship-auv_s1_l-2-2_l-2-3_a))
             (not (free_l-2-2))
             (when (and (free_l-2-1))
                   (and (wenab-move-ship-free_s1_l-2-2_l-2-1)))
             
             (when (and (at_a_l-2-1) (operational_a))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-1_a)))
             
             (when (and (operational_a) (at_a_l-2-3))
                   (and (wenab-move-ship-auv_s1_l-2-2_l-2-3_a)))
             )
)



(:action move-ship-free_s1_l-2-2_l-2-1-noop
:parameters ()
:precondition (and 
                    (disab-move-ship-free_s1_l-2-2_l-2-1)
                    (selected-move-ship-free_s1_l-2-2_l-2-1)
              )
:effect (and 
             (notsel-move-ship-free_s1_l-2-2_l-2-1)
             (not (selected-move-ship-free_s1_l-2-2_l-2-1)))
)

(:action move-ship-free_s1_l-2-2_l-2-3-noop
:parameters ()
:precondition (and 
                    (disab-move-ship-free_s1_l-2-2_l-2-3)
                    (selected-move-ship-free_s1_l-2-2_l-2-3)
              )
:effect (and 
             (notsel-move-ship-free_s1_l-2-2_l-2-3)
             (not (selected-move-ship-free_s1_l-2-2_l-2-3)))
)

(:action move-ship-free_s1_l-2-1_l-2-2-noop
:parameters ()
:precondition (and 
                    (selected-move-ship-free_s1_l-2-1_l-2-2)
                    (disab-move-ship-free_s1_l-2-1_l-2-2)
              )
:effect (and 
             (notsel-move-ship-free_s1_l-2-1_l-2-2)
             (not (selected-move-ship-free_s1_l-2-1_l-2-2)))
)

(:action move-ship-free_s1_l-2-3_l-2-2-noop
:parameters ()
:precondition (and 
                    (selected-move-ship-free_s1_l-2-3_l-2-2)
                    (disab-move-ship-free_s1_l-2-3_l-2-2)
              )
:effect (and 
             (notsel-move-ship-free_s1_l-2-3_l-2-2)
             (not (selected-move-ship-free_s1_l-2-3_l-2-2)))
)

(:action move-ship-auv_s1_l-2-2_l-2-1_a-noop
:parameters ()
:precondition (and 
                    (disab-move-ship-auv_s1_l-2-2_l-2-1_a)
                    (selected-move-ship-auv_s1_l-2-2_l-2-1_a)
              )
:effect (and 
             (notsel-move-ship-auv_s1_l-2-2_l-2-1_a)
             (not (selected-move-ship-auv_s1_l-2-2_l-2-1_a)))
)

(:action move-ship-auv_s1_l-2-2_l-2-3_a-noop
:parameters ()
:precondition (and 
                    (selected-move-ship-auv_s1_l-2-2_l-2-3_a)
                    (disab-move-ship-auv_s1_l-2-2_l-2-3_a)
              )
:effect (and 
             (notsel-move-ship-auv_s1_l-2-2_l-2-3_a)
             (not (selected-move-ship-auv_s1_l-2-2_l-2-3_a)))
)

(:action move-ship-auv_s1_l-2-1_l-2-2_a-noop
:parameters ()
:precondition (and 
                    (disab-move-ship-auv_s1_l-2-1_l-2-2_a)
                    (selected-move-ship-auv_s1_l-2-1_l-2-2_a)
              )
:effect (and 
             (notsel-move-ship-auv_s1_l-2-1_l-2-2_a)
             (not (selected-move-ship-auv_s1_l-2-1_l-2-2_a)))
)

(:action move-ship-auv_s1_l-2-3_l-2-2_a-noop
:parameters ()
:precondition (and 
                    (disab-move-ship-auv_s1_l-2-3_l-2-2_a)
                    (selected-move-ship-auv_s1_l-2-3_l-2-2_a)
              )
:effect (and 
             (notsel-move-ship-auv_s1_l-2-3_l-2-2_a)
             (not (selected-move-ship-auv_s1_l-2-3_l-2-2_a)))
)


;;;;;;;;;;
;;; resort
;;;;;;;;;;

(:action resort
:parameters ()
:precondition (and (ev-turn2) 
                    (notsel-move-ship-free_s1_l-2-2_l-2-1)
                    (notsel-move-ship-free_s1_l-2-2_l-2-3)
                    (notsel-move-ship-free_s1_l-2-1_l-2-2)
                    (notsel-move-ship-free_s1_l-2-3_l-2-2)
                    (notsel-move-ship-auv_s1_l-2-2_l-2-1_a)
                    (notsel-move-ship-auv_s1_l-2-2_l-2-3_a)
                    (notsel-move-ship-auv_s1_l-2-1_l-2-2_a)
                    (notsel-move-ship-auv_s1_l-2-3_l-2-2_a)
              )
:effect (and (act-turn) (not (ev-turn2))
             (when (and (wenab-move-ship-free_s1_l-2-2_l-2-1))
                   (and (not (wenab-move-ship-free_s1_l-2-2_l-2-1))
                        (not (disab-move-ship-free_s1_l-2-2_l-2-1))
                        (enab-move-ship-free_s1_l-2-2_l-2-1)
                   )
             )
             
             (when (and (wenab-move-ship-free_s1_l-2-2_l-2-3))
                   (and (not (wenab-move-ship-free_s1_l-2-2_l-2-3))
                        (not (disab-move-ship-free_s1_l-2-2_l-2-3))
                        (enab-move-ship-free_s1_l-2-2_l-2-3)
                   )
             )
             
             (when (and (wenab-move-ship-free_s1_l-2-1_l-2-2))
                   (and (not (wenab-move-ship-free_s1_l-2-1_l-2-2))
                        (not (disab-move-ship-free_s1_l-2-1_l-2-2))
                        (enab-move-ship-free_s1_l-2-1_l-2-2)
                   )
             )
             
             (when (and (wenab-move-ship-free_s1_l-2-3_l-2-2))
                   (and (not (wenab-move-ship-free_s1_l-2-3_l-2-2))
                        (not (disab-move-ship-free_s1_l-2-3_l-2-2))
                        (enab-move-ship-free_s1_l-2-3_l-2-2)
                   )
             )
             
             (when (and (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
                   (and (not (wenab-move-ship-auv_s1_l-2-2_l-2-1_a))
                        (not (disab-move-ship-auv_s1_l-2-2_l-2-1_a))
                        (enab-move-ship-auv_s1_l-2-2_l-2-1_a)
                   )
             )
             
             (when (and (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
                   (and (not (wenab-move-ship-auv_s1_l-2-2_l-2-3_a))
                        (not (disab-move-ship-auv_s1_l-2-2_l-2-3_a))
                        (enab-move-ship-auv_s1_l-2-2_l-2-3_a)
                   )
             )
             
             (when (and (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
                   (and (not (wenab-move-ship-auv_s1_l-2-1_l-2-2_a))
                        (not (disab-move-ship-auv_s1_l-2-1_l-2-2_a))
                        (enab-move-ship-auv_s1_l-2-1_l-2-2_a)
                   )
             )
             
             (when (and (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
                   (and (not (wenab-move-ship-auv_s1_l-2-3_l-2-2_a))
                        (not (disab-move-ship-auv_s1_l-2-3_l-2-2_a))
                        (enab-move-ship-auv_s1_l-2-3_l-2-2_a)
                   )
             )
             )
)


)