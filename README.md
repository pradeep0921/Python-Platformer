# 🕹️ Pygame Platformer Game

A fun side-scrolling platformer built using **Pygame**! This game includes levels, enemies, coins, moving platforms, lava, background music, sound effects, and custom tiles.

---

## 🎮 Features

- Multiple levels with different terrain and obstacles
- Animated player character with smooth controls
- Collectible coins that increase score
- Moving platforms and patrolling enemies
- Lava hazards and exit portals
- Main menu with Start and Exit buttons
- Restart functionality
- Background music and sound effects

---

## 🖼️ Screenshots

> _Add screenshots of your game here_  
> You can press `Print Screen` or use tools like Snipping Tool or ShareX to take screenshots while running the game.

---

## 📂 Folder Structure

```
project/
│
├── main.py                # Main game loop and logic
├── level1_data            # Level data saved as a pickle file
├── img/                   # Folder containing all game assets
│   ├── bg.png
│   ├── sun.png
│   ├── dirt.png
│   ├── grass.png
│   ├── guy1.png ... guy4.png
│   ├── coin.png
│   ├── blob.png
│   ├── lava.png
│   ├── exit.png
│   ├── platform.png
│   ├── start_btn.png
│   ├── exit_btn.png
│   ├── restart_btn.png
│   ├── music.wav
│   ├── jump.wav
│   ├── coin.wav
│   └── game_over.wav
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.x installed on Windows
- Pygame installed

To install Pygame:

```bash
pip install pygame
```

---

## ▶️ How to Run

1. Clone the repository or download the ZIP
2. Ensure the `img/` folder and level data are in the same directory as `main.py`
3. Run the game:

```bash
python main.py
```

Use:
- `←` and `→` to move
- `Space` to jump
- Mouse to click menu buttons

---

## 🧠 Game Logic Overview

- The game reads level data from pickled files
- Player and enemy sprites are handled with custom classes
- Collision detection, gravity, and animations are implemented manually
- Sound and music are integrated with `pygame.mixer`

---

## ✍️ Credits

Game developed by [Your Name]  
Assets and music are placeholders – replace with your own or credited free-use content.

---

## 📜 License

This project is for educational purposes. Modify it however you like!
