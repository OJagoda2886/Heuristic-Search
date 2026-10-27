import time

from AStarSearch import AStarSearch


def compare_heuristics(puzzle):
    """Compare both heuristics for one Puzzle object."""
    if not puzzle.is_solvable():
        return {
            heuristic_name: {
                "solution": None,
                "expanded_nodes": 0,
                "computation_time": 0.0,
                "solution_found": False,
            }
            for heuristic_name in ["hamming", "manhattan"]
        }

    search = AStarSearch(puzzle)
    heuristics = ["hamming", "manhattan"]
    results = {}

    for heuristic_name in heuristics:
        start_time = time.perf_counter()
        solution, expanded_nodes = search.search(puzzle.start, heuristic_name)
        elapsed_time = time.perf_counter() - start_time

        results[heuristic_name] = {
            "solution": solution,
            "expanded_nodes": expanded_nodes,
            "computation_time": elapsed_time,
            "solution_found": solution is not None,
        }

    return results
