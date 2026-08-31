HILL RUSH
==========

A one-button Pygame hill runner with 4 fixed, progressively harder levels.

HOW TO RUN
1. Install Python 3.
2. Install pygame:  pip install pygame
3. Open this folder in Terminal / VS Code.
4. Run:  python3 main.py

CONTROLS
- SPACE: start
- Hold SPACE: run / accelerate
- Release SPACE: slow down and stop
- Double-tap SPACE: jump
- R: restart after Game Over; play again after completing Level 4
- ESC: return to Home

LEVEL 1 INTRODUCTION
- Pressing START begins with a short interactive How to Play section for Level 1.
- It teaches running/stopping, puffer timing, bird movement and launcher projectiles.
- Finish the introduction to enter Level 1.
- Press S during the introduction to skip it and start Level 1 immediately.
- The tutorial does not appear as a separate Main Menu option.

ENEMIES
- Puffer: grows/shrinks and moves vertically. Time the jump marker.
- Winged enemy: high = run under, low = jump over, middle = stop and wait.
- Launcher: watch the red warning and dodge its projectile.

LEVEL DIFFICULTY
- Level 1: MODERATE
- Level 2: MODERATE - HARD
- Level 3: HARD
- Level 4: HARDEST

Each level has a fixed, different obstacle layout. The house is the finish line.
Coins earn points used to unlock characters. Progress, points, character selection,
best time and music settings are saved in save_data.json.

AUDIO
- 13.mp3: start
- 4.mp3: game over
- 5.mp3: booster
- 6.mp3: coin
- 5(1).mp3 / 1.mp3 / 2.mp3: selectable background music
