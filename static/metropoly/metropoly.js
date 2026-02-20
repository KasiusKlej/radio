// -----------------------------
// Full graphic asset mapping
// -----------------------------

// ASSET_MAP: numeric and string keys
const ASSET_MAP = {
    // Roads (0-10)
    0: 'roaddl.png', 1: 'roaddr.png', 2: 'roadlr.png', 3: 'roadud.png',
    4: 'roadul.png', 5: 'roadur.png', 6: 'road3n.png', 7: 'road3e.png',
    8: 'road3w.png', 9: 'road3s.png', 10: 'road4.png',

    // Tiles (11-19)
    11: 'h0.png', 12: 'h1.png', 13: 'h2.png', 14: 'h3.png', 15: 'h4.png', 16: 'h5.png',
    17: 'school.png', 18: 'job.png', 19: 'jail.png',

    // Road adjacency mapping
    roads: {
        '1100': 'roadud.png', '0011': 'roadlr.png', '0110': 'roaddl.png',
        '0101': 'roaddr.png', '1010': 'roadul.png', '1001': 'roadur.png',
        '0111': 'road3s.png', '1011': 'road3n.png', '1101': 'road3e.png',
        '1110': 'road3w.png', '1111': 'road4.png'
    },

    // Semaphore mapping
    semafor: {
        33: 'n2.png', 34: 'n3.png', 35: 'n4.png', 36: 's1.png', 37: 's3.png', 38: 's4.png',
        39: 'w1.png', 40: 'w2.png', 41: 'w4.png', 42: 'e1.png', 43: 'e2.png', 44: 'e3.png'
    },

    // Players / Flags (20-26)
    20: 'flag1.png', 21: 'flag2.png', 22: 'flag3.png', 23: 'flag4.png',
    24: 'flag5.png', 25: 'flag6.png', 26: 'flag7.png',

    // Dice (27-32)
    27: 'dice1.png', 28: 'dice2.png', 29: 'dice3.png',
    30: 'dice4.png', 31: 'dice5.png', 32: 'dice6.png',

    // Gauges / map editor (45-54)
    45: 'gaug0.png', 46: 'gaug1.png', 47: 'gaug2.png', 48: 'gaug3.png', 49: 'gaug4.png',
    50: 'gaug5.png', 51: 'gaug6.png', 52: 'gaug7.png', 53: 'gaug8.png', 54: 'gaug9.png'
};

// -----------------------------
// ASSETS object for convenient access in game
// -----------------------------
const ASSETS = {};

// Populate from ASSET_MAP
for (const [key, value] of Object.entries(ASSET_MAP)) {
    if (typeof value === 'string') {
        ASSETS[key] = `/static/icons/${value}`;
    } else if (typeof value === 'object') {
        ASSETS[key] = {};
        for (const [subKey, subVal] of Object.entries(value)) {
            ASSETS[key][subKey] = `/static/icons/${subVal}`;
        }
    }
}

// Example usage:
// ASSETS[0] -> '/static/icons/roaddl.png'
// ASSETS.roads['1100'] -> '/static/icons/roadud.png'
// ASSETS.semafor[33] -> '/static/icons/n2.png'


const N = 1;
const S = 2;
const W = 4;
const E = 8;


class MetropolyGame {
    constructor() {
        this.players = [];
        this.map = [];              // 2D array
        this.currentPlayer = 0;
        this.numPlayers = 0;
        this.showGrid = false;
        this.gameOver = false;
        this.turn = 0;
        
        this.state = null;
        this.isMoving = false;
        this.boardElement = document.getElementById('game-board');
        this.statusElement = document.getElementById('status-bar');

        this.dayOfWeek = 1;
        this.faza = 1; // phase
        this.auto_end_turn = false;
        this.fast_mode = false;
        this.sound_enabled = true;
        this.graphics_enabled = true;
    }

    // --- INITIALIZATION ---
    async init() {
        const response = await fetch('/api/get_state'); // Initial load
        this.state = await response.json();
        this.renderBoard();
        this.updateUI();
    }

