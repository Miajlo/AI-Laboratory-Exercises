import time

class NQueens:
    def __init__(self, size, num_queens, mrv = True):
        self.size = size
        self.num_queens = num_queens
        self.board = [-1] * num_queens
        self.domains = [set(range(size)) for _ in range(num_queens)]
        self.total_passes = 0
        self.mrv = mrv

    def count_remaining_moves(self, row, col):
        """Count valid moves for rows below the current row."""
        count = 0
        for r in range(row + 1, self.num_queens):
            # Calculate potential conflicts
            diagonal_left = col - (r - row)
            diagonal_right = col + (r - row)

            # Count valid moves: exclude conflicts from the domain
            if col not in self.domains[r]:
                count += 1
            if diagonal_left not in self.domains[r]:
                count += 1
            if diagonal_right not in self.domains[r]:
                count += 1
            self.total_passes += 1
        return count

    def mrv_heuristic(self, row):
        """Return columns for a given row sorted by Minimum Remaining Values (MRV)."""

        return sorted(self.domains[row], key=lambda col: self.count_remaining_moves(row, col)) # N logN * C


    def custom_heuristic(self, row):

        def count_effected_squares(col):
            count = 0
            for r in range(row + 1, self.num_queens):
                if col in self.domains[r]:
                    count += 1
                if (col - (r - row)) in self.domains[r]:
                    count += 1
                if (col + (r - row)) in self.domains[r]:
                    count += 1
                self.total_passes += 1
            return count

        # Sort the columns by the number of remaining valid moves
        return sorted(self.domains[row], key=count_effected_squares)

    def forward_check(self, row, col):
        """Update domains using forward checking when a queen is placed."""
        updates = []
        for r in range(row + 1, self.num_queens):
            self.total_passes += 1
            for conflict in (col, col - (r - row), col + (r - row)):
                if conflict in self.domains[r]:
                    self.domains[r].remove(conflict)
                    updates.append((r, conflict))
            if not self.domains[r]:  # Early exit if any domain becomes empty
                return False, updates
        return True, updates

    def restore_domains(self, updates):
        """Undo the changes to the domains."""
        for r, col in updates:
            self.domains[r].add(col)

    def solve(self, row=0):
        """Solve the N-Queens problem using backtracking with MRV and forward checking."""
        if row == self.num_queens:
            return True

        for col in self.mrv_heuristic(row) if self.mrv else self.custom_heuristic(row):
            self.board[row] = col
            is_valid, updates = self.forward_check(row, col)

            if is_valid and self.solve(row + 1):
                return True

            self.restore_domains(updates)  # Backtrack: Restore domains
            self.board[row] = -1
        return False

    def print_board(self):
        """Print the board configuration."""
        for r in range(self.size):
            row = ["Q" if r < self.num_queens and self.board[r] == c else "." for c in range(self.size)]
            print(" ".join(row))
        print()

if __name__ == "__main__":
    use_mrv = False
    n = 16  # Size of the board (n x n)
    num_queens = 16  # Number of queens to place
    nq = NQueens(n, num_queens, use_mrv)

    start_time = time.time()
    if nq.solve():
        print("Solution found:")
        nq.print_board()
    else:
        print("No solution exists.")

    end_time = time.time()
    print("Time taken:", end_time - start_time)
    print("Total passes: ", nq.total_passes)
