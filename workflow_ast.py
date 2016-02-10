import workflow_parser


class Workflow:
    def __init__(self, model):
        self.entities = []

    def add_activity(self, activity):
        activity.workflow = self
        self.entities.append(activity)

    def add_transition(self, transition):
        self.entities.append(transition)


class Activity:
    def __init__(self, name):
        self.workflow = None
        self.name = name


class Transition:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst


def activity_to_ast(activity_record):
    _, name, meta, parameters = activity_record
    return Activity(name=name)


def transition_to_ast(transition_record):
    _, src, dst, meta, parameters = transition_record
    return Transition(src, dst)


def workflow_to_ast(workflow_record):
    _, model, meta, entities = workflow_record

    workflow = Workflow(model)

    for entity in entities:
        if entity[0] == 'activity':
            workflow.add_activity(activity_to_ast(entity))
        elif entity[0] == 'transition':
            workflow.add_transition(transition_to_ast(entity))
    return workflow


def tree_to_ast(tree):
    if tree[0] == 'workflow':
        return workflow_to_ast(tree)


def get_ast(code):
    tree = workflow_parser.parse(code)
    return tree_to_ast(tree)
