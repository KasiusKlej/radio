/* ============================================================================
 * CLOVEK (LUDO) - JavaScript Game Engine
 * ============================================================================
 * Handles animations, keyboard input, sound, and game state rendering
 * ============================================================================
 */

/* ============================================================================
 * INITIALIZATION & GLOBAL STATE
 * ============================================================================ */

// Get factory settings from server (passed via template)
const FACTORY = window.CLOVEK?.FACTORY || window.FACTORY || {
    // Fallback factory settings if not provided
    dice: { size: 48 },
    pawns: { width: 28, height: 28 },
    dice_throw_area: {
        red: { x: 100, y: 450, width: 60, height: 60 },
        blue: { x: 730, y: 50, width: 60, height: 60 }
    }
};

const canvas = document.getElementById("clovekCanvas");
const ctx = canvas ? canvas.getContext("2d") : null;

// Game state
const gameState = {
    mode: "NETWORK",
    paused: true,
    currentTurn: "red",
    diceValue: 6,       // Initial dice value (before any rolls)
    dicePosition: null, // Will be set to center initially
    animating: false,
    options: {
        fast: false,    // Fast-forward animations
        sound: true     // Play sounds
    }
};

// Asset storage
const assets = {
    dice: {},       // dice1.png - dice6.png
    pawns: {},      // R1-R4, M5-M8
    sounds: {},     // KOCKA, FIGURA, GREMO0-4, DA0-4, NE0-4
    board: null     // tabla.png (already loaded in HTML)
};

// Animation queue
const animationQueue = [];
let currentAnimation = null;

/* ============================================================================
 * ASSET LOADING
 * ============================================================================ */

function loadAssets() {
    const basePath = "/static/clovek/";
    
    // Load dice images (1-6)
    for (let i = 1; i <= 6; i++) {
        const img = new Image();
        img.src = `${basePath}dice${i}.png`;
        assets.dice[i] = img;
    }
    
    // Load pawn images (R1-R4 = red, M5-M8 = blue)
    const pawnIds = ["R1", "R2", "R3", "R4", "M5", "M6", "M7", "M8"];
    pawnIds.forEach(id => {
        const img = new Image();
        img.src = `${basePath}${id}.png`;
        assets.pawns[id] = img;
    });
    
    // Load sounds
    loadSounds(basePath);
    
    console.log("✅ Assets loaded");
}

function loadSounds(basePath) {
    // Dice throw sound
    assets.sounds.KOCKA = new Audio(`${basePath}KOCKA.WAV`);
    
    // Pawn step sound
    assets.sounds.FIGURA = new Audio(`${basePath}FIGURA.WAV`);
    
    // Happy sounds (leaving home) - GREMO0-4
    assets.sounds.GREMO = [];
    for (let i = 0; i <= 4; i++) {
        assets.sounds.GREMO.push(new Audio(`${basePath}GREMO${i}.WAV`));
    }
    
    // Victory sounds (capturing) - DA0-4
    assets.sounds.DA = [];
    for (let i = 0; i <= 4; i++) {
        assets.sounds.DA.push(new Audio(`${basePath}DA${i}.WAV`));
    }
    
    // Sad sounds (going home) - NE0-4
    assets.sounds.NE = [];
    for (let i = 0; i <= 4; i++) {
        assets.sounds.NE.push(new Audio(`${basePath}NE${i}.WAV`));
    }
}

/* ============================================================================
 * KEYBOARD SHORTCUTS
 * ============================================================================ */

document.addEventListener("keydown", (e) => {
    // Prevent if animating
    if (gameState.animating) return;
    
    // Space = throw dice
    if (e.code === "Space") {
        e.preventDefault();
        throwDice();
        return;
    }
    
    // 1-8 = select pawn to move
    const key = e.key;
    if (key >= "1" && key <= "8") {
        e.preventDefault();
        const pawnId = parseInt(key);
        selectPawn(pawnId);
    }
});

