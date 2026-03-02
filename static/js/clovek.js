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
    diceValue: 6,
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
    
    // CRITICAL: Check if waiting for dice roll
    if (!gameState.waitingForDiceRoll) {
        console.log("❌ Already rolled dice this turn");
        return;
    }
    
    const currentPlayer = gameState.currentTurn;
    console.log(`🎲 ${currentPlayer} throwing dice...`);
    
    // DON'T set waitingForDiceRoll = false here!
    // Let animateDiceRoll handle it after server confirms
    
    // Request dice roll from server
    fetch("/clovek/api/game/roll-dice", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Server confirmed roll - now update state and animate
            gameState.waitingForDiceRoll = false;  // ← MOVED HERE
            animateDiceRoll(data.dice_value);
            handleAIMovesResponse(data);
        } else {
            console.error("Dice roll failed:", data.error);
            // waitingForDiceRoll stays true
        }
    })
    .catch(err => {
        console.error("Dice roll error:", err);
        // waitingForDiceRoll stays true
    });
}

function animateDiceRoll(finalValue, isAI = false) {
    gameState.animating = true;
    
    // Play dice sound
    // if (!gameState.options.sound)  BUG
    playSound("KOCKA");
    
    // CRITICAL: Store who is rolling BEFORE animation
    const rollingPlayer = gameState.currentTurn;
    
    // Get dice area based on current turn
    const area = gameState.currentTurn === "red" 
        ? FACTORY.dice_throw_area.red 
        : FACTORY.dice_throw_area.blue;
    
    // Random position within area (billiard style)
    const targetX = area.x + Math.random() * (area.width - 48);
    const targetY = area.y + Math.random() * (area.height - 48);
    
    console.log(`🎲 ${gameState.currentTurn} rolling dice to (${Math.round(targetX)}, ${Math.round(targetY)})`);
    
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
            drawDice(targetX, targetY, randomValue);
            
            setTimeout(() => requestAnimationFrame(animateFrame), frameDelay);
        } else {
            // Show final value and store position
            gameState.diceValue = finalValue;
            gameState.dicePosition = { x: targetX, y: targetY };
            drawDice(targetX, targetY, finalValue);
            gameState.animating = false;
            
            console.log(`🎲 ${rollingPlayer} rolled: ${finalValue}`);
            
            // Check if player can move ONLY for human players
            // AI moves are already handled by server
            if (!isAI) {
                checkIfPlayerCanMove(rollingPlayer);
            }
        }
    }
    
    requestAnimationFrame(animateFrame);
}

//buggy
// function animateDiceRoll(finalValue) {
//     // Flying animation from current position to target area
//     const startX = gameState.dicePosition?.x || canvas.width / 2;
//     const startY = gameState.dicePosition?.y || canvas.height / 2;
    
//     const targetX = targetArea.x + Math.random() * (targetArea.width - 48);
//     const targetY = targetArea.y + Math.random() * (targetArea.height - 48);
    
//     // Flies, then rolls, then STAYS VISIBLE
//     gameState.dicePosition = { x: targetX, y: targetY };
// }

