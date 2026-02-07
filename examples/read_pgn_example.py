#!/usr/bin/env python3
"""
Read PGN Example - Generate LaTeX from PGN file

This script reads a PGN file and produces a complete LaTeX document with:
1. All PGN headers
2. All comments from the PGN
3. Diagrams where there is a "D" annotation
4. All variations (sidelines)

Usage:
    python read_pgn_example.py <pgn_file> [--output <output.tex>] [--pdf]
"""

import argparse
import sys
from pathlib import Path
from io import StringIO
from typing import List, Optional, Tuple

# Add parent directory to path to import chess_generator
sys.path.insert(0, str(Path(__file__).parent.parent))

import chess
import chess.pgn
from chess_generator import ChessDiagramGenerator


def preprocess_pgn(pgn_content: str) -> str:
    """
    Preprocess PGN to convert standalone 'D' diagram annotations into comments.
    
    Some PGN formats use 'D' directly before a move (e.g., '15.Nd2 D Qc7?!')
    to indicate a diagram should be shown. This converts them to comments
    that python-chess will preserve: '15.Nd2 {DIAGRAM} Qc7?!'
    """
    import re
    
    # Pattern matches 'D ' that appears after a move or at start of a variation
    # but before another move. This handles patterns like:
    # - '15.Nd2 D Qc7?!' -> '15.Nd2 {DIAGRAM} Qc7?!'
    # - '18.Nxc5 D Bxc5?!' -> '18.Nxc5 {DIAGRAM} Bxc5?!'
    
    # Match 'D' followed by space and a move (letter or O for castling)
    pattern = r'\bD\s+([A-Za-z0-9]|O-O)'
    
    def replace_diagram(match):
        return '{DIAGRAM} ' + match.group(1)
    
    return re.sub(pattern, replace_diagram, pgn_content)


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in text."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def has_diagram_annotation(comment: str) -> bool:
    """Check if a comment indicates a diagram should be shown."""
    comment = comment.strip()
    return comment.startswith('D ') or comment == 'DIAGRAM' or comment.startswith('DIAGRAM ')


def strip_diagram_annotation(comment: str) -> str:
    """Remove diagram annotation from a comment if present."""
    comment = comment.strip()
    if comment.startswith('D '):
        return comment[2:].strip()
    if comment == 'DIAGRAM':
        return ''
    if comment.startswith('DIAGRAM '):
        return comment[8:].strip()
    return comment


