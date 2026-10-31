import time  # Provides a precise timer for measuring each search.

from AStarSearch import AStarSearch  # Imports the algorithm that explores puzzle boards.


def compare_heuristics(puzzle):
    """Run A* with both distance estimates and collect results for one puzzle."""
    # Avoid starting searches when the starting arrangement cannot reach the goal.
    if not puzzle.is_solvable():
        # Return the same result fields used below, with empty/zero values for each method.
        return {
            # Build one result entry for each heuristic name.
            heuristic_name: {
                "solution": None,       # No path exists for an unsolvable board.
                "expanded_nodes": 0,    # No search positions were expanded.
                "computation_time": 0.0,  # No search time was spent.
                "solution_found": False,  # Record clearly that no solution was found.
            }
            for heuristic_name in ["hamming", "manhattan"]
        }

    # Create the search object once; it can run repeatedly with different estimates.
    search = AStarSearch(puzzle)
    # These are the two estimates this benchmark compares.
    heuristics = ["hamming", "manhattan"]
    results = {}  # Store the measurements under each estimate's name.

    # Run one search for each heuristic method.
    for heuristic_name in heuristics:
        # Record the clock reading immediately before the search starts.
        start_time = time.perf_counter()
        # Search from the puzzle's starting board and get its path and expansion count.
        solution, expanded_nodes = search.search(puzzle.start, heuristic_name)
        # Subtract the start reading to get how long this search took.
        elapsed_time = time.perf_counter() - start_time

        # Save all useful outputs and measurements for this heuristic.
        results[heuristic_name] = {
            "solution": solution,  # The ordered boards from start to goal, or None.
            "expanded_nodes": expanded_nodes,  # Number of boards expanded by A*.
            "computation_time": elapsed_time,  # Measured duration in seconds.
            "solution_found": solution is not None,  # True only when a path was returned.
        }

    # Give both methods' collected results back to the calling code.
    return results
