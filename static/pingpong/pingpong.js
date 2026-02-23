/**
 * PINGPONG.JS
 * Real-time Engine with Negative Scoring
 */

// 1. FACTORY SETTINGS
const WIN_SCORE = 52;
const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");

// 2. GAME STATE (Single declarations only)
let gameRunning = false;
let isPaused = false;
let opponentMode = 'AI'; // 'HUMAN', 'AI', 'NETWORK'
let aiDifficulty = 0.1;   

let p1 = { score: 0, y: 200, height: 80, width: 10 };
let p2 = { score: 0, y: 200, height: 80, width: 10 };
let ball = { x: 400, y: 250, dx: 5, dy: 5, radius: 8 };
let keys = {};

// 3. BALL COSTUMES
const ballCostumes = [
    { type: 'circle', color: '#000080' },
    { type: 'square', color: '#ff0000' },
    { type: 'diamond', color: '#006400' }
];
let currentCostume = 0;


/**
 * PINGPONG.JS - Animated Dice-Ball Edition
 */

const DICE_RESOURCES = [];
let diceLoaded = 0;

// Current penalty value shown on the ball (1-6)
let currentBallValue = 1; 

function loadDiceImages() {
    const path = window.FACTORY.dice_path; 
    
    for (let i = 1; i <= 6; i++) {
        const img = new Image();
        // img.src = `${path}dice${i}.png`;
        img.src = `/metropoly/metro_static/assets/graphics/dice${i}.png`;
        img.onload = () => {
            diceLoaded++;
            if (diceLoaded === 6) console.log("🎲 All Dice Ball costumes loaded.");
        };
        DICE_RESOURCES[i] = img;
    }
}

loadDiceImages();

// --- THE VALUE TIMER (VB Timer equivalent) ---
setInterval(() => {
    if (gameRunning && !isPaused) {
        // Change the ball's "face" randomly between 1 and 6
        currentBallValue = Math.floor(Math.random() * 6) + 1;
    }
}, 800); // BALL_FLIP_FREQ from factory

function handleGoal(missingPlayer) {
    // 🎲 Use the CURRENT value shown on the dice-ball
    const penalty = currentBallValue;
    window.game.execSviraj('KOCKA.WAV');

    if (missingPlayer === 1) {
        p2.score += penalty;
        document.getElementById("status-text").innerText = `P1 penalized: -${penalty} pts`;
    } else {
        p1.score += penalty;
        document.getElementById("status-text").innerText = `P2 penalized: -${penalty} pts`;
    }

    updateScoreUI();
    if (p1.score >= WIN_SCORE || p2.score >= WIN_SCORE) {
        gameRunning = false;
        alert("Game Over!");
    } else {
        resetBall();
    }
}

function draw() {
    // 1. Clear Playground
    ctx.fillStyle = "#C0C0C0";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Draw Paddles
    ctx.fillStyle = "#000080";
    ctx.fillRect(0, p1.y, p1.width, p1.height);
    ctx.fillRect(canvas.width - p2.width, p2.y, p2.width, p2.height);

    // 3. DRAW THE DICE-BALL
    const ballImg = DICE_RESOURCES[currentBallValue];
    const size = window.FACTORY.ball_size; // e.g., 32
    
    if (ballImg) {
        // Center the image on the ball's coordinates
        ctx.drawImage(
            ballImg, 
            ball.x - size / 2, 
            ball.y - size / 2, 
            size, 
            size
        );
    }

    // 4. Center Line
    ctx.setLineDash([5, 15]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = "#808080";
    ctx.stroke();
}




// --- BRIDGE FUNCTIONS (For HTML Menu) ---

window.newGame = function() {
    p1.score = 0;
    p2.score = 0;
    window.resetBall();
    gameRunning = true;
    isPaused = false;
    updateScoreUI();
    document.getElementById("status-text").innerText = "Game Started!";
};

window.togglePause = function() {
    if (opponentMode === 'NETWORK') return;
    isPaused = !isPaused;
    document.getElementById("menu-play").classList.toggle("hidden", !isPaused);
    document.getElementById("id-pause").classList.toggle("hidden", isPaused);
    document.getElementById("status-text").innerText = isPaused ? "PAUSED" : "RUNNING";
};

window.exitGame = function() {
    window.location.href = "/pingpong/exit";
};

window.setDifficulty = function(level) {
    if (level === 'GOOD') {
        aiDifficulty = 0.15; // High precision
        document.getElementById("status-text").innerText = "AI: The Good";
    } 
    else if (level === 'BAD') {
        aiDifficulty = 0.04; // Very slow/clumsy
        document.getElementById("status-text").innerText = "AI: The Bad";
    } 
    else if (level === 'UGLY') {
        // Unpredictable mode: decent speed but introduces random errors
        aiDifficulty = 0.08; 
        document.getElementById("status-text").innerText = "AI: The Ugly";
    }
    
    // Automatically switch to AI mode if a level is picked
    opponentMode = 'AI';
    window.newGame(); 
};

window.setDifficulty = function(level) {
    opponentMode = 'AI';
    
    if (level === 'GOOD') {
        aiDifficulty = 0.15; 
        aiJitter = 0; // Perfect tracking
    } 
    else if (level === 'BAD') {
        aiDifficulty = 0.05; 
        aiJitter = 0; // Just slow
    } 
    else if (level === 'UGLY') {
        aiDifficulty = 0.10; 
        aiJitter = 25; // 25px random error margin
    }
    
    document.getElementById("status-text").innerText = "Mode: Computer (" + level + ")";
    window.newGame();
};

window.showAbout = function() {
    alert("Metropoly Ping-Pong v1.0\nVB6 Port Project");
};

// --- CORE LOGIC ---

window.resetBall = function() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = (Math.random() > 0.5 ? 5 : -5);
    ball.dy = (Math.random() * 6) - 3;
};