/* ============================================================================
 * DICE ANIMATION
 * ============================================================================ */

function throwDice() {
    if (gameState.paused || gameState.animating) {
        console.log("Cannot throw dice: game paused or animating");
        return;
    }
    
    // Request dice roll from server
    fetch("/clovek/api/game/roll-dice", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            animateDiceRoll(data.dice_value);
            handleAIMovesResponse(data);
        } else {
            console.error("Dice roll failed:", data.error);
        }
    })
    .catch(err => console.error("Dice roll error:", err));
}

function animateDiceRoll(finalValue) {
    gameState.animating = true;
    
    // Play dice sound
    playSound("KOCKA");
    
    // Get dice position based on current turn
    const area = gameState.currentTurn === "red" 
        ? FACTORY.dice_throw_area.red 
        : FACTORY.dice_throw_area.blue;
    
    // Clear the initial center position (only used for display before game starts)
    gameState.dicePosition = null;
    
    const duration = gameState.options.fast ? 400 : 800;
    const frameDelay = gameState.options.fast ? 60 : 120;
    const startTime = performance.now();
    
    function animateFrame(currentTime) {
        const elapsed = currentTime - startTime;
        
        // Clear canvas during animation
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        redrawAllPawns();  // Keep pawns visible
        
        if (elapsed < duration) {
            // Show random dice face during roll
            const randomValue = Math.floor(Math.random() * 6) + 1;
            drawDice(area.x, area.y, randomValue);
            
            setTimeout(() => requestAnimationFrame(animateFrame), frameDelay);
        } else {
            // Show final value and store position
            gameState.diceValue = finalValue;
            gameState.dicePosition = { x: area.x, y: area.y };
            drawDice(area.x, area.y, finalValue);
            gameState.animating = false;
            
            console.log(`🎲 Dice rolled: ${finalValue}`);
            
            // Check if player can move at all
            checkIfPlayerCanMove();
        }
    }
    
    requestAnimationFrame(animateFrame);
}

function drawDice(x, y, value) {
    if (!ctx || !assets.dice[value]) return;
    
    // Get dice size from FACTORY or use default
    const size = FACTORY?.dice?.size || 48;
    
    const diceImage = assets.dice[value];
    if (diceImage && diceImage.complete) {
        ctx.drawImage(diceImage, x, y, size, size);
    }
}

/* ============================================================================
 * PAWN SELECTION & MOVEMENT
 * ============================================================================ */

function selectPawn(pawnId) {
    if (gameState.animating || !gameState.diceValue) {
        console.log("Cannot select pawn: animating or no dice roll");
        return;
    }
    
    // Send move request to server
    fetch("/clovek/api/game/move-pawn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pawn_id: pawnId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.animation_sequence) {
            // Queue animation sequence from server
            queueAnimationSequence(data.animation_sequence);
            handleAIMovesResponse(data);
        } else {
            console.error("Move failed:", data.error);
        }
    })
    .catch(err => console.error("Move error:", err));
}

/* ============================================================================
 * ANIMATION SEQUENCE SYSTEM
 * ============================================================================ */

/**
 * Animation sequence format from server:
 * [
 *   { pawn: 1, from: 33, to: 45, sound: "GREMO" },
 *   { pawn: 1, from: 45, to: 46 },
 *   { pawn: 1, from: 46, to: 47 },
 *   { pawn: 5, from: 47, to: 111, sound: "DA" }
 * ]
 */

// Store pawn positions for persistent rendering
const pawnPositions = {};  // { pawn_id: tile_id }

function queueAnimationSequence(sequence) {
    // Add all animations to the queue
    sequence.forEach(anim => animationQueue.push(anim));
    
    console.log(`📋 Queued ${sequence.length} animations (total: ${animationQueue.length})`);
    
    if (!gameState.animating) {
        processNextAnimation();
    }
}

