(define (problem {{problem_name}})
(:domain {{domain_name}})

(:init
{%- for i in inits %}
    {{i}}
{%- endfor %}
)

(:goal
    (and
    {%- for g in goals %}
        {{g}}
    {%- endfor %}
    )
)

)