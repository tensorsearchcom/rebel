.. _metrics:

#######
Metrics
#######

REBEL supports a wide range of evaluation metrics, from simple rule-based checks to sophisticated AI-judged evaluations. This guide covers how to use built-in metrics and how to create your own.

For a complete list of all metric-related classes and their parameters, please refer to the :ref:`api-reference`.

Implement a Custom Metric
=========================

You can create your own deterministic metric by inheriting from the abstract base class :class:`~rebel.models.metric.Metric` and implementing two methods:

1.  **`measure()`**: Contains your core evaluation logic.
2.  **`get_name()`**: Returns a unique, human-readable name for your metric.

.. code-block:: python

   from rebel.models import Metric, AssistantInput, AssistantOutput, EvaluationResult, EvaluationVerdict

   class MyCustomMetric(Metric):
       """A simple metric that checks if the output contains a specific keyword."""

       def __init__(self, keyword: str):
           self.keyword = keyword.lower()

       def measure(self, input: AssistantInput, expected: AssistantOutput, actual: AssistantOutput) -> EvaluationResult:
           if self.keyword in actual.output.lower():
               return EvaluationResult(
                   score=1.0,
                   verdict=EvaluationVerdict.PASSED,
                   reason=f"Successfully found the keyword '{self.keyword}'."
               )
           else:
               return EvaluationResult(
                   score=0.0,
                   verdict=EvaluationVerdict.FAILED,
                   reason=f"The keyword '{self.keyword}' was not found in the output."
               )
       
       def get_name(self) -> str:
           return f"KeywordMatch ({self.keyword})"


Built-in REBEL Metrics
======================

REBEL provides several powerful, ready-to-use metrics for common evaluation tasks.

ContextualFScore
----------------

The :class:`~rebel.metrics.contextual_f_score.ContextualFScore` metric is designed for **RAG (Retrieval-Augmented Generation)** evaluation. It uses an LLM judge to assess the factual consistency (precision) and completeness (recall) of an assistant's response against a provided context.

**How it works:**
1.  It breaks down the model's output into a list of "claims."
2.  It compares these claims against the ground truths found in the retrieval context.
3.  It calculates precision (to penalize hallucinations) and recall (to penalize incompleteness), then combines them into a final F-score.

**Example Usage:**

This metric requires a `model` (a judge LLM) and a `template` that provides the prompts for the evaluation steps.

**Step 1: Configure Your Judge LLM**

First, set up the client for the LLM that will perform the evaluation.

.. code-block:: python

   from rebel.utils.openai_client import OpenAIClientWrapper

   judge_config = {
       "model": "gpt-4",
       "api_key": "YOUR_JUDGE_API_KEY",
       "base_url": "https://api.openai.com/v1"
   }
   judge_model = OpenAIClientWrapper(judge_config)

**Step 2: Define a Prompt Template**

The core of this metric is the prompt template. You must create a class that inherits from :class:`~rebel.metrics.contextual_f_score.ContextualFScoreTemplate` and implements its four abstract methods. Each method should return a string that will be used as a prompt for the judge LLM.

Here is an example of a custom template:

.. code-block:: python

   from typing import List
   from rebel.metrics.contextual_f_score import ContextualFScoreTemplate

   class MyRAGTemplate(ContextualFScoreTemplate):
       """A custom template with prompts for RAG evaluation."""

       def generate_claims(self, actual_output: str) -> str:
           return f"""
           Deconstruct the following text into a list of simple, self-contained, factual claims.
           
           Text:
           {actual_output}
           """

       def generate_truths(self, retrieval_context: List[str], input_question: str) -> str:
           context_str = "\n".join(retrieval_context)
           return f"""
           Based on the provided context, extract a list of key facts that are directly relevant to answering the following question.
           
           Question: {input_question}
           Context: {context_str}
           """

       def generate_hallucination_verdicts(self, claims: List[str], retrieval_context: List[str]) -> str:
           claims_str = "\n".join([f"- {c}" for c in claims])
           context_str = "\n".join(retrieval_context)
           return f"""
           For each claim below, verify if it is supported by the provided context. Respond with only 'yes' if it is supported, or 'no' if it contradicts the context.
           
           Context: {context_str}
           
           Claims to Verify:
           {claims_str}
           """
       
       def generate_completeness_verdicts(self, truths: List[str], claims: List[str]) -> str:
           truths_str = "\n".join([f"- {t}" for t in truths])
           claims_str = "\n".join([f"- {c}" for c in claims])
           return f"""
           For each ground truth statement below, determine if it is fully covered by the list of claims. Respond with 'yes' if it is covered, or 'no' if it is not.
           
           Ground Truths:
           {truths_str}
           
           Claims:
           {claims_str}
           """

