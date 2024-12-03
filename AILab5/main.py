class NQueens:
    def __init__(self, size, num_queens):
        self.size = size
        self.num_queens = num_queens
        self.board = [-1] * num_queens  # Represents the queen positions on the board. -1 means no queen placed yet.
        self.domains = [list(range(size)) for _ in range(num_queens)]  # Domains of each row.

    def is_safe(self, row, col):
        """Check if placing a queen at (row, col) is safe."""
        for r in range(row):
            c = self.board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def mrv_heuristic(self, row):
        """Return columns for a given row sorted by Minimum Remaining Values (MRV)."""
        return sorted(self.domains[row], key=lambda col: len([
            r for r in range(row + 1, self.num_queens)  # Check rows below
            if col in self.domains[r] or
               col - (r - row) in self.domains[r] or
               col + (r - row) in self.domains[r]
        ]))

    def forward_check(self, row, col):
        """Update domains using forward checking when a queen is placed."""
        updated_domains = [list(self.domains[i]) for i in range(self.num_queens)]
        print("placement:", row, col)
        print("pre", updated_domains)
        for r in range(row + 1, self.num_queens):
            if col in updated_domains[r]:
                updated_domains[r].remove(col)
            diagonal_left = col - (r - row)
            diagonal_right = col + (r - row)
            if diagonal_left in updated_domains[r]:
                updated_domains[r].remove(diagonal_left)
            if diagonal_right in updated_domains[r]:
                updated_domains[r].remove(diagonal_right)
        print("post:", updated_domains)
        return updated_domains


    def count_constraints(self, row, col):
        """Count constraints imposed by placing a queen at (row, col)."""
        count = 0
        for r in range(row + 1, self.num_queens):
            if col in self.domains[r]:
                count += 1
            diagonal_left = col - (r - row)
            diagonal_right = col + (r - row)
            if diagonal_left in self.domains[r]:
                count += 1
            if diagonal_right in self.domains[r]:
                count += 1
        return count


    def degree_heuristic(self, row):
        """Apply degree heuristic to choose the next column."""
        a = sorted(self.domains[row], key=lambda col: self.count_constraints(row, col))
        print(a)
        return a

    def solve(self, row=0):
        """Solve the N-Queens problem using backtracking, forward checking, and degree heuristic."""
        if row == self.num_queens:
            return True

        for col in self.degree_heuristic(row):
            if self.is_safe(row, col):
                self.board[row] = col
                original_domains = self.domains
                self.domains = self.forward_check(row, col)

                if all(self.domains[r] for r in range(row + 1, self.num_queens)) and self.solve(row + 1):
                    return True

                self.domains = original_domains
                self.board[row] = -1

        return False

    def print_board(self):
        """Print the board configuration."""
        for r in range(self.size):
            row = ["Q" if r < self.num_queens and self.board[r] == c else "." for c in range(self.size)]
            print(" ".join(row))
        print()

if __name__ == "__main__":
    n = 8  # Size of the board (n x n)
    num_queens = 4  # Number of queens to place
    nq = NQueens(n, num_queens)

    if nq.solve() and n <= num_queens:
        print("Solution found:")
        nq.print_board()
    else:
        print("No solution exists.")
