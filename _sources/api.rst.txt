.. _api-reference:

API Reference
=============

This page contains the auto-generated API reference for the REBEL library.

.. contents::
   :local:
   :depth: 2

Test Definition & Execution
---------------------------

These components are used to define, configure, and run your tests.

.. automodule:: rebel.extractor.test_case_registry
   :members: test_case

.. autoclass:: rebel.models.group.TestGroup
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.TestSuite
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.TestInfo
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.TestCase
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.TestAttempt
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.TestAttemptExecuted
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.RetryParams
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.test.RetryAggregationStrategy
   :members:

.. autoclass:: rebel.models.test.ParameterGrid
   :members:
   :show-inheritance:


Core Data Models
----------------

These models define the fundamental data structures for assistant conversations.

.. autoclass:: rebel.models.RoleEnum
   :members:

.. autoclass:: rebel.models.Function
   :members:

.. autoclass:: rebel.models.ToolCall
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.Message
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.AssistantInput
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.AssistantOutput
   :members:
   :show-inheritance:


Evaluation & Metrics
--------------------

These models define the structure for evaluating test results and implementing metrics.

.. automodule:: rebel.models.metric
   :members: Metric, SerializableMetric

.. autoclass:: rebel.models.evaluation.EvaluationVerdict
   :members:

.. autoclass:: rebel.models.evaluation.EvaluationResult
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.evaluation.EvaluationAttempt
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.evaluation.EvaluationAttemptEvaluated
   :members:
   :show-inheritance:

.. autoclass:: rebel.models.evaluation.TestCaseEvaluated
   :members:
   :show-inheritance:


Built-in Metrics
~~~~~~~~~~~~~~~~

.. autoclass:: rebel.metrics.contextual_f_score.ContextualFScore
   :members:
   :show-inheritance:

.. autoclass:: rebel.metrics.tool_calls_accuracy.ToolCallsAccuracy
   :members:
   :show-inheritance:


Metric Utilities
~~~~~~~~~~~~~~~~

.. autoclass:: rebel.metrics.tool_calls_accuracy.ToolCallDistance
   :members:

.. autoclass:: rebel.metrics.tool_calls_accuracy.ExactMatchToolCallDistance
   :members:
   :show-inheritance:

.. autoclass:: rebel.metrics.tool_calls_accuracy.CosineSimilarityToolCallDistance
   :members:
   :show-inheritance:

.. autoclass:: rebel.metrics.tool_calls_accuracy.Encoder
   :members:

.. autoclass:: rebel.metrics.contextual_f_score.ContextualFScoreTemplate
   :members:


DeepEval Integration
--------------------

Components for integrating with the DeepEval framework.

.. autoclass:: rebel.deepeval.metric.DeepevalMetric
   :members:
   :show-inheritance:

.. autoclass:: rebel.deepeval.client.OpenAIClientLLM
   :members:
   :show-inheritance:


API Clients & Utilities
-----------------------

Clients for interacting with LLM APIs and other utilities.

.. autoclass:: rebel.collector.api_client.APIClient
   :members:

.. autoclass:: rebel.collector.openai_api_client.OpenAIAPIClient
   :members:
   :show-inheritance:

.. autoclass:: rebel.utils.openai_client.OpenAIClientWrapper
   :members:

