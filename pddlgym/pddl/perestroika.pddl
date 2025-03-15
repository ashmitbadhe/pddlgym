(define (domain Perestroika)
(:requirements :typing :equality)
(:types location resource lvl - object

)

(:predicates (act-turn)
             (at-agent ?l - location)
             (connected ?l1 ?l2 - location)
             (at-res ?r - resource ?l - location)
             (taken ?r - resource)
             (accessible ?l - location)
             (alive)
             (dead)
             (solid ?l - location)
             (none ?l - location)
             (level ?l - location ?lvl - lvl)
             (next ?l1 ?l2 - lvl)
             (level-max ?l - location ?lmax - lvl)
             (level-min ?lmin - lvl)
             (free ?l - location)
)

(:action move
:parameters (?l1 ?l2 - location)
:precondition (and (at-agent ?l1)
                   (alive)
                   (connected ?l1 ?l2)
                   (accessible ?l2)
              )
:effect (and (not (at-agent ?l1))
             (free ?l1)
             (not (free ?l2))
             (at-agent ?l2)
        )
)

(:action collect
:parameters (?r - resource ?l - location)
:precondition (and (at-agent ?l)
                   (at-res ?r ?l)
                   (not (taken ?r))
                   (alive)
              )
:effect (and (taken ?r)
        )
)


(:event shrink
:parameters (?l - location ?lvl1 - lvl ?lvl2 - lvl)
:precondition (and (level ?l ?lvl2)
                   (next ?lvl1 ?lvl2)
              )
:effect (and (level ?l ?lvl1)
             (not (level ?l ?lvl2))
        )
)


(:event shrink-small-empty
:parameters (?l - location ?lmin - lvl)
:precondition (and (level-min ?lmin)
                   (level ?l ?lmin)
                   ;(not (at-agent ?l))
                   (free ?l)
                   (accessible ?l)
              )
:effect (and (none ?l)
             (not (level ?l ?lmin))
             (not (accessible ?l))
        )
)

(:event shrink-small-agent
:parameters (?l - location ?lmin - lvl)
:precondition (and (level-min ?lmin)
                   (level ?l ?lmin)
                   (at-agent ?l)
                   (accessible ?l)
                   (alive)              ;; this this useless for domain definition, but it is useful for finding safe states
                   (not (dead))         ;; this this useless for domain definition, but it is useful for finding safe states
              )
:effect (and (none ?l)
             (not (level ?l ?lmin))
             (not (accessible ?l))
             (not (alive))
             (dead)
        )
)

(:event create
:parameters (?l - location ?lmax - lvl)
:precondition (and (none ?l)
                   (level-max ?l ?lmax)
                   (not (accessible ?l))
              )
:effect (and (level ?l ?lmax)
             (not (none ?l))
             (accessible ?l)
        )
)

)
