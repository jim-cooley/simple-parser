from test.cases.assignment import assignment_tests
from test.cases.binary_operators import binary_operators_tests
from test.cases.duration import duration_tests
from test.cases.errors import errors_tests
from test.cases.expressions import expressions_tests
from test.cases.functions import functions_tests
from test.cases.grouping import grouping_tests
from test.cases.identifiers import identifiers_tests
from test.cases.indexed_parameters import indexed_parameters_tests
from test.cases.indexing import indexing_tests
from test.cases.lists import lists_tests
from test.cases.property_reference import property_reference_tests
from test.cases.keywords import keywords_tests
from test.cases.language import language_tests
from test.cases.literals import literals_tests
from test.cases.logical import logical_tests
from test.cases.plists import plists_tests
from test.cases.range import range_tests
from test.cases.regression import regression_tests
from test.cases.sequences import sequences_tests
from test.cases.set_operations import set_operations_tests
from test.cases.set_parameters import set_parameters_tests
from test.cases.set_unary import set_unary_tests
from test.cases.sets import sets_tests
from test.cases.shell import shell_tests
from test.cases.statements import statements_tests
from test.cases.time import time_tests
from test.cases.trades1 import trades1_tests
from test.cases.trades2 import trades2_tests
from test.cases.unary_operators import unary_operators_tests

test_data = {
    'regression': regression_tests,

    'assignment': assignment_tests,
    'binary_operators': binary_operators_tests,
    'duration': duration_tests,
    'errors': errors_tests,
    'expressions': expressions_tests,
    'functions': functions_tests,
    'grouping': grouping_tests,
    'identifiers': identifiers_tests,
    'indexed_expressions': indexed_parameters_tests,
    'indexing': indexing_tests,
    'keywords': keywords_tests,
    'language': language_tests,
    'lists': lists_tests,
    'literals': literals_tests,
    'logical': logical_tests,
    'plists': plists_tests,
    'property_reference': property_reference_tests,
    'range' : range_tests,
    'sequences': sequences_tests,
    'set_operations': set_operations_tests,
    'set_parameters': set_parameters_tests,
    'set_unary': set_unary_tests,
    'sets': sets_tests,
    'shell': shell_tests,
    'simple': 'simple.dsl',
    'simple2': 'simple2.dsl',
    'simpler': 'simpler.dsl',
    'statements': statements_tests,
    'system1': 'system1.dsl',
    'time': time_tests,
    'trades1': trades1_tests,
    'trades2': trades2_tests,
    'unary_operators': unary_operators_tests,
}
