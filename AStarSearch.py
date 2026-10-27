import heapq


class AStarSearch:
    """Finds a shortest path between two boards using A*."""

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def search(self, start, heuristic_name="manhattan"):
        # Reject impossible boards before constructing or expanding the search.
        if not self.puzzle.is_solvable(start):
            return None, 0

        # Tuples are immutable, so boards can be used as dictionary keys.
        start = tuple(tuple(row) for row in start)
        goal = tuple(tuple(row) for row in self.puzzle.goal)

        # Each queue item stores estimated total cost, moves so far, and board.
        boards_to_check = [
            (self.puzzle.get_heuristic(start, heuristic_name), 0, start)
        ]
        moves_so_far = {start: 0}
        previous_board = {start: None}
        expanded_nodes = 0

        # Keep searching while boards remain not empty and heappop takes the element
        # with the lowest estimated cost.
        while boards_to_check:
            estimated_cost, moves, board = heapq.heappop(boards_to_check)

            if board == goal:
                path = []
                while board is not None:
                    path.append([list(row) for row in board])
                    board = previous_board[board]
                path.reverse()
                # The solution is either a path or None.
                return path, expanded_nodes

            # Skip an old queue entry if a shorter route to this board was found if for example i went up and then down again the  just start from the beggining
            if moves != moves_so_far[board]:
                continue

            expanded_nodes += 1
            # Gives the position where 0 is.
            zero_row, zero_column = self.puzzle.find_position(board, 0)
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

            for row_change, column_change in directions:
                new_row = zero_row + row_change
                new_column = zero_column + column_change

                # This if checks if we are still in bounds.
                if 0 <= new_row < 3 and 0 <= new_column < 3:
                    new_board = [list(row) for row in board]
                    # Here it swaps 0 with the number that was on the position where 0
                    # is going to be in the new board.
                    new_board[zero_row][zero_column] = new_board[new_row][new_column]
                    new_board[new_row][new_column] = 0
                    new_board = tuple(tuple(row) for row in new_board)
                    new_moves = moves + 1

                    # Here I check if the new board is one of the boards I already had
                    # before and, if yes, whether the number of moves was lower before.
                    if new_board not in moves_so_far or new_moves < moves_so_far[new_board]:
                        # Create key-value pair.
                        moves_so_far[new_board] = new_moves
                        # Add the new board to the list of the boards.
                        previous_board[new_board] = board
                        heuristic_value = self.puzzle.get_heuristic(
                            new_board, heuristic_name
                        )
                        # f(n) = g(n) + h(n)
                        total_cost = new_moves + heuristic_value
                        heapq.heappush(
                            boards_to_check,
                            (total_cost, new_moves, new_board)
                        )

        # If it checked all the possible boards and found no solution, there is no
        # solution and return None and expanded nodes.
        return None, expanded_nodes
