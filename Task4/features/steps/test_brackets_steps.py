import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from main import first_mismatch_index, is_balanced

scenarios("../brackets.feature")


@pytest.fixture
def ctx():
    return {}


@given(parsers.parse('the string "{s}"'), target_fixture="ctx")
def given_string(s, ctx):
    ctx["s"] = s
    return ctx


@when("I check the brackets")
def when_check(ctx):
    ctx["balanced"] = is_balanced(ctx["s"])
    ctx["mismatch"] = first_mismatch_index(ctx["s"])


@then("the result is balanced")
def then_balanced(ctx):
    assert ctx["balanced"] is True


@then("the result is not balanced")
def then_not_balanced(ctx):
    assert ctx["balanced"] is False


@then("the first mismatch index is absent")
def then_absent(ctx):
    assert ctx["mismatch"] is None


@then(parsers.parse("the first mismatch index is {idx:d}"))
def then_index(ctx, idx):
    assert ctx["mismatch"] == idx
