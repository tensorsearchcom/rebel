.. _deepeval_integration:

######################
DeepEval Integration
######################

REBEL seamlessly integrates with the `DeepEval <https://github.com/confident-ai/deepeval>`_ framework, allowing you to use its advanced, AI-judged metrics in your benchmarks.

Using DeepEval Metrics
======================

To use a metric from DeepEval, create a new class that inherits from ``DeepevalMetric``. You need to implement ``get_name`` and ``get_deepeval_metric``.

See our `China Alignment Metric example on GitHub <https://github.com/tensorsearchcom/rebel/example/openrouter/openrouter/metrics/china_alignment.py>`_ for a complete implementation.

.. code-block:: python

   from rebel.deepeval.metric import DeepevalMetric
   from deepeval.metrics import GEval
   from deepeval.test_case import LLMTestCaseParams

   class MyDeepevalMetric(DeepevalMetric):
       threshold: float = 0.7
       
       def get_name(self):
           return "My DeepEval Metric"
       
       def get_deepeval_metric(self):
           return GEval(
               name="Custom Evaluation",
               criteria="Evaluate response quality and accuracy",
               evaluation_steps=[
                   "Check factual accuracy",
                   "Assess response completeness",
                   "Verify appropriate tone"
               ],
               evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
               threshold=self.threshold,
               model=self.judge_llm
           )

Configuring the Judge Model
===========================

The judge model is the LLM that performs the evaluation. You can configure it using the DeepEval client.

.. code-block:: python

   from rebel.deepeval.client import OpenAIClientLLM

   judge_config = {
       "model": "gpt-4",
       "api_key": "your-key",
       "base_url": "https://api.openai.com/v1",
       "temperature": 0.1
   }

   judge_llm = OpenAIClientLLM(judge_config)
