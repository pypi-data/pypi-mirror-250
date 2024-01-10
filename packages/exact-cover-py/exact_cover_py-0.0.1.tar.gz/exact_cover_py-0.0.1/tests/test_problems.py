from itertools import islice

import pytest

from exact_cover_py import exact_covers

try:
    from . import problems
except:
    import problems

all_problems = [
    problem for problem in problems.__dict__ if "_problem" in problem
]

# make a set of sorted tuples
def canonical(iterable):
    return set(tuple(sorted(x)) for x in iterable)


def define_test(problem_name):
    """
    for a given problem found defined in problems.py
    say small_trimino_problem
    we define a derived function named like
    say test_small_trimino_problem
    """

    def test_solutions(problem):
        match problem:
            case {'data': data, 'solutions': solutions}:
                canonical_solutions = canonical(solutions)
                try:
                    canonical_partial_computed = set(
                        tuple(sorted(x)) for x in exact_covers(data))
                    assert canonical_partial_computed == canonical_solutions
                except StopIteration:
                    assert solutions == set()
            case {'data': data, 'first_solutions': first_solutions}:
                canonical_first_solutions = canonical(first_solutions)
                how_many = len(canonical_first_solutions)
                try:
                    canonical_partial_computed = set(
                        tuple(sorted(x)) for x in islice(exact_covers(data), how_many))
                    assert canonical_partial_computed == canonical_first_solutions
                except StopIteration:
                    assert 'first_solutions' == set()
    problem = problems.__dict__[problem_name]()
    test_name = f"test_{problem_name}"
    # assign the global variable test_name to the newly defined function
    globals()[test_name] = lambda: test_solutions(problem)

for problem in all_problems:
    define_test(problem)
