from pddlgym.structs import Anti


class SimpleSTRIPSProblem:
    def __init__(self, env):
        self.env = env
        self.predicates = set()
        self.actions = []
        self.events = env.action_space.event_literals  # List of possible events
        self.all_effects = set()

        # Process all actions in the environment
        for action in env.action_space._compute_all_ground_literals(env._state):
            self.extract_action_info(action)

        for event in env.action_space.event_literals:
            self.extract_action_info(event)
        self.static_predicates = set(pred for pred in self.predicates if pred not in self.all_effects)

    def extract_action_info(self, action):
        self.env.action_space._update_objects_from_state(self.env._state)

        # Extract preconditions, add and delete effects
        pre = self.env.action_space._ground_action_to_pos_preconds.get(action, set())
        negpre = self.env.action_space._ground_action_to_neg_preconds.get(action, set())
        effects = self.env.action_space._ground_action_to_effects.get(action, set())

        # Simplify: treat any Anti(x) as a delete effect
        add_effects = set(e for e in effects if "Anti" not in str(e))  # Exclude Anti effects from add effects
        del_effects = set(e for e in effects if "Anti" in str(e))  # Only Anti effects are delete effects

        self.all_effects.update(lit.predicate for lit in add_effects)

        # Update predicates with the relevant literals (preconditions, add effects, delete effects)
        self.predicates.update(lit.predicate for lit in pre.union(add_effects, del_effects))

        # Create action object to store the action details
        act = type('Operator', (), {})()  # Anonymous object with fields
        act.literal = action
        act.preconditions = pre
        act.add_effects = add_effects
        act.del_effects = del_effects
        self.actions.append(act)

    def get_predicates(self):
        return list(self.env.domain.predicates)

    def get_actions(self):
        return self.actions

    def get_events(self):
        return self.events  # Add events if they are available (to be used in wait-for verification)

    def apply(self, state, action):
        """
        Applies the effects of an action to a given state and returns the new state.
        """
        state_literals = set(state.literals)
        all_effects = self.env.action_space._ground_action_to_effects[action]

        for effect in all_effects:
            if "Anti" in str(effect):
                state_literals.discard(effect.literal)  # Apply delete effect
            else:
                state_literals.add(effect)  # Apply add effect

        return state.with_literals(frozenset(state_literals))