function processNextAnimation() {
    if (animationQueue.length === 0) {
        gameState.animating = false;
        gameState.diceValue = null;
        console.log("✅ Animation sequence complete");
        
        // Redraw all pawns in their final positions
        redrawAllPawns();
        
        // Unpause game after preparation
        gameState.paused = false;
        console.log("▶️  Game unpaused, ready to play!");
        
        return;
    }
    
    gameState.animating = true;
    const anim = animationQueue.shift();
    
    console.log(`🎬 Animating pawn ${anim.pawn}: ${anim.from} → ${anim.to}`);
    
    animatePawnMove(anim);
}

function animatePawnMove(anim) {
    const { pawn, from, to, sound } = anim;
    
    // Get board tile positions
    const fromTile = getBoardTile(from);
    const toTile = getBoardTile(to);
    
    if (!fromTile || !toTile) {
        console.error(`Invalid tiles: from=${from}, to=${to}`);
        processNextAnimation();
        return;
    }
    
    // Play sound based on the sound parameter:
    // - "GREMO", "DA", "NE" = play that sound variation
    // - undefined = play FIGURA (default step sound)
    // - null = silent (preparation moves)
    if (sound === "GREMO" || sound === "DA" || sound === "NE") {
        playSoundVariation(sound);
    } else if (sound === undefined) {
        // Default step sound
        playSound("FIGURA");
    }
    // If sound === null, it's silent (preparation)
    
    // Get duration based on fast mode
    const duration = gameState.options.fast ? 150 : 300;
    const startTime = performance.now();
    const pawnImage = getPawnImage(pawn);
    
    function animateFrame(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Clear canvas and redraw everything
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Redraw all other pawns at their current positions
        redrawAllPawns(pawn);  // Exclude the animating pawn
        
        // Interpolate position for animating pawn
        const x = fromTile.x + (toTile.x - fromTile.x) * progress;
        const y = fromTile.y + (toTile.y - fromTile.y) * progress;
        
        // Draw animating pawn at interpolated position
        drawPawn(x, y, pawnImage);
        
        // Redraw dice if visible
        if (gameState.diceValue && gameState.dicePosition) {
            drawDice(
                gameState.dicePosition.x,
                gameState.dicePosition.y,
                gameState.diceValue
            );
        }
        
        if (progress < 1) {
            requestAnimationFrame(animateFrame);
        } else {
            // Animation complete - update pawn position
            pawnPositions[pawn] = to;
            console.log(`✓ Pawn ${pawn} now at tile ${to}`);
            
            // Process next animation after a small delay
            setTimeout(() => processNextAnimation(), 50);
        }
    }
    
    requestAnimationFrame(animateFrame);
}

function redrawAllPawns(excludePawn = null) {
    /**
     * Redraw all pawns at their stored positions.
     * Optionally exclude one pawn (the one currently animating).
     */
    for (const [pawnId, tileId] of Object.entries(pawnPositions)) {
        const pawnIdNum = parseInt(pawnId);
        
        // Skip the excluded pawn
        if (pawnIdNum === excludePawn) {
            continue;
        }
        
        const tile = getBoardTile(tileId);
        if (tile) {
            const pawnImage = getPawnImage(pawnIdNum);
            if (pawnImage && pawnImage.complete) {
                drawPawn(tile.x, tile.y, pawnImage);
            }
        }
    }
}

/* ============================================================================
 * DRAWING FUNCTIONS
 * ============================================================================ */

// Pawn position offsets (adjust these to fine-tune pawn placement)
const PAWN_OFFSET_X = 22;  // Pixels to the right
const PAWN_OFFSET_Y = 19;  // Pixels down

function drawPawn(x, y, image) {
    if (!ctx || !image) return;
    
    const size = FACTORY?.pawns?.width || 28;
    
    // Apply offsets and center the pawn
    const offsetX = x + PAWN_OFFSET_X - size / 2;
    const offsetY = y + PAWN_OFFSET_Y - size / 2;
    
    ctx.drawImage(image, offsetX, offsetY, size, size);
}

