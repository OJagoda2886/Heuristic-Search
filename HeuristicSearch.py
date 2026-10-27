import random

from Benchmark import compare_heuristics
from Puzzle import Puzzle


SS = [[7, 2, 4],
      [5, 0, 6],
      [8, 3, 1]]

GS = [[0, 1, 2],
      [3, 4, 5],
      [6, 7, 8]]


if __name__ == "__main__":

    # Run the example search and print the results

    example_puzzle = Puzzle(SS, GS)
    example_results = compare_heuristics(example_puzzle)
    print("Example search results for SS and GS:")
    for heuristic_name in ["hamming", "manhattan"]:
        print(heuristic_name.capitalize() + ":")
        solution = example_results[heuristic_name]["solution"]
        if solution is None:
            print("  No solution found.")
        else:
            print("  Path:")
            for step, board in enumerate(solution):
                print("    Step", step)
                for row in board:
                    print("     ", row)
            print("  Number of moves:", len(solution) - 1)
        print("  Expanded nodes:", example_results[heuristic_name]["expanded_nodes"])
        print("  Computation time:", round(
            example_results[heuristic_name]["computation_time"], 6
        ), "seconds")


    # Run multiple random searches and compare heuristics

    number_of_searches = 100
    total_nodes = {"hamming": 0, "manhattan": 0}
    total_time = {"hamming": 0, "manhattan": 0}
    solvable_boards = 0
    unsolvable_boards = 0

    for _ in range(number_of_searches):
        numbers = list(range(9))
        random.shuffle(numbers)
        random_start = [numbers[0:3], numbers[3:6], numbers[6:9]]
        random_puzzle = Puzzle(random_start, GS)

        if not random_puzzle.is_solvable():
            unsolvable_boards += 1
            continue

        solvable_boards += 1
        results = compare_heuristics(random_puzzle)

        for heuristic_name in ["hamming", "manhattan"]:
            total_nodes[heuristic_name] += results[heuristic_name]["expanded_nodes"]
            total_time[heuristic_name] += results[heuristic_name]["computation_time"]

    print()
    print("###############################################")
    print("Solvable random boards:", solvable_boards)
    print("Unsolvable random boards:", unsolvable_boards)
    print("Average results from", solvable_boards, "solvable random start states:")
    for heuristic_name in ["hamming", "manhattan"]:
        print(heuristic_name.capitalize() + ":")
        if solvable_boards:
            average_nodes = total_nodes[heuristic_name] / solvable_boards
            average_time = total_time[heuristic_name] / solvable_boards
            print("  Average expanded nodes:", round(average_nodes, 2))
            print("  Average computation time:", round(average_time, 6), "seconds")
        else:
            print("  No solvable boards to average.")