function handleGoal(missingPlayer) {
    // VB Logic: Random penalty 1 to 6
    const penalty = Math.floor(Math.random() * 6) + 1;
    
    if (missingPlayer === 1) {
        p2.score += penalty; // P1 missed, P2 gets points
    } else {
        p1.score += penalty;
    }

    updateScoreUI();

    if (p1.score >= WIN_SCORE || p2.score >= WIN_SCORE) {
        gameRunning = false;
        alert("Game Over! Final Score: " + p1.score + " - " + p2.score);
    } else {
        window.resetBall();
    }
}

function updateScoreUI() {
    document.getElementById("score-p1").innerText = "P1: " + p1.score;
    document.getElementById("score-p2").innerText = "P2: " + p2.score;
}

// --- ENGINE LOOP ---

document.addEventListener("keydown", (e) => keys[e.code] = true);
document.addEventListener("keyup", (e) => keys[e.code] = false);

function loop() {
    if (gameRunning && !isPaused) {
        // Move P1
        if (keys["KeyW"] && p1.y > 0) p1.y -= 7;
        if (keys["KeyS"] && p1.y < canvas.height - p1.height) p1.y += 7;

        // Move P2 (AI or Human)
        if (opponentMode === 'AI') {
            let targetY = ball.y - p2.height / 2;
            p2.y += (targetY - p2.y) * aiDifficulty;
        } else if (opponentMode === 'HUMAN') {
            if (keys["ArrowUp"] && p2.y > 0) p2.y -= 7;
            if (keys["ArrowDown"] && p2.y < canvas.height - p2.height) p2.y += 7;
        }

        // Ball Physics
        ball.x += ball.dx;
        ball.y += ball.dy;

        if (ball.y <= 0 || ball.y >= canvas.height) ball.dy *= -1;

        // Paddle Collision
        if (ball.x <= p1.width && ball.y > p1.y && ball.y < p1.y + p1.height) ball.dx *= -1.1;
        if (ball.x >= canvas.width - p2.width && ball.y > p2.y && ball.y < p2.y + p2.height) ball.dx *= -1.1;

        // Goals
        if (ball.x < 0) handleGoal(1);
        if (ball.x > canvas.width) handleGoal(2);
    }

    draw();
    requestAnimationFrame(loop);
}

function draw() {
    ctx.fillStyle = "#C0C0C0"; // Grey Playground
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Center Line
    ctx.setLineDash([5, 10]);
    ctx.beginPath();
    ctx.moveTo(canvas.width/2, 0);
    ctx.lineTo(canvas.width/2, canvas.height);
    ctx.strokeStyle = "#808080";
    ctx.stroke();

    // Paddles
    ctx.fillStyle = "#000080"; // Dark Blue
    ctx.fillRect(0, p1.y, p1.width, p1.height);
    ctx.fillRect(canvas.width - p2.width, p2.y, p2.width, p2.height);

    // Ball (Costume Logic)
    const costume = ballCostumes[currentCostume];
    ctx.fillStyle = costume.color;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
}

// Costume Timer
setInterval(() => {
    if (gameRunning && !isPaused) currentCostume = (currentCostume + 1) % ballCostumes.length;
}, 1000);

loop();

/**
 * PINGPONG.JS - Advanced Physics Edition
 */

