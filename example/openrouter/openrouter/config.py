import os
import json
from dataclasses import dataclass
from deepeval.models.base_model import DeepEvalBaseLLM
from rebel.utils.openai_client import OpenAIClientWrapper
from rebel.deepeval.client import OpenAIClientLLM


@dataclass
class Config:
    judge_model: OpenAIClientWrapper
    deepeval_judge_model: DeepEvalBaseLLM


def load_config():
    judge_model_config_path = os.environ.get('JUDGE_MODEL_CONFIG_PATH', 'judge_model_config.json')
    with open(judge_model_config_path) as file:
        judge_model_config = json.load(file)
    return Config(
        judge_model=OpenAIClientWrapper(judge_model_config),
        deepeval_judge_model=OpenAIClientLLM(judge_model_config)
    )

DEFAULT_CONFIG = load_config()
