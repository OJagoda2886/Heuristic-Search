import random  # Provides a way to shuffle tiles for random test boards.

from Benchmark import compare_heuristics  # Runs both search estimates and collects their results.
from Puzzle import Puzzle  # Provides the board and distance calculations used by the search.


# Define the example starting arrangement; 0 marks the empty space.
SS = [[7, 2, 4],
      [5, 0, 6],
      [8, 3, 1]]

# Define the arrangement that counts as solved.
GS = [[0, 1, 2],
      [3, 4, 5],
      [6, 7, 8]]


# Run this demonstration only when this file is started directly, not when imported.
if __name__ == "__main__":
    # Create an object that holds the example start and goal boards.
    example_puzzle = Puzzle(SS, GS)
    # Solve the example once with each heuristic and collect timing and search counts.
    example_results = compare_heuristics(example_puzzle)
    # Print a heading so the results below have context.
    print("Example search results for SS and GS:")
    # Show the two heuristic methods one at a time.
    for heuristic_name in ["hamming", "manhattan"]:
        print(heuristic_name.capitalize() + ":")
        # Get the sequence of boards returned by the search for this method.
        solution = example_results[heuristic_name]["solution"]
        # A missing solution means no path was found.
        if solution is None:
            print("  No solution found.")
        else:
            print("  Path:")
            # Number each board in the solution, starting with step zero.
            for step, board in enumerate(solution):
                print("    Step", step)
                # Print each row so the 3-by-3 board is easy to read.
                for row in board:
                    print("     ", row)
            # A path contains the starting board too, so moves equal boards minus one.
            print("  Number of moves:", len(solution) - 1)
        # Report how many board positions this search expanded.
        print("  Expanded nodes:", example_results[heuristic_name]["expanded_nodes"])
        # Report elapsed seconds rounded to six decimal places.
        print("  Computation time:", round(
            example_results[heuristic_name]["computation_time"], 6
        ), "seconds")

    # Choose how many shuffled starting arrangements to examine.
    number_of_searches = 100
    # Keep a running total of expanded boards separately for each method.
    total_nodes = {"hamming": 0, "manhattan": 0}
    # Keep a running total of elapsed seconds separately for each method.
    total_time = {"hamming": 0, "manhattan": 0}
    solvable_boards = 0    # Count random arrangements that can be solved.
    unsolvable_boards = 0  # Count random arrangements that cannot be solved.

    # Repeat the random-board experiment the chosen number of times.
    for _ in range(number_of_searches):
        # Make a list of all tile values, including 0 for the empty space.
        numbers = list(range(9))
        # Put those tile values in a different random order.
        random.shuffle(numbers)
        # Split the shuffled list into three rows to make a 3-by-3 board.
        random_start = [numbers[0:3], numbers[3:6], numbers[6:9]]
        # Pair this random start with the same target board used in the example.
        random_puzzle = Puzzle(random_start, GS)

        # Skip the costly searches when this start cannot reach the target.
        if not random_puzzle.is_solvable():
            unsolvable_boards += 1
            continue

        # Record this as a solvable start and compare both search methods on it.
        solvable_boards += 1
        results = compare_heuristics(random_puzzle)

        # Add each method's results to its own running totals.
        for heuristic_name in ["hamming", "manhattan"]:
            total_nodes[heuristic_name] += results[heuristic_name]["expanded_nodes"]
            total_time[heuristic_name] += results[heuristic_name]["computation_time"]

    # Print a divider and the counts from the random-board experiment.
    print()
    print("###############################################")
    print("Solvable random boards:", solvable_boards)
    print("Unsolvable random boards:", unsolvable_boards)
    print("Average results from", solvable_boards, "solvable random start states:")
    # Calculate and print average results for each method.
    for heuristic_name in ["hamming", "manhattan"]:
        print(heuristic_name.capitalize() + ":")
        # Division is possible only if at least one solvable start was searched.
        if solvable_boards:
            # Divide each running total by the number of solvable boards.
            average_nodes = total_nodes[heuristic_name] / solvable_boards
            average_time = total_time[heuristic_name] / solvable_boards
            # Round the averages to make the output readable.
            print("  Average expanded nodes:", round(average_nodes, 2))
            print("  Average computation time:", round(average_time, 6), "seconds")
        else:
            # Explain why no averages were printed if all random starts were impossible.
            print("  No solvable boards to average.")
