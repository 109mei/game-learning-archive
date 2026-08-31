<!-- 
   🛠️ Download Link : https://github.com/coderboe/FlyMan.git
   📝 Language : Python
   💻 Framework : Pygame
   📚 Description : A simple game where the player controls a man to fly through gaps between pipes.
   👨‍💻 Author : Lu Taw, Min Thant Htin and Thae Htet Htet Khaing
   📚 License : MIT License
-->
# Fly Man Game with One Button

A simple Fly Man Game created using Python and Pygame.

## Overview

This game challenges the player to navigate a man through gaps between moving pipes by pressing the spacebar to flap. The game gradually becomes more difficult by increasing pipe speed and narrowing gaps. Features include:

- Start menu with options: Start, Help, About, Exit  
- In-game exit button to return to the menu  
- Score and high score tracking with sound effects  
- Gradient background and simple graphics

## Screenshots
![image](https://github.com/coderboe/repo-image/blob/master/img/Gamemenu.png)

---
📂 Project Structure

-  FlyMan
-  ├── assets/ # Images and sounds for the game
-  │ ├── flyMan_fly.png # Bird sprite image
-  │ ├── flap.wav # Flap sound effect
-  │ ├── score.wav # Score sound effect
-  │ └── hit.wav # Hit sound effect
-  ├── game.py # Main Python game script
-  ├── highscore.txt # File to store high score (auto-generated)
-  ├── LICENSE # License file (MIT License)
-  └── README.md # This filefor documentation

## Controls

- **Spacebar**: Make the man flap (jump upwards)  
- **R**: Restart the game after a game over  
- **Mouse Click**: Use buttons in menu and exit button in-game  
- **ESC**: Return to menu from Help or About screens

## Requirements

- Python 3.x  
- Pygame library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/coderboe/FlyMan.git
   ```
    And then:
   ```
   cd FlyMan
    ```
2. Install the required dependencies:
    ```bash
    pip install pygame
    ```
3. Run the game:
    ```bash
    python game.py
    ```
---
📌 Purpose
- This project was created for school projects and usage of Pygame, a Python library for create One Button Game applications.

## License

This project is licensed under the [MIT License](LICENSE).
