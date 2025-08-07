# Pokemon-Catch-Battle

A simple web-based Pokemon catching and battling game built with FastAPI for the backend and vanilla HTML, CSS, and JavaScript for the frontend. Catch Pokemon, build your team, and battle opponents in this interactive web game!

## 🎮 Features

- **Catch Pokemon**: Random Pokemon appear for you to catch
- **Team Building**: Build a team of up to 6 Pokemon
- **Battle System**: Fight against random opponent Pokemon
- **Scoring System**: Earn points for winning battles
- **Game Over**: Lose after 3 consecutive defeats
- **Beautiful UI**: Pokemon-themed interface with animations

## Game Preview

![Game Preview](https://github.com/user-attachments/assets/2c3d8183-09ae-4f23-ae1a-a4b1ac506e6c)

## Backend

The `pokemon_api.py` file runs the FastAPI server, acting as the backend. It manages game sessions, fetches Pokemon data from an external API, and handles game logic like catching and battling.

## Battle Winner Calculation

In battles, each Pokemon's base stats (HP, Attack, Defense, etc.) are summed to determine their initial power. A random multiplier (0.8 to 1.2) is applied to this power. The Pokemon with the higher final power wins. Winning increases your score, while losing decreases it and adds a consecutive loss. The game ends after 3 consecutive losses.

## 🚀 How to Run Locally

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shreyahhh/Pokemon-Catch-Battle-using-FastAPI.git
    cd Pokemon-Catch-Battle-using-FastAPI
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI server:**

    ```bash
    python -m uvicorn pokemon_api:app --reload --port 8080
    ```

4.  **Access the game:**

    Open your web browser and go to `http://127.0.0.1:8080`.

    You can also access the API documentation at `http://127.0.0.1:8080/docs`.

## 🌐 Deployment

This project is configured for deployment on Vercel:

### Deploy to Vercel

1. **Push your code to GitHub**
2. **Connect your GitHub repository to Vercel**
3. **Deploy** - Vercel will automatically detect the FastAPI configuration

The project includes:
- `main.py` - Entry point for Vercel
- `vercel.json` - Vercel configuration file
- `requirements.txt` - Python dependencies

### Live Demo
*Add your deployed URL here after deployment*

## 📁 Project Structure

```
Pokemon-Catch-Battle-using-FastAPI/
├── main.py                 # Entry point for deployment
├── pokemon_api.py          # FastAPI backend
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
├── templates/
│   └── index.html         # Main HTML file
└── static/
    ├── styles.css         # CSS styling
    └── script.js          # JavaScript functionality
```

## ⚔️ Battle System

In battles, each Pokemon's base stats (HP, Attack, Defense, etc.) are summed to determine their initial power. A random multiplier (0.8 to 1.2) is applied to this power to add excitement. The Pokemon with the higher final power wins the battle.

**Scoring:**
- **Win**: +10 points, reset consecutive losses
- **Lose**: -5 points, +1 consecutive loss
- **Game Over**: After 3 consecutive losses

## 🛠️ Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **API**: PokeAPI for Pokemon data
- **HTTP Client**: httpx for async requests
- **Deployment**: Vercel

## 🎯 API Endpoints

- `GET /` - Serve the main game page
- `POST /game/start` - Start a new game session
- `POST /game/{session_id}/catch` - Catch a Pokemon
- `GET /game/{session_id}/team` - Get current team
- `POST /game/{session_id}/battle` - Battle with a Pokemon
- `GET /game/{session_id}/score` - Get current score
- `DELETE /game/{session_id}` - End game session

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

---

**Gotta Catch 'Em All!** 🌟
