.. _results:

#######
Results
#######

REBEL generates a comprehensive JSON report for each benchmark run, allowing for detailed investigation and analysis.

Result Analysis Features
========================

- **Individual Attempt Tracking**: Complete execution history for each retry.
- **Aggregated Scores**: Statistical summaries based on your configured aggregation strategy.
- **Execution Metadata**: Performance metrics including response times.
- **Detailed Reasoning**: Comprehensive failure analysis and success explanations from metrics.
- **Structured Output**: Machine-readable JSON format for automated processing.

Understanding the Output File
=============================

REBEL saves results in a structured JSON file, making it easy to parse and analyze programmatically. Below is an example report followed by a detailed breakdown of its structure.

Example Report
--------------

.. code-block:: json

   {
     "metadata": {
       "timestamp": "20250808_125233",
       "total_test_cases": 1
     },
     "test_cases": [
       {
         "name": "test_counting_accuracy_[]",
         "tags": [],
         "retry_params": {
           "count": 3,
           "aggregation_strategy": "mean"
         },
         "input": {
           "messages": [
             {
               "role": "system",
               "content": "You are a helpful assistant..."
             },
             {
               "role": "user",
               "content": "The brave warrior rode rapidly through the forest..."
             }
           ],
           "api_params": {}
         },
         "expected_output": {
           "output": "",
           "tools_called": [],
           "context": [],
           "execution_time": null
         },
         "metrics": [
           {}
         ],
         "actual_outputs": [
           {
             "output": "13",
             "tools_called": [],
             "context": [],
             "execution_time": 0.9248490333557129
           },
           {
             "output": "13",
             "tools_called": [],
             "context": [],
             "execution_time": 1.0037972927093506
           },
           {
             "output": "13",
             "tools_called": [],
             "context": [],
             "execution_time": 0.8853063583374023
           }
         ],
         "evaluation_results": [
           {
             "score": 0.0,
             "verdict": "failed",
             "reason": "Incorrect result, expected 14, got 13"
           },
           {
             "score": 0.0,
             "verdict": "failed",
             "reason": "Incorrect result, expected 14, got 13"
           },
           {
             "score": 0.0,
             "verdict": "failed",
             "reason": "Incorrect result, expected 14, got 13"
           }
         ],
         "aggregated_result": {
           "score": 0.0,
           "verdict": "failed",
           "reason": ""
         }
       }
     ]
   }

How to Read the Report
----------------------

Here is a breakdown of the key fields in the JSON report:

- **`metadata`**: Contains high-level information about the benchmark run, including the ``timestamp`` and ``total_test_cases`` executed.

- **`test_cases`**: A list where each object represents a fully evaluated test case.

  - **`name`** and **`tags`**: Identify the test case, derived from the test function's name and any associated tags.

  - **`retry_params`**: Shows the configuration for this test case. In the example, the test was run ``"count": 3`` times, and the results were summarized using the ``"aggregation_strategy": "mean"``.

  - **`input`**: A complete record of the prompt (``messages``) and ``api_params`` sent to the model for this test case.

  - **`actual_outputs`**: A list containing the detailed response from each retry attempt. The length of this list matches the ``count`` in `retry_params`. Each object includes the model's ``output`` and the ``execution_time``. In the example, the model returned "13" on all three attempts.

  - **`evaluation_results`**: This list contains the detailed outcome from each metric for each attempt.
    - Its length is `(number of metrics) * (number of retries)`.
    - In the example, one metric was run on three attempts, resulting in three evaluation objects. Each one shows a ``score`` of `0.0` and a ``verdict`` of `"failed"` because the model's output ("13") did not match the metric's expected value (14).

  - **`aggregated_result`**: This is the final, single verdict for the entire test case.
    - The ``score`` is calculated by applying the ``aggregation_strategy`` to the scores from the `evaluation_results`.
    - In this example, the strategy was `"mean"`, so the final score is `mean(0.0, 0.0, 0.0)`, which is `0.0`. This leads to an overall ``verdict`` of `"failed"` for this test case.

For more details on the output format, you can refer to the data models in the :ref:`api-reference`, such as :class:`~rebel.models.evaluation.TestCaseEvaluated`.
