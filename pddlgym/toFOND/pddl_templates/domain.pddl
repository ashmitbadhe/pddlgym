(define (domain {{domain_name}})
(:requirements :non-deterministic)

(:predicates {% for p in events %}
             (selected-{{p.name[1:-1]}})
             (enab-{{p.name[1:-1]}})
             (disab-{{p.name[1:-1]}})
             {%- endfor %}
             {% for p in atoms %}
             {{p}}
             {%- endfor %}
             (act-turn)
             (ev-turn)
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
;;; switcher
;;;;;;;;;;;

(:action switch
:parameters ()
:precondition (and (ev-turn))
:effect (oneof (and (not (ev-turn))(act-turn))
               {% for e in events -%}
               (and (not (ev-turn))(selected-{{e.name[1:-1]}}))
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


)