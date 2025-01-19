import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Optional
from .utils import Node

class TreeVisualizer:
    """Handles visualization of the Tree of Thoughts."""
    
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize

    def create_graph(self, nodes: Dict[str, Node]) -> nx.DiGraph:
        """Create a NetworkX graph from the tree nodes."""
        G = nx.DiGraph()
        
        # Add nodes
        for node_id, node in nodes.items():
            G.add_node(node_id, 
                      prompt=node.prompt,
                      score=node.score)
            
            # Add edges from parent to children
            if node.parent_id is not None:
                G.add_edge(node.parent_id, node_id)
        
        return G

    def visualize(self, nodes: Dict[str, Node], 
                 title: Optional[str] = "Tree of Thoughts Exploration",
                 save_path: Optional[str] = None):
        """
        Visualize the tree structure.
        
        Args:
            nodes: Dictionary of node_id to Node objects
            title: Title for the visualization
            save_path: If provided, save the visualization to this path
        """
        G = self.create_graph(nodes)
        
        plt.figure(figsize=self.figsize)
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, 
                             node_color=[float(G.nodes[n]['score'])/10 for n in G.nodes],
                             node_size=1000,
                             cmap=plt.cm.RdYlGn,
                             vmin=0, vmax=1)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
        
        # Add labels
        labels = {node: f"{G.nodes[node]['score']:.1f}" for node in G.nodes}
        nx.draw_networkx_labels(G, pos, labels)
        
        plt.title(title)
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show()

    def plot_score_distribution(self, nodes: Dict[str, Node],
                              title: Optional[str] = "Score Distribution",
                              save_path: Optional[str] = None):
        """Plot the distribution of scores across all nodes."""
        scores = [node.score for node in nodes.values()]
        
        plt.figure(figsize=(8, 6))
        plt.hist(scores, bins=20, range=(1, 10), edgecolor='black')
        plt.xlabel('Score')
        plt.ylabel('Count')
        plt.title(title)
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show() 