function moveDiceToCurrentPlayer() {
    // Random position in target area (billiard style - never same spot)
    const randomX = targetArea.x + Math.random() * (targetArea.width - 48);
    const randomY = targetArea.y + Math.random() * (targetArea.height - 48);
    
    gameState.dicePosition = { x: randomX, y: randomY };
    render();
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
    console.log(`🎯 selectPawn(${pawnId}) called - State: turn=${gameState.currentTurn}, waiting=${gameState.waitingForDiceRoll}, dice=${gameState.diceValue}`);
    
    if (gameState.animating) {
        console.log("❌ Cannot select pawn: animating");
        return;
    }
    
    // CRITICAL: Check if dice has been rolled this turn
    if (gameState.waitingForDiceRoll) {
        console.log("❌ Must roll dice first! (waitingForDiceRoll=true)");
        return;
    }
    
    if (!gameState.diceValue) {
        console.log("❌ No dice value available (diceValue is null/0)");
        return;
    }
    
    // CRITICAL: Validate that pawn belongs to current player
    const pawnColor = pawnId <= 4 ? "red" : "blue";
    if (pawnColor !== gameState.currentTurn) {
        console.log(`❌ Cannot move ${pawnColor} pawn - it's ${gameState.currentTurn}'s turn!`);
        return;
    }
    
    console.log(`✓ Valid selection: ${pawnColor} pawn ${pawnId} on ${gameState.currentTurn}'s turn with dice=${gameState.diceValue}`);
    
    // Send move request to server
    fetch("/clovek/api/game/move-pawn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pawn_id: pawnId })
    })
    .then(response => {
        if (!response.ok) {
            console.error(`❌ Server returned ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("🎯 Move pawn response:", data);
        
        if (data.success && data.animation_sequence) {
            // Update turn and waiting state
            if (data.current_turn) {
                gameState.currentTurn = data.current_turn;
            }
            gameState.waitingForDiceRoll = true;  // Ready for next dice roll
            
            // Queue animation sequence from server
            queueAnimationSequence(data.animation_sequence);
            
            // Handle AI response if any
            if (data.ai_moves) {
                console.log(`📦 Received ${data.ai_moves.length} AI moves from server`);
            }
            handleAIMovesResponse(data);
        } else {
            console.error(`❌ Move failed: ${data.error}`);
            console.error(`   Client state: turn=${gameState.currentTurn}, waiting=${gameState.waitingForDiceRoll}, dice=${gameState.diceValue}`);
            console.error(`   This indicates client/server state mismatch!`);
            
            // Try to recover by resetting client state
            if (data.error === "Roll dice first" || data.error === "Dice not rolled") {
                console.warn("⚠️  Server says dice not rolled - resetting client state");
                gameState.waitingForDiceRoll = true;
                gameState.diceValue = 6;  // Show neutral dice
                render();
            }
        }
    })
    .catch(err => {
        console.error("❌ Move error:", err);
        console.error(`   Client state at error: turn=${gameState.currentTurn}, waiting=${gameState.waitingForDiceRoll}, dice=${gameState.diceValue}`);
    });
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
        console.log("✅ Animation sequence complete");
        
        // Redraw all pawns in their final positions
        redrawAllPawns();
        
        // Keep dice visible after animations
        if (gameState.diceValue && gameState.dicePosition) {
            drawDice(gameState.dicePosition.x, gameState.dicePosition.y, gameState.diceValue);
        }
        
        // Unpause game after preparation
        if (gameState.paused) {
            gameState.paused = false;
            console.log("▶️  Game unpaused, ready to play!");
        }
        
        // Only move dice if we're in active gameplay (not preparation)
        // Check if waitingForDiceRoll is true, meaning turn has ended
        if (!gameState.paused && gameState.waitingForDiceRoll) {
            moveDiceToCurrentPlayer();
        }
        
        // Update status bar
        updateStatusBar();
        
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
    
    // don't play sounds if Zvok option is off for a player
    if (!gameState.options.sound) {
        if (sound === "GREMO" || sound === "DA" || sound === "NE") {
            playSoundVariation(sound);
        } else if (sound == undefined) {
            playSound("FIGURA");
        }

    }


    
    if (!fromTile || !toTile) {
        console.error(`Invalid tiles: from=${from}, to=${to}`);
        processNextAnimation();
        return;
    }
    
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
    
    // Reset game state for new game
    gameState.currentTurn = "red";
    gameState.waitingForDiceRoll = true;
    gameState.paused = true;
    
    // Move dice to red player's area for new game
    const redArea = FACTORY.dice_throw_area.red;
    gameState.diceValue = 6;
    gameState.dicePosition = {
        x: redArea.x + Math.random() * (redArea.width - 48),
        y: redArea.y + Math.random() * (redArea.height - 48)
    };
    
    console.log("🎲 Dice reset to red area for new game");
    
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
    
    // ALWAYS draw dice if we have a value and position
    if (gameState.diceValue && gameState.dicePosition) {
        drawDice(gameState.dicePosition.x, gameState.dicePosition.y, gameState.diceValue);
    }
    
    updateStatusBar();
}

// Continuous render loop to keep dice visible
function startRenderLoop() {
    function renderFrame() {
        if (!gameState.animating) {
            render();
        }
        requestAnimationFrame(renderFrame);
    }
    requestAnimationFrame(renderFrame);
    console.log("🎬 Continuous render loop started");
}

/* ============================================================================
 * TURN MANAGEMENT
 * ============================================================================ */

function checkIfPlayerCanMove(rollingPlayer) {
    /**
     * Check if current player has any valid moves.
     * If not, automatically pass turn to opponent.
     * 
     * @param rollingPlayer - Who rolled the dice (to verify correctness)
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
            console.log(`❌ ${rollingPlayer} cannot move (rolled ${gameState.diceValue}), passing turn`);
            
            // CRITICAL: Verify we're passing for the right player
            if (data.current_player && data.current_player !== rollingPlayer) {
                console.warn(`⚠️  Server says current_player is ${data.current_player}, but ${rollingPlayer} rolled!`);
            }
            
            // Auto-pass after short delay
            setTimeout(() => {
                passTurn();
            }, 1000);
        } else if (data.success && data.can_move) {
            console.log(`✓ ${rollingPlayer} has ${data.valid_moves} valid moves`);
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
            console.log(`🔄 Turn passed from ${gameState.currentTurn} to ${data.current_turn}`);
            
            // Update game state
            gameState.currentTurn = data.current_turn;
            gameState.waitingForDiceRoll = true;
            
            // Keep dice visible with value 6 (neutral)
            gameState.diceValue = 6;
            
            // Move dice to new player's area
            moveDiceToCurrentPlayer();
            
            console.log(`✅ ${data.current_turn} must now roll dice (old roll cleared)`);
            
            // Handle AI moves if any (server may return ai_moves after pass)
            if (data.ai_moves) {
                console.log(`📦 Received ${data.ai_moves.length} AI moves after pass`);
                handleAIMovesResponse(data);
            }
            
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

// bug- pawns can't be clicked
// if (canvas) {
//     canvas.addEventListener("click", (e) => {
//         if (gameState.animating) return;
        
//         if (gameState.dicePosition) {
//             const diceSize = 48;
//             const diceRect = {
//                 x: gameState.dicePosition.x,
//                 y: gameState.dicePosition.y,
//                 width: diceSize,
//                 height: diceSize
//             };
            
//             if (isPointInRect(x, y, diceRect)) {
//                 throwDice();  // ← Only clicking dice itself
//                 return;
//             }
//         }
        
//         // Check if clicked on any pawn
//         const clickedPawn = findPawnAtPosition(x, y);
//         if (clickedPawn) {
//             console.log(`🎯 Pawn ${clickedPawn} clicked`);
//             selectPawn(clickedPawn);
//             return;
//         }
//     });
// }

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
        x: Math.floor(canvas.width / 2 - 70),
        y: Math.floor(canvas.height / 2 - 30)
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
    
    // Start continuous render loop
    startRenderLoop();
    
    // Wait for assets to load before initial display
    setTimeout(() => {
        displayInitialPawnsAndDice();
        render();
    }, 500);
    
    console.log("✅ Game initialized");
}

// function handleAIMovesResponse(data) {
//     if (data.ai_moves && data.ai_moves.length > 0) {
//         console.log(`🤖 Processing ${data.ai_moves.length} AI moves`);
        
//         data.ai_moves.forEach(aiMove => {
//             if (aiMove.animations && aiMove.animations.length > 0) {
//                 queueAnimationSequence(aiMove.animations);
//             }
//         });
        
//         // Update to final turn
//         const lastMove = data.ai_moves[data.ai_moves.length - 1];
//         gameState.currentTurn = lastMove.current_turn;
//     }
// }


// function handleAIMovesResponse(data) {
//     if (data.ai_moves && data.ai_moves.length > 0) {
//         console.log(`🤖 Processing ${data.ai_moves.length} AI moves`);
        
//         // Process EACH AI move (might be multiple if AI rolls 6)
//         data.ai_moves.forEach((aiMove, index) => {
//             console.log(`🤖 AI move ${index + 1}:`, aiMove);
            
//             // 1. Show AI dice roll
//             if (aiMove.dice_value) {
//                 console.log(`🎲 AI rolled: ${aiMove.dice_value}`);
//                 gameState.diceValue = aiMove.dice_value;  // ← UPDATE STATE
                
//                 // 2. Move dice to AI player's side
//                 const aiPlayer = aiMove.current_turn === "red" ? "blue" : "red";
//                 const aiDiceArea = aiPlayer === "red" 
//                     ? FACTORY.dice_throw_area.red 
//                     : FACTORY.dice_throw_area.blue;
                
//                 gameState.dicePosition = {
//                     x: aiDiceArea.x + 6,
//                     y: aiDiceArea.y + 6
//                 };  // ← MOVE DICE VISUALLY
//             }
            
//             // 3. Queue animations
//             if (aiMove.animations && aiMove.animations.length > 0) {
//                 queueAnimationSequence(aiMove.animations);
//             }
//         });
        
//         // 4. Update to final turn
//         const lastMove = data.ai_moves[data.ai_moves.length - 1];
//         gameState.currentTurn = lastMove.current_turn;
        
//         // 5. Move dice to final player
//         moveDiceToCurrentPlayer();
//     }
// }

function handleAIMovesResponse(data) {
    if (data.ai_moves && data.ai_moves.length > 0) {
        console.log(`🤖 Received ${data.ai_moves.length} AI moves from server`);
        
        // Wait for any current animations to finish before AI plays
        function waitAndPlayAI() {
            if (gameState.animating) {
                console.log("⏳ Waiting for animations to complete before AI plays...");
                setTimeout(waitAndPlayAI, 100);
                return;
            }
            
            // Now process AI moves
            processAIMoves(data.ai_moves);
        }
        
        waitAndPlayAI();
    }
}

function processAIMoves(aiMoves) {
    let moveIndex = 0;
    
    function playNextAIMove() {
        if (moveIndex >= aiMoves.length) {
            console.log("✅ All AI moves complete");
            return;
        }
        
        const aiMove = aiMoves[moveIndex];
        console.log(`🤖 AI move ${moveIndex + 1}/${aiMoves.length}:`, aiMove);
        
        // Update game state for AI turn
        gameState.currentTurn = aiMove.current_turn === "red" ? "blue" : "red"; // AI is opposite of result
        gameState.waitingForDiceRoll = false;
        
        // Animate AI dice roll
        if (aiMove.dice_value) {
            console.log(`🤖 AI rolling dice...`);
            animateDiceRoll(aiMove.dice_value, true);  // ← Pass isAI=true
            
            // Wait for dice animation, then play pawn animations
            setTimeout(() => {
                if (aiMove.animations && aiMove.animations.length > 0) {
                    queueAnimationSequence(aiMove.animations);
                    
                    // Wait for pawn animations, then next AI move
                    waitForAnimationsComplete(() => {
                        // Update to result turn
                        gameState.currentTurn = aiMove.current_turn;
                        gameState.waitingForDiceRoll = true;
                        moveDiceToCurrentPlayer();
                        
                        moveIndex++;
                        setTimeout(playNextAIMove, 500);
                    });
                } else {
                    // No animations, just update turn and continue
                    gameState.currentTurn = aiMove.current_turn;
                    gameState.waitingForDiceRoll = true;
                    moveDiceToCurrentPlayer();
                    
                    moveIndex++;
                    setTimeout(playNextAIMove, 500);
                }
            }, 1200);
        }
    }
    
    playNextAIMove();
}

function waitForAnimationsComplete(callback) {
    function checkComplete() {
        if (gameState.animating || animationQueue.length > 0) {
            setTimeout(checkComplete, 100);
        } else {
            callback();
        }
    }
    checkComplete();
}


function moveDiceToCurrentPlayer() {
    const targetArea = gameState.currentTurn === "red" 
        ? FACTORY.dice_throw_area.red 
        : FACTORY.dice_throw_area.blue;
    
    // Random position in target area (billiard style - never same spot)
    const randomX = targetArea.x + Math.random() * (targetArea.width - 48);
    const randomY = targetArea.y + Math.random() * (targetArea.height - 48);
    
    gameState.dicePosition = { x: randomX, y: randomY };
    
    console.log(`🎲 Dice moved to ${gameState.currentTurn} area at (${Math.round(randomX)}, ${Math.round(randomY)})`);
    
    render();  // Keeps dice visible
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


function updateStatusBar() {
    const statusElement = document.getElementById("status-turn");
    if (!statusElement) return;
    
    const player = gameState.currentTurn === "red" ? "RDEČI" : "MODRI";
    const playerEng = gameState.currentTurn === "red" ? "RED" : "BLUE";
    const color = gameState.currentTurn === "red" ? "#dc2626" : "#2563eb";
    
    let statusText;
    if (gameState.waitingForDiceRoll) {
        statusText = `Na potezi je ${player}. Vrži kocko.`;
    } else if (gameState.diceValue) {
        statusText = `${player} je na potezi. Premakni figuro (${playerEng}: ${gameState.diceValue})`;
    } else {
        statusText = `Na potezi je ${player}`;
    }
    
    statusElement.textContent = statusText;
    statusElement.style.color = color;
    statusElement.style.fontWeight = "bold";
    
    console.log(`📊 Status: ${statusText}`);
}

