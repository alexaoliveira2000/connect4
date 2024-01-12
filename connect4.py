import numpy as np

class Game:
    def __init__(self, player, depth = 5):
        self.board = np.zeros((6,7))
        self.human = player
        self.computer = 2 if player == 1 else 1
        self.depth = depth

    def can_insert(self, column):
        return column >= 0 and column <= 6 and self.board[0, column] == 0
    
    def insert(self, board, player, column):
        row = 5
        while row >= 0 and board[row, column] != 0:
            row -= 1
        board[row, column] = player
        return board

    def successors(self, board, player):
        possible_moves = []
        for column in range(7):
            if self.can_insert(column):
                successor = self.insert(np.copy(board), player, column)
                possible_moves.append(successor)
        return possible_moves
    
    def has_won(self, player):
        for row in range(6):
            for col in range(4):
                if all(self.board[row, col + i] == player for i in range(4)):
                    return True
        for col in range(7):
            for row in range(3, 6):
                if all(self.board[row - i, col] == player for i in range(4)):
                    return True
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i, col + i] == player for i in range(4)):
                    return True
        for row in range(3, 6):
            for col in range(3, 7):
                if all(self.board[row - i, col - i] == player for i in range(4)):
                    return True
                
    def play(self):
        _, move = self.max_value(self.board, float('-inf'), float('inf'), self.depth, self.computer)
        return move
    
    def max_value(self, board, alpha, beta, depth, player):
        if depth == 0 or self.has_won(self.computer) or self.has_won(self.human):
            return self.utility(board), None
        best_value = float('-inf')
        best_successor = None
        next_player = 2 if player == 1 else 1
        for successor in self.successors(board, player):
            value, _ = self.min_value(successor, alpha, beta, depth - 1, next_player)
            if value > best_value:
                best_value = value
                best_successor = successor
            if value >= beta:
                return best_value, best_successor
            alpha = max(alpha, best_value)
        return best_value, best_successor

    def min_value(self, board, alpha, beta, depth, player):
        if depth == 0 or self.has_won(self.computer) or self.has_won(self.human):
            return self.utility(board), None
        best_value = float('inf')
        best_successor = None
        next_player = 2 if player == 1 else 1
        for successor in self.successors(board, player):
            value, _ = self.max_value(successor, alpha, beta, depth - 1, next_player)
            if value < best_value:
                best_value = value
                best_successor = successor
            if value <= alpha:
                return best_value, best_successor
            beta = min(beta, best_value)
        return best_value, best_successor

    def utility(self, board):
        computer_sequence_counts = self.count_sequences(board, self.computer)
        human_sequence_counts = self.count_sequences(board, self.human)
        if human_sequence_counts[4] > 0:
            return -3
        elif computer_sequence_counts[4] > 0:
            return 3
        elif human_sequence_counts[3] > 0:
            return -2
        elif computer_sequence_counts[3] > 0:
            return 2
        elif human_sequence_counts[2] > 0:
            return -1
        elif computer_sequence_counts[2] > 0:
            return 1
        return 0

    def count_sequences(self, board, player):
        sequence_counts = {2: 0, 3: 0, 4: 0}
        for row in range(6):
            sequence_counts = self.update_sequence_counts(board[row, :], player, sequence_counts)
        for col in range(7):
            sequence_counts = self.update_sequence_counts(board[:, col], player, sequence_counts)
        for i in range(-2, 4):
            sequence_counts = self.update_sequence_counts(np.diagonal(board, i), player, sequence_counts)
        for i in range(-2, 4):
            sequence_counts = self.update_sequence_counts(np.diagonal(np.flipud(board), i), player, sequence_counts)
        return sequence_counts

    def update_sequence_counts(self, line, player, sequence_counts):
        current_count = 0
        for cell in line:
            if cell == player:
                current_count += 1
                if current_count >= 2:
                    sequence_counts[current_count] = sequence_counts.get(current_count, 0) + 1
            else:
                current_count = 0
        return sequence_counts

    def start(self):
        player = 1
        while not self.has_won(self.computer) and not self.has_won(self.human):
            self.show_board()
            if player == self.computer:
                self.board = self.play()
            else:
                can_insert = False
                column = None
                while not can_insert:
                    column = int(input("Column: "))
                    can_insert = self.can_insert(column)
                self.board = self.insert(self.board, self.human, column)
            player = 2 if player == 1 else 1
        self.show_board()
        if self.has_won(self.computer):
            print("Computer has won!")
        elif self.has_won(self.human):
            print("Human has won!")

    def show_board(self):
        for row in range(6):
            for col in range(7):
                if self.board[row, col] == 0:
                    print("| ", end="")
                elif self.board[row, col] == self.computer:
                    print("|O", end="")
                else:
                    print("|X", end="")
            print("|")
        print("---------------")

game = Game(player = 2)
game.start()