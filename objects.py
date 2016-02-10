class Workflow:
    def __init__(self, model, parameters=None, entities=None):
        self.model = model
        parameters = dict(parameters or [])
        self.on_create = bool(parameters.get('create', False))

        self.oid = parameters.get('id', False)

        self.entities = entities or []

    @property
    def activities(self):
        return [
            entity
            for entity in self.entities
            if isinstance(entity, Activity)
        ]

    @property
    def transitions(self):
        return [
            entity
            for entity in self.entities
            if isinstance(entity, Transition)
        ]

    def __repr__(self):
        return 'Workflow {} {} {}'.format(
            self.model,
            self.activities,
            self.transitions
        )

    def to_xml(self, root):
        record_tag = etree.SubElement(root, 'record', id=self.oid, model='workflow')
        etree.SubElement(record_tag, 'field', name='name').text = self.model
        etree.SubElement(record_tag, 'field', name='osv').text = self.model
        etree.SubElement(record_tag, 'field', name='on_create').text = str(self.on_create)

        root.append(etree.Comment('Activities'))
        for entity in self.activities:
            entity.to_xml(root)

        root.append(etree.Comment('Transitions'))

        for entity in self.transitions:
            entity.to_xml(root)


class Activity:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = dict(parameters or [])

    def __repr__(self):
        return 'Activity ({})'.format(self.name)

    def to_xml(self, root):
        record_tag = etree.SubElement(root, 'record',
            model='workflow.activity',
            id=self.oid
        )
        etree.SubElement(record_tag, 'field', name='wkf_id', ref='wkf')
        etree.SubElement(record_tag, 'field', name='name').text = self.name
        flow_start = self.parameters.get('start', None)
        if flow_start is not None:
            etree.SubElement(record_tag, 'field', name='flow_start').text = str(flow_start)

        flow_stop = self.parameters.get('stop', None)
        if flow_stop is not None:
            etree.SubElement(record_tag, 'field', name='flow_stop').text = str(flow_stop)

        function = self.parameters.get('function')
        if function:
            etree.SubElement(record_tag, 'field', name='action').text = function
            etree.SubElement(record_tag, 'field', name='kind').text = 'function'



    @property
    def oid(self):
        return '{}_{}'.format('act', self.name)

class Transition:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return 'Transition ({} -> {})'.format(self.src, self.dst)

    @property
    def oid(self):
        return '{}_to_{}'.format(self.src, self.dst)

    def to_xml(self, root):
        record_tag = etree.SubElement(root, 'record',
            model='workflow.transition',
            id=self.oid,
        )
        etree.SubElement(record_tag, 'field', name='act_from').text = self.src
        etree.SubElement(record_tag, 'field', name='act_to').text = self.dst