**Step 3: Instantiate the Metric**

Finally, create an instance of `ContextualFScore`, passing in your judge model and your custom template.

.. code-block:: python

   from rebel.metrics import ContextualFScore

   # Use the template defined in Step 2
   my_template = MyRAGTemplate()

   # Instantiate the metric
   rag_metric = ContextualFScore(
       beta=1.0,  # Balances precision and recall. 1.0 gives them equal weight.
       threshold=0.7,
       model=judge_model,
       template=my_template
   )

ToolCallsAccuracy
-----------------

The :class:`~rebel.metrics.tool_calls_accuracy.ToolCallsAccuracy` metric evaluates the accuracy of function/tool calls made by an assistant. It compares the list of expected tool calls with the actual ones using a configurable distance metric.

**How it works:**
1.  It takes the list of expected and actual tool calls.
2.  It uses a greedy matching algorithm to pair the most similar expected and actual calls.
3.  The similarity between each pair is calculated using a specified **distance** function (e.g., exact match or cosine similarity).

**Example Usage:**

By default, this metric performs an exact match on the function name and arguments.

.. code-block:: python

   from rebel.metrics import ToolCallsAccuracy, ExactMatchToolCallDistance

   # Simple usage with default exact matching
   exact_match_metric = ToolCallsAccuracy(
       threshold=0.9,
       strict_mode=True  # Fails if the number of tool calls doesn't match
   )

For more nuanced comparisons, you can use the :class:`~rebel.metrics.tool_calls_accuracy.CosineSimilarityToolCallDistance`, which requires a text encoder.

.. code-block:: python

   from rebel.metrics import ToolCallsAccuracy, CosineSimilarityToolCallDistance, Encoder
   import numpy as np
   
   # 1. Provide an encoder class (e.g., using sentence-transformers)
   class MySentenceTransformerEncoder(Encoder):
       def __init__(self, model_name: str):
           from sentence_transformers import SentenceTransformer
           self.model = SentenceTransformer(model_name)
       
       def encode(self, texts: list[str]) -> np.ndarray:
           return self.model.encode(texts)

   # 2. Instantiate the distance metric with your encoder
   cosine_distance = CosineSimilarityToolCallDistance(
       encoder=MySentenceTransformerEncoder("all-MiniLM-L6-v2"),
       aggregation_method="mean"
   )

   # 3. Instantiate the main metric with the custom distance
   semantic_tool_metric = ToolCallsAccuracy(
       distance=cosine_distance,
       threshold=0.85
   )

DeepEval Integration
====================

REBEL offers seamless integration with the `DeepEval <https://github.com/confident-ai/deepeval>`_ framework, allowing you to use any of its advanced, AI-judged metrics in your benchmarks.

To use a DeepEval metric, you simply need to wrap it in a class that inherits from :class:`~rebel.deepeval.metric.DeepevalMetric`.

**How it works:**
1.  Create a class that inherits from `DeepevalMetric`.
2.  Implement the `get_deepeval_metric()` method to return an instance of the DeepEval metric you want to use (e.g., `AnswerRelevancy`, `GEval`).
3.  REBEL handles the conversion between its data format and DeepEval's `LLMTestCase` automatically.

**Example Usage (wrapping `AnswerRelevancy`):**

.. code-block:: python

   from rebel.deepeval.metric import DeepevalMetric
   from rebel.deepeval.client import OpenAIClientLLM
   from deepeval.metrics import AnswerRelevancy

   # 1. Configure your judge LLM
   judge_config = {
       "model": "gpt-4",
       "api_key": "YOUR_JUDGE_API_KEY",
       "base_url": "https://api.openai.com/v1"
   }
   judge_llm = OpenAIClientLLM(judge_config)

   # 2. Create your wrapper class
   class AnswerRelevancyMetric(DeepevalMetric):
       threshold: float = 0.8
       
       def get_name(self):
           return "Answer Relevancy (DeepEval)"
       
       def get_deepeval_metric(self):
           # Return an instance of the DeepEval metric
           return AnswerRelevancy(
               threshold=self.threshold,
               model=self.judge_llm,
               include_reason=True
           )

   # 3. Instantiate your new metric
   relevancy_metric = AnswerRelevancyMetric(
       threshold=0.85,
       judge_llm=judge_llm
   )