function drawAllPawns(pawnPositions) {
    /**
     * Draw all pawns at their current positions.
     * pawnPositions: { pawn_id: tile_id, ... }
     */
    if (!ctx || !pawnPositions) return;
    
    for (const [pawnId, tileId] of Object.entries(pawnPositions)) {
        const tile = getBoardTile(tileId);
        if (tile) {
            const pawnImage = getPawnImage(parseInt(pawnId));
            if (pawnImage && pawnImage.complete) {
                drawPawn(tile.x, tile.y, pawnImage);
            }
        }
    }
}

function getPawnImage(pawnId) {
    // Pawn IDs: 1-4 = R1-R4 (red), 5-8 = M5-M8 (blue)
    if (pawnId >= 1 && pawnId <= 4) {
        return assets.pawns[`R${pawnId}`];
    } else if (pawnId >= 5 && pawnId <= 8) {
        return assets.pawns[`M${pawnId}`];
    }
    return null;
}

function getBoardTile(tileId) {
    // Get tile position from loaded board data
    if (window.BOARD_TILES && window.BOARD_TILES[tileId]) {
        return window.BOARD_TILES[tileId];
    }
    
    // Fallback: return approximate center position
    console.warn(`Tile ${tileId} not found, using fallback position`);
    return { 
        x: canvas.width / 2, 
        y: canvas.height / 2 
    };
}

/* ============================================================================
 * SOUND SYSTEM
 * ============================================================================ */

function playSound(soundName) {
    if (!gameState.options.sound) return;
    
    const sound = assets.sounds[soundName];
    if (sound) {
        sound.currentTime = 0;
        sound.play().catch(err => console.warn("Sound play failed:", err));
    }
}

function playSoundVariation(soundFamily) {
    if (!gameState.options.sound) return;
    
    // Sound families: GREMO, DA, NE (each has 0-4 variations)
    const sounds = assets.sounds[soundFamily];
    if (sounds && sounds.length > 0) {
        const randomIndex = Math.floor(Math.random() * sounds.length);
        const sound = sounds[randomIndex];
        sound.currentTime = 0;
        sound.play().catch(err => console.warn("Sound play failed:", err));
    }
}

/* ============================================================================
 * GAME STATE UPDATES
 * ============================================================================ */

function updateGameState(newState) {
    Object.assign(gameState, newState);
    
    // If state includes pawn positions, redraw
    if (newState.pawns) {
        drawAllPawns(newState.pawns);
    }
    
    render();
}

function updateOptions(options) {
    gameState.options = { ...gameState.options, ...options };
    console.log("Options updated:", gameState.options);
}

function handlePreparationAnimations(animations) {
    /**
     * Handle the 8 preparation moves when game starts.
     * These move pawns from random positions to home squares.
     */
    if (!animations || animations.length === 0) {
        console.log("No preparation animations");
        return;
    }
    
    console.log(`🏠 Processing ${animations.length} preparation animations`);
    
    // Queue all preparation animations
    queueAnimationSequence(animations);
}

/* ============================================================================
 * RENDERING
 * ============================================================================ */

function render() {
    if (!ctx) return;
    
    // Clear canvas (board image is in background HTML img tag)
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw all pawns at their stored positions
    redrawAllPawns();
    
    // Draw dice if we have a value and position
    if (gameState.diceValue && gameState.dicePosition) {
        drawDice(
            gameState.dicePosition.x, 
            gameState.dicePosition.y, 
            gameState.diceValue
        );
    } else if (gameState.diceValue) {
        // Fallback: draw at center if no position set
        const area = gameState.currentTurn === "red" 
            ? (FACTORY?.dice_throw_area?.red || { x: 100, y: 450 })
            : (FACTORY?.dice_throw_area?.blue || { x: 730, y: 50 });
        drawDice(area.x, area.y, gameState.diceValue);
    }
}

