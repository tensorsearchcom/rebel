.. _defining_tests:

##############
Defining Tests
##############

In REBEL, tests are defined using the ``@test_case`` decorator on a generator function. This approach allows for flexible and powerful test suite creation.

Core Features
=============

- **Parameter Grids**: Automatically expand tests across combinations of API parameters using the :class:`~rebel.models.test.ParameterGrid` class.
- **Retry Mechanisms**: Configure retry counts and aggregation strategies (mean, min, max, median) with the :class:`~rebel.models.test.RetryParams` class.
- **Tagging System**: Organize and filter tests using tags.
- **Expected Outputs**: Specify ground truth responses for direct comparison.

Comprehensive Example
=====================

Here is an example demonstrating multiple features, including a parameter grid and different test groups for various metrics.

.. code-block:: python

   from rebel import test_case
   from rebel.models import Message, RoleEnum, TestGroup, RetryParams, ParameterGrid

   @test_case(
       messages=[Message(role=RoleEnum.user, content="Test query")],
       tags=["accuracy", "basic"],
       api_params={"temperature": 0.7},
       param_grid=ParameterGrid(parameters={"max_tokens": [100, 200, 500]})
   )
   def test_comprehensive_evaluation():
       # This group will run 3 times and be evaluated for accuracy
       yield TestGroup(
           metrics=[AccuracyMetric()],
           retry_params=RetryParams(count=3, aggregation_strategy="mean"),
           tags=["primary"]
       )
       
       # This group will run 5 times and be evaluated for latency
       yield TestGroup(
           metrics=[LatencyMetric()],
           retry_params=RetryParams(count=5, aggregation_strategy="median"),
           tags=["performance"]
       )

For more examples, see our `test examples on GitHub <https://github.com/tensorsearchcom/rebel/example/openrouter/openrouter/tests>`_.
