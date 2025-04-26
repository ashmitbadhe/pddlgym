(define (domain {{domain_name}})
(:requirements :non-deterministic)

(:predicates {% for p in events %}
             (selected-{{p.name[1:-1]}})
             (enab-{{p.name[1:-1]}})
             (disab-{{p.name[1:-1]}})
             (notsel-{{p.name[1:-1]}})
             (wenab-{{p.name[1:-1]}})
             {%- endfor %}
             {% for p in atoms %}
             {{p}}
             {%- endfor %}
             (act-turn)
             (ev-turn)
             (ev-turn2)
)


{% for action_name, precond, add_effect, del_effect, ceffs in actions %}
(:action {{action_name[1:-1]}}
:parameters ()
:precondition (and {% for p in precond %}
                    {{p}}
                   {%- endfor %}
              )
:effect (and {% for p in add_effect %}
             {{p}}
             {%- endfor %}
             {%- for p in del_effect %}
             (not {{p}})
             {%- endfor %}
             {%- for ce in ceffs %}
             (when (and {%- for c in ce.condition %} {{c}} {%- endfor %})
                   (and {%- for e in ce.effects %} {{e}} {%- endfor %}))
             {% endfor -%}
        )
)
{% endfor %}

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
               {% for s in indep_sets -%}
               (and
                    (not (ev-turn))
                    (ev-turn2)
                    {% for e in s -%}
                    (not (notsel-{{e[1:-1]}}))
                    {% endfor -%}
                    {% for e in s -%}
                    (selected-{{e[1:-1]}})
                    {% endfor -%}
               )
               {% endfor -%}

        )
)

;;;;;;;;;;;
;;; events
;;;;;;;;;;;

{% for action_name, precond, add_effect, del_effect, ceffs in events %}
(:action {{action_name[1:-1]}}
:parameters ()
:precondition (and {% for p in precond %}
                    {{p}}
                   {%- endfor %}
              )
:effect (and {% for p in add_effect %}
             {{p}}
             {%- endfor %}
             {%- for p in del_effect %}
             (not {{p}})
             {%- endfor %}
             {%- for ce in ceffs %}
             (when (and {%- for c in ce.condition %} {{c}} {%- endfor %})
                   (and {%- for e in ce.effects %} {{e}} {%- endfor %}))
             {% endfor -%}
        )
)
{% endfor %}

{% for action_name, precond, add_effect, del_effect, ceffs in noop_events %}
(:action {{action_name[1:-1]}}
:parameters ()
:precondition (and {% for p in precond %}
                    {{p}}
                   {%- endfor %}
              )
:effect (and {% for p in add_effect %}
             {{p}}
             {%- endfor %}
             {%- for p in del_effect %}
             (not {{p}})
             {%- endfor %}
             {%- for ce in ceffs %}
             (when (and {%- for c in ce.condition %} {{c}} {%- endfor %})
                   (and {%- for e in ce.effects %} {{e}} {%- endfor %}))
             {% endfor -%}
        )
)
{% endfor %}

;;;;;;;;;;
;;; resort
;;;;;;;;;;

(:action resort
:parameters ()
:precondition (and (ev-turn2) {% for ev in events %}
                    (notsel-{{ev.name[1:-1]}})
                   {%- endfor %}
              )
:effect (and (act-turn) (not (ev-turn2))
             {%- for ev in events %}
             (when (and (wenab-{{ev.name[1:-1]}}))
                   (and (not (wenab-{{ev.name[1:-1]}}))
                        (not (disab-{{ev.name[1:-1]}}))
                        (enab-{{ev.name[1:-1]}})
                   )
             )
             {% endfor -%}
        )
)


)