/* ============================================================================
 * TURN MANAGEMENT
 * ============================================================================ */

function checkIfPlayerCanMove() {
    /**
     * Check if current player has any valid moves.
     * If not, automatically pass turn to opponent.
     */
    fetch("/clovek/api/game/check-moves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            dice_value: gameState.diceValue 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && !data.can_move) {
            console.log(`❌ ${data.current_player} cannot move, passing turn`);
            
            // Auto-pass after short delay
            setTimeout(() => {
                passTurn();
            }, 1000);
        } else if (data.success && data.can_move) {
            console.log(`✓ ${data.current_player} has ${data.valid_moves} valid moves`);
        }
    })
    .catch(err => console.error("Error checking moves:", err));
}

function passTurn() {
    /**
     * Pass turn to opponent (no valid moves available).
     */
    fetch("/clovek/api/game/pass-turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`🔄 Turn passed to ${data.current_turn}`);
            
            // Update game state
            gameState.currentTurn = data.current_turn;
            gameState.diceValue = null;
            gameState.dicePosition = null;
            
            // Redraw board
            render();
        }
    })
    .catch(err => console.error("Error passing turn:", err));
}


/* ============================================================================
 * CLICK HANDLERS
 * ============================================================================ */

if (canvas) {
    canvas.addEventListener("click", (e) => {
        if (gameState.animating) return;
        
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        
        console.log(`🖱️  Click at (${Math.round(x)}, ${Math.round(y)})`);
        
        // Check if clicked on dice area
        const diceArea = gameState.currentTurn === "red" 
            ? FACTORY?.dice_throw_area?.red 
            : FACTORY?.dice_throw_area?.blue;
        
        if (diceArea && isPointInRect(x, y, diceArea)) {
            console.log("🎲 Dice clicked");
            throwDice();
            return;
        }
        
        // Check if clicked on any pawn
        const clickedPawn = findPawnAtPosition(x, y);
        if (clickedPawn) {
            console.log(`🎯 Pawn ${clickedPawn} clicked`);
            selectPawn(clickedPawn);
            return;
        }
    });
}

function isPointInRect(x, y, rect) {
    return x >= rect.x && x <= rect.x + rect.width &&
           y >= rect.y && y <= rect.y + rect.height;
}

function findPawnAtPosition(clickX, clickY) {
    /**
     * Find which pawn (if any) was clicked.
     * Returns pawn ID (1-8) or null.
     */
    const clickRadius = 20;  // Click tolerance in pixels
    
    for (const [pawnId, tileId] of Object.entries(pawnPositions)) {
        const tile = getBoardTile(tileId);
        if (!tile) continue;
        
        // Calculate pawn's actual drawn position (with offsets)
        const pawnX = tile.x + PAWN_OFFSET_X;
        const pawnY = tile.y + PAWN_OFFSET_Y;
        
        // Check if click is within radius
        const distance = Math.sqrt(
            Math.pow(clickX - pawnX, 2) + 
            Math.pow(clickY - pawnY, 2)
        );
        
        if (distance <= clickRadius) {
            return parseInt(pawnId);
        }
    }
    
    return null;
}

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================ */

function loadBoardTiles() {
    // Load tile positions from server
    fetch("/clovek/api/board/tiles")
        .then(response => {
            if (!response.ok) {
                console.warn("Board tiles endpoint not found, using built-in positions");
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.tiles) {
                // Store tile positions for animation
                window.BOARD_TILES = data.tiles;
                console.log("✅ Board tiles loaded:", Object.keys(data.tiles).length);
            } else {
                // Use built-in tile positions as fallback
                console.log("⚠️  Using fallback tile positions");
            }
        })
        .catch(err => {
            console.warn("Failed to load board tiles, continuing without server data:", err.message);
        });
}

