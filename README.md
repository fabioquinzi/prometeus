# Tree of Thoughts Implementation

This project implements the Tree of Thoughts (ToT) approach for iteratively improving prompts through a tree-based exploration strategy. The implementation focuses on improving image moderation prompts by evaluating and generating better versions through a tree-based search.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── example.py
├── tot/
│   ├── __init__.py
│   ├── tree_of_thoughts.py    # Main ToT implementation
│   ├── evaluator.py           # Evaluation function implementations
│   ├── visualization.py       # Tree visualization utilities
│   └── utils.py              # Helper functions
```

## Features

- Tree-based prompt exploration
- Configurable evaluation functions
- Visual representation of the exploration tree
- Support for both script and Jupyter notebook usage
- Progress tracking and exploration history
- Early stopping when perfect score is reached
- Customizable improvement thresholds and iteration limits

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (optional but recommended):
```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS

# Or using conda
conda create -n tot python=3.8
conda activate tot
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Example Script

The simplest way to try the project is to run the example script:

```bash
python example.py
```

This will:
1. Start with an initial prompt
2. Explore improvements using the Tree of Thoughts approach
3. Display progress with a progress bar
4. Show the best prompt found
5. Generate visualizations of the tree and score distribution

### Using in Your Own Code

```python
from tot import TreeOfThoughts, SimpleEvaluator

# Initialize with custom parameters
tot = TreeOfThoughts(
    initial_prompt="Your initial prompt here",
    evaluator=SimpleEvaluator(),
    min_improvement_threshold=0.2,  # Minimum score improvement required
    max_iterations=20,             # Maximum exploration iterations
    max_children_per_node=2        # Number of variations to generate per prompt
)

# Run the exploration
nodes = tot.explore(verbose=True)

# Get the best result
best_node = tot.get_best_node()
print(f"Best prompt: {best_node.prompt}")
print(f"Score: {best_node.score}")

# Visualize results
tot.visualize(title="Prompt Improvement Tree")
tot.plot_score_distribution()
```

### Using in Jupyter Notebook

```python
# Import required components
from tot import TreeOfThoughts, SimpleEvaluator
import matplotlib.pyplot as plt
%matplotlib inline

# Rest of the code is same as above
# The visualizations will appear in the notebook cells
```

## Customization

### Creating Custom Evaluators

You can create custom evaluators by subclassing `BaseEvaluator`:

```python
from tot import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str) -> float:
        # Implement your evaluation logic here
        # Return a score between 1 and 10
        return score

    def generate_improvements(self, prompt: str, score: float, n: int = 2) -> List[str]:
        # Implement your prompt improvement logic here
        # Return a list of n improved prompts
        return improved_prompts
```

### Configuring the Tree of Thoughts

Key parameters you can adjust:
- `min_improvement_threshold`: Minimum score improvement required to explore a branch
- `max_iterations`: Maximum number of iterations to run
- `max_children_per_node`: Maximum number of variations to generate per prompt

## Requirements

- Python 3.8+
- networkx
- matplotlib
- tqdm
- graphviz (optional, for better visualization)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements. 