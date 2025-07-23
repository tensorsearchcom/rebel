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
