from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union
import uuid
import httpx
import random
import os

app = FastAPI(
    title="Pokemon Game Server",
    description="A simple Pokemon game API where you can catch Pokemon and battle!",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error serving index.html: {str(e)}"
        )

# Response models
class PokemonStats(BaseModel):
    base_stat: int
    effort: int
    stat: Dict[str, str]

class PokemonResponse(BaseModel):
    name: str = Field(..., description="Pokemon name")
    id: int = Field(..., description="Pokemon ID")
    stats: List[PokemonStats] = Field(..., description="Pokemon stats")
    sprites: dict = Field(..., description="Pokemon images (all sprite data as dict)")

class GameSession(BaseModel):
    session_id: str = Field(..., description="Unique game session ID")
    message: str = Field(..., description="Welcome message")

class CatchResponse(BaseModel):
    message: str = Field(..., description="Success message")
    pokemon: PokemonResponse = Field(..., description="Caught Pokemon details")
    team_size: int = Field(..., description="Current team size")

class TeamResponse(BaseModel):
    team: List[PokemonResponse] = Field(..., description="List of Pokemon in team")
    team_size: int = Field(..., description="Current team size")

class BattleResponse(BaseModel):
    message: str = Field(..., description="Battle description")
    result: str = Field(..., description="Battle result (won/lost)")
    score: int = Field(..., description="Current score")
    game_over: bool = Field(..., description="Whether the game is over")
    selected_pokemon: PokemonResponse = Field(..., description="Selected Pokemon for battle")
    opponent_pokemon: PokemonResponse = Field(..., description="Opponent Pokemon")

class ScoreResponse(BaseModel):
    score: int = Field(..., description="Current game score")
    game_over: bool = Field(..., description="Whether the game is over")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")

# In-memory store for game sessions
game_sessions: Dict[str, Dict] = {}

class PokemonGame:
    def __init__(self):
        self.player_pokemon = []
        self.opponent_pokemon = None
        self.score = 0
        self.game_state = "active"
        self.consecutive_losses = 0
        self.max_consecutive_losses = 3  # Game over after 3 consecutive losses

    def calculate_pokemon_power(self, pokemon):
        # Calculate total power based on all stats
        return sum(stat['base_stat'] for stat in pokemon['stats'])

async def fetch_pokemon(pokemon_id: int) -> Dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pokemon with ID {pokemon_id} not found"
                )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Pokemon API is currently unavailable"
            )

async def get_random_pokemon() -> Dict:
    pokemon_id = random.randint(1, 151)  # First 151 Pokemon
    return await fetch_pokemon(pokemon_id)

@app.post("/game/start", 
    response_model=GameSession,
    responses={
        200: {"description": "Game session created successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    })
async def start_game():
    """Start a new Pokemon game session."""
    try:
        session_id = str(uuid.uuid4())
        game = PokemonGame()
        game_sessions[session_id] = game
        return GameSession(
            session_id=session_id,
            message="Game started! Use /game/{session_id}/catch to catch Pokemon!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def normalize_pokemon(data):
    return {
        "name": data["name"],
        "id": data["id"],
        "stats": data["stats"],
        "sprites": data["sprites"]
    }

@app.post("/game/{session_id}/catch",
    response_model=CatchResponse,
    responses={
        200: {"description": "Pokemon caught successfully"},
        404: {"model": ErrorResponse, "description": "Game session not found"},
        400: {"model": ErrorResponse, "description": "Team is full (max 6 Pokemon)"}
    })
async def catch_pokemon(session_id: str):
    """Catch a random Pokemon and add it to your team."""
    if session_id not in game_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    game = game_sessions[session_id]
    if len(game.player_pokemon) >= 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your Pokemon team is full!"
        )
    
    pokemon_raw = await get_random_pokemon()
    pokemon = normalize_pokemon(pokemon_raw)
    game.player_pokemon.append(pokemon)
    return CatchResponse(
        message=f"You caught {pokemon['name'].capitalize()}!",
        pokemon=pokemon,
        team_size=len(game.player_pokemon)
    )

@app.get("/game/{session_id}/team",
    response_model=TeamResponse,
    responses={
        200: {"description": "Team retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Game session not found"}
    })
async def get_team(session_id: str):
    """Get your current Pokemon team."""
    if session_id not in game_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    game = game_sessions[session_id]
    return TeamResponse(
        team=game.player_pokemon,
        team_size=len(game.player_pokemon)
    )

@app.post("/game/{session_id}/battle/{pokemon_index}",
    response_model=BattleResponse,
    responses={
        200: {"description": "Battle completed successfully"},
        404: {"model": ErrorResponse, "description": "Game session not found"},
        400: {"model": ErrorResponse, "description": "Invalid Pokemon selection"}
    })
async def start_battle(session_id: str, pokemon_index: int):
    """Start a battle with a selected Pokemon."""
    if session_id not in game_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    game = game_sessions[session_id]
    if len(game.player_pokemon) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need at least one Pokemon to battle!"
        )
    
    if pokemon_index < 0 or pokemon_index >= len(game.player_pokemon):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Pokemon selection"
        )
    
    player_pokemon = game.player_pokemon[pokemon_index]
    opponent_pokemon_raw = await get_random_pokemon()
    opponent_pokemon = normalize_pokemon(opponent_pokemon_raw)
    game.opponent_pokemon = opponent_pokemon
    
    # Calculate battle power
    player_power = game.calculate_pokemon_power(player_pokemon)
    opponent_power = game.calculate_pokemon_power(opponent_pokemon)
    
    # Add some randomness to make battles more interesting
    player_power *= random.uniform(0.8, 1.2)
    opponent_power *= random.uniform(0.8, 1.2)
    
    if player_power > opponent_power:
        game.score += 1
        game.consecutive_losses = 0
        result = "won"
    else:
        game.score = max(0, game.score - 1)  # Can't go below 0
        game.consecutive_losses += 1
        result = "lost"
    
    game_over = game.consecutive_losses >= game.max_consecutive_losses
    
    return BattleResponse(
        message=f"Battle between {player_pokemon['name'].capitalize()} and {opponent_pokemon['name'].capitalize()}!",
        result=f"You {result} the battle!",
        score=game.score,
        game_over=game_over,
        selected_pokemon=player_pokemon,
        opponent_pokemon=opponent_pokemon
    )

@app.get("/game/{session_id}/score",
    response_model=ScoreResponse,
    responses={
        200: {"description": "Score retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Game session not found"}
    })
async def get_score(session_id: str):
    """Get your current game score."""
    if session_id not in game_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    game = game_sessions[session_id]
    return ScoreResponse(
        score=game.score,
        game_over=game.consecutive_losses >= game.max_consecutive_losses
    )

@app.delete("/game/{session_id}",
    responses={
        200: {"description": "Game session ended successfully"},
        404: {"model": ErrorResponse, "description": "Game session not found"}
    })
async def end_game(session_id: str):
    """End your current game session."""
    if session_id in game_sessions:
        del game_sessions[session_id]
        return {"message": "Game ended"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Game session not found"
    )

# Vercel compatibility: expose 'app' at module level
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
