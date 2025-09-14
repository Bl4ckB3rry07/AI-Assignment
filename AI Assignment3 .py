import chess
import time

class State:
    def __init__(self, board=None, player=True):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        self.player = player  # True = White's turn, False = Black's turn

    def goalTest(self):
        # Check if the game is over
        if self.board.is_checkmate():
            return not self.player  # The opponent just made a winning move
        return None

    def isTerminal(self):
        return self.board.is_game_over()

    def moveGen(self):
        # Generate next states
        children = []
        for move in self.board.legal_moves:
            new_board = self.board.copy()
            new_board.push(move)
            children.append(State(new_board, not self.player))
        return children

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        return self.board.fen() == other.board.fen() and self.player == other.player

    def __hash__(self):
        return hash((self.board.fen(), self.player))

    def evaluate(self):

        if self.board.is_checkmate():
            return -1000 if self.player else 1000  # Current player is mated
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            return 0

        score = 0.0

        # Material values
        piece_values = {
            chess.PAWN: 1.0,
            chess.KNIGHT: 3.0,
            chess.BISHOP: 3.0,
            chess.ROOK: 5.0,
            chess.QUEEN: 9.0,
            chess.KING: 0.0  # King has no material value
        }

        # (a) Material balance
        for sq, piece in self.board.piece_map().items():
            value = piece_values.get(piece.piece_type, 0.0)
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        # (b) Center control (bonus for pieces on central squares)
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        center_bonus = 0.2
        for sq in center_squares:
            piece = self.board.piece_at(sq)
            if piece:
                if piece.color == chess.WHITE:
                    score += center_bonus
                else:
                    score -= center_bonus

        # (c) Mobility (number of legal moves)
        mobility_factor = 0.05
        b = self.board.copy()
        b.turn = chess.WHITE
        white_mobility = len(list(b.legal_moves))
        b.turn = chess.BLACK
        black_mobility = len(list(b.legal_moves))
        score += mobility_factor * (white_mobility - black_mobility)

        # (d) King safety (penalty for attackers on king)
        safety_penalty = 0.5
        white_king_sq = self.board.king(chess.WHITE)
        black_king_sq = self.board.king(chess.BLACK)
        if white_king_sq is not None:
            black_attackers = self.board.attackers(chess.BLACK, white_king_sq)
            score -= safety_penalty * len(black_attackers)
        if black_king_sq is not None:
            white_attackers = self.board.attackers(chess.WHITE, black_king_sq)
            score += safety_penalty * len(white_attackers)

        return score
        # ------------------------------------


def minimax(state, depth, alpha, beta, maximizingPlayer, maxDepth):
    if state.isTerminal() or depth == maxDepth:
        return state.evaluate(), None

    best_move = None

    if maximizingPlayer:  # MAX node (White)
        maxEval = float('-inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, False, maxDepth)

            if eval_score > maxEval:
                maxEval = eval_score
                best_move = child.board.peek()  # Last move made

            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break  # Alpha-beta pruning

        return maxEval, best_move

    else:  # MIN node (Black)
        minEval = float('inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, True, maxDepth)

            if eval_score < minEval:
                minEval = eval_score
                best_move = child.board.peek()

            beta = min(beta, eval_score)
            if alpha >= beta:
                break

        return minEval, best_move


def play_game():
    current_state = State(player=True)  # White starts
    maxDepth = 3  # Try experimenting with the Search depth for more inteligent ai

    print("Artificial Intelligence – Assignment 3")
    print("Simple Chess AI (Text Mode)")
    print("You are playing as White (enter moves in UCI format, e.g., e2e4)")
    print("Type 'quit' to stop.")

    while not current_state.isTerminal():
        # Update the display (text only)
        print("\nCurrent board:")
        print(current_state)
        print("\nLegal moves:", [move.uci() for move in current_state.board.legal_moves])

        if current_state.player:  # Human move (White)
            try:
                move_uci = input("\nEnter your move (e.g., e2e4, g1f3, a7a8q) or 'quit': ")

                if move_uci.lower() == 'quit':
                    break

                move = chess.Move.from_uci(move_uci)

                if move in current_state.board.legal_moves:
                    new_board = current_state.board.copy()
                    new_board.push(move)
                    current_state = State(new_board, False)
                else:
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Invalid input format! Use UCI format like 'e2e4'.")
                continue
        else:  # AI move (Black)
            print("AI is thinking...")
            start_time = time.time()
            eval_score, best_move = minimax(current_state, 0, float('-inf'), float('inf'), False, maxDepth)
            end_time = time.time()

            print(f"AI thought for {end_time - start_time:.2f} seconds")

            if best_move:
                new_board = current_state.board.copy()
                new_board.push(best_move)
                current_state = State(new_board, True)
                print(f"AI plays: {best_move.uci()}")
            else:
                # Fallback
                legal_moves = list(current_state.board.legal_moves)
                if legal_moves:
                    move = legal_moves[0]
                    new_board = current_state.board.copy()
                    new_board.push(move)
                    current_state = State(new_board, True)
                    print(f"AI plays (fallback): {move.uci()}")
                else:
                    break

    # Game over
    print("\nGame over!")
    print("Final board:")
    print(current_state)

    if current_state.board.is_checkmate():
        print("Checkmate! " + ("White" if not current_state.player else "Black") + " wins!")
    elif current_state.board.is_stalemate():
        print("Stalemate! It's a draw.")
    elif current_state.board.is_insufficient_material():
        print("Insufficient material! It's a draw.")
    elif current_state.board.can_claim_draw():
        print("Draw by repetition or 50-move rule!")


if __name__ == "__main__":
    play_game()
