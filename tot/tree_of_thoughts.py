from typing import Dict, Optional, List, Tuple
from tqdm import tqdm

from .utils import Node, generate_node_id, calculate_improvement
from .evaluator import BaseEvaluator
from .visualization import TreeVisualizer

class TreeOfThoughts:
    """
    Main class implementing the Tree of Thoughts approach for prompt improvement.
    """
    
    def __init__(self, 
                 initial_prompt: str,
                 evaluator: BaseEvaluator,
                 min_improvement_threshold: float = 0.1,
                 max_iterations: int = 100,
                 max_children_per_node: int = 2):
        """
        Initialize the Tree of Thoughts explorer.
        
        Args:
            initial_prompt: The starting prompt to improve
            evaluator: Instance of BaseEvaluator to score prompts
            min_improvement_threshold: Minimum score improvement required to explore a branch
            max_iterations: Maximum number of iterations to run
            max_children_per_node: Maximum number of children to generate per node
        """
        self.evaluator = evaluator
        self.min_improvement_threshold = min_improvement_threshold
        self.max_iterations = max_iterations
        self.max_children_per_node = max_children_per_node
        
        # Initialize tree with root node
        self.nodes: Dict[str, Node] = {}
        root_id = generate_node_id()
        root_score = self.evaluator.evaluate(initial_prompt)
        self.nodes[root_id] = Node(
            prompt=initial_prompt,
            score=root_score,
            node_id=root_id
        )
        
        self.visualizer = TreeVisualizer()
        
    def _generate_and_evaluate_children(self, 
                                      parent_id: str) -> List[Tuple[str, float]]:
        """Generate and evaluate children for a given parent node."""
        parent = self.nodes[parent_id]
        
        # Generate improved prompts
        child_prompts = self.evaluator.generate_improvements(
            parent.prompt, 
            parent.score,
            n=self.max_children_per_node
        )
        
        results = []
        for prompt in child_prompts:
            child_id = generate_node_id()
            score = self.evaluator.evaluate(prompt)
            
            # Create child node
            child = Node(
                prompt=prompt,
                score=score,
                node_id=child_id,
                parent_id=parent_id
            )
            
            self.nodes[child_id] = child
            parent.add_child(child_id)
            results.append((child_id, score))
            
        return results
    
    def explore(self, verbose: bool = True) -> Dict[str, Node]:
        """
        Explore the tree of thoughts to find improved prompts.
        
        Returns:
            Dictionary of all nodes in the tree
        """
        iteration = 0
        nodes_to_explore = [(node_id, node.score) 
                           for node_id, node in self.nodes.items()]
        
        with tqdm(total=self.max_iterations, disable=not verbose) as pbar:
            while nodes_to_explore and iteration < self.max_iterations:
                # Sort by score (highest first) and take the best node
                nodes_to_explore.sort(key=lambda x: x[1], reverse=True)
                current_id, current_score = nodes_to_explore.pop(0)
                current_node = self.nodes[current_id]
                
                # Generate and evaluate children
                children = self._generate_and_evaluate_children(current_id)
                
                # Add promising children to exploration queue
                for child_id, child_score in children:
                    improvement = calculate_improvement(current_score, child_score)
                    if improvement > self.min_improvement_threshold:
                        nodes_to_explore.append((child_id, child_score))
                
                iteration += 1
                pbar.update(1)
                
                # Early stopping if we reach a perfect score
                if any(node.score == 10.0 for node in self.nodes.values()):
                    break
        
        return self.nodes
    
    def get_best_node(self) -> Node:
        """Return the node with the highest score."""
        return max(self.nodes.values(), key=lambda x: x.score)
    
    def visualize(self, title: Optional[str] = None, save_path: Optional[str] = None):
        """Visualize the current state of the tree."""
        self.visualizer.visualize(self.nodes, title=title, save_path=save_path)
    
    def plot_score_distribution(self, save_path: Optional[str] = None):
        """Plot the distribution of scores across all nodes."""
        self.visualizer.plot_score_distribution(self.nodes, save_path=save_path) 