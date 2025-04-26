from collections import namedtuple
import os
import sys
import itertools

import jinja2

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './fast_downward/translate'))

Action = namedtuple("Action", ["name", "pre", "add", "delete", "ceff"])
Event = namedtuple("Event", ["name", "pre", "add", "delete", "ceff"])
ConditionalEffect = namedtuple("ConditionalEffect", ["condition", "effects"])


def enabler(action, event):
    return action.add & event.pre


def disabler(action, event):
    return action.delete & event.pre


def sole_enabler(action, event):
    return event.pre <= action.add


def missing_precond(action, event):
    return event.pre - action.add


def independent(a1, a2):
    return not ((a1.add & a2.delete) | (a2.add & a1.delete) | (a1.delete & a2.pre) | (a2.delete & a1.pre))


def atom_to_name(atom):
    if atom.args:
        return "(" + atom.predicate + "_" + "_".join(atom.args) + ")"
    return "(" + atom.predicate + ")"


def transform_action(action):
    add_effects = set(map(lambda x: atom_to_name(x[1]), action.add_effects))
    del_effects = set(map(lambda x: atom_to_name(x[1]), action.del_effects))
    pre = set(map(atom_to_name, action.precondition))

    return Action(action.name.replace(" ", "_"), pre, add_effects, del_effects, [])


def powerset(iterable, limit=None):
    xs = list(iterable)
    if not limit:
        limit = len(xs)
    limit = min(limit, len(xs)) + 1
    return itertools.chain.from_iterable(itertools.combinations(xs, n) for n in range(limit))


