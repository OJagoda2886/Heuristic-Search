class Puzzle:
    """Stores the puzzle boards and calculates heuristic values."""
    #Names of the variables only
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def find_position(self, board, number):
        for row in range(3):
            for column in range(3):
                if board[row][column] == number:
                    return row, column

    def is_solvable(self, board=None):
        """Check solvability using inversion parity for the 3x3 goal order."""
        board = self.start if board is None else board
        numbers = [number for row in board for number in row if number != 0]
        inversions = 0

        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] > numbers[j]:
                    inversions += 1

        return inversions % 2 == 0

    def hamming_distance(self, board):
        distance = 0

        for row in range(3):
            for column in range(3):
                number = board[row][column]
                if number != self.goal[row][column]:
                    distance += 1

        return distance

    def manhattan_distance(self, board):
        distance = 0

        for row in range(3):
            for column in range(3):
                number = board[row][column]


                goal_row, goal_column = self.find_position(self.goal, number)
                distance += abs(row - goal_row) + abs(column - goal_column)

        return distance

    def get_heuristic(self, board, heuristic_name):
        if heuristic_name == "hamming":
            return self.hamming_distance(board)
        if heuristic_name == "manhattan":
            return self.manhattan_distance(board)

        raise ValueError("Incorrect input. Choose 'hamming' or 'manhattan'")