    // --- RENDERING (Equivalent to draw_map) ---
    renderBoard() {
        this.boardElement.innerHTML = '';
        this.boardElement.style.gridTemplateColumns = `repeat(${this.state.dimx}, 32px)`;
        
        for (let y = 1; y <= this.state.dimy; y++) {
            for (let x = 1; x <= this.state.dimx; x++) {
                const tile = this.state.grid[y-1][x-1];
                const tileDiv = this.createElement('div', 'tile', `tile-${x}-${y}`);
                
                // Layer 1: Ground/Building
                const groundImg = tile.tip === 1 ? `h${tile.stage}.png` : 'h0.png';
                tileDiv.appendChild(this.createImg(groundImg, 'layer-base'));

                // Layer 2: Road (if tip is 0 or 5)
                if (tile.tip === 0 || tile.tip === 5) {
                    const roadImg = this.getRoadAsset(tile.adjacency); 
                    tileDiv.appendChild(this.createImg(roadImg, 'layer-road'));
                }

                // Layer 3: Flag (if owner > 0)
                if (tile.owner > 0) {
                    tileDiv.appendChild(this.createImg(`flag${tile.owner}.png`, 'layer-flag'));
                }

                this.boardElement.appendChild(tileDiv);
            }
        }
        this.renderPlayers();
    }

    renderPlayers() {
        // Remove old pawns
        document.querySelectorAll('.pawn').forEach(el => el.remove());

        Object.values(this.state.players).forEach(p => {
            const pawn = this.createElement('div', `pawn player-${p.id}`, `pawn-${p.id}`);
            pawn.style.backgroundColor = p.color; // Using the Long color from VB
            
            // Move pawn to specific grid coordinate
            this.movePawnToCoord(pawn, p.x, p.y);
            this.boardElement.appendChild(pawn);
        });
    }