if __name__ == '__main__':

    limit = None;
    output_domain_and_problem = []
    if len(sys.argv) > 5:
        limit = int(sys.argv[4])
        output_domain_and_problem.append(sys.argv[5])
        output_domain_and_problem.append(sys.argv[6])
        sys.argv = sys.argv[:5]

    from pddlgym.downward_translate import pddl_parser
    from pddlgym.downward_translate import instantiate

    task = pddl_parser.open(sys.argv[1], sys.argv[2])
    actions = task.actions
    events = task.events

    output_domain_path = output_domain_and_problem[0]
    output_problem_path = output_domain_and_problem[1]

    print(output_domain_path)
    print(output_problem_path)

    os.makedirs(os.path.dirname(output_domain_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_problem_path), exist_ok=True)



    action_names = list(map(lambda a: a.name, task.actions))
    event_names = list(map(lambda e: e.name, task.events))

    task.actions = actions + events
    inst = instantiate.explore(task)

    inst_actions = [a for a in inst[2] if a.name.split(' ')[0][1:] in action_names]
    inst_events = [a for a in inst[2] if a.name.split(' ')[0][1:] in event_names]

    task.actions = actions

    inst_atoms = inst[1]

    ground_actions = list(map(transform_action, inst_actions))
    ground_events = list(map(transform_action, inst_events))
    ground_atoms = list(map(atom_to_name, inst_atoms))

    groups = dict()

    key = lambda e: e.name.split('_')[1]  # key for AUV domain

    # key for the SS-BW domain
    # def key(e):
    #    if e.name.startswith('(stick_'):
    #        return e.name[1:-1]
    #    if e.name.startswith('(slip_'):
    #        hand = e.name[1:-1].split('_')[-1]
    #        return 'slip_' + hand
    #    print(e)

    for e in ground_events:
        k = key(e)
        vals = groups.get(k, [])
        vals.append(e)
        groups[k] = vals

    # print(groups)

    print('Group keys:', groups.keys())
    print('Group sizes: ', [len(g) for g in groups.values()])

    sets = list(itertools.product(*groups.values()))

    indep_sets = set()
    for s in sets:
        for s2 in powerset(s, limit):
            if s2 and all(map(lambda x: independent(*x), itertools.combinations(s2, 2))):
                indep_sets.add(frozenset(map(lambda x: x.name, s2)))

    # print(indep_sets)

    print(f'Found {len(ground_actions)} ground actions and {len(ground_events)} ground events')
    print(f'There are {len(indep_sets)} independent sets of events')

    for a in ground_actions:
        a.pre.add('(act-turn)')
        a.delete.add('(act-turn)')
        a.add.add('(ev-turn)')

    init = set([i for i in map(atom_to_name, task.init) if not i.startswith('(=_')])
    goal = task.goal.parts

    for e in ground_events:
        if e.pre <= init:
            init.add(f'(enab-{e.name[1:-1]})')
        else:
            init.add(f'(disab-{e.name[1:-1]})')
        init.add(f'(notsel-{e.name[1:-1]})')

    if '(act-turn)' not in init:
        init.add('(act-turn)')
    init = sorted(init)

    for a in ground_actions:
        for e in ground_events:
            if enabler(a, e) and not sole_enabler(a, e):
                # print(a.name, "is an enabler of", e.name, a.add, e.pre)
                a.ceff.append(ConditionalEffect(missing_precond(a, e),
                                                [f"(enab-{e.name[1:-1]})", f"(not (disab-{e.name[1:-1]}))"]))
                # print("\t missing preconditions:", missing_precond(a, e))
            if disabler(a, e):
                a.delete.add(f"(enab-{e.name[1:-1]})")
                a.add.add(f"(disab-{e.name[1:-1]})")
                # print(a.name, "is a disabler of", e.name)
            if sole_enabler(a, e):
                a.add.add(f"(enab-{e.name[1:-1]})")
                a.delete.add(f"(disab-{e.name[1:-1]})")
                # print(a.name, "is a sole enabler of", e.name)

    for a in ground_events:
        for e in ground_events:
            if a.name != e.name and enabler(a, e) and not sole_enabler(a, e):
                # print(a.name, "is an enabler of", e.name, a.add, e.pre)
                a.ceff.append(ConditionalEffect(missing_precond(a, e), [f"(wenab-{e.name[1:-1]})"]))
                # print("\t missing preconditions:", missing_precond(a, e))
            if disabler(a, e):
                a.delete.add(f"(enab-{e.name[1:-1]})")
                a.delete.add(f"(wenab-{e.name[1:-1]})")
                a.add.add(f"(disab-{e.name[1:-1]})")
                # print(a.name, "is a disabler of", e.name)
            if a.name != e.name and sole_enabler(a, e):
                a.add.add(f"(wenab-{e.name[1:-1]})")
                # print(a.name, "is a sole enabler of", e.name)

    for a in ground_events:
        a.pre.clear()
        a.pre.add(f'(selected-{a.name[1:-1]})')
        a.pre.add(f'(enab-{a.name[1:-1]})')
        a.delete.add(f'(selected-{a.name[1:-1]})')
        a.add.add(f'(notsel-{a.name[1:-1]})')
        # a.add.add('(ev-turn)')

    noop_events = []
    for e in ground_events:
        pre = {f'(selected-{e.name[1:-1]})', f'(disab-{e.name[1:-1]})'}
        delete = {f'(selected-{e.name[1:-1]})'}
        add = {f'(notsel-{e.name[1:-1]})'}
        noop_events.append(Action(f'({e.name[1:-1]}-noop)', pre, add, delete, []))

    typed_objects = {}
    for o in task.objects:
        if o.type_name not in typed_objects:
            typed_objects[o.type_name] = []
        typed_objects[o.type_name].append(o.name)

    goal_atoms = list(map(atom_to_name, goal))
    # print(goal_atoms)

    print("=" * 80)

    template_loader = jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(os.path.realpath(__file__)), "./pddl_templates"))
    template_env = jinja2.Environment(loader=template_loader)
    problem_template = template_env.get_template('problem2.pddl')
    output_text = problem_template.render(problem_name=task.task_name,
                                          domain_name=task.domain_name,
                                          goals=goal_atoms,
                                          inits=init)

    p_path, p_name = os.path.split(sys.argv[2])

    name_prefix = ''
    if limit:
        name_prefix = f'lim-{limit}-'

    with open(output_problem_path, 'w') as f_problem:
        f_problem.write(output_text)

    domain_template = template_env.get_template('domain2.pddl')
    output_text = domain_template.render(domain_name=task.domain_name,
                                         actions=ground_actions,
                                         events=ground_events,
                                         noop_events=noop_events,
                                         atoms=ground_atoms,
                                         indep_sets=indep_sets)

    with open(output_domain_path, 'w') as f_domain:
        f_domain.write(output_text)
