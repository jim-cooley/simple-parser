from etc.test.assignment import assignment_tests
from etc.test.binary_operators import binary_operators_tests
from etc.test.duration import duration_tests
from etc.test.errors import errors_tests
from etc.test.expresssions import expressions_tests
from etc.test.functions import functions_tests
from etc.test.identifiers import identifiers_tests
from etc.test.indexed_parameters import indexed_parameters_tests
from etc.test.indexing import indexing_tests
from etc.test.keywords import keywords_tests
from etc.test.language import language_tests
from etc.test.literals import literals_tests
from etc.test.logical import logical_tests
from etc.test.plists import plists_tests
from etc.test.regression import regression_tests
from etc.test.sequences import sequences_tests
from etc.test.set_operations import set_operations_tests
from etc.test.set_parameters import set_parameters_tests
from etc.test.sets import sets_tests
from etc.test.statements import statements_tests
from etc.test.time import time_tests
from etc.test.unary_operators import unary_operators_tests

test_data = {
    'regression': regression_tests,

    'assignment': assignment_tests,
    'binary_operators': binary_operators_tests,
    'duration': duration_tests,
    'errors': errors_tests,
    'expressions': expressions_tests,
    'functions': functions_tests,
    'identifiers': identifiers_tests,
    'indexing': indexing_tests,
    'indexed_expressions': indexed_parameters_tests,
    "keywords": keywords_tests,
    'language': language_tests,
    'literals': literals_tests,
    'logical': logical_tests,
    'plists': plists_tests,
    'sequences': sequences_tests,
    'sets': sets_tests,
    'set_operations': set_operations_tests,
    'set_parameters': set_parameters_tests,
    'statements': statements_tests,
    'time': time_tests,
    'unary_operators': unary_operators_tests,
}


skip_tests = [
    'regression',
    'errors',
]
