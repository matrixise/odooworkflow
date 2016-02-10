import pytest
import workflow_parser
from pprint import pprint as pp


def test_empty_workflow():
    code = 'account.invoice {}'
    result = workflow_parser.parse(code)
    assert result == ('workflow', 'account.invoice', [], [])


def test_workflow_with_arguments():
    code = "account.invoice(id: 'wkf') {}"
    result = workflow_parser.parse(code)
    assert result == ('workflow', 'account.invoice',
                      [('id', 'wkf')], [])


def test_parse_activity():
    code = """account.invoice {
        draft {
        }
    }"""
    result = workflow_parser.parse(code)
    # pp(result)
    assert result == ('workflow', 'account.invoice',
                      [],
                      [('activity', 'draft', [], [])])


def test_parse_activity_and_parameters():
    code = """
    account.invoice {
        draft {
            start: True,
            stop: False
        }
    }
    """
    result = workflow_parser.parse(code)
    assert result == ('workflow', 'account.invoice',
                      [],
                      [('activity', 'draft', [],
                        [('start', True), ('stop', False)])])


def test_parse_transitions():
    code = """
    account.invoice {
        draft -> open
        open -> closed
    }
    """
    result = workflow_parser.parse(code)

    assert result == ('workflow', 'account.invoice',
                      [],
                      [('transition', 'draft', 'open', [], []),
                       ('transition', 'open', 'closed', [], [])])


def test_parse_transitions_with_meta():
    code = """
    account.invoice {
        draft -> open (id: 'draft_to_open')
    }
    """

    result = workflow_parser.parse(code)

    assert result == ('workflow', 'account.invoice',
                      [],
                      [('transition', 'draft', 'open', [('id', 'draft_to_open')], [])])


def test_parse_transitions_with_meta_and_parameters():
    code = """
    account.invoice {
        draft -> open {
            condition: 'True'
        }
    }
    """

    result = workflow_parser.parse(code)

    assert result == ('workflow', 'account.invoice',
                      [],
                      [('transition', 'draft', 'open',
                        [],
                        [('condition', 'True')])]
                      )

def test_parse_full():
    code = """
    account.invoice(id: 'wkf') {
        draft(id: 'act_draft') {
            start: True
        }
        draft -> open (id: 'draft_to_open') {
            signal: 'no_signal'
        }
    }
    """

    result = workflow_parser.parse(code)

    assert result == ('workflow', 'account.invoice',
                      [('id', 'wkf')],
                      [('activity', 'draft',
                        [('id', 'act_draft')],
                        [('start', True)]),
                       ('transition', 'draft', 'open',
                        [('id', 'draft_to_open')],
                        [('signal', 'no_signal')]
                        )
                       ]
                      )