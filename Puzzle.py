class Puzzle:
    """Keep the starting and target boards and measure how far a board is from the target."""

    def __init__(self, start, goal):
        self.start = start  # Save the board the search should begin with.
        self.goal = goal    # Save the board the search is trying to reach.

    def find_position(self, board, number):
        """Return the row and column where a chosen tile appears."""
        # Check each of the three rows, using row as the current row number.
        for row in range(3):
            # Within this row, check each of its three columns.
            for column in range(3):
                # Compare the tile at this location with the number we are seeking.
                if board[row][column] == number:
                    # Return both coordinates so other methods can use its location.
                    return row, column

    def is_solvable(self, board=None):
        """Return whether a 3-by-3 board can reach this puzzle's goal arrangement."""
        # If no board was supplied, check the puzzle's saved starting board instead.
        board = self.start if board is None else board
        # Flatten the rows into one list and leave out 0, which represents the empty space.
        numbers = [number for row in board for number in row if number != 0]
        inversions = 0  # Count tile pairs that appear in the opposite order.

        # Choose each tile as the first member of a pair.
        for i in range(len(numbers)):
            # Compare it with every later tile so each pair is counted once.
            for j in range(i + 1, len(numbers)):
                # A larger tile before a smaller tile is called an inversion.
                if numbers[i] > numbers[j]:
                    inversions += 1

        # On a 3-by-3 board with the standard ordered goal, an even count is solvable.
        return inversions % 2 == 0

    def hamming_distance(self, board):
        """Count locations whose tile differs from the tile in the goal board."""
        distance = 0  # Start with no mismatched locations counted.

        # Visit every row in the 3-by-3 board.
        for row in range(3):
            # Visit every column in the current row.
            for column in range(3):
                number = board[row][column]  # Read the tile at this location.
                # Add one when the current tile is not the goal tile for this location.
                if number != self.goal[row][column]:
                    distance += 1

        # Give the total mismatch count back to the caller.
        return distance

    def manhattan_distance(self, board):
        """Add up how many row and column steps each tile is from its goal location."""
        distance = 0  # This will accumulate the distance for all nine tiles.

        # Visit every row in the current board.
        for row in range(3):
            # Visit every column in the current row.
            for column in range(3):
                number = board[row][column]  # Read the tile currently at this location.
                # Look up the row and column where this tile belongs in the goal board.
                goal_row, goal_column = self.find_position(self.goal, number)
                # Add vertical steps plus horizontal steps needed to reach that location.
                distance += abs(row - goal_row) + abs(column - goal_column)

        # Return the combined distance for every tile.
        return distance

    def get_heuristic(self, board, heuristic_name):
        """Choose and calculate the requested estimate of distance to the goal."""
        # Use the mismatch-count estimate when the caller asks for Hamming distance.
        if heuristic_name == "hamming":
            return self.hamming_distance(board)
        # Use the tile travel-distance estimate when the caller asks for Manhattan distance.
        if heuristic_name == "manhattan":
            return self.manhattan_distance(board)

        # Stop with a clear error if the caller supplied an unsupported name.
        raise ValueError("Incorrect input. Choose 'hamming' or 'manhattan'")

