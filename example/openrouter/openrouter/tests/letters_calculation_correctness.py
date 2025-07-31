from rebel import test_case
from rebel.models import (
    Message,
    RoleEnum,
    TestGroup,
    RetryParams,
    RetryAggregationStrategy,
)

from openrouter.metrics.letters_calculation import LettersCalculationCorrectness
from openrouter.config import DEFAULT_CONFIG


LETTERS_CALCULATION_RETRY_PARAMS = RetryParams(
    count=3,
    aggregation_strategy=RetryAggregationStrategy.MEAN # for better representativity
)
LETTERS_CALCULATION_METRIC_FACTORY = lambda: [LettersCalculationCorrectness(letter='r')]
LETTERS_CALCULATION_SYSTEM_PROMPT = "You are a helpful assistant. When a user sends you a message, count the number of times the letter 'r' appears in their message and respond with ONLY the numerical count. Do not include any other text, explanations, or formatting - just the number."


@test_case(
    messages=[
        Message(role=RoleEnum.system, content=LETTERS_CALCULATION_SYSTEM_PROMPT),
        Message(role=RoleEnum.user, content="The brave warrior rode rapidly through the forest, carrying three arrows in his quiver.")
    ]
)
def test_letter_r_counting_accuracy():
    yield TestGroup(
        retry_params=LETTERS_CALCULATION_RETRY_PARAMS,
        metrics=LETTERS_CALCULATION_METRIC_FACTORY()
    )


@test_case(
    messages=[
        Message(role=RoleEnum.system, content=LETTERS_CALCULATION_SYSTEM_PROMPT),
        Message(role=RoleEnum.user, content="The big white cat sat on the mat.")
    ]
)
def test_zero_r_counting():
    yield TestGroup(
        retry_params=LETTERS_CALCULATION_RETRY_PARAMS,
        metrics=LETTERS_CALCULATION_METRIC_FACTORY()
    )


@test_case(
    messages=[
        Message(role=RoleEnum.system, content=LETTERS_CALCULATION_SYSTEM_PROMPT),
        Message(role=RoleEnum.user, content="Robert really enjoys Reading books about Roman history.")
    ]
)
def test_case_insensitive_r_counting():
    yield TestGroup(
        retry_params=LETTERS_CALCULATION_RETRY_PARAMS,
        metrics=LETTERS_CALCULATION_METRIC_FACTORY()
    )


@test_case(
    messages=[
        Message(role=RoleEnum.system, content=LETTERS_CALCULATION_SYSTEM_PROMPT),
        Message(role=RoleEnum.user, content="r" * 50)
    ]
)
def test_rrrrrrrrrrrr_r_counting():
    yield TestGroup(
        retry_params=LETTERS_CALCULATION_RETRY_PARAMS,
        metrics=LETTERS_CALCULATION_METRIC_FACTORY()
    )
    

@test_case(
    messages=[
        Message(role=RoleEnum.system, content=LETTERS_CALCULATION_SYSTEM_PROMPT),
        Message(role=RoleEnum.user, content="Programming requires regular practice and persistent effort to master various programming paradigms, algorithms, and data structures for software development.")
    ]
)
def test_long_text_r_counting():
    yield TestGroup(
        retry_params=LETTERS_CALCULATION_RETRY_PARAMS,
        metrics=LETTERS_CALCULATION_METRIC_FACTORY()
    )
