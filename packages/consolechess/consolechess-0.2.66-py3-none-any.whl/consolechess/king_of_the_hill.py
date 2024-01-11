"""King of the hill chess."""

from .board import COLORS, ChessBoard, Color, GameStatus


class KingOfTheHillBoard(ChessBoard):
    """King of the hill chessboard."""

    def __init__(
        self,
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a KingOfTheHillBoard."""
        super().__init__(fen, pgn, empty=empty, import_fields=import_fields)
        self._fields["Variant"] = "King of the Hill"
        for color in COLORS:
            self._has_moved["king", color, None] = True

    def __repr__(self) -> str:
        """Represent KingOfTheHillBoard as string."""
        if self.AUTOPRINT:
            self.print()
        return f"KingOfTheHillBoard('{self.fen}')"

    def is_checkmate(self, *, kings_known_in_check: list[Color] | None = None) -> bool:
        """Check if either color's king is checkmated."""
        for color in COLORS:
            if self._kings[color] in ("d4", "d5", "e4", "e5"):
                self._moves[-1] = (
                    self._moves[-1].replace("+", "").replace("#", "") + "#"
                )
                self._status = GameStatus(
                    game_over=True, winner=color, description="king_reached_hill"
                )
                return True
        return super().is_checkmate(kings_known_in_check=kings_known_in_check)
