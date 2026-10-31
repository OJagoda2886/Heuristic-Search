import heapq  # Supplies a priority queue that removes the lowest-cost item first.


class AStarSearch:
    """Use A* search to find a path with the fewest moves from start to goal."""

    def __init__(self, puzzle):
        self.puzzle = puzzle  # Keep the puzzle so its goal and distance methods are available.

    def search(self, start, heuristic_name="manhattan"):
        """Find a solution path and return it with the number of boards expanded."""
        # Reject impossible boards before doing the more expensive search work.
        if not self.puzzle.is_solvable(start):
            # None means there is no path; zero means no boards were expanded.
            return None, 0

        # Convert each row and the whole board to tuples so they can be dictionary keys.
        # Tuples cannot be edited accidentally, which makes them safe to use as keys.
        start = tuple(tuple(row) for row in start)
        goal = tuple(tuple(row) for row in self.puzzle.goal)

        # The priority queue stores (estimated complete cost, moves already made, board).
        # Starting cost is the chosen estimate for the start plus zero moves so far.
        boards_to_check = [
            (self.puzzle.get_heuristic(start, heuristic_name), 0, start)
        ]
        moves_so_far = {start: 0}  # Record the fewest known moves needed to reach each board.
        previous_board = {start: None}  # Remember each board's predecessor to rebuild the path.
        expanded_nodes = 0  # Count how many boards are taken from the queue and explored.

        # Continue until the queue is empty or the goal is found.
        while boards_to_check:
            # Remove the board with the lowest estimated total solution cost.
            estimated_cost, moves, board = heapq.heappop(boards_to_check)

            # Reaching the goal means we can reconstruct the full path.
            if board == goal:
                path = []  # Boards will be collected backwards from goal to start.
                # Follow predecessor links until reaching the start, whose predecessor is None.
                while board is not None:
                    # Convert immutable tuple rows back to ordinary lists for the result.
                    path.append([list(row) for row in board])
                    board = previous_board[board]
                # The links were followed backwards, so reverse them to get start-to-goal order.
                path.reverse()
                # Return the full route and how many boards were explored along the way.
                return path, expanded_nodes

            # Ignore an outdated queue entry if a shorter route to this board was found later.
            if moves != moves_so_far[board]:
                continue

            # This current board is now being explored, so increase the expansion count.
            expanded_nodes += 1
            # Find where 0 (the empty space) is; only it can move to a neighboring square.
            zero_row, zero_column = self.puzzle.find_position(board, 0)
            # These row/column changes represent moving the empty space up, left, down, or right.
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

            # Try each possible direction for moving the empty space.
            for row_change, column_change in directions:
                # Calculate the neighboring square's row and column.
                new_row = zero_row + row_change
                new_column = zero_column + column_change

                # A move is legal only when the neighboring square is inside the 3-by-3 board.
                if 0 <= new_row < 3 and 0 <= new_column < 3:
                    # Copy the board so this move does not change the current board.
                    new_board = [list(row) for row in board]
                    # Move the neighboring tile into the empty space.
                    new_board[zero_row][zero_column] = new_board[new_row][new_column]
                    # Put the empty-space marker in the neighbor's old location.
                    new_board[new_row][new_column] = 0
                    # Freeze the changed board into tuples so it can be stored as a dictionary key.
                    new_board = tuple(tuple(row) for row in new_board)
                    new_moves = moves + 1  # This move adds exactly one step to the route.

                    # Save the board if it is new or if this route reaches it in fewer moves.
                    if new_board not in moves_so_far or new_moves < moves_so_far[new_board]:
                        # Update the best known number of moves for this board.
                        moves_so_far[new_board] = new_moves
                        # Remember which board led here so the path can be rebuilt at the end.
                        previous_board[new_board] = board
                        # Estimate how many moves this board is from the goal.
                        heuristic_value = self.puzzle.get_heuristic(
                            new_board, heuristic_name
                        )
                        # A* prioritizes actual moves so far plus estimated moves still needed.
                        total_cost = new_moves + heuristic_value
                        # Queue this board to be explored in cost order.
                        heapq.heappush(
                            boards_to_check,
                            (total_cost, new_moves, new_board)
                        )

        # The queue ran out, so return no path and the number of boards that were explored.
        return None, expanded_nodes
