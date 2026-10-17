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
    example_puzzle = Puzzle(SS, GS)
    example_results = compare_heuristics(example_puzzle)
    print("Example search results for SS and GS:")
    for heuristic_name in ["hamming", "manhattan"]:
        print(heuristic_name.capitalize() + ":")
        print("  Expanded nodes:", example_results[heuristic_name]["expanded_nodes"])
        print("  Computation time:", round(
            example_results[heuristic_name]["computation_time"], 6
        ), "seconds")

    number_of_searches = 3
    total_nodes = {"hamming": 0, "manhattan": 0}
    total_time = {"hamming": 0, "manhattan": 0}
    solvable_boards = 0

    for _ in range(number_of_searches):
        numbers = list(range(9))
        random.shuffle(numbers)
        random_start = [numbers[0:3], numbers[3:6], numbers[6:9]]
        random_puzzle = Puzzle(random_start, GS)
        results = compare_heuristics(random_puzzle)

        if results["hamming"]["solution_found"]:
            solvable_boards += 1

        for heuristic_name in ["hamming", "manhattan"]:
            total_nodes[heuristic_name] += results[heuristic_name]["expanded_nodes"]
            total_time[heuristic_name] += results[heuristic_name]["computation_time"]

    print("Solvable random boards:", solvable_boards, "out of", number_of_searches)
    print("Average results from", number_of_searches, "random start states:")
    for heuristic_name in ["hamming", "manhattan"]:
        average_nodes = total_nodes[heuristic_name] / number_of_searches
        average_time = total_time[heuristic_name] / number_of_searches
        print(heuristic_name.capitalize() + ":")
        print("  Average expanded nodes:", round(average_nodes, 2))
        print("  Average computation time:", round(average_time, 6), "seconds")
