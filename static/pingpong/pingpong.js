/* ============================================================================
 * PINGPONG.JS - Complete with 3 AI Difficulty Levels
 * ============================================================================
 * Modes: HUMAN, AI_EASY, AI_MEDIUM, AI_HARD, NETWORK
 * ============================================================================
 */

/* ============================================================================
 * INITIALIZATION & CONSTANTS
 * ============================================================================ */

const { factory, state } = window.PINGPONG;

const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");

// Set canvas dimensions from factory
canvas.width = factory.geometry.width;
canvas.height = factory.geometry.height;

// Game constants from factory
const WIN_SCORE = factory.rules.max_score;
const PADDLE_WIDTH = factory.racket.width;
const PADDLE_HEIGHT = factory.racket.height;
const PADDLE_SPEED = factory.racket.speed;
const BALL_RADIUS = factory.ball.radius;
const BALL_SPEED = factory.ball.speed;

// Physics tuning constants
const PHYSICS = {
    paddleSpinFactor: 0.75,         // How much paddle motion affects ball dy
    wallBouncePreserve: -1,      // Wall bounce (perfect reflection)
    maxBallDY: BALL_SPEED * 15,   // Prevent ball from going too vertical
    effortPerSecond: 2.0,        // Effort accumulation rate
    effortSpeedBonus: 0.60       // Speed boost per effort point
};

// AI Configuration
const AI_CONFIG = {
    EASY: {
        reactionSpeed: 0.15,     // Slow reaction (0-1, higher = faster)
        predictionAccuracy: 0.3, // Poor prediction (0-1)
        errorMargin: 60,         // Large random errors in pixels
        updateDelay: 8,          // Slow update (frames between AI updates)
        speedMultiplier: 0.7,    // 70% of normal speed
        smartness: 0.2           // 20% chance to make optimal move
    },
    MEDIUM: {
        reactionSpeed: 0.35,
        predictionAccuracy: 0.6,
        errorMargin: 30,
        updateDelay: 4,
        speedMultiplier: 0.9,
        smartness: 0.5
    },
    HARD: {
        reactionSpeed: 0.65,
        predictionAccuracy: 0.9,
        errorMargin: 10,
        updateDelay: 2,
        speedMultiplier: 1.1,
        smartness: 0.8
    }
};

/* ============================================================================
 * ASSET LOADING
 * ============================================================================ */

const DICE = [];
for (let i = 1; i <= 6; i++) {
    const img = new Image();
    img.src = `${factory.assets.dice_path}dice${i}.png`;
    DICE[i] = img;
}

/* ============================================================================
 * GAME STATE
 * ============================================================================ */

const game = {
    running: false,
    paused: false
};

const player1 = {
    y: canvas.height / 2 - PADDLE_HEIGHT / 2,
    score: 0,
    velocity: 0,
    effort: 0,
    lastMoveTime: performance.now()
};

const player2 = {
    y: canvas.height / 2 - PADDLE_HEIGHT / 2,
    score: 0,
    velocity: 0,
    effort: 0,
    lastMoveTime: performance.now(),
    // AI-specific state
    targetY: canvas.height / 2,
    aiUpdateCounter: 0,
    lastBallX: canvas.width / 2
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: BALL_SPEED,
    dy: 0,
    value: 1
};

const keys = {};

/* ============================================================================
 * INPUT HANDLING
 * ============================================================================ */

document.addEventListener("keydown", e => {
    keys[e.code] = true;
});

document.addEventListener("keyup", e => {
    keys[e.code] = false;
});

/* ============================================================================
 * WINDOW EVENTS
 * ============================================================================ */

window.addEventListener('load', () => {
    resizeCanvas();
    updateScoreDisplay();
});

window.addEventListener('resize', () => {
    resizeCanvas();
    updateScoreDisplay();
});

/* ============================================================================
 * BALL DICE VALUE TIMER
 * ============================================================================ */

setInterval(() => {
    if (game.running && !game.paused) {
        ball.value = Math.floor(Math.random() * 6) + 1;
    }
}, 800);

/* ============================================================================
 * GAME INITIALIZATION
 * ============================================================================ */

function initGame() {
    resetBall();
    game.running = true;
    game.paused = false;
    requestAnimationFrame(gameLoop);
}

