from dataclasses import dataclass
from typing import Optional, List, Dict
import uuid

@dataclass
class Node:
    """Represents a node in the Tree of Thoughts."""
    prompt: str
    score: float
    node_id: str
    parent_id: Optional[str] = None
    children_ids: List[str] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.children_ids is None:
            self.children_ids = []
        if self.metadata is None:
            self.metadata = {}

    def add_child(self, child_id: str):
        """Add a child node ID to this node."""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)

    def is_leaf(self) -> bool:
        """Check if this node is a leaf node (has no children)."""
        return len(self.children_ids) == 0

def generate_node_id() -> str:
    """Generate a unique ID for a node."""
    return str(uuid.uuid4())

def calculate_improvement(parent_score: float, child_score: float) -> float:
    """Calculate the improvement of a child node over its parent."""
    return child_score - parent_score 