def nag_to_symbol(nag: int) -> str:
    """Convert NAG (Numeric Annotation Glyph) to symbol or descriptive text."""
    # Standard PGN NAG definitions (1-139) for LaTeX output
    nag_symbols = {
        # Move assessments
        1: '!',      # Good move
        2: '?',      # Mistake
        3: '!!',     # Brilliant move
        4: '??',     # Blunder
        5: '!?',     # Interesting move
        6: '?!',     # Questionable move
        7: r'\nagforced ', # Only move
        8: '[singular move]',
        9: r'\nagworst ', # Worst move
        
        # Positional assessments
        10: '=',     # Drawish
        11: '[equal chances, quiet]',
        12: '[equal chances, active]',
        13: r'\nagunclear ', # Unclear
        14: r'\nagwbetter ', # Slight advantage White
        15: r'\nagbbetter ', # Slight advantage Black
        16: r'\nagwhitebetter ', # Better White
        17: r'\nagblackbetter ', # Better Black
        18: r'\nagwwinning ', # Winning White
        19: r'\nagbwinning ', # Winning Black
        20: r'+--',  # Crushing White
        21: r'--+',  # Crushing Black
        22: r'\nagzugzwang ', # Zugzwang White
        23: r'\nagzugzwang ', # Zugzwang Black
        24: '[space advantage White]',
        25: '[space advantage Black]',
        26: r'\ensuremath{\circ}',   # Space advantage White
        27: '[space advantage Black]',
        28: '[decisive space advantage White]',
        29: '[decisive space advantage Black]',
        30: '[development advantage White]',
        31: '[development advantage Black]',
        32: r'\nagdevadv ',   # Development advantage White
        33: r'\nagdevadv ',   # Development advantage Black
        34: '[decisive development advantage White]',
        35: '[decisive development advantage Black]',
        36: r'\naginitiative ', # Initiative White
        37: r'\naginitiative ', # Initiative Black
        38: '[lasting initiative White]',
        39: '[lasting initiative Black]',
        40: r'\nagattack ',   # Attack White
        41: r'\nagattack ',   # Attack Black
        42: '[insufficient compensation White]',
        43: '[insufficient compensation Black]',
        44: r'\nagcompensation ', # Compensation White
        45: '[compensation Black]',
        46: '[more than adequate compensation White]',
        47: '[more than adequate compensation Black]',
        48: '[center control advantage White]',
        49: '[center control advantage Black]',
        50: '[moderate center control White]',
        51: '[moderate center control Black]',
        52: '[decisive center control White]',
        53: '[decisive center control Black]',
        54: '[kingside control White]',
        55: '[kingside control Black]',
        56: '[moderate kingside control White]',
        57: '[moderate kingside control Black]',
        58: '[decisive kingside control White]',
        59: '[decisive kingside control Black]',
        60: '[queenside control White]',
        61: '[queenside control Black]',
        62: '[moderate queenside control White]',
        63: '[moderate queenside control Black]',
        64: '[decisive queenside control White]',
        65: '[decisive queenside control Black]',
        66: '[vulnerable first rank White]',
        67: '[vulnerable first rank Black]',
        68: '[well protected first rank White]',
        69: '[well protected first rank Black]',
        70: '[poorly protected king White]',
        71: '[poorly protected king Black]',
        72: '[well protected king White]',
        73: '[well protected king Black]',
        74: '[poorly placed king White]',
        75: '[poorly placed king Black]',
        76: '[well placed king White]',
        77: '[well placed king Black]',
        78: '[very weak pawn structure White]',
        79: '[very weak pawn structure Black]',
        80: '[moderately weak pawn structure White]',
        81: '[moderately weak pawn structure Black]',
        82: '[moderately strong pawn structure White]',
        83: '[moderately strong pawn structure Black]',
        84: '[very strong pawn structure White]',
        85: '[very strong pawn structure Black]',
        86: '[poor knight placement White]',
        87: '[poor knight placement Black]',
        88: '[good knight placement White]',
        89: '[good knight placement Black]',
        90: '[poor bishop placement White]',
        91: '[poor bishop placement Black]',
        92: '[good bishop placement White]',
        93: '[good bishop placement Black]',
        94: '[poor rook placement White]',
        95: '[poor rook placement Black]',
        96: '[good rook placement White]',
        97: '[good rook placement Black]',
        98: '[poor queen placement White]',
        99: '[poor queen placement Black]',
        100: '[good queen placement White]',
        101: '[good queen placement Black]',
        102: '[poor piece coordination White]',
        103: '[poor piece coordination Black]',
        104: '[good piece coordination White]',
        105: '[good piece coordination Black]',
        106: '[opening played very poorly White]',
        107: '[opening played very poorly Black]',
        108: '[opening played poorly White]',
        109: '[opening played poorly Black]',
        110: '[opening played well White]',
        111: '[opening played well Black]',
        112: '[opening played very well White]',
        113: '[opening played very well Black]',
        114: '[middlegame played very poorly White]',
        115: '[middlegame played very poorly Black]',
        116: '[middlegame played poorly White]',
        117: '[middlegame played poorly Black]',
        118: '[middlegame played well White]',
        119: '[middlegame played well Black]',
        120: '[middlegame played very well White]',
        121: '[middlegame played very well Black]',
        122: '[ending played very poorly White]',
        123: '[ending played very poorly Black]',
        124: '[ending played poorly White]',
        125: '[ending played poorly Black]',
        126: '[ending played well White]',
        127: '[ending played well Black]',
        128: '[ending played very well White]',
        129: '[ending played very well Black]',
        130: '[slight counterplay White]',
        131: '[slight counterplay Black]',
        132: r'\nagcounterplay ', # Counterplay White
        133: r'\nagcounterplay ', # Counterplay Black
        134: '[decisive counterplay White]',
        135: '[decisive counterplay Black]',
        
        # Time pressure
        136: '[time pressure White]',
        137: '[time pressure Black]',
        138: r'\nagzeitnot ', # Severe time pressure White
        139: r'\nagzeitnot ', # Severe time pressure Black
    }
    return nag_symbols.get(nag, '')


def format_evaluation(comment: str) -> str:
    """Format engine evaluation comments nicely."""
    # Detect patterns like "27:+1.26" (depth:eval) or "+/−" evaluations
    import re
    
    # Pattern for stockfish-style depth:eval
    eval_pattern = re.compile(r'(\d+):([+-]?\d+\.\d+)')
    match = eval_pattern.search(comment)
    if match:
        depth, evaluation = match.groups()
        return f"[depth {depth}: {evaluation}]"
    
    return comment