/* ============================================================================
 * MAIN GAME LOOP
 * ============================================================================ */

function gameLoop() {
    if (game.running && !game.paused) {
        updatePaddles();
        updateBall();
        checkCollisions();
    }
    
    render();
    requestAnimationFrame(gameLoop);
}

/* ============================================================================
 * PADDLE PHYSICS
 * ============================================================================ */

function updatePaddles() {
    const baseSpeed = PADDLE_SPEED;
    
    // ────────────────────────────────────────────────────────────
    // Player 1 (Left - W/S keys)
    // ────────────────────────────────────────────────────────────
    const p1Moving = keys["KeyW"] || keys["KeyS"];
    updateEffort(player1, p1Moving);
    
    const speed1 = baseSpeed * (1 + player1.effort * PHYSICS.effortSpeedBonus);
    
    player1.velocity = 0;
    if (keys["KeyW"]) {
        player1.velocity = -speed1;
    }
    if (keys["KeyS"]) {
        player1.velocity = speed1;
    }
    
    player1.y += player1.velocity;
    player1.y = clampPaddle(player1.y);
    
    // ────────────────────────────────────────────────────────────
    // Player 2 (Right - Human or AI)
    // ────────────────────────────────────────────────────────────
    if (state.mode === "HUMAN") {
        // Human player with arrow keys
        const p2Moving = keys["ArrowUp"] || keys["ArrowDown"];
        updateEffort(player2, p2Moving);
        
        const speed2 = baseSpeed * (1 + player2.effort * PHYSICS.effortSpeedBonus);
        
        player2.velocity = 0;
        if (keys["ArrowUp"]) {
            player2.velocity = -speed2;
        }
        if (keys["ArrowDown"]) {
            player2.velocity = speed2;
        }
        
        player2.y += player2.velocity;
        player2.y = clampPaddle(player2.y);
        
    } else if (state.mode === "AI_EASY" || state.mode === "AI_MEDIUM" || state.mode === "AI_HARD") {
        // AI opponent
        updateAI();
    }
}

function updateEffort(player, isMoving) {
    const now = performance.now();
    const dt = (now - player.lastMoveTime) / 1000;
    
    if (isMoving) {
        player.effort += dt * PHYSICS.effortPerSecond;
        player.effort = Math.min(player.effort, 1);
    } else {
        player.effort = Math.max(0, player.effort - dt * 2);
    }
    
    player.lastMoveTime = now;
}

function clampPaddle(y) {
    return Math.max(0, Math.min(canvas.height - PADDLE_HEIGHT, y));
}

/* ============================================================================
 * AI LOGIC - Three Difficulty Levels
 * ============================================================================ */

function updateAI() {
    // Get difficulty config
    let config;
    if (state.mode === "AI_EASY") config = AI_CONFIG.EASY;
    else if (state.mode === "AI_MEDIUM") config = AI_CONFIG.MEDIUM;
    else config = AI_CONFIG.HARD;
    
    // Update AI at specified interval (not every frame)
    player2.aiUpdateCounter++;
    if (player2.aiUpdateCounter < config.updateDelay) {
        // Continue moving towards last target
        moveTowardsTarget(config);
        return;
    }
    player2.aiUpdateCounter = 0;
    
    // ────────────────────────────────────────────────────────────
    // Decide target position
    // ────────────────────────────────────────────────────────────
    
    // Check if ball is moving towards AI
    const ballMovingTowardsAI = ball.dx > 0;
    
    if (!ballMovingTowardsAI) {
        // Ball moving away - return to center (with some laziness)
        player2.targetY = canvas.height / 2 - PADDLE_HEIGHT / 2;
        
        // Easy AI is very lazy
        if (state.mode === "AI_EASY" && Math.random() > 0.3) {
            return; // Don't update target 70% of the time when ball is away
        }
    } else {
        // Ball moving towards AI - calculate intercept
        const interceptY = predictBallIntercept(config);
        player2.targetY = interceptY - PADDLE_HEIGHT / 2;
        
        // Add random error based on difficulty
        const error = (Math.random() - 0.5) * config.errorMargin;
        player2.targetY += error;
        
        // Smart move: occasionally aim for optimal position
        if (Math.random() < config.smartness) {
            // Aim for paddle center to maximize control
            player2.targetY = interceptY - PADDLE_HEIGHT / 2;
        }
    }
    
    // Move towards target
    moveTowardsTarget(config);
}

