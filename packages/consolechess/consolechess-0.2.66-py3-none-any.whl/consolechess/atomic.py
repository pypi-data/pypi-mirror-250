"""Atomic chess."""

from collections.abc import Iterator
from typing import Literal, overload

from .board import (
    CASTLING_FINAL_SQUARES,
    COLORS,
    DIRECTION_GENERATORS,
    FILES,
    PLAINTEXT_ABBRS,
    SIDES,
    ChessBoard,
    Color,
    GameStatus,
    InvalidMoveError,
    OtherPlayersTurnError,
    Piece,
    PieceType,
    Side,
    en_passant_final_square_from_file,
    en_passant_final_square_from_pawn_square,
    get_adjacent_squares,
    king_navigable_squares,
    other_color,
    step_left,
    step_right,
)


class AtomicBoard(ChessBoard):
    """Atomic chessboard."""

    def __init__(
        self,
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a Crazyhouse board."""
        super().__init__(fen=fen, pgn=pgn, empty=empty, import_fields=import_fields)
        self._fields["Variant"] = "Atomic"

    def __repr__(self) -> str:
        """Represent board as string."""
        if self.AUTOPRINT:
            self.print()
        return f"AtomicBoard('{self.fen}')"

    def promote_pawn(self, square: str, piece_type: PieceType) -> None:
        """Promote a pawn on the farthest rank from where it started."""
        if self[square] is None:
            self._double_forward_last_move = None
            self._must_promote_pawn = None
            updated_notation = f"{self._moves[-1]}={PLAINTEXT_ABBRS[piece_type]}"
            if self.king_is_in_check(oc := other_color(self.turn)):
                if self.is_checkmate(kings_known_in_check=[oc]) or self.king_exploded():
                    updated_notation += "#"
                else:
                    updated_notation += "+"
            self._moves[-1] = updated_notation
            self.alternate_turn(reset_halfmove_clock=True)
        else:
            super().promote_pawn(square, piece_type)

    def king_is_in_check(self, color: Color) -> bool | None:
        """Whether king is in check."""
        if self._kings.get(color) is None:
            return None
        if self.king_exploded():
            return False
        if any(
            (pc := self[sq]) is not None
            and pc.piece_type == "king"
            and pc.color == other_color(color)
            for sq in king_navigable_squares(self._kings[color])
        ):
            return False
        return super().king_is_in_check(color)

    def _explode(self, final_square: str) -> None:
        """Create an atomic "explosion" after a capture."""
        for sq in self._explosion_dict(final_square):
            if (pc := self._grid[sq]) is not None and pc.piece_type == "king":
                self._status = GameStatus(
                    game_over=True,
                    winner=other_color(pc.color),
                    description="explosion",
                )
            self[sq] = None

    def _explosion_dict(self, final_square: str) -> dict[str, Piece | None]:
        """Return dict of explosion changes without actually exploding."""
        return {
            sq: None
            for sq in (final_square, *king_navigable_squares(final_square))
            if sq == final_square
            or ((pc := self._grid[sq]) is not None and pc.piece_type != "pawn")
        }

    def king_exploded(self) -> GameStatus | None:
        """Whether a king has exploded (ending the game)."""
        for color in COLORS:
            if self[self._kings[color]] is None:
                return GameStatus(
                    game_over=True, winner=other_color(color), description="explosion"
                )
        return None

    def can_explode_opponent_king(self, color: Color) -> bool:
        """Whether color can indirectly explode opponent's king."""
        return self.can_explode_piece(self._kings[other_color(color)])

    def can_explode_piece(self, square: str) -> bool:
        """Whether a piece can be removed by capturing an adjacent piece."""
        piece = self._grid[square]
        if piece is None:
            msg = f"No piece at square '{square}'."
            raise ValueError(msg)
        unsafe_to_capture = [
            sq
            for sq in king_navigable_squares(self._kings[other_color(piece.color)])
            if (pc := self[sq]) is not None
        ]
        if_captured_then_piece_explodes = (
            [
                sq
                for sq in king_navigable_squares(square)
                if (pc := self[sq]) is not None
                and pc.color == piece.color
                and sq not in unsafe_to_capture
            ]
            if piece.piece_type != "pawn"
            else []
        )
        other_color_pieces = [
            sq
            for sq in self
            if (pc := self._grid[sq]) is not None
            and pc.color == other_color(piece.color)
        ]
        for square_ in other_color_pieces:
            if any(
                sq in if_captured_then_piece_explodes
                for sq in self._pseudolegal_squares(square_, capture_only=True)
                if self.can_move_piece(square_, sq)
            ):
                return True
        return False

    def _king_pseudolegal_squares(
        self,
        initial_square: str,
        piece: Piece,
        *,
        check_castle: bool = False,
    ) -> Iterator[str]:
        """Get king pseudolegal squares (ignores king capture rules)."""
        yield from (
            sq
            for sq in king_navigable_squares(initial_square)
            if self._grid[sq] is None
        )
        if check_castle:
            yield from (
                CASTLING_FINAL_SQUARES[piece.color, side][1]
                for side in SIDES
                if self.can_castle(piece.color, side)
            )

    def can_explode_out_of_check(self, color: Color) -> bool:
        """Whether check can be resolved by exploding a threatening piece."""
        return all(
            self.can_explode_piece(sq) for sq in self.get_threatening_pieces(color)
        )

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: Literal[False],
        game_over_checked: bool = False,
    ) -> None: ...

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: Literal[True],
        game_over_checked: bool = False,
    ) -> dict[str, str | bool]: ...

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: bool = False,
        game_over_checked: bool = False,
    ) -> dict[str, str | bool] | None: ...

    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: bool = False,
        game_over_checked: bool = False,
    ) -> dict[str, str | bool] | None:
        """Move a game piece."""
        piece = self._grid[initial_square]
        if not skip_checks and self._must_promote_pawn is not None:
            if piece is None:
                msg = f"No piece at initial_square '{initial_square}'."
                raise InvalidMoveError(msg)
            msg = (
                f"Must promote pawn at square '{self._must_promote_pawn}' "
                "before next move."
            )
            raise InvalidMoveError(msg)
        assert piece is not None
        if (
            not skip_checks
            and self._grid[final_square] is not None
            and (
                piece.piece_type == "king"
                or self._kings[piece.color] in king_navigable_squares(final_square)
            )
        ):
            msg = "Suicidal capture not allowed."
            raise InvalidMoveError(msg)
        if allow_castle_and_en_passant:
            # Try to castle if king is moving to a final castling square,
            # or if rook is jumping over a king.
            castle_side: Side = (
                "queenside" if final_square[0] in ("c", "d") else "kingside"
            )
            if (
                piece.piece_type == "king"
                and final_square in ("c1", "c8", "g1", "g8")
                and self.can_castle(piece.color, castle_side)
            ):
                self.castle(piece.color, castle_side, skip_checks=True)
                return (
                    {"move_type": "castle", "side": castle_side}
                    if return_metadata
                    else None
                )
            # Reroute to self.en_passant if pawn captures on empty final square.
            if (
                piece.piece_type == "pawn"
                and initial_square[0] != final_square[0]
                and self._grid[final_square] is None
            ):
                self.en_passant(initial_square, final_square)
                return (
                    {"move_type": "en_passant", "capture": True}
                    if return_metadata
                    else None
                )

        if not skip_checks:
            # Check correct player's piece is being moved.
            if not ignore_turn and piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            # Check piece can navigate to square.
            if final_square not in self._pseudolegal_squares(
                initial_square, check_castle=False
            ):
                msg = "Not a valid move."
                raise InvalidMoveError(msg)
            # Test if king would be in check if moved.
            king_would_be_in_check = False
            changes = {final_square: piece, initial_square: None}
            if self._grid[final_square] is not None:
                changes.update(self._explosion_dict(final_square))
            with self.test_position(changes):
                if self.king_is_in_check(self.turn):
                    king_would_be_in_check = True
            if king_would_be_in_check:
                msg = "Cannot move piece because king would be in check."
                raise InvalidMoveError(msg)

        # Add piece type notation, disambiguating if necessary.
        piece_at_final_square = self._grid[final_square]
        notation = (
            PLAINTEXT_ABBRS[piece.piece_type] if piece.piece_type != "pawn" else ""
        )
        notation += self._write_disambiguator(
            initial_square,
            final_square,
            piece,
            piece_at_final_square,
            no_disambiguator=no_disambiguator,
        )

        # Update clocks and notation to denote capture, and raise exceptions
        # for illegal captures.
        if piece_at_final_square is not None:
            if piece.piece_type == "pawn" and len(notation) == 0:
                notation += initial_square[0]
            notation += "x"
            is_capture = True
            if piece_at_final_square.color == piece.color:
                msg = "Cannot place piece at square occupied by same color piece."
                raise InvalidMoveError(msg)
            elif piece_at_final_square.piece_type == "king":
                msg = "Cannot capture king."
                raise InvalidMoveError(msg)
        else:
            is_capture = False
        notation += final_square

        # Update has_moved variables (used to determine castling availability).
        if piece.piece_type == "king":
            self._has_moved["king", piece.color, None] = True
        elif piece.piece_type == "rook":
            if initial_square == self._initial_squares.get(
                ("rook", piece.color, "kingside")
            ):
                side: Side | None = "kingside"
            elif initial_square == self._initial_squares.get(
                ("rook", piece.color, "queenside")
            ):
                side = "queenside"
            else:
                side = None
            if side is not None:
                self._has_moved["rook", piece.color, side] = True
        self._double_forward_last_move = (
            final_square
            if piece.piece_type == "pawn"
            and abs(int(initial_square[1]) - int(final_square[1])) == 2
            else None
        )

        # Move piece.
        self[initial_square] = None
        if not piece.has_moved and piece.piece_type == "pawn":
            piece = Piece(
                piece_type=piece.piece_type,
                color=piece.color,
                promoted=piece.promoted,
                has_moved=True,
            )
        self[final_square] = piece
        if is_capture:
            self._explode(final_square)

        # If pawn moving to final rank, require pawn promotion. Else, check
        # for check / checkmate, append moves, and return.
        if piece.piece_type == "pawn" and final_square[1] in ("1", "8"):
            self._must_promote_pawn = final_square
        else:
            self._must_promote_pawn = None
            if self.king_is_in_check(oc := other_color(self.turn)):
                if self.is_checkmate(kings_known_in_check=[oc]) or self.king_exploded():
                    notation += "#"
                else:
                    notation += "+"
            self.alternate_turn(
                reset_halfmove_clock=(piece.piece_type == "pawn" or is_capture),
            )
        self._moves.append(notation)
        return (
            (
                {
                    "move_type": "normal",
                    "capture": is_capture,
                    "capture_piece_type": piece_at_final_square.piece_type,
                    "capture_piece_is_promoted": piece_at_final_square.promoted,
                }
                if piece_at_final_square is not None
                else {"move_type": "normal", "capture": is_capture}
            )
            if return_metadata
            else None
        )

    def en_passant(
        self,
        initial_square: str,
        final_square: str,
        *,
        skip_checks: bool = False,
        game_over_checked: bool = False,
    ) -> None:
        """Capture an adjacent file pawn that has just made a double forward advance."""
        super().en_passant(initial_square, final_square, skip_checks=skip_checks)
        self._explode(final_square)
        self._moves[-1] = self._moves[-1].replace("+", "").replace("#", "")
        if self.king_is_in_check(self.turn):
            if (
                self.is_checkmate(kings_known_in_check=[self.turn])
                or self.king_exploded()
            ):
                self._moves[-1] += "#"
            else:
                self._moves[-1] += "+"

    @property
    def status(self) -> GameStatus:
        """Check the board for a checkmate or draw."""
        if self.king_exploded():
            return self._status
        return super().status

    def can_move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        navigability_already_checked: bool = False,
    ) -> bool:
        """
        Check if a piece can be moved to final_square without castling or en passant.
        Does not check turn.
        """
        piece = self._grid[initial_square]
        piece_at_final_square = self._grid[final_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        if (
            not navigability_already_checked
            and final_square
            not in self._pseudolegal_squares(initial_square, check_castle=False)
        ):
            return False
        if piece_at_final_square is not None and (
            (
                piece_at_final_square.piece_type == "king"
                and piece_at_final_square.color == piece.color
            )
            or piece.piece_type == "king"
        ):
            return False
        changes = {final_square: piece, initial_square: None}
        if piece_at_final_square is not None:
            changes.update(self._explosion_dict(final_square))
        with self.test_position(changes):
            if self.king_is_in_check(piece.color):
                return False
        return True

    def is_checkmate(self, *, kings_known_in_check: list[Color] | None = None) -> bool:
        """Check if either color's king is checkmated."""
        if self.king_exploded():
            return True
        for color in COLORS:
            if (
                (
                    (kings_known_in_check is not None and color in kings_known_in_check)
                    or self.king_is_in_check(color)
                )
                and not self.can_block_or_capture_check(color)
                and not self.king_can_escape_check(color)
                and not self.can_explode_opponent_king(color)
                and not self.can_explode_out_of_check(color)
            ):
                self._status = GameStatus(
                    game_over=True, winner=other_color(color), description="checkmate"
                )
                return True
        return False

    @property
    def moves(self) -> str:
        """Export moves to string."""
        if self.is_checkmate():
            self._moves[-1] = f"{self._moves[-1].replace('+', '').replace('#', '')}#"
        return super().moves

    def checked_squares(self, color: Color) -> Iterator[str]:
        """Get all checked squares for a color."""
        oc = other_color(color)
        other_color_pieces = [
            sq for sq in self if (pc := self._grid[sq]) is not None and pc.color == oc
        ]
        protected_by_suicide_rule = king_navigable_squares(
            self._kings[other_color(color)]
        )
        already_yielded: list[str] = []
        for init_sq in other_color_pieces:
            for sq in self._pseudolegal_squares(
                init_sq, capture_only=True, check_castle=False
            ):
                if sq not in already_yielded and sq not in protected_by_suicide_rule:
                    yield sq
                    already_yielded.append(sq)

    def can_en_passant(
        self,
        initial_square: str | None = None,
        capture_file: str | None = None,
    ) -> bool:
        """Check if an en passant capture is possible."""
        if self._double_forward_last_move is None:
            return False
        if initial_square is None:
            return any(
                (pc := self._grid[sq]) is not None
                and pc.piece_type == "pawn"
                and pc.color == self.turn
                for sq in get_adjacent_squares(self._double_forward_last_move)
            )
        candidate_squares = []
        for func in (step_left, step_right):
            if (square := func(initial_square, 1)) is None:
                continue
            if capture_file is None or capture_file in square:
                candidate_squares.append(square)
        if (
            self._double_forward_last_move not in candidate_squares
            or (piece := self._grid[initial_square]) is None
        ):
            return False
        color = piece.color
        final_sq = en_passant_final_square_from_file(capture_file, color)
        changes = {
            initial_square: None,
            final_sq: Piece("pawn", color),
            self._double_forward_last_move: None,
        }
        changes.update(self._explosion_dict(final_sq))
        with self.test_position(changes):
            if self.king_is_in_check(color):
                return False
        return True

    def can_block_or_capture_check(
        self, color: Color, *, drop_pool: list[PieceType] | None = None
    ) -> bool | None:
        """
        Return True if a check can be blocked by another piece or if the threatening
        piece can be captured.
        """
        # Sort pieces by color.
        pieces = self.pieces
        same_color_pieces_except_king = []
        other_color_pieces = []
        king: str | None = None
        for sq in pieces:
            if (pc := pieces[sq]).color == color:
                if pc.piece_type == "king":
                    king = sq
                else:
                    same_color_pieces_except_king.append(sq)
            else:
                other_color_pieces.append(sq)
        if king is None:
            return None
        # Identify squares that, if occupied, would move the king out of check.
        squares_that_would_block_check = []
        for check in (
            checks := [
                piece
                for piece in other_color_pieces
                if king
                in self._pseudolegal_squares(
                    piece, capture_only=True, check_castle=False
                )
            ]
        ):
            if (rank_difference := int(king[1]) - int(check[1])) > 0:
                rank_direction = "up"  # i.e. king is upward of piece
            else:
                rank_direction = "inline" if rank_difference == 0 else "down"
            if (file_difference := FILES.index(king[0]) - FILES.index(check[0])) > 0:
                file_direction = "right"  # i.e. king is to the right of piece
            else:
                file_direction = "inline" if file_difference == 0 else "left"
            possible_squares = [
                check,
                *list(DIRECTION_GENERATORS[rank_direction, file_direction](check)),
            ]
            if self._kings[color] not in king_navigable_squares(check):
                if (pt := pieces[check].piece_type) in ("knight", "pawn"):
                    squares_that_would_block_check.append(check)
                if pt in ("rook", "bishop", "queen"):
                    for square in possible_squares:
                        if square == king:
                            break
                        squares_that_would_block_check.append(square)
        # Aggregate possible moves.
        possible_moves: list[tuple[str, str]] = []  # [(from, to), ...]
        for sq in same_color_pieces_except_king:
            possible_moves.extend(
                [
                    (sq, move)
                    for move in self._pseudolegal_squares(sq, check_castle=False)
                ]
            )
        # Check if en passant capture can block check.
        if self._double_forward_last_move is not None:
            for square in get_adjacent_squares(self._double_forward_last_move):
                if (
                    (piece := self._grid[square]) is not None
                    and piece.piece_type == "pawn"
                    and piece.color == color
                    and self.can_en_passant(square, self._double_forward_last_move[0])
                ):
                    with self.test_position(
                        {
                            self._double_forward_last_move: None,
                            square: None,
                            en_passant_final_square_from_pawn_square(
                                self._double_forward_last_move, color
                            ): Piece("pawn", color),
                        }
                    ):
                        if not self.king_is_in_check(color):
                            return True
        # Check if player can navigate to square that would block check.
        squares_that_can_be_moved_to = [move[1] for move in possible_moves]
        for square in squares_that_can_be_moved_to:
            if square in squares_that_would_block_check:
                candidates = [move for move in possible_moves if move[1] == square]
                for initial_sq, final_sq in candidates:
                    changes = {initial_sq: None, final_sq: self._grid[initial_sq]}
                    if self._grid[final_sq] is not None:
                        changes.update(self._explosion_dict(final_sq))
                    with self.test_position(changes):
                        if not self.king_is_in_check(color):
                            return True
        return False