def generate_latex_preamble() -> str:
    """Generate LaTeX preamble for chess documents with variation support."""
    return r"""\documentclass[11pt]{article}
\usepackage{xskak}
\usepackage{chessboard}
\usepackage{amssymb}
\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{parskip}
\usepackage{xcolor}

% Custom commands for NAG symbols to ensure math-safety and compatibility
\newcommand{\nagforced}{\ensuremath{\square}}
\newcommand{\nagworst}{\ensuremath{\boxtimes}}
\newcommand{\nagunclear}{\ensuremath{\infty}}
\newcommand{\nagwbetter}{\ensuremath{\pm}}
\newcommand{\nagbbetter}{\ensuremath{\mp}}
\newcommand{\nagwhitebetter}{\ensuremath{\pm}}
\newcommand{\nagblackbetter}{\ensuremath{\mp}}
\newcommand{\nagwwinning}{\ensuremath{+-}}
\newcommand{\nagbwinning}{\ensuremath{-+}}
\newcommand{\nagzugzwang}{\ensuremath{\odot}}
\newcommand{\nagdevadv}{\ensuremath{\circlearrowright}}
\newcommand{\naginitiative}{\ensuremath{\uparrow}}
\newcommand{\nagattack}{\ensuremath{\rightarrow}}
\newcommand{\nagcompensation}{\ensuremath{\overline{\infty}}}
\newcommand{\nagcounterplay}{\ensuremath{\leftrightarrow}}
\newcommand{\nagzeitnot}{\ensuremath{\oplus}}

% Custom chess board styling
\setchessboard{
    showmover=true,
    pgfstyle=border
}

% Define colors for variations and comments
\definecolor{commentcolor}{RGB}{0, 100, 0}
\definecolor{variationcolor}{RGB}{100, 100, 100}
\definecolor{evalcolor}{RGB}{0, 0, 150}

% Commands for formatting
\newcommand{\gamecomment}[1]{\textcolor{commentcolor}{\textit{#1}}}
\newcommand{\sideline}[1]{\textcolor{variationcolor}{(#1)}}
\newcommand{\evaltext}[1]{\textcolor{evalcolor}{\small #1}}

\begin{document}
"""


def generate_latex_postamble() -> str:
    """Generate LaTeX postamble."""
    return r"""
\end{document}
"""


def format_headers_latex(game: chess.pgn.Game) -> str:
    """Format all PGN headers as LaTeX."""
    latex = ""
    
    # Title with players
    white = game.headers.get("White", "?")
    black = game.headers.get("Black", "?")
    white_elo = game.headers.get("WhiteElo", "")
    black_elo = game.headers.get("BlackElo", "")
    white_title = game.headers.get("WhiteTitle", "")
    black_title = game.headers.get("BlackTitle", "")
    
    # Format player names with titles and ratings
    white_display = f"{white_title} {white}".strip() if white_title else white
    black_display = f"{black_title} {black}".strip() if black_title else black
    if white_elo:
        white_display += f" ({white_elo})"
    if black_elo:
        black_display += f" ({black_elo})"
    
    latex += f"\\section*{{{escape_latex(white_display)} vs {escape_latex(black_display)}}}\n\n"
    
    # Event information
    latex += "\\begin{tabular}{ll}\n"
    
    # Define which headers to display and in what order
    header_display = [
        ("Event", "Event"),
        ("Site", "Site"),
        ("Date", "Date"),
        ("Round", "Round"),
        ("Result", "Result"),
        ("ECO", "ECO Code"),
        ("Opening", "Opening"),
        ("Variation", "Variation"),
        ("WhiteTeam", "White Team"),
        ("BlackTeam", "Black Team"),
        ("EventType", "Event Type"),
        ("Annotator", "Annotator"),
    ]
    
    for header_key, display_name in header_display:
        value = game.headers.get(header_key)
        if value and value != "?":
            latex += f"\\textbf{{{display_name}:}} & {escape_latex(value)} \\\\\n"
    
    latex += "\\end{tabular}\n\n"
    latex += "\\vspace{1em}\n\n"
    
    return latex


def format_move_with_number(board: chess.Board, move: chess.Move, move_count: int) -> str:
    """Format a move with proper move number."""
    san = board.san(move)
    if board.turn == chess.WHITE:
        return f"{move_count}. {san}"
    else:
        return san