    // --- ACTION HANDLERS (The API Calls) ---
    async rollDice() {
        if (this.isMoving) return;
        
        this.playSound('KOCKA.WAV');
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ event: 'roll' })
        });
        
        const result = await response.json();
        await this.animateDice(result.dice);
        await this.animateMovement(result.steps);
        
        if (result.action_required) {
            this.showDecisionModal(result.action_required);
        } else {
            this.showEndTurnButton();
        }
    }

    // --- ANIMATION (Equivalent to TimerSkokFigure) ---
    async animateMovement(steps) {
        this.isMoving = true;
        for (const step of steps) {
            const pawn = document.getElementById(`pawn-${this.state.curpl}`);
            this.movePawnToCoord(pawn, step.x, step.y);
            this.playSound('FIGURA.WAV');
            await this.sleep(300); // interval from VB
        }
        this.isMoving = false;
    }

    async animateDice(values) {
        const diceDiv = document.getElementById('dice-container');
        // Simple shuffle animation
        for(let i=0; i<10; i++) {
            const r1 = Math.floor(Math.random() * 6) + 1;
            const r2 = Math.floor(Math.random() * 6) + 1;
            diceDiv.innerHTML = `<img src="dice${r1}.png"><img src="dice${r2}.png">`;
            await this.sleep(50);
        }
        diceDiv.innerHTML = `<img src="dice${values[0]}.png"><img src="dice${values[1]}.png">`;
    }

    // --- MODALS (Equivalent to MsgBox / frmBuyDialog) ---
    showDecisionModal(action) {
        const modal = document.getElementById('decision-modal');
        const text = document.getElementById('modal-text');
        
        // Use the lngg lines we ported
        text.innerText = action.message; 
        modal.style.display = 'block';

        document.getElementById('btn-yes').onclick = () => this.handleDecision('yes', action);
        document.getElementById('btn-no').onclick = () => this.handleDecision('no', action);
    }

    async handleDecision(choice, actionData) {
        document.getElementById('decision-modal').style.display = 'none';
        
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                event: 'confirm_choice', 
                choice: choice,
                action_data: actionData 
            })
        });
        
        const result = await response.json();
        this.state = result.game;
        this.renderBoard(); // Refresh board to show new house/flag
        this.showEndTurnButton();
    }

    // --- HELPERS ---
    movePawnToCoord(pawn, x, y) {
        pawn.style.gridColumn = x;
        pawn.style.gridRow = y;
        // Handle VB's "nekdo_ze_stoji_tle" offset
        const others = this.countPlayersAt(x, y);
        if (others > 1) {
            pawn.style.transform = `translate(${others * 4}px, ${others * 4}px)`;
        }
    }

    sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
    
    createElement(tag, className, id) {
        const el = document.createElement(tag);
        if (className) el.className = className;
        if (id) el.id = id;
        return el;
    }

    createImg(src, className) {
        const img = document.createElement('img');
        img.src = `/static/graphics/${src}`;
        img.className = className;
        return img;
    }

    expandTerit(x, y) {
        let expanded = false;

        // helper to create a fresh land tile
        const newLandTile = () => {
            const letters = "ABCDEFGHIJKLMNOPQRSTUVWXWZ";
            const c = letters[Math.floor(Math.random() * letters.length)];
            return {
            tip: 1,
            stage: 0,
            owner: 0,
            price: c.charCodeAt(0) - 45
            };
        };

        // scroll right (x === 0)
        if (x === 0 && this.dimx < 100) {
            this.dimx++;
            expanded = true;
            this.startx++;
            this.jailx++;

            this.map.unshift([]);
            for (let j = 0; j < this.dimy; j++) {
            this.map[0][j] = newLandTile();
            }

            for (const p of this.players) {
            p.x++;
            }
        }

        // add right column
        if (x === this.dimx - 1 && this.dimx < 100) {
            this.dimx++;
            expanded = true;

            const col = [];
            for (let j = 0; j < this.dimy; j++) {
            col.push(newLandTile());
            }
            this.map.push(col);
        }

        // scroll down (y === 0)
        if (y === 0 && this.dimy < 100) {
            this.dimy++;
            expanded = true;
            this.starty++;
            this.jaily++;

            for (let i = 0; i < this.dimx; i++) {
            this.map[i].unshift(newLandTile());
            }

            for (const p of this.players) {
            p.y++;
            }
        }

        // add bottom row
        if (y === this.dimy - 1 && this.dimy < 100) {
            this.dimy++;
            expanded = true;

            for (let i = 0; i < this.dimx; i++) {
            this.map[i].push(newLandTile());
            }
        }

        if (expanded) {
            this.drawMap();
            if (this.mapEditorMode === 0) this.drawPlayers();
            if (this.showGrid) this.displayGrid();
        }

    // ------------------------
    // SAVE GAME
    // ------------------------
    saveGame(filename) {
        const state = JSON.stringify(this.to_dict());
        const saves = JSON.parse(localStorage.getItem("metropoly_saves") || "[]");

        // Overwrite if exists
        const index = saves.findIndex(f => f.name === filename);
        if (index >= 0) saves[index].data = state;
        else saves.push({ name: filename, data: state });

        localStorage.setItem("metropoly_saves", JSON.stringify(saves));
        console.log(`Game saved as ${filename}`);
    }

    // ------------------------
    // LOAD GAME
    // ------------------------
    loadGame(filename) {
        const saves = JSON.parse(localStorage.getItem("metropoly_saves") || "[]");
        const saved = saves.find(f => f.name === filename);

        if (!saved) return alert(`Save file "${filename}" not found.`);

        const data = JSON.parse(saved.data);
        this.from_dict(data);
        console.log(`Game loaded from ${filename}`);
    }

    // ------------------------
    // SAVE MAP
    // ------------------------
    saveMap(filename) {
        const mapState = JSON.stringify(this.map); // Only the map
        const maps = JSON.parse(localStorage.getItem("metropoly_maps") || "[]");

        const index = maps.findIndex(f => f.name === filename);
        if (index >= 0) maps[index].data = mapState;
        else maps.push({ name: filename, data: mapState });

        localStorage.setItem("metropoly_maps", JSON.stringify(maps));
        console.log(`Map saved as ${filename}`);
    }

    // ------------------------
    // LOAD MAP
    // ------------------------
    loadMap(filename) {
        const maps = JSON.parse(localStorage.getItem("metropoly_maps") || "[]");
        const saved = maps.find(f => f.name === filename);
        if (!saved) return alert(`Map "${filename}" not found.`);

        this.map = JSON.parse(saved.data);
        console.log(`Map loaded from ${filename}`);
    }

    // ------------------------
    // HELPER: convert current game state to a plain object
    // ------------------------
    to_dict() {
        return {
            players: this.players,
            map: this.map,
            curpl: this.curpl,
            dayOfWeek: this.dayOfWeek,
            faza: this.faza,
            auto_end_turn: this.auto_end_turn,
            fast_mode: this.fast_mode,
            show_grid: this.show_grid,
            sound_enabled: this.sound_enabled,
            graphics_enabled: this.graphics_enabled
            // add other properties as needed
        };

    // ------------------------
    // HELPER: restore game state from plain object
    // ------------------------
    from_dict(data) {
        Object.assign(this, data);
    }
    

}

// global game object
window.game = new MetropolyGame();

//const game = new MetropolyGame();
window.onload = () => game.init();


// metropoly.js

function hideLandInfo() {
    fetch("/metropoly/ui/hide-land-info", { method: "POST" })
        .then(r => r.json())
        .then(updateUI);
}

function selectTool(index) {
    fetch(`/metropoly/ui/select-tool/${index}`, { method: "POST" })
        .then(r => r.json())
        .then(updateUI);
}

// audio

// audio.js
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

const SOUND_FILES = {
    KOCKA: "/static/audio/KOCKA.WAV",
    SKOK: "/static/audio/FIGURA.WAV",   
};

const audioBuffers = {};

async function loadSounds() {
    for (const [id, url] of Object.entries(SOUND_FILES)) {
        const res = await fetch(url);
        const arrayBuffer = await res.arrayBuffer();
        audioBuffers[id] = await audioContext.decodeAudioData(arrayBuffer);
    }
}

function playSound(id, volume = 0.4) {
    const buffer = audioBuffers[id];
    if (!buffer) return;

    const source = audioContext.createBufferSource();
    const gainNode = audioContext.createGain();

    gainNode.gain.value = Math.min(volume, 0.5);

    source.buffer = buffer;
    source.connect(gainNode).connect(audioContext.destination);
    source.start(0);
}

function processAudioQueue(audioQueue) {
    audioQueue.forEach(s => {
        playSound(s.id, s.volume);
    });
}

//open save
function saveGame(slotName, gameState) {
    const payload = {
        version: 1,
        type: "game",
        timestamp: Date.now(),
        state: gameState
    };

    localStorage.setItem(
        `metropoly.save.${slotName}`,
        JSON.stringify(payload)
    );
}

function loadGame(slotName) {
    const raw = localStorage.getItem(`metropoly.save.${slotName}`);
    if (!raw) return null;

    return JSON.parse(raw);
}

function listSavedGames() {
    return Object.keys(localStorage)
        .filter(k => k.startsWith("metropoly.save."))
        .map(k => k.replace("metropoly.save.", ""));
}

let dialogMode = "open"; // "open" | "save"

function openDialog(mode) {
  dialogMode = mode;

  document.getElementById("win-dialog-title").textContent =
    mode === "save" ? "Save" : "Open";

  document.getElementById("win-filename").value =
    mode === "save" ? "game.sav" : "";

  refreshFileList();

  document.getElementById("win-dialog").classList.remove("hidden");
  document.getElementById("win-dialog-overlay").classList.remove("hidden");
}

function closeDialog() {
  document.getElementById("win-dialog").classList.add("hidden");
  document.getElementById("win-dialog-overlay").classList.add("hidden");
}

function refreshFileList() {
  const list = document.getElementById("win-file-list");
  list.innerHTML = "";

  Object.keys(localStorage)
    .filter(k => k.startsWith("metropoly.save."))
    .forEach(key => {
      const name = key.replace("metropoly.save.", "");
      const div = document.createElement("div");
      div.textContent = name;
      div.onclick = () => {
        document.getElementById("win-filename").value = name;
      };
      list.appendChild(div);
    });
}

async function confirmDialog() {
  const filename = document.getElementById("win-filename").value.trim();
  if (!filename) return;

  if (dialogMode === "save") {
    const res = await fetch("/metropoly/api/save");
    const gameState = await res.json();

    localStorage.setItem(
      `metropoly.save.${filename}`,
      JSON.stringify({
        version: 1,
        timestamp: Date.now(),
        state: gameState
      })
    );
  }

  if (dialogMode === "open") {
    const raw = localStorage.getItem(`metropoly.save.${filename}`);
    if (!raw) return;

    const payload = JSON.parse(raw);

    await fetch("/metropoly/api/load", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  }

  closeDialog();
  location.reload(); // simplest for now
}

// ---------------------------
// Menu buttons bindings
// ---------------------------

document.addEventListener("DOMContentLoaded", () => {
    // Assuming you have Win95-style menu items like <button id="menu-save-btn">Save</button>
    const saveBtn = document.getElementById("menu-save-btn");
    const openBtn = document.getElementById("menu-open-btn");

    if (saveBtn) {
        saveBtn.addEventListener("click", () => {
            saveGameDialog(); // calls wire.js save
        });
    }

    if (openBtn) {
        openBtn.addEventListener("click", () => {
            openGameDialog(); // calls wire.js open
        });
    }
});


// metropoly/metropoly.js

document.addEventListener('keydown', function(event) {
    // If the user is typing in an input box, don't trigger shortcuts
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
    }

    const key = event.key.toLowerCase();
    const shortcuts = game.state.shortcuts; // [r, s, e, o, space]


    if (game.state.clkMode === 33) {
        // Handle map editing (placing roads/buildings with the current tool)
        handleEditorClick(x, y);
    }

    // 1. Build Road
    if (key === shortcuts[0]) {
        console.log("Shortcut: Build Road");
        game.setClickMode(2); // Equivalent to clkMode = 2
    }
    // 2. Sell
    else if (key === shortcuts[1]) {
        console.log("Shortcut: Sell Mode");
        game.setClickMode(1); // Equivalent to clkMode = 1
    }
    // 3. Create Semaphore
    else if (key === shortcuts[2]) {
        game.setClickMode(3); // Equivalent to clkMode = 3
    }
    // 4. Rotate Semaphores
    else if (key === shortcuts[3]) {
        game.rotateSemaphores(); // API call to your turn_semaphores route
    }
    // 5. End Turn (Commonly the Space bar)
    else if (key === shortcuts[4] || (shortcuts[4] === ' ' && event.code === 'Space')) {
        // Prevent page from scrolling down when pressing space
        event.preventDefault(); 
        game.endTurn();
    }
    
});

// Helper to update the UI when mode changes
MetropolyGame.prototype.setClickMode = function(mode) {
    this.state.clkMode = mode;
    this.updateCursor(); // Change cursor to show building/selling
    this.statusElement.innerText = "Mode changed..."; 
};

// -----------------------------
// Map Editor Menu Actions
// -----------------------------

// Save Map menu
function mnuSaveMap_Click() {
    // Open save dialog for maps (mode "save_map")
    openDialog('save_map');          // reuse our existing dialog code
    document.getElementById('win-filename').value = 'my.map'; // default filename

    // Refresh map editor file list if present
    const fileList = document.getElementById('win-file-list');
    if (fileList) refreshFileList(); // repopulate file list

    // Optional: refresh any other editor UI
    if (window.frmMapEditor && frmMapEditor.File1) frmMapEditor.File1.refresh();
    if (window.NewGame && NewGame.File1) {
        NewGame.File1.refresh();
        if (typeof NewGame.fill_combo === 'function') NewGame.fill_combo();
    }
}

// Exit Map Editor menu
function mnuExitMapEditor_Click() {
    end_map_editor(); // call your map editor cleanup function
}

// -----------------------------
// Bind menu buttons (if using HTML buttons)
// -----------------------------
document.addEventListener('DOMContentLoaded', () => {
    const saveMapBtn = document.getElementById('menu-save-map-btn');
    const exitMapBtn = document.getElementById('menu-exit-map-btn');

    if (saveMapBtn) saveMapBtn.addEventListener('click', mnuSaveMap_Click);
    if (exitMapBtn) exitMapBtn.addEventListener('click', mnuExitMapEditor_Click);
});

// metropoly.js

MetropolyGame.prototype.toggleEditorUI = function(active) {
    const container = document.getElementById('metropoly-app');
    
    if (active) {
        // Equivalent to begin_map_editor visual changes
        container.classList.add('mode-editor');
        this.hidePawns(true);
        this.statusElement.innerText = "Map Editor Active";
    } else {
        // Equivalent to end_map_editor visual changes
        container.classList.remove('mode-editor');
        this.hidePawns(false);
    }
};

MetropolyGame.prototype.hidePawns = function(hide) {
    document.querySelectorAll('.pawn').forEach(p => {
        p.style.display = hide ? 'none' : 'block';
    });
};

// Example of an API call to start editing
async function startEditing() {
    const response = await fetch('/api/editor/begin', { method: 'POST' });
    const newState = await response.json();
    game.state = newState;
    game.toggleEditorUI(true);
}


// metropoly.js

async function handleNewGameSubmit() {
    const payload = {
        map_name: document.getElementById('map-select').value,
        x: document.getElementById('input-x').value,
        y: document.getElementById('input-y').value
    };

    const response = await fetch('/metropoly/api/game/new', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (data.success) {
        // Equivalent to Me.Hide and draw_map
        document.getElementById('new-game-modal').style.display = 'none';
        game.state = data.game;
        game.renderBoard();
        game.updateUI();
        console.log("New game started!");
    }
}