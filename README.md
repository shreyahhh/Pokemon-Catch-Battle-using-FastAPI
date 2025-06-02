# Pokemon-Catch-Battle

A simple web-based Pokemon catching and battling game built with FastAPI for the backend and vanilla HTML, CSS, and JavaScript for the frontend.

## Game Preview

![Game Preview](https://github.com/user-attachments/assets/2c3d8183-09ae-4f23-ae1a-a4b1ac506e6c)


## Backend (MCP Server)

The `MCP.py` file runs the FastAPI server, acting as the backend. It manages game sessions, fetches Pokemon data from an external API, and handles game logic like catching and battling.

## Battle Winner Calculation

In battles, each Pokemon's base stats (HP, Attack, Defense, etc.) are summed to determine their initial power. A random multiplier (0.8 to 1.2) is applied to this power. The Pokemon with the higher final power wins. Winning increases your score, while losing decreases it and adds a consecutive loss. The game ends after 3 consecutive losses. 
