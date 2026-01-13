# 🏰 AI Chess Game

A **Python-based AI Chess Game** with interactive GUI, visual indicators, and AI opponent.  
Play against the computer with selectable difficulty levels (Easy, Medium, Hard) and enjoy a fully animated chess experience!

---

## 🎮 Features

- **Playable in Python (Pygame)**  
- **Interactive Menu** with clickable buttons:
  - Select **Difficulty**: Easy, Medium, Hard  
  - Start Game button
- **Turn-based gameplay**: Player (White) and AI (Black) take alternate turns  
- **AI Opponent**:
  - Easy → Random moves  
  - Medium → Prefer captures  
  - Hard → Capture highest-value piece moves  
  - 2-second delay for AI moves for realism
- **Full Chess Rules**:
  - Legal moves for each piece (King, Queen, Rook, Bishop, Knight, Pawn)  
  - Pawn promotion implemented
- **Visual Indicators**:
  - Current turn highlighted via glowing overlay  
  - Selected piece highlighted with pulsing circle  
  - Legal moves indicated with green dots  
  - Animated Unicode chess pieces ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟

---

## 🛠 Tech Stack

- **Python 3.x**  
- **Pygame** for GUI and animations  
- Unicode symbols for chess pieces (no external images)  

---

## 📂 Project Structure

simple-Ai-chess-game/
│
├─ main.py # Main game loop, menu, AI, visuals
├─ board.py # Board setup, move logic
├─ pieces.py # Chess piece classes and symbols
├─ README.md # Project description (this file)
├─ requirements.txt # Required packages

yaml
Copy code

---

## ⚡ How to Run Locally

1. Make sure **Python 3.x** is installed
2. Install **Pygame**:
```bash
pip install pygame
Run the game:

bash
Copy code
python main.py
Select difficulty and click Start Game in the menu

Enjoy playing against the AI!

🎯 Gameplay Rules
Player is White, AI is Black

Turns alternate automatically; you cannot move twice in a row

Pieces move according to standard chess rules:

King: 1 square any direction

Queen: any number of squares, straight or diagonal

Rook: straight lines only

Bishop: diagonal only

Knight: L-shaped jumps

Pawn: forward 1 (or 2 on first move), capture diagonally, promote at last rank

Legal moves are highlighted

Pawn promotion is automatic to Queen

📸 Screenshots
