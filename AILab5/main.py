import time

class NQueens:
    def __init__(self, size, num_queens):
        self.size = size
        self.num_queens = num_queens
        self.board = [-1] * num_queens  # Represents the queen positions on the board. -1 means no queen placed yet.
        self.domains = [set(range(size)) for _ in range(num_queens)]
        self.total_passes = 0

    def is_safe(self, row, col):
        """Check if placing a queen at (row, col) is safe."""
        for r in range(row):
            c = self.board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def mrv_heuristic(self, row):
        """Return columns for a given row sorted by Minimum Remaining Values (MRV)."""
        num_queens = self.num_queens
        #print("pre: ", self.domains)
        def count_remaining_moves(col):
            """Count how many valid moves remain for all rows below the current row."""
            valid_moves = 0
            for r in range(row + 1, num_queens):

                if col not in self.domains[r]:
                    valid_moves += 1
                if col - (r - row) not in self.domains[r]:
                    valid_moves += 1
                if col + (r - row) not in self.domains[r]:
                    valid_moves += 1

                self.total_passes += 1

            return valid_moves

        # Sort columns in the domain of the current row by remaining valid moves
        return sorted(self.domains[row], key=count_remaining_moves)



    def forward_check(self, row, col):
        """Update domains using forward checking when a queen is placed."""
        updated_domains = [set(self.domains[i]) for i in range(self.num_queens)]
        for r in range(row + 1, self.num_queens):
            self.total_passes += 1
            if col in updated_domains[r]:
                updated_domains[r].remove(col)
            diagonal_left = col - (r - row)
            diagonal_right = col + (r - row)
            if diagonal_left in updated_domains[r]:
                updated_domains[r].remove(diagonal_left)
            if diagonal_right in updated_domains[r]:
                updated_domains[r].remove(diagonal_right)
        return updated_domains

    def solve(self, row=0):
        """Solve the N-Queens problem using backtracking, forward checking, and degree heuristic."""
        if row == self.num_queens:  # Solution is found when we've placed all queens
            return True

        for col in self.mrv_heuristic(row):
            if self.is_safe(row, col):
                self.board[row] = col
                original_domains = self.domains
                self.domains = self.forward_check(row, col)

                if all(self.domains[r] for r in range(row + 1, self.num_queens)) and self.solve(row + 1):
                    return True

                self.domains = original_domains
                self.board[row] = -1
                self.total_passes += 1
        return False

    def print_board(self):
        """Print the board configuration."""
        for r in range(self.size):
            row = ["Q" if r < self.num_queens and self.board[r] == c else "." for c in range(self.size)]
            print(" ".join(row))
        print()

if __name__ == "__main__":
    n = 30  # Size of the board (n x n)
    num_queens = 30  # Number of queens to place
    nq = NQueens(n, num_queens)

    start_time = time.time()
    if nq.solve():
        print("Solution found:")
        nq.print_board()
    else:
        print("No solution exists.")

    end_time = time.time()
    print("Time taken:", end_time - start_time)
    print("Total passes: ", nq.total_passes)
