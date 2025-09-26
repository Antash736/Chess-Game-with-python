# Chess-Game-with-python
A fully functional 2D Chess game built with Python and Pygame, featuring:  Smooth animations  Sound effects for moves, captures, and win  Basic AI opponent using Minimax with Alpha-Beta pruning  Castling support  Interactive UI with highlighted moves
# ♟️ Advanced Chess AI Game – Python + Pygame

A beautiful and strategic **Chess Game** built with **Python** and **Pygame**, featuring:
- A smart AI opponent using **Minimax + Alpha-Beta Pruning**
- Realistic **sound effects** for movement and capture
- **Castling**, move highlighting, and smooth piece interaction
- Clean interface with **start and end screens**

---

## 🧠 Why This Project?

Whether you're a fan of chess, learning game development, or diving into AI algorithms — this project blends all three in an elegant, educational, and playable way.

---

## 🎮 Features Overview

| Feature                  | Description                                              |
|--------------------------|----------------------------------------------------------|
| ✅ Human vs AI           | Play as White against a smart Black AI                   |
| ✅ Minimax AI             | Simple but effective strategy up to depth 2              |
| ✅ Alpha-Beta Pruning     | Speeds up the AI search significantly                    |
| ✅ Move & Capture Sounds  | Enhances realism and game feel                           |
| ✅ Castling               | Fully supported for both sides                           |
| ✅ Move Highlights        | Helps player visualize options                           |
| ✅ Win Detection          | Ends the game when King is captured                      |
| ✅ UI Screens             | Welcome and win messages                                 |

---

## 🖼️ Screenshots

> *(Optional: Add screenshots in `images/` and enable these)*

📍 Start Screen 📍 In-Game View 📍 Win Screen
+-------------------+ +-------------------+ +-------------------+
| [ Start Image ] | | [ Game Image ] | | [ Win Image ] |
+-------------------+ +-------------------+ +-------------------+

yaml
Copy code

---

## 🛠 Installation

### 🔗 Clone the repository

```bash
git clone https://github.com/your-username/chess-ai-pygame.git
cd chess-ai-pygame
📦 Install dependencies
bash
Copy code
pip install pygame
▶️ Run the game
bash
Copy code
python chess_game.py
📁 Folder Structure
bash
Copy code
chess-ai-pygame/
│
├── Sounds/               # MP3 files for move, capture, win
│   ├── move_Sound.mp3
│   ├── capture_Sound.mp3
│   └── win_Sound.mp3
│
├── images/               # Chess piece images (PNG)
│   ├── white king.png
│   ├── black queen.png
│   └── ...
│
├── chess_game.py         # Main game file
└── README.md             # You're reading it!
🧠 How the AI Works
AI is implemented using Minimax algorithm with Alpha-Beta pruning

Evaluation is based on simple material balance

Current depth: 2 plies

Can be expanded to add position-based evaluation, checkmate detection, or opening books

📌 Upcoming Enhancements
♟️ Pawn promotion

❗ Check / Checkmate detection

⏳ Turn timer

📱 GUI/UX polish

🤝 2-player mode (local)

🌐 Online multiplayer

🔓 License
This project is licensed under the MIT License.
Free to use, share, and modify!

🙌 Acknowledgments
Pygame Library

Chess piece icons from Wikimedia Commons

Sound assets from FreeSound.org

👨‍💻 Built With
Python 3.x

Pygame

💡 Passion for chess and game development

⭐ Show Your Support
If you liked the project:

🌟 Star this repo

🍴 Fork it and build your own features

🐛 Report issues or suggest improvements