function predictBallIntercept(config) {
    // Simple prediction: where will ball be when it reaches paddle?
    const distanceToAI = (canvas.width - PADDLE_WIDTH) - ball.x;
    const timeToReach = distanceToAI / Math.abs(ball.dx);
    
    // Predict Y position
    let predictedY = ball.y + (ball.dy * timeToReach * config.predictionAccuracy);
    
    // Account for wall bounces (simplified)
    while (predictedY < 0 || predictedY > canvas.height) {
        if (predictedY < 0) {
            predictedY = -predictedY;
        }
        if (predictedY > canvas.height) {
            predictedY = 2 * canvas.height - predictedY;
        }
    }
    
    // Add prediction inaccuracy
    if (config.predictionAccuracy < 1) {
        const inaccuracy = (1 - config.predictionAccuracy) * 100;
        predictedY += (Math.random() - 0.5) * inaccuracy;
    }
    
    return predictedY;
}

function moveTowardsTarget(config) {
    const paddleCenter = player2.y + PADDLE_HEIGHT / 2;
    const diff = player2.targetY + PADDLE_HEIGHT / 2 - paddleCenter;
    
    // Calculate movement speed
    const baseSpeed = PADDLE_SPEED * config.speedMultiplier;
    const moveSpeed = baseSpeed * config.reactionSpeed;
    
    // Move towards target
    if (Math.abs(diff) > 2) {
        player2.velocity = Math.sign(diff) * moveSpeed;
        player2.y += player2.velocity;
        player2.y = clampPaddle(player2.y);
    } else {
        player2.velocity = 0;
    }
}

/* ============================================================================
 * BALL PHYSICS
 * ============================================================================ */

function updateBall() {
    // Move ball
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // Wall collisions (top/bottom)
    if (ball.y - BALL_RADIUS <= 0 || ball.y + BALL_RADIUS >= canvas.height) {
        ball.dy *= PHYSICS.wallBouncePreserve;
        
        // Keep ball in bounds
        if (ball.y - BALL_RADIUS < 0) ball.y = BALL_RADIUS;
        if (ball.y + BALL_RADIUS > canvas.height) ball.y = canvas.height - BALL_RADIUS;
    }
    
    // Goal detection
    if (ball.x - BALL_RADIUS < 0) {
        handleGoal(2); // Player 2 scores
    }
    if (ball.x + BALL_RADIUS > canvas.width) {
        handleGoal(1); // Player 1 scores
    }
}

function checkCollisions() {
    // Check Player 1 paddle collision
    if (ball.dx < 0) { // Ball moving left
        if (
            ball.x - BALL_RADIUS <= PADDLE_WIDTH &&
            ball.y >= player1.y &&
            ball.y <= player1.y + PADDLE_HEIGHT
        ) {
            handlePaddleHit(player1);
        }
    }
    
    // Check Player 2 paddle collision
    if (ball.dx > 0) { // Ball moving right
        if (
            ball.x + BALL_RADIUS >= canvas.width - PADDLE_WIDTH &&
            ball.y >= player2.y &&
            ball.y <= player2.y + PADDLE_HEIGHT
        ) {
            handlePaddleHit(player2);
        }
    }
}

function handlePaddleHit(player) {
    // Reverse horizontal direction
    ball.dx = -ball.dx;
    
    // Add spin from paddle motion
    ball.dy += player.velocity * PHYSICS.paddleSpinFactor;
    
    // Clamp vertical speed
    ball.dy = Math.max(-PHYSICS.maxBallDY, Math.min(PHYSICS.maxBallDY, ball.dy));
    
    // Keep ball from getting stuck in paddle
    if (player === player1) {
        ball.x = PADDLE_WIDTH + BALL_RADIUS;
    } else {
        ball.x = canvas.width - PADDLE_WIDTH - BALL_RADIUS;
    }
    
    // Play sound (if available)
    if (window.game?.execSviraj) {
        window.game.execSviraj("FIGURA.WAV");
    }
}

