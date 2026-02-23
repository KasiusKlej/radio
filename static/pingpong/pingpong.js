/* ============================================================================
 * PINGPONG.JS - Clean Complete Rewrite
 * ============================================================================
 * Production-ready ping pong game with:
 * - Proper factory/state data model integration
 * - No duplicated logic
 * - Clear separation of concerns
 * - Consistent physics
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
    paddleSpinFactor: 0.1,      // How much paddle motion affects ball dy
    wallBouncePreserve: -1,      // Wall bounce (perfect reflection)
    maxBallDY: BALL_SPEED * 1.5, // Prevent ball from going too vertical
    effortPerSecond: 1.0,        // Effort accumulation rate
    effortSpeedBonus: 0.11       // 11% speed boost per effort point
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
    velocity: 0,        // Current velocity (for ball spin)
    effort: 0,          // Accumulated effort
    lastMoveTime: performance.now()
};

const player2 = {
    y: canvas.height / 2 - PADDLE_HEIGHT / 2,
    score: 0,
    velocity: 0,
    effort: 0,
    lastMoveTime: performance.now()
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: BALL_SPEED,
    dy: 0,
    value: 1  // Dice face (1-6)
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
    // Player 2 (Right - Arrow keys or AI)
    // ────────────────────────────────────────────────────────────
    if (state.mode === "HUMAN") {
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
        
    } else if (state.mode === "AI") {
        // Simple AI: follow ball
        const paddleCenter = player2.y + PADDLE_HEIGHT / 2;
        const diff = ball.y - paddleCenter;
        
        player2.velocity = diff * factory.ai.difficulty;
        player2.y += player2.velocity;
        player2.y = clampPaddle(player2.y);
    }
}

function updateEffort(player, isMoving) {
    const now = performance.now();
    const dt = (now - player.lastMoveTime) / 1000;
    
    if (isMoving) {
        player.effort += dt * PHYSICS.effortPerSecond;
        player.effort = Math.min(player.effort, 1); // Cap at 1
    } else {
        player.effort = Math.max(0, player.effort - dt * 2); // Decay faster
    }
    
    player.lastMoveTime = now;
}

function clampPaddle(y) {
    return Math.max(0, Math.min(canvas.height - PADDLE_HEIGHT, y));
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
        ball.dx = -BALL_SPEED; // Serve to player 1
    } else if (lastScorer === 2) {
        ball.dx = BALL_SPEED;  // Serve to player 2
    } else {
        // Random serve
        ball.dx = (Math.random() > 0.5 ? 1 : -1) * BALL_SPEED;
    }
    
    // Random vertical velocity
    ball.dy = (Math.random() * BALL_SPEED) - (BALL_SPEED / 2);
}

function handleGoal(scoringPlayer) {
    const points = ball.value; // Dice value determines points
    
    if (scoringPlayer === 1) {
        player1.score += points;
    } else {
        player2.score += points;
    }
    
    updateScoreDisplay();
    
    // Check for winner
    if (player1.score >= WIN_SCORE || player2.score >= WIN_SCORE) {
        game.running = false;
        
        const winner = player1.score >= WIN_SCORE ? "Left Player" : "Right Player";
        setTimeout(() => {
            alert(`${winner} Wins!`);
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
        // Fallback: draw white circle if dice not loaded
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
    
    updateScoreDisplay();
    resetBall();
    
    game.running = true;
    game.paused = false;
};

window.togglePause = function() {
    if (state.mode === "NETWORK") return; // Can't pause network games
    game.paused = !game.paused;
};

window.exitGame = function() {
    location.href = "/pingpong/exit";
};

/* ============================================================================
 * START GAME
 * ============================================================================ */

initGame();