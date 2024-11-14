"""
The GameState superclass.

NOTE: You do not have to run python-ta on this file.
"""

from typing import Any


class GameState:
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        self.p1_turn = is_p1_turn

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        raise NotImplementedError

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        raise NotImplementedError

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        raise NotImplementedError

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        raise NotImplementedError

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        raise NotImplementedError


class SubtractSquareGameState(GameState):
    """
    Subtract Square game state, a game where players subtract square numbers
    from a total. The player who cannot make a move loses.
    """

    def __init__(self, is_p1_turn: bool, current_value: int) -> None:
        """
        Initialize the Subtract Square game state with the given current value
        and whose turn it is.
        """
        super().__init__(is_p1_turn)
        self.current_value = current_value

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return f'Current value: {self.current_value}, Player turn: {self.get_current_player_name()}'

    def get_possible_moves(self) -> list:
        """
        Return all possible moves (square numbers that can be subtracted)
        that can be applied to this state.
        """
        return [i * i for i in range(1, int(self.current_value ** 0.5) + 1)]

    def make_move(self, move: Any) -> 'SubtractSquareGameState':
        """
        Return the SubtractSquareGameState that results from applying move to this GameState.
        The move is a square number that is subtracted from the current value.
        """
        new_value = self.current_value - move
        return SubtractSquareGameState(not self.p1_turn, new_value)

    def __repr__(self) -> Any:
        """
        Return a representation of this state, which can be used for
        equality testing.
        """
        return f'SubtractSquareGameState(p1_turn={self.p1_turn}, current_value={self.current_value})'

    def rough_outcome(self) -> float:
        """
        Return an estimate of the best outcome the current player can guarantee.
        If the player has a winning move, return WIN; if no winning move is possible, return LOSE or DRAW.
        """
        if not self.get_possible_moves():
            return GameState.LOSE

        # Check if any move leads to a losing position for the opponent
        for move in self.get_possible_moves():
            next_state = self.make_move(move)
            if next_state.rough_outcome() == GameState.LOSE:
                return GameState.WIN

        return GameState.DRAW


if __name__ == "__main__":
    # Example interaction
    current_game_state = SubtractSquareGameState(True, 10)

    print("Initial game state:")
    print(current_game_state)

    # Game loop (for testing)
    while not current_game_state.get_possible_moves() == []:
        print(f"Possible moves: {current_game_state.get_possible_moves()}")
        move = int(input(f"{current_game_state.get_current_player_name()}'s turn. Choose your move: "))

        if current_game_state.is_valid_move(move):
            current_game_state = current_game_state.make_move(move)
            print(current_game_state)
        else:
            print("Invalid move. Try again.")

    if current_game_state.get_current_player_name() == 'p1':
        print("Player 2 wins!")
    else:
        print("Player 1 wins!")
