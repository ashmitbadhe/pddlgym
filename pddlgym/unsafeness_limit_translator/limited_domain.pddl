(define (domain limited-domain)
  (:requirements :strips)
  (:types location resource lvl - object)
  (:predicates (act-turn)
   move
:parameters (?l1 ?l2 - location
   collect
:parameters (?r - resource ?l - location
)
