(define (domain auv)
(:requirements :non-deterministic)

(:predicates 
             
             (operational_a)
             (free_l-2-2)
             (at_s1_l-2-3)
             (sampled_r1)
             (free_l-1-3)
             (at_s1_l-2-2)
             (at_a_l-2-3)
             (at_a_l-1-1)
             (free_l-3-3)
             (at_a_l-3-1)
             (free_l-1-1)
             (at_a_l-1-3)
             (free_l-3-1)
             (free_l-3-2)
             (at_a_l-3-3)
             (free_l-2-1)
             (free_l-1-2)
             (at_a_l-3-2)
             (at_s1_l-2-1)
             (at_a_l-2-1)
             (at_a_l-1-2)
             (free_l-2-3)
             (at_a_l-2-2)
             (act-turn)
             (ev-turn)
             (ev-turn2)
)



(:action move_a_l-1-2_l-1-1
:parameters ()
:precondition (and 
                    (at_a_l-1-2)
                    (free_l-1-1)
                    (act-turn)
                    (operational_a)
              )
:effect (and 
             (free_l-1-2)
             (ev-turn)
             (at_a_l-1-1)
             (not (at_a_l-1-2))
             (not (free_l-1-1))
             (not (act-turn)))
)

(:action move_a_l-1-2_l-1-3
:parameters ()
:precondition (and 
                    (at_a_l-1-2)
                    (act-turn)
                    (free_l-1-3)
                    (operational_a)
              )
:effect (and 
             (free_l-1-2)
             (at_a_l-1-3)
             (ev-turn)
             (not (at_a_l-1-2))
             (not (act-turn))
             (not (free_l-1-3)))
)

(:action move_a_l-1-1_l-2-1
:parameters ()
:precondition (and 
                    (free_l-2-1)
                    (act-turn)
                    (operational_a)
                    (at_a_l-1-1)
              )
:effect (and 
             (free_l-1-1)
             (ev-turn)
             (at_a_l-2-1)
             (not (free_l-2-1))
             (not (act-turn))
             (not (at_a_l-1-1)))
)

(:action move_a_l-1-1_l-1-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-1-2)
                    (operational_a)
                    (at_a_l-1-1)
              )
:effect (and 
             (at_a_l-1-2)
             (free_l-1-1)
             (ev-turn)
             (not (act-turn))
             (not (free_l-1-2))
             (not (at_a_l-1-1)))
)

(:action move_a_l-1-3_l-2-3
:parameters ()
:precondition (and 
                    (free_l-2-3)
                    (act-turn)
                    (at_a_l-1-3)
                    (operational_a)
              )
:effect (and 
             (at_a_l-2-3)
             (free_l-1-3)
             (ev-turn)
             (not (free_l-2-3))
             (not (act-turn))
             (not (at_a_l-1-3)))
)

(:action move_a_l-1-3_l-1-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-1-2)
                    (at_a_l-1-3)
                    (operational_a)
              )
:effect (and 
             (at_a_l-1-2)
             (free_l-1-3)
             (ev-turn)
             (not (act-turn))
             (not (free_l-1-2))
             (not (at_a_l-1-3)))
)

(:action move_a_l-1-2_l-2-2
:parameters ()
:precondition (and 
                    (at_a_l-1-2)
                    (act-turn)
                    (free_l-2-2)
                    (operational_a)
              )
:effect (and 
             (at_a_l-2-2)
             (free_l-1-2)
             (ev-turn)
             (not (at_a_l-1-2))
             (not (act-turn))
             (not (free_l-2-2)))
)

(:action move_a_l-2-1_l-1-1
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-1-1)
                    (at_a_l-2-1)
                    (operational_a)
              )
:effect (and 
             (free_l-2-1)
             (ev-turn)
             (at_a_l-1-1)
             (not (act-turn))
             (not (free_l-1-1))
             (not (at_a_l-2-1)))
)

(:action move_a_l-2-1_l-3-1
:parameters ()
:precondition (and 
                    (free_l-3-1)
                    (act-turn)
                    (at_a_l-2-1)
                    (operational_a)
              )
:effect (and 
             (at_a_l-3-1)
             (free_l-2-1)
             (ev-turn)
             (not (free_l-3-1))
             (not (act-turn))
             (not (at_a_l-2-1)))
)

(:action move_a_l-2-1_l-2-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-2-2)
                    (at_a_l-2-1)
                    (operational_a)
              )
:effect (and 
             (free_l-2-1)
             (at_a_l-2-2)
             (ev-turn)
             (not (act-turn))
             (not (free_l-2-2))
             (not (at_a_l-2-1)))
)

(:action move_a_l-2-3_l-1-3
:parameters ()
:precondition (and 
                    (act-turn)
                    (at_a_l-2-3)
                    (free_l-1-3)
                    (operational_a)
              )
:effect (and 
             (free_l-2-3)
             (at_a_l-1-3)
             (ev-turn)
             (not (act-turn))
             (not (at_a_l-2-3))
             (not (free_l-1-3)))
)

(:action move_a_l-2-3_l-3-3
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-3-3)
                    (at_a_l-2-3)
                    (operational_a)
              )