def process_node(
    node: chess.pgn.GameNode,
    board: chess.Board,
    move_count: int,
    depth: int = 0,
    diagram_positions: List[Tuple[str, str]] = None
) -> Tuple[str, int, List[Tuple[str, str]]]:
    """
    Process a game node recursively, handling moves, comments, and variations.
    
    CRITICAL: The board parameter is MUTABLE and will be modified during processing.
    This is intentional for the mainline but variations must use copies.
    
    Returns:
        Tuple of (latex_content, updated_move_count, diagram_positions)
    """
    if diagram_positions is None:
        diagram_positions = []
    
    latex = ""
    
    for child in node.variations:
        move = child.move
        is_mainline = (child == node.variation(0))
        
        # Check for diagram annotation in starting_comment or comment
        starting_comment = child.starting_comment.strip() if child.starting_comment else ""
        comment = child.comment.strip() if child.comment else ""
        
        # Check for diagram annotation
        show_diagram = has_diagram_annotation(starting_comment) or has_diagram_annotation(comment)
        if has_diagram_annotation(starting_comment):
            starting_comment = strip_diagram_annotation(starting_comment)
        if has_diagram_annotation(comment):
            comment = strip_diagram_annotation(comment)
        
        # Add starting comment if present
        if starting_comment:
            formatted_comment = format_evaluation(starting_comment)
            latex += f"\\gamecomment{{{escape_latex(formatted_comment)}}} "
        
        if is_mainline:
            # Format the move
            san = board.san(move)
            san = escape_latex(san)  # Escape special characters like # for checkmate
            if board.turn == chess.WHITE:
                latex += f"{move_count}. {san}"
            else:
                latex += f"{san}"
            
            # Add NAGs (annotation symbols like !, ?, !!, etc.)
            for nag in child.nags:
                symbol = nag_to_symbol(nag)
                if symbol:
                    latex += symbol
            
            # Show diagram if requested
            if show_diagram:
                # Save current board state
                board.push(move)
                fen = board.fen()
                board.pop()
                
                caption = f"After {move_count}{'.' if board.turn == chess.WHITE else '...'} {san}"
                diagram_positions.append((fen, caption))
                
                latex += "\n\n\\vspace{0.5em}\n"
                latex += f"\\chessboard[setfen={fen}]\n\n"
                latex += f"\\begin{{center}}\\small\\textit{{{caption}}}\\end{{center}}\n\n"
            
            # Add comment if present
            if comment:
                formatted_comment = format_evaluation(comment)
                latex += f" \\gamecomment{{{escape_latex(formatted_comment)}}}"
            
            latex += " "
            
            # Make the move on the board
            board.push(move)
            
            # Update move count AFTER making the move
            if board.turn == chess.WHITE:
                move_count += 1
            
            # Process variations at the PARENT level (alternatives to the move we just made)
            # node.variations contains: [child (mainline), alt1, alt2, ...]
            # So node.variations[1:] are the alternatives to the move we just made
            if len(node.variations) > 1:
                for alt_idx, alt_child in enumerate(node.variations[1:], 1):
                    # Create a fresh board copy and go back to BEFORE the mainline move
                    var_board = board.copy()
                    var_board.pop()  # Remove the mainline move we just made
                    
                    # Calculate move count for the position before the mainline move
                    var_move_count = move_count - (1 if board.turn == chess.WHITE else 0)
                    
                    var_latex, var_diagrams = process_variation(
                        alt_child, 
                        var_board,  # At position before mainline move
                        var_move_count,
                        depth + 1
                    )
                    latex += f"\\sideline{{{var_latex.strip()}}}"
                    diagram_positions.extend(var_diagrams)
                    latex += " "
            
            # Continue with mainline (board is already updated)
            child_latex, move_count, diagram_positions = process_node(
                child, board, move_count, depth, diagram_positions
            )
            latex += child_latex
            
            break  # Only process mainline here, variations handled above
    
    return latex, move_count, diagram_positions


