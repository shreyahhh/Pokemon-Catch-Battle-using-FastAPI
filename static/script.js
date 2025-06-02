let gameSessionId = null;

// DOM Elements
const startGameBtn = document.getElementById('start-game');
const catchPokemonBtn = document.getElementById('catch-pokemon');
const teamDisplay = document.getElementById('team-display');
const battleDisplay = document.getElementById('battle-display');
const battleMessage = document.getElementById('battle-message');
const scoreDisplay = document.getElementById('score');
const teamCountDisplay = document.querySelector('.team-count');

// Create catch message element
const catchMessage = document.createElement('div');
catchMessage.className = 'catch-message';
document.body.appendChild(catchMessage);

// Event Listeners
startGameBtn.addEventListener('click', startGame);
catchPokemonBtn.addEventListener('click', catchPokemon);

async function startGame() {
    try {
        const response = await fetch('/game/start', {
            method: 'POST'
        });
        const data = await response.json();
        gameSessionId = data.session_id;
        
        // Enable game controls
        catchPokemonBtn.disabled = false;
        
        // Clear previous game state
        teamDisplay.innerHTML = '';
        battleDisplay.style.display = 'none';
        battleMessage.textContent = '';
        scoreDisplay.textContent = '0';
        teamCountDisplay.textContent = '(0/6)';
        
        showCatchMessage('Game started! Catch some Pokemon!');
    } catch (error) {
        console.error('Error starting game:', error);
        showCatchMessage('Failed to start game. Please try again.', true);
    }
}

function showCatchMessage(message, isError = false) {
    catchMessage.textContent = message;
    catchMessage.style.background = isError ? 
        'linear-gradient(45deg, #ff6b6b, #ff8e8e)' : 
        'linear-gradient(45deg, #4ecdc4, #45b7af)';
    catchMessage.classList.add('show');
    
    setTimeout(() => {
        catchMessage.classList.remove('show');
    }, 3000);
}

async function catchPokemon() {
    if (!gameSessionId) return;
    
    try {
        const response = await fetch(`/game/${gameSessionId}/catch`, {
            method: 'POST'
        });
        const data = await response.json();
        
        // Add Pokemon to team display
        const pokemonCard = createPokemonCard(data.pokemon);
        teamDisplay.appendChild(pokemonCard);
        
        // Show catch message
        showCatchMessage(`You caught ${data.pokemon.name.toUpperCase()}!`);
        
        // Update team size
        teamCountDisplay.textContent = `(${data.team_size}/6)`;
        if (data.team_size >= 6) {
            catchPokemonBtn.disabled = true;
            showCatchMessage('Your team is full! Time to battle!');
        }
    } catch (error) {
        console.error('Error catching Pokemon:', error);
        showCatchMessage('Failed to catch Pokemon. Please try again.', true);
    }
}

function createPokemonCard(pokemon) {
    const card = document.createElement('div');
    card.className = 'pokemon-card';
    card.dataset.pokemonIndex = teamDisplay.children.length;
    
    const image = document.createElement('div');
    image.className = 'pokemon-image';
    image.style.backgroundImage = `url(${pokemon.sprites.front_default})`;
    
    const name = document.createElement('div');
    name.className = 'pokemon-name';
    name.textContent = pokemon.name;
    
    const stats = document.createElement('div');
    stats.className = 'pokemon-stats';
    
    // Add individual stats
    pokemon.stats.forEach(stat => {
        const statItem = document.createElement('div');
        statItem.className = 'stat-item';
        
        const statName = document.createElement('span');
        statName.className = 'stat-name';
        statName.textContent = stat.stat.name.replace('-', ' ');
        
        const statValue = document.createElement('span');
        statValue.className = 'stat-value';
        statValue.textContent = stat.base_stat;
        
        statItem.appendChild(statName);
        statItem.appendChild(statValue);
        stats.appendChild(statItem);
    });
    
    const totalPower = document.createElement('div');
    totalPower.className = 'pokemon-power';
    const power = pokemon.stats.reduce((sum, stat) => sum + stat.base_stat, 0);
    totalPower.textContent = `Total Power: ${power}`;
    
    const battleButton = document.createElement('button');
    battleButton.className = 'btn battle-btn';
    battleButton.textContent = 'Battle!';
    battleButton.addEventListener('click', () => startBattle(card.dataset.pokemonIndex));
    
    card.appendChild(image);
    card.appendChild(name);
    card.appendChild(stats);
    card.appendChild(totalPower);
    card.appendChild(battleButton);
    
    return card;
}

async function startBattle(pokemonIndex) {
    if (!gameSessionId) return;
    
    try {
        const response = await fetch(`/game/${gameSessionId}/battle/${pokemonIndex}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        // Show battle display
        battleDisplay.style.display = 'flex';
        
        // Update battle message
        battleMessage.textContent = `${data.message} ${data.result}`;
        
        // Update score
        scoreDisplay.textContent = data.score;
        
        // Update battle display
        updateBattleDisplay(data.selected_pokemon, data.opponent_pokemon);
        
        // Check if game is over
        if (data.game_over) {
            showCatchMessage('Game Over! You lost 3 consecutive battles. Start a new game to try again!', true);
            startGameBtn.disabled = false;
            catchPokemonBtn.disabled = true;
            document.querySelectorAll('.battle-btn').forEach(btn => btn.disabled = true);
        }
    } catch (error) {
        console.error('Error starting battle:', error);
        showCatchMessage('Failed to start battle. Please try again.', true);
    }
}

function updateBattleDisplay(playerPokemon, opponentPokemon) {
    const playerCard = battleDisplay.querySelector('.player');
    const opponentCard = battleDisplay.querySelector('.opponent');

    // Fallbacks for missing data
    const playerSprite = playerPokemon && playerPokemon.sprites && playerPokemon.sprites.front_default
        ? playerPokemon.sprites.front_default
        : 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
    const playerName = playerPokemon && playerPokemon.name ? playerPokemon.name : 'Unknown';
    const playerPower = playerPokemon ? playerPokemon.stats.reduce((sum, stat) => sum + stat.base_stat, 0) : 0;

    const opponentSprite = opponentPokemon && opponentPokemon.sprites && opponentPokemon.sprites.front_default
        ? opponentPokemon.sprites.front_default
        : 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
    const opponentName = opponentPokemon && opponentPokemon.name ? opponentPokemon.name : 'Unknown';
    const opponentPower = opponentPokemon ? opponentPokemon.stats.reduce((sum, stat) => sum + stat.base_stat, 0) : 0;

    // Update player Pokemon
    playerCard.querySelector('.pokemon-image').style.backgroundImage = `url(${playerSprite})`;
    playerCard.querySelector('.pokemon-name').textContent = playerName;
    playerCard.querySelector('.pokemon-power').textContent = `Power: ${playerPower}`;

    // Update opponent Pokemon
    opponentCard.querySelector('.pokemon-image').style.backgroundImage = `url(${opponentSprite})`;
    opponentCard.querySelector('.pokemon-name').textContent = opponentName;
    opponentCard.querySelector('.pokemon-power').textContent = `Power: ${opponentPower}`;
} 