:effect (and 
             (at_a_l-3-3)
             (free_l-2-3)
             (ev-turn)
             (not (act-turn))
             (not (at_a_l-2-3))
             (not (free_l-3-3)))
)

(:action move_a_l-2-3_l-2-2
:parameters ()
:precondition (and 
                    (free_l-2-2)
                    (act-turn)
                    (at_a_l-2-3)
                    (operational_a)
              )
:effect (and 
             (at_a_l-2-2)
             (free_l-2-3)
             (ev-turn)
             (not (free_l-2-2))
             (not (act-turn))
             (not (at_a_l-2-3)))
)

(:action move_a_l-2-2_l-2-1
:parameters ()
:precondition (and 
                    (free_l-2-1)
                    (at_a_l-2-2)
                    (act-turn)
                    (operational_a)
              )
:effect (and 
             (free_l-2-2)
             (at_a_l-2-1)
             (ev-turn)
             (not (free_l-2-1))
             (not (at_a_l-2-2))
             (not (act-turn)))
)

(:action move_a_l-2-2_l-2-3
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (act-turn)
                    (free_l-2-3)
                    (operational_a)
              )
:effect (and 
             (free_l-2-2)
             (at_a_l-2-3)
             (ev-turn)
             (not (at_a_l-2-2))
             (not (act-turn))
             (not (free_l-2-3)))
)

(:action move_a_l-2-2_l-3-2
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (act-turn)
                    (free_l-3-2)
                    (operational_a)
              )
:effect (and 
             (free_l-2-2)
             (at_a_l-3-2)
             (ev-turn)
             (not (at_a_l-2-2))
             (not (act-turn))
             (not (free_l-3-2)))
)

(:action move_a_l-2-2_l-1-2
:parameters ()
:precondition (and 
                    (at_a_l-2-2)
                    (act-turn)
                    (free_l-1-2)
                    (operational_a)
              )
:effect (and 
             (at_a_l-1-2)
             (free_l-2-2)
             (ev-turn)
             (not (at_a_l-2-2))
             (not (act-turn))
             (not (free_l-1-2)))
)

(:action move_a_l-3-1_l-2-1
:parameters ()
:precondition (and 
                    (at_a_l-3-1)
                    (act-turn)
                    (free_l-2-1)
                    (operational_a)
              )
:effect (and 
             (free_l-3-1)
             (ev-turn)
             (at_a_l-2-1)
             (not (at_a_l-3-1))
             (not (act-turn))
             (not (free_l-2-1)))
)

(:action move_a_l-3-1_l-3-2
:parameters ()
:precondition (and 
                    (at_a_l-3-1)
                    (act-turn)
                    (free_l-3-2)
                    (operational_a)
              )
:effect (and 
             (free_l-3-1)
             (ev-turn)
             (at_a_l-3-2)
             (not (at_a_l-3-1))
             (not (act-turn))
             (not (free_l-3-2)))
)

(:action move_a_l-3-3_l-2-3
:parameters ()
:precondition (and 
                    (at_a_l-3-3)
                    (act-turn)
                    (free_l-2-3)
                    (operational_a)
              )
:effect (and 
             (ev-turn)
             (at_a_l-2-3)
             (free_l-3-3)
             (not (at_a_l-3-3))
             (not (act-turn))
             (not (free_l-2-3)))
)

(:action move_a_l-3-3_l-3-2
:parameters ()
:precondition (and 
                    (at_a_l-3-3)
                    (act-turn)
                    (free_l-3-2)
                    (operational_a)
              )
:effect (and 
             (ev-turn)
             (at_a_l-3-2)
             (free_l-3-3)
             (not (at_a_l-3-3))
             (not (act-turn))
             (not (free_l-3-2)))
)

(:action move_a_l-3-2_l-3-1
:parameters ()
:precondition (and 
                    (free_l-3-1)
                    (act-turn)
                    (at_a_l-3-2)
                    (operational_a)
              )
:effect (and 
             (at_a_l-3-1)
             (free_l-3-2)
             (ev-turn)
             (not (free_l-3-1))
             (not (act-turn))
             (not (at_a_l-3-2)))
)

(:action move_a_l-3-2_l-3-3
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-3-3)
                    (at_a_l-3-2)
                    (operational_a)
              )
:effect (and 
             (at_a_l-3-3)
             (free_l-3-2)
             (ev-turn)
             (not (act-turn))
             (not (at_a_l-3-2))
             (not (free_l-3-3)))
)

(:action move_a_l-3-2_l-2-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (free_l-2-2)
                    (at_a_l-3-2)
                    (operational_a)
              )
:effect (and 
             (at_a_l-2-2)
             (free_l-3-2)
             (ev-turn)
             (not (act-turn))
             (not (free_l-2-2))
             (not (at_a_l-3-2)))
)

(:action sample_a_r1_l-3-2
:parameters ()
:precondition (and 
                    (act-turn)
                    (at_a_l-3-2)
                    (operational_a)
              )
:effect (and 
             (sampled_r1)
             (ev-turn)
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
               )
)

;;;;;;;;;;;
;;; events
;;;;;;;;;;;





;;;;;;;;;;
;;; resort
;;;;;;;;;;

(:action resort
:parameters ()
:precondition (and (ev-turn2) 
              )
:effect (and (act-turn) (not (ev-turn2)))
)


)