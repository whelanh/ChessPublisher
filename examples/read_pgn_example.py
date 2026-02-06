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
    """Convert NAG (Numeric Annotation Glyph) to symbol."""
    nag_symbols = {
        1: '!',      # Good move
        2: '?',      # Mistake
        3: '!!',     # Brilliant move
        4: '??',     # Blunder
        5: '!?',     # Interesting move
        6: '?!',     # Dubious move
        10: '=',     # Equal position
        13: '∞',     # Unclear
        14: '+=',    # Slight advantage for White
        15: '=+',    # Slight advantage for Black
        16: '+/−',   # White is better
        17: '−/+',   # Black is better
        18: '+−',    # White is winning
        19: '−+',    # Black is winning
        22: '⨀',    # Zugzwang
        36: '→',     # Initiative
        40: '↑',     # Attack
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
\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{parskip}
\usepackage{xcolor}

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
        
        # Check both starting_comment and comment for diagram annotation
        show_diagram = has_diagram_annotation(starting_comment) or has_diagram_annotation(comment)
        
        if has_diagram_annotation(starting_comment):
            starting_comment = strip_diagram_annotation(starting_comment)
        if has_diagram_annotation(comment):
            comment = strip_diagram_annotation(comment)
        
        # Format the move
        if is_mainline:
            # Mainline move
            san = board.san(move)
            if board.turn == chess.WHITE:
                latex += f"\\textbf{{{move_count}. {san}}}"
            else:
                # For black moves at start of line or after diagram/comment, add move number
                if not latex.strip() or latex.rstrip().endswith('}'):
                    latex += f"\\textbf{{{move_count}... {san}}}"
                else:
                    latex += f" \\textbf{{{san}}}"
            
            # Add NAGs (annotation symbols)
            for nag in child.nags:
                symbol = nag_to_symbol(nag)
                if symbol:
                    latex += f"\\textbf{{{symbol}}}"
            
            # Add diagram if requested (after showing the move)
            if show_diagram:
                # Store position for diagram
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
            
            # Update move count
            if board.turn == chess.WHITE:
                move_count += 1
            
            # Process child variations (sidelines) - these are alternatives at this point
            if len(node.variations) > 1:
                for alt_idx, alt_child in enumerate(node.variations[1:], 1):
                    # This is a variation/sideline
                    var_board = board.copy()
                    var_board.pop()  # Go back to position before mainline move
                    
                    var_latex, var_diagrams = process_variation(
                        alt_child, var_board, 
                        move_count - (1 if board.turn == chess.WHITE else 0),
                        depth + 1
                    )
                    latex += f"\\sideline{{{var_latex.strip()}}}"
                    diagram_positions.extend(var_diagrams)
                    latex += " "
            
            # Continue with mainline
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
    Follows the mainline of the variation and handles nested sub-variations.
    """
    diagram_positions = []
    latex = ""
    
    current_node = node
    first_move = True
    
    while current_node.move is not None:
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
        
        # Make the move
        board.push(move)
        if board.turn == chess.WHITE:
            move_count += 1
        
        # Check for nested variations (alternatives at this position)
        if len(current_node.variations) > 1:
            for alt_child in current_node.variations[1:]:
                # Nested sideline
                subvar_board = board.copy()
                subvar_board.pop()  # Go back to position before the move
                subvar_latex, subvar_diagrams = process_variation(
                    alt_child, subvar_board,
                    move_count - (1 if board.turn == chess.WHITE else 0),
                    depth + 1
                )
                latex += f"\\sideline{{{subvar_latex.strip()}}} "
                diagram_positions.extend(subvar_diagrams)
        
        # Move to next node in the variation (mainline of this variation)
        if current_node.variations:
            current_node = current_node.variation(0)
        else:
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
    
    # Final position
    latex += "\\subsection*{Final Position}\n\n"
    latex += "\\chessboard\n\n"
    
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