function displayInitialPawnsAndDice() {
    /**
     * Show pawns and dice randomly on board until game starts.
     * Once players join, engine will position pawns in home squares.
     */
    if (!ctx || !canvas) {
        console.warn("Canvas not available for initial display");
        return;
    }
    
    // Random positions for initial display
    const randomPositions = [
        { x: 150, y: 250 },
        { x: 300, y: 150 },
        { x: 450, y: 200 },
        { x: 600, y: 350 },
        { x: 250, y: 400 },
        { x: 500, y: 450 },
        { x: 700, y: 250 },
        { x: 350, y: 300 }
    ];
    
    // Store initial pawn positions (these will be overwritten during preparation)
    for (let i = 1; i <= 8; i++) {
        pawnPositions[i] = 0;  // 0 = undefined/random position
    }
    
    // Draw all 8 pawns randomly
    for (let i = 1; i <= 8; i++) {
        const pos = randomPositions[i - 1];
        const pawnImage = getPawnImage(i);
        if (pawnImage && pawnImage.complete) {
            drawPawn(pos.x, pos.y, pawnImage);
        }
    }
    
    // Set initial dice value and position (center of board)
    gameState.diceValue = 6; // Show 6 initially
    gameState.dicePosition = {
        x: Math.floor(canvas.width / 2 - 24),
        y: Math.floor(canvas.height / 2 - 24)
    };
    
    // Draw dice at center
    const diceImage = assets.dice[6];
    if (diceImage && diceImage.complete) {
        drawDice(gameState.dicePosition.x, gameState.dicePosition.y, 6);
    }
    
    console.log("🎲 Initial pawns and dice displayed (dice=6 at center)");
}

/* ============================================================================
 * INITIALIZATION
 * ============================================================================ */

function initGame() {
    console.log("🎲 Initializing Clovek game...");
    
    // Load assets
    loadAssets();
    
    // Load board tile positions (optional, has fallback)
    loadBoardTiles();
    
    // Wait for assets to load before initial display
    setTimeout(() => {
        displayInitialPawnsAndDice();
        render();
    }, 500);
    
    console.log("✅ Game initialized");
}

function handleAIMovesResponse(data) {
    if (data.ai_moves && data.ai_moves.length > 0) {
        console.log(`🤖 Processing ${data.ai_moves.length} AI moves`);
        
        data.ai_moves.forEach(aiMove => {
            if (aiMove.animations && aiMove.animations.length > 0) {
                queueAnimationSequence(aiMove.animations);
            }
        });
        
        // Update to final turn
        const lastMove = data.ai_moves[data.ai_moves.length - 1];
        gameState.currentTurn = lastMove.current_turn;
    }
}





// Start when DOM is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGame);
} else {
    initGame();
}

/* ============================================================================
 * GLOBAL API (for menu integration)
 * ============================================================================ */

window.clovekGame = {
    throwDice,
    selectPawn,
    updateOptions,
    updateGameState,
    queueAnimationSequence,
    handlePreparationAnimations,
    drawAllPawns
};

/* ============================================================================
 * EXAMPLE ANIMATION SEQUENCE FROM SERVER
 * ============================================================================ */

/**
 * Server should send animation sequences like this:
 * 
 * {
 *   "success": true,
 *   "animation_sequence": [
 *     { "pawn": 1, "from": 33, "to": 45, "sound": "GREMO" },
 *     { "pawn": 1, "from": 45, "to": 46 },
 *     { "pawn": 1, "from": 46, "to": 47 },
 *     { "pawn": 5, "from": 47, "to": 111, "sound": "DA" }
 *   ]
 * }
 * 
 * Sound options:
 * - "GREMO" = Happy (leaving home square, random 0-4)
 * - "DA" = Victory (capturing enemy pawn, random 0-4)
 * - "NE" = Sad (being captured, random 0-4)
 * - null/undefined = Default "FIGURA" step sound
 */
