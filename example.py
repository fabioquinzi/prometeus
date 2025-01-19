from tot import TreeOfThoughts, SimpleEvaluator

def main():
    # Initial prompt to improve
    initial_prompt = (
        "Rate this image good if the product in the image is below 70% "
        "of the total image, rate it bad if it's more"
    )
    
    # Initialize the Tree of Thoughts explorer
    tot = TreeOfThoughts(
        initial_prompt=initial_prompt,
        evaluator=SimpleEvaluator(),
        min_improvement_threshold=0.2,  # Require at least 0.2 point improvement
        max_iterations=20,              # Stop after 20 iterations
        max_children_per_node=2         # Generate 2 children per node
    )
    
    # Explore the tree
    print("Exploring prompt improvements...")
    tot.explore(verbose=True)
    
    # Get the best result
    best_node = tot.get_best_node()
    print("\nBest prompt found:")
    print(f"Score: {best_node.score:.2f}")
    print(f"Prompt: {best_node.prompt}")
    
    # Visualize the tree
    print("\nGenerating visualizations...")
    tot.visualize(title="Prompt Improvement Tree")
    tot.plot_score_distribution()

if __name__ == "__main__":
    main() 