function resetBall(lastScorer) {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    
    // Serve towards player who didn't score
    if (lastScorer === 1) {
        ball.dx = -BALL_SPEED;
    } else if (lastScorer === 2) {
        ball.dx = BALL_SPEED;
    } else {
        // Random serve
        ball.dx = (Math.random() > 0.5 ? 1 : -1) * BALL_SPEED;
    }
    ball.dx = ball.dx + (Math.random()-0.5)*0.1 * ball.dx

    // Random vertical velocity
    ball.dy = (Math.random() * BALL_SPEED) - (BALL_SPEED / 2);
    
    // Reset AI tracking
    player2.lastBallX = ball.x;
}

function handleGoal(scoringPlayer) {
    const points = ball.value;
    
    if (scoringPlayer === 1) {
        player1.score += points;
    } else {
        player2.score += points;
    }
    
    updateScoreDisplay();
    
    // Check for winner
    if (player1.score >= WIN_SCORE || player2.score >= WIN_SCORE) {
        game.running = false;
        
        const winner = player1.score >= WIN_SCORE ? "Levi igralec " : "Desni igralec ";
        setTimeout(() => {
            alert(`${winner} je zmagal!`);
            //openMsgBox(`Zmaga`, `${winner} je zmagal!`)
            newGame();
        }, 100);
        return;
    }
    
    // Reset ball (serve towards scorer)
    resetBall(scoringPlayer);
}



/* ============================================================================
 * RENDERING
 * ============================================================================ */

function render() {
    drawField();
    drawPaddles();
    drawBall();
}

function drawField() {
    // Green background
    ctx.fillStyle = "#006400";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Center line
    ctx.save();
    ctx.setLineDash([8, 16]);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.restore();
}

function drawPaddles() {
    ctx.fillStyle = "#ffffff";
    
    // Player 1 (left)
    ctx.fillRect(0, player1.y, PADDLE_WIDTH, PADDLE_HEIGHT);
    
    // Player 2 (right)
    ctx.fillRect(
        canvas.width - PADDLE_WIDTH,
        player2.y,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    );
}

function drawBall() {
    const img = DICE[ball.value];
    
    if (!img || !img.complete) {
        // Fallback: draw white circle
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, BALL_RADIUS, 0, Math.PI * 2);
        ctx.fill();
        return;
    }
    
    // Draw dice image
    const size = BALL_RADIUS * 2;
    ctx.drawImage(
        img,
        ball.x - BALL_RADIUS,
        ball.y - BALL_RADIUS,
        size,
        size
    );
}

/* ============================================================================
 * SCORE DISPLAY
 * ============================================================================ */

function updateScoreDisplay() {
    const leftDiv = document.getElementById("score-left");
    const rightDiv = document.getElementById("score-right");
    
    if (!leftDiv || !rightDiv) return;
    
    // Scale font size with canvas
    const fontSize = canvas.height * 0.07;
    leftDiv.style.fontSize = `${fontSize}px`;
    rightDiv.style.fontSize = `${fontSize}px`;
    
    // Update scores
    leftDiv.textContent = player1.score;
    rightDiv.textContent = player2.score;
}

/* ============================================================================
 * CANVAS RESIZE
 * ============================================================================ */

function resizeCanvas() {
    const container = document.getElementById('game-container');
    if (!container) return;
    
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    
    // Maintain aspect ratio from factory geometry
    const aspect = factory.geometry.width / factory.geometry.height;
    
    let width = containerWidth;
    let height = width / aspect;
    
    if (height > containerHeight) {
        height = containerHeight;
        width = height * aspect;
    }
    
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
}

/* ============================================================================
 * MENU BRIDGE FUNCTIONS
 * ============================================================================ */

window.newGame = function() {
    player1.score = 0;
    player2.score = 0;
    player1.effort = 0;
    player2.effort = 0;
    player2.aiUpdateCounter = 0;
    
    updateScoreDisplay();
    resetBall();
    
    game.running = true;
    game.paused = false;
};

window.togglePause = function() {
    if (state.mode === "NETWORK") return;
    game.paused = !game.paused;
};

window.exitGame = function() {
    location.href = "/pingpong/exit";
};

function closeMsgBox() {
    document.getElementById('win95-modal-overlay').style.display = 'none';
}

/* ============================================================================
 * START GAME
 * ============================================================================ */

initGame();