// 1. INPUT TRACKING (Effort Accumulator)
let keyTimers = {
    "KeyW": 0, "KeyS": 0, "ArrowUp": 0, "ArrowDown": 0
};

// 2. CONSTANTS FROM FACTORY
const CONFIG = window.FACTORY || {
    effortRate: 0.02,
    maxSpeedMult: 2.5,
    basePaddleSpeed: 5,
    spinFactor: 0.6,
    speedBoost: 1.2
};

// --- CORE MOVEMENT & EFFORT ---

function getEffort(keyCode) {
    // Linear growth capped at 1.0 (100%)
    return Math.min(keyTimers[keyCode] * CONFIG.effortRate, 1.0);
}

function movePaddles() {
    // Reset velocities for this frame
    p1.v = 0;
    p2.v = 0;

    // Player 1 (W/S)
    if (keys["KeyW"]) {
        keyTimers["KeyW"]++;
        let speed = CONFIG.basePaddleSpeed * (1 + getEffort("KeyW") * CONFIG.maxSpeedMult);
        p1.y -= speed;
        p1.v = -speed; // Track velocity for spin
    } else { keyTimers["KeyW"] = 0; }

    if (keys["KeyS"]) {
        keyTimers["KeyS"]++;
        let speed = CONFIG.basePaddleSpeed * (1 + getEffort("KeyS") * CONFIG.maxSpeedMult);
        p1.y += speed;
        p1.v = speed;
    } else { keyTimers["KeyS"] = 0; }

    // Player 2 / AI
    if (opponentMode === 'HUMAN') {
        if (keys["ArrowUp"]) {
            keyTimers["ArrowUp"]++;
            p2.v = -(CONFIG.basePaddleSpeed * (1 + getEffort("ArrowUp") * CONFIG.maxSpeedMult));
            p2.y += p2.v;
        } else { keyTimers["ArrowUp"] = 0; }
        
        if (keys["ArrowDown"]) {
            keyTimers["ArrowDown"]++;
            p2.v = (CONFIG.basePaddleSpeed * (1 + getEffort("ArrowDown") * CONFIG.maxSpeedMult));
            p2.y += p2.v;
        } else { keyTimers["ArrowDown"] = 0; }
    } else {
        // AI Tracking (simplified for example)
        let targetY = ball.y - p2.height / 2;
        let diff = targetY - p2.y;
        p2.v = diff * aiDifficulty;
        p2.y += p2.v;
    }
}

// --- ADVANCED PHYSICS (The Spin Logic) ---

function handleCollision(paddle) {
    window.game.execSviraj('FIGURA.WAV');

    // 1. Direction reversal
    ball.dx *= -1;

    // 2. CALCULATE SPIN (Effort Influence)
    // In classic physics: angle_out = angle_in.
    // In our logic: angle_out = angle_in + (paddle_velocity * spin_strength)
    
    // Impact point relative to paddle center (-1 to 1)
    let impact = (ball.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2);
    
    // Add the "Effort" effect from the racket's movement
    // If you are moving UP while hitting, the ball flys UP sharper.
    ball.dy = (impact * 5) + (paddle.v * CONFIG.spinFactor);

    // 3. BOOST SPEED
    // A fast-moving racket makes the ball return faster
    let speedBonus = Math.abs(paddle.v) * CONFIG.speedBoost;
    ball.dx = (ball.dx > 0) ? (ball.dx + speedBonus) : (ball.dx - speedBonus);
    
    // Clamp speed to prevent ball escaping world
    const MAX_BALL_SPEED = 20;
    if (Math.abs(ball.dx) > MAX_BALL_SPEED) ball.dx = Math.sign(ball.dx) * MAX_BALL_SPEED;
}
function draw() {
    // 1. Clear Playground
    ctx.fillStyle = "#C0C0C0";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Draw Paddles
    ctx.fillStyle = "#000080";
    ctx.fillRect(0, p1.y, p1.width, p1.height);
    ctx.fillRect(canvas.width - p2.width, p2.y, p2.width, p2.height);

    // 3. DRAW THE DICE-BALL
    const ballImg = DICE_RESOURCES[currentBallValue];
    const size = window.FACTORY.ball_size; // e.g., 32
    
    if (ballImg) {
        // Center the image on the ball's coordinates
        ctx.drawImage(
            ballImg, 
            ball.x - size / 2, 
            ball.y - size / 2, 
            size, 
            size
        );
    }

    // 4. Center Line
    ctx.setLineDash([5, 15]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = "#808080";
    ctx.stroke();
}
