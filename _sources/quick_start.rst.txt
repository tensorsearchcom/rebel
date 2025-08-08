.. _quick_start:

###########
Quick Start
###########

This guide provides a high-level overview of the REBEL workflow, from defining your evaluation criteria to running a benchmark.

1. Choose or Define Your Metrics
=================================

The first step in any evaluation is deciding *how* to measure performance. REBEL allows you to use built-in metrics or easily create your own.

For a comprehensive guide on all metric types, see the :ref:`metrics` page.

Here is an example of a simple custom metric that checks if the assistant correctly counts the occurrences of a specific letter in its output.

.. code-block:: python

    from rebel.models import (
        Metric,
        AssistantInput,
        AssistantOutput,
        EvaluationResult,
        EvaluationVerdict,
    )

    class LettersCalculationCorrectness(Metric):
        letter: str
        
        def measure(
            self,
            input: AssistantInput,
            expected: AssistantOutput,
            actual: AssistantOutput
        ):
            user_message = input.messages[-1].content
            expected_letter_count = user_message.lower().count(self.letter)
            
            try:
                actual_letter_count = int(actual.output)
            except ValueError:
                return EvaluationResult(
                    score=0.0,
                    verdict=EvaluationVerdict.FAILED,
                    reason=f'Invalid answer format, expected int, got "{actual.output}"'
                )
            
            if actual_letter_count != expected_letter_count:
                return EvaluationResult(
                    score=0.0,
                    verdict=EvaluationVerdict.FAILED,
                    reason=f'Incorrect result, expected {expected_letter_count}, got {actual_letter_count}'
                )
            
            return EvaluationResult(
                score=1.0,
                verdict=EvaluationVerdict.PASSED,
                reason=f'Good job :)'
            )
        
        def get_name(self):
            return 'Letters Calculation Correctness'


2. Define Your Tests
====================

Once you have your metric, you can define test cases using the ``@test_case`` decorator. This example uses the `LetterCountMetric` we defined above to evaluate the test.

.. code-block:: python

    from rebel import test_case
    from rebel.models import Message, RoleEnum, TestGroup, RetryParams, RetryAggregationStrategy

    # Assuming LetterCountMetric is defined in the same file or imported

    @test_case(
        messages=[
            Message(role=RoleEnum.system, content="You are a helpful assistant. When a user sends you a message, count the number of times the letter 'r' appears in their message and respond with ONLY the numerical count. Do not include any other text, explanations, or formatting - just the number."),
            Message(role=RoleEnum.user, content="The brave warrior rode rapidly through the forest, carrying three arrows in his quiver.")
        ]
    )
    def test_counting_accuracy():
        # The model should respond with the number 6.
        yield TestGroup(
            retry_params=RetryParams(count=3, aggregation_strategy=RetryAggregationStrategy.MEAN),
            metrics=[LettersCalculationCorrectness(letter='r')]
        )

For more details on creating tests, see the :ref:`defining_tests` guide.

3. Run Your Benchmarks
======================

Execute your tests using the ``rebel`` command from your terminal. You must provide a directory for your tests, a folder for the results, and a method for configuring the API client.

There are two primary ways to configure the client:

**Option 1: Using a Configuration File (Recommended)**

This is the simplest method. Create a JSON file with your API credentials and pass its path to the ``--api-config`` argument. This will use the built-in ``OpenAIAPIClient``.

For example, you can create a file named `model_config.json` with the following content. Be sure to replace `"YOUR_API_KEY_HERE"` with your actual API key.

.. code-block:: json

   {
       "model": "google/gemini-2.5-flash",
       "base_url": "https://openrouter.ai/api/v1",
       "api_key": "YOUR_API_KEY_HERE"
   }

You can then run the benchmark by referencing this file:

.. code-block:: bash

   rebel --test-dir tests/ --output-folder results/ --api-config model_config.json

**Option 2: Using a Custom API Client**

For advanced use cases, such as integrating with a different API provider, you can create your own client class. Your custom class must inherit from :class:`rebel.collector.api_client.APIClient` and implement the ``request`` method.

Here is a basic template for a custom client:

.. code-block:: python

   # my_package/my_client.py
   from rebel.collector import APIClient
   from rebel.models import AssistantInput, AssistantOutput

   class MyAPIClient(APIClient):
       def __init__(self, api_key: str, retries: int = 3):
           self.api_key = api_key
           self.retries = retries
           # ... your client initialization logic ...

       def request(self, input: AssistantInput) -> AssistantOutput:
           # ... your logic to call the external API ...
           # ... format the response into an AssistantOutput object ...
           return AssistantOutput(output="Response from custom client.")

You can then run the benchmark with your custom client. The arguments in `--api-client-args` will be passed to your class's constructor.

.. code-block:: bash

   rebel --test-dir tests/ --output-folder results/ \
     --api-client-module my_package.my_client \
     --api-client-class MyAPIClient \
     --api-client-args '{"api_key": "your-secret-key", "retries": 3}'

Command-Line Arguments
----------------------

Here is a complete list of all available CLI arguments.

.. list-table:: REBEL CLI Arguments
   :widths: 30 60 10
   :header-rows: 1

   * - Argument
     - Description
     - Required
   * - ``--test-dir``
     - Directory containing the test files to be discovered.
     - **Yes**
   * - ``--output-folder``
     - Directory where the test results will be saved.
     - **Yes**
   * - ``--api-config``
     - Path to the API configuration JSON file. Used if a custom client is not specified.
     - Conditional
   * - ``--api-client-module``
     - The Python module path for a custom API client (e.g., 'my_package.my_client'). Takes priority over ``--api-config``.
     - Conditional
   * - ``--api-client-class``
     - The class name of your custom API client.
     - Conditional
   * - ``--api-client-args``
     - A JSON string of keyword arguments to pass to your custom client's constructor.
     - No
   * - ``--keyword``
     - Filter tests to run only those whose names contain this keyword.
     - No
   * - ``--tags``
     - Filter tests to run only those that have the specified tag(s).
     - No
   * - ``--exclude-tags``
     - Exclude any tests that have the specified tag(s).
     - No
   * - ``--num-workers-api``
     - The number of parallel worker threads for making API calls. (Default: 4)
     - No
   * - ``--num-workers-eval``
     - The number of parallel worker threads for running evaluations. (Default: 4)
     - No

4. Analyze the Results
======================

REBEL generates a detailed JSON report in your specified output directory, organized by model and timestamp. This allows for easy comparison and historical analysis.

See the :ref:`results` guide for more information on the output format.

Next Steps
----------

For a complete, end-to-end implementation with multiple models and advanced metrics, check out our detailed walkthrough: :ref:`example_openrouter`.
