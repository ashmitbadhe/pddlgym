(define (problem AUV-problem-3x3-2)
(:domain AUV)
(:objects
l-1-1 l-2-1 l-3-1 l-1-2 l-2-2 l-3-2 l-1-3 l-2-3 l-3-3 - location
r1 - resource
a - auv
s1 - ship
)
(:init
(operational a)
(at a l-1-2)
(connected l-1-1 l-2-1)
(connected l-2-1 l-1-1)
(connected l-1-1 l-1-2)
(connected l-1-2 l-1-1)
(connected l-2-1 l-3-1)
(connected l-3-1 l-2-1)
(connected l-2-1 l-2-2)
(connected l-2-2 l-2-1)
(connected l-3-1 l-3-2)
(connected l-3-2 l-3-1)
(connected l-1-2 l-2-2)
(connected l-2-2 l-1-2)
(connected l-1-2 l-1-3)
(connected l-1-3 l-1-2)
(connected l-2-2 l-3-2)
(connected l-3-2 l-2-2)
(connected l-2-2 l-2-3)
(connected l-2-3 l-2-2)
(connected l-3-2 l-3-3)
(connected l-3-3 l-3-2)
(connected l-1-3 l-2-3)
(connected l-2-3 l-1-3)
(connected l-2-3 l-3-3)
(connected l-3-3 l-2-3)
(at-res r1 l-3-2)
(at s1 l-2-2)
(connected-ship s1 l-2-1 l-2-2)
(connected-ship s1 l-2-2 l-2-1)
(connected-ship s1 l-2-2 l-2-3)
(connected-ship s1 l-2-3 l-2-2)
(free l-1-1)
(free l-3-1)
(free l-2-1)
(free l-3-2)
(free l-1-3)
(free l-2-3)
(free l-3-3)
)
(:goal
(and
(operational a)
(sampled r1)
(at a l-1-2)
)
)
)
