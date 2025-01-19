from abc import ABC, abstractmethod
import random
from typing import List

class BaseEvaluator(ABC):
    """Abstract base class for prompt evaluators."""
    
    @abstractmethod
    def evaluate(self, prompt: str) -> float:
        """Evaluate a prompt and return a score between 1 and 10."""
        pass

    @abstractmethod
    def generate_improvements(self, prompt: str, score: float, n: int = 2) -> List[str]:
        """Generate n improved versions of the prompt."""
        pass

class SimpleEvaluator(BaseEvaluator):
    """A simple evaluator implementation for testing purposes."""
    
    def evaluate(self, prompt: str) -> float:
        """
        Evaluate prompt quality based on simple heuristics.
        Returns a score between 1 and 10.
        """
        score = 5.0  # Base score
        
        # Example heuristics (these should be replaced with real evaluation logic)
        if len(prompt.split()) >= 10:  # Reward more detailed prompts
            score += 1
        if "%" in prompt:  # Reward quantitative criteria
            score += 1
        if "if" in prompt and "else" in prompt:  # Reward conditional logic
            score += 1
        if any(word in prompt.lower() for word in ["good", "bad", "rate", "classify"]):
            score += 1
            
        return min(10.0, max(1.0, score))

    def generate_improvements(self, prompt: str, score: float, n: int = 2) -> List[str]:
        """
        Generate n improved versions of the prompt.
        This is a simple implementation that should be enhanced with real NLP/LLM capabilities.
        """
        improvements = []
        base_improvements = [
            f"Please {prompt.lower()}",
            f"Analyze the image and {prompt.lower()}",
            f"Carefully examine the image to {prompt.lower()}",
            f"Using precise measurements, {prompt.lower()}"
        ]
        
        # Select n random improvements
        selected = random.sample(base_improvements, min(n, len(base_improvements)))
        improvements.extend(selected)
        
        return improvements[:n] 