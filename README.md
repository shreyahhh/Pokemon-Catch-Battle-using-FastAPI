# Pokemon-Catch-Battle

A simple web-based Pokemon catching and battling game built with FastAPI for the backend and vanilla HTML, CSS, and JavaScript for the frontend.

## Game Preview

![Game Preview](https://github.com/user-attachments/assets/2c3d8183-09ae-4f23-ae1a-a4b1ac506e6c)

## Backend

The `MCP.py` file runs the FastAPI server, acting as the backend. It manages game sessions, fetches Pokemon data from an external API, and handles game logic like catching and battling.

## Battle Winner Calculation

In battles, each Pokemon's base stats (HP, Attack, Defense, etc.) are summed to determine their initial power. A random multiplier (0.8 to 1.2) is applied to this power. The Pokemon with the higher final power wins. Winning increases your score, while losing decreases it and adds a consecutive loss. The game ends after 3 consecutive losses.

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shreyahhh/Pokemon-Catch-Battle-using-FastAPI.git
    cd Pokemon-Catch-Battle-using-FastAPI
    ```

2.  **Set up a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    *   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the FastAPI server:**

    ```bash
    uvicorn MCP:app --host 0.0.0.0 --port 8000 --reload
    ```

6.  **Access the game:**

    Open your web browser and go to `http://127.0.0.1:8000`.

    You can also access the API documentation at `http://127.0.0.1:8000/docs`.
