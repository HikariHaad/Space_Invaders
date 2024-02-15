# Space Invaders Game

## Overview

This Python script implements a basic version of the classic Space Invaders game using the Processing library for graphics and sound effects. The game features a player-controlled spaceship, alien invaders, and various power-ups.

## Key Features

- **Spaceship Movement:** The player can control the spaceship's horizontal movement using the left and right arrow keys.

- **Shooting Bullets:** The player can shoot bullets by pressing the spacebar. Bullets move vertically and can hit alien invaders.

- **Alien Invaders:** The game includes different types of alien invaders with varying movement patterns. The player's objective is to eliminate these invaders by shooting them.

- **Power-ups:** Power-ups appear on the screen and grant special abilities to the player. These abilities include increased bullet and spaceship speed, a temporary invincible torch mode, and extra lives.

- **Scoring System:** Players earn points by shooting and eliminating alien invaders. The game keeps track of the player's score.

- **Lives:** The player starts with three lives. Colliding with alien invaders reduces the number of lives.

- **Game Start/End:** The game begins when the space key is pressed. It ends when the player loses all lives, displaying an end screen.

## Game Components

The code includes several classes:

- **Torch Class:** Represents the player-controlled spaceship with the ability to switch between regular and torch modes.

- **BulletTorch Class:** Represents bullets shot by the player's spaceship in torch mode.

- **BulletInvader Class:** Represents bullets shot by alien invaders.

- **Invader Class:** Represents different types of alien invaders.

- **Powerup Class:** Represents power-up objects that provide special abilities to the player.

- **Space Class:** Integrates all the game components, manages game events, and controls game flow.

## Sound Effects

The game incorporates sound effects for shooting, power-up collection, and damage. Background music is played throughout the game.

## Getting Started

1. **Libraries:** Ensure that the required libraries (`os`, `random`, `time`, and `minim`) are installed.

2. **Processing:** Run the script using the Processing environment.

3. **Controls:** Use the left and right arrow keys for spaceship movement. Press the spacebar to shoot bullets.

4. **Game Start:** Press the spacebar to start the game.

5. **Game End:** The game ends when the player runs out of lives, displaying an end screen.

Enjoy playing Space Invaders!