def process_variation(
    node: chess.pgn.GameNode,
    board: chess.Board,
    move_count: int,
    depth: int
) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Process a variation (sideline) and return its LaTeX representation.
    
    CRITICAL FIX: This function receives a COPY of the board and will modify it.
    Each recursive call must get its own fresh copy.
    
    The board parameter should be positioned at the point where the variation begins.
    """
    diagram_positions = []
    latex = ""
    
    current_node = node
    first_move = True
    
    while current_node is not None and current_node.move is not None:
        move = current_node.move
        comment = current_node.comment.strip() if current_node.comment else ""
        starting_comment = current_node.starting_comment.strip() if current_node.starting_comment else ""
        
        # Check for diagram annotation
        show_diagram = has_diagram_annotation(starting_comment) or has_diagram_annotation(comment)
        if has_diagram_annotation(starting_comment):
            starting_comment = strip_diagram_annotation(starting_comment)
        if has_diagram_annotation(comment):
            comment = strip_diagram_annotation(comment)
        
        # Format the move
        san = board.san(move)
        san = escape_latex(san)  # Escape special characters like # for checkmate
        if board.turn == chess.WHITE:
            latex += f"{move_count}. {san}"
        else:
            # Show move number for first move or after a comment
            if first_move:
                latex += f"{move_count}... {san}"
            else:
                latex += f"{san}"
        
        first_move = False
        
        # Add NAGs
        for nag in current_node.nags:
            symbol = nag_to_symbol(nag)
            if symbol:
                latex += symbol
        
        # Add comment
        if comment:
            formatted_comment = format_evaluation(comment)
            latex += f" {escape_latex(formatted_comment)}"
        
        latex += " "
        
        # Make the move on THIS board (it's our own copy, so this is safe)
        board.push(move)
        
        # Update move count AFTER making the move
        if board.turn == chess.WHITE:
            move_count += 1
        
        # Move to next node in this variation's mainline
        if current_node.variations:
            # BEFORE moving to the next node, check if there are alternatives
            # current_node.variations[0] is the mainline (next move we'll process)
            # current_node.variations[1:] are alternatives to that next move
            if len(current_node.variations) > 1:
                for alt_child in current_node.variations[1:]:
                    # The board is currently at the RIGHT position for these alternatives
                    # They are alternatives to the next move, starting from current position
                    subvar_board = board.copy()
                    
                    # Recursively process with a fresh board copy
                    subvar_latex, subvar_diagrams = process_variation(
                        alt_child,
                        subvar_board,  # Fresh copy at current position
                        move_count,
                        depth + 1
                    )
                    latex += f"\\sideline{{{subvar_latex.strip()}}} "
                    diagram_positions.extend(subvar_diagrams)
            
            # Now move to the next node in the mainline
            current_node = current_node.variation(0)
        else:
            # No more moves in this variation
            break
    
    return latex, diagram_positions


def generate_game_latex(game: chess.pgn.Game) -> str:
    """Generate complete LaTeX for a chess game."""
    latex = generate_latex_preamble()
    
    # Add headers
    latex += format_headers_latex(game)
    
    # Start the game
    latex += "\\newchessgame\n\n"
    latex += "\\subsection*{Game}\n\n"
    
    # Process the game tree
    board = game.board()
    move_count = 1
    diagram_positions = []
    
    game_latex, final_move_count, diagram_positions = process_node(
        game, board, move_count, 0, diagram_positions
    )
    
    latex += game_latex
    
    # Add result
    result = game.headers.get("Result", "*")
    latex += f"\n\n\\textbf{{{result}}}\n\n"
    
    # Final position - use the board state after processing all mainline moves
    final_fen = board.fen()
    latex += "\\subsection*{Final Position}\n\n"
    latex += f"\\chessboard[setfen={final_fen}]\n\n"
    
    latex += generate_latex_postamble()
    
    return latex


def main():
    parser = argparse.ArgumentParser(
        description="Read a PGN file and produce LaTeX output with diagrams at 'D' annotations"
    )
    parser.add_argument("pgn_file", help="Path to the PGN file")
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: <pgn_name>.tex)"
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also compile to PDF"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Read the PGN file
    pgn_path = Path(args.pgn_file)
    if not pgn_path.exists():
        print(f"Error: PGN file not found: {pgn_path}")
        sys.exit(1)
    
    if args.verbose:
        print(f"Reading PGN file: {pgn_path}")
    
    with open(pgn_path, 'r') as f:
        pgn_content = f.read()
    
    # Preprocess to convert standalone 'D' annotations to comments
    pgn_content = preprocess_pgn(pgn_content)
    
    if args.verbose:
        print("Preprocessed PGN for diagram annotations")
    
    # Parse the PGN
    pgn = StringIO(pgn_content)
    game = chess.pgn.read_game(pgn)
    
    if not game:
        print("Error: Failed to parse PGN file")
        sys.exit(1)
    
    if args.verbose:
        print(f"Parsed game: {game.headers.get('White', '?')} vs {game.headers.get('Black', '?')}")
        print(f"Event: {game.headers.get('Event', '?')}")
    
    # Generate LaTeX
    latex_content = generate_game_latex(game)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = pgn_path.with_suffix('.tex')
    
    # Write LaTeX file
    output_path.write_text(latex_content, encoding='utf-8')
    print(f"✓ LaTeX file written: {output_path}")
    
    # Optionally compile to PDF
    if args.pdf:
        try:
            generator = ChessDiagramGenerator(verbose=args.verbose)
            pdf_path = output_path.with_suffix('.pdf')
            success = generator.engine.compile(latex_content, pdf_path)
            if success:
                print(f"✓ PDF compiled: {pdf_path}")
            else:
                print("✗ PDF compilation failed")
                sys.exit(1)
        except Exception as e:
            print(f"✗ PDF compilation error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
