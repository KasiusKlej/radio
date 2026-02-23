/**
 * METROPOLY.JS
 * Consolidated Game Engine and UI Bridge
 */

/* =========================================================
 * 1. CONFIGURATION & RESOURCE LOADING
 * ======================================================= */


// const BASE_GFX = "/metropoly/assets/graphics/"; // Matches Blueprint static_url_path
// const BASE_SOUND = "/metropoly/assets/sound/";





// 🩹 UPDATE THESE to include the physical 'assets' folder:
const BASE_GFX   = "/metropoly/metro_static/assets/graphics/"; 
const BASE_SOUND = "/metropoly/metro_static/assets/sound/";










const ASSET_MAP = {
    roads: {
        "1100": "roadud.png", "0011": "roadlr.png", "0110": "roaddl.png",
        "0101": "roaddr.png", "1010": "roadul.png", "1001": "roadur.png",
        "0111": "road3s.png", "1011": "road3n.png", "1101": "road3e.png",
        "1110": "road3w.png", "1111": "road4.png"
    }
};

const Resources = {
    players: {}, tiles: {}, roads: {}, flags: {}, dice: {}, sounds: {}
};

async function loadImage(path) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = () => {
            console.warn("Failed to load image:", path);
            resolve(null);
        };
        img.src = path;
    });
}

/* =========================================================
 * 2. THE GAME ENGINE CLASS
 * ======================================================= */
class MetropolyGame {
    constructor() {
        this.state = window.INITIAL_STATE || {};
        this.isMoving = false;
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        this.audioBuffers = {};
    }

    async init() {
        console.log("⚓ Engine Starting...");
        // Load basic icons
        for (let i = 1; i <= 7; i++) {
            Resources.players[i] = await loadImage(`${BASE_GFX}p${i}.png`);
            Resources.flags[i] = await loadImage(`${BASE_GFX}flag${i}.png`);
        }
        for (let i = 0; i <= 5; i++) Resources.tiles[i] = await loadImage(`${BASE_GFX}h${i}.png`);
        
        Resources.tiles.school = await loadImage(`${BASE_GFX}school.png`);
        Resources.tiles.job = await loadImage(`${BASE_GFX}job.png`);
        Resources.tiles.jail = await loadImage(`${BASE_GFX}jail.png`);

        await this.loadSounds();
        this.renderBoard();
        this.updateUI();
    }

    renderBoard() {
        const board = document.getElementById("game-board");
        if (!board || !this.state.grid) return;

        board.innerHTML = "";
        board.style.display = "grid";
        board.style.gridTemplateColumns = `repeat(${this.state.dimx}, 32px)`;

        this.state.grid.forEach(row => {
            row.forEach(tile => {
                const div = document.createElement("div");
                div.className = "tile";
                div.style.gridColumn = tile.x;
                div.style.gridRow = tile.y;
                div.onclick = () => window.handleTileClick(tile.x, tile.y);

                // Layer 1: Base
                const base = document.createElement("img");
                base.src = `${BASE_GFX}h${tile.stage}.png`;
                base.className = "layer-base";
                div.appendChild(base);

                // Layer 2: Roads/Special
                if (tile.tip === 0 && tile.road_visual_id !== undefined) {
                    const road = document.createElement("img");
                    road.src = `${BASE_GFX}img${tile.road_visual_id}.png`;
                    road.className = "layer-road";
                    div.appendChild(road);
                }
                if (tile.tip === 2) this.addOverlay(div, "school.png");
                if (tile.tip === 3) this.addOverlay(div, "job.png");
                if (tile.tip === 4) this.addOverlay(div, "jail.png");

                // Layer 3: Flags
                if (tile.owner > 0) {
                    const flag = document.createElement("img");
                    flag.src = `${BASE_GFX}flag${tile.owner}.png`;
                    flag.className = "layer-flag";
                    div.appendChild(flag);
                }
                board.appendChild(div);
            });
        });
        this.renderPlayers();
    }

    addOverlay(parent, className, filename) {
        const img = document.createElement('img');
        // 🩹 FIX: Use BASE_GFX instead of a hardcoded string
        img.src = BASE_GFX + filename; 
        img.className = className;
        parent.appendChild(img);
    }

    // renderPlayers() {
    //     document.querySelectorAll('.pawn').forEach(p => p.remove());
    //     if (!this.state.players) return;
    //     Object.values(this.state.players).forEach(p => {
    //         const img = document.createElement("img");
    //         img.src = `${BASE_GFX}p${p.id}.png`;
    //         img.className = `pawn pawn-offset-${p.id}`;
    //         img.style.gridColumn = p.x;
    //         img.style.gridRow = p.y;
    //         document.getElementById("game-board").appendChild(img);
    //     });
    // }

    renderPlayers() {
        document.querySelectorAll(".pawn").forEach(p => p.remove());
        
        const players = Object.values(this.state.players || {});
        players.forEach(p => {
            // 🩹 Defensive check:
            if (p && p.id && Resources.players[p.id]) {
                const pawn = document.createElement("img");
                pawn.className = `pawn pawn-offset-${p.id}`;
                pawn.src = Resources.players[p.id].src;
                pawn.style.gridColumn = p.x;
                pawn.style.gridRow = p.y;
                this.boardEl.appendChild(pawn);
            } else {
                console.warn(`⚓ Pawn Error: Player ${p.id} exists but graphic is missing.`);
            }
        });
    }

    updateUI() {
        const status = document.getElementById("status-text");
        if (status) status.innerText = this.state.status_label || "Ready";
        const endBtn = document.getElementById("btn-end-turn");
        if (endBtn) endBtn.classList.toggle("hidden", this.state.faza !== 4);
    }

    async loadSounds() {
        const sounds = { KOCKA: 'KOCKA.WAV', FIGURA: 'FIGURA.WAV' };
        for (const [id, file] of Object.entries(sounds)) {
            try {
                const r = await fetch(BASE_SOUND + file);
                const b = await r.arrayBuffer();
                this.audioBuffers[id] = await this.audioCtx.decodeAudioData(b);
            } catch (e) { console.warn("Sound error:", file); }
        }
    }

    execSviraj(id) {
        const buf = this.audioBuffers[id.split('.')[0].toUpperCase()];
        if (!buf) return;
        const src = this.audioCtx.createBufferSource();
        src.buffer = buf;
        src.connect(this.audioCtx.destination);
        src.start();
    }

    renderTile(tile) {
        const el = document.createElement("div");
        el.className = "tile";
        el.style.gridColumn = tile.x;
        el.style.gridRow = tile.y;

        // 1. Base Ground/Building
        this.addImg(el, Resources.tiles[tile.stage ?? 0], "layer-base");

        // 2. Road Logic - FIX: Use 'visual_id' to match Python Tile class
        // Also, Roads (0-10) are stored in Resources.tiles, not Resources.roads
        if (tile.tip === 0 && tile.visual_id !== undefined) {
            this.addImg(el, Resources.tiles[tile.visual_id], "layer-road");
        }

        // 3. Special Tiles
        if (tile.tip === 2) this.addImg(el, Resources.tiles.school, "layer-special");
        if (tile.tip === 3) this.addImg(el, Resources.tiles.job,    "layer-special");
        if (tile.tip === 4) this.addImg(el, Resources.tiles.jail,   "layer-special");

        // 4. Flags
        if (tile.owner > 0) {
            this.addImg(el, Resources.flags[tile.owner], "layer-flag");
        }

        this.boardEl.appendChild(el);
    }

    addImg(parent, imgObj, cls) {
        // 🩹 THE SHIELD: If the image object is missing, stop here!
        if (!imgObj || !imgObj.src) {
            // This prevents the browser from ever asking for "/graphics/undefined"
            return; 
        }
        
        const img = document.createElement("img");
        img.src = imgObj.src;
        img.className = cls;
        parent.appendChild(img);
    }

}

/* =========================================================
 * 3. GLOBAL MENU & BRIDGE FUNCTIONS (Fixes 'Undefined' errors)
 * ======================================================= */

window.game = new MetropolyGame();

window.exitGame = function() {
    console.log("🚪 Exiting...");
    window.location.href = "/metropoly/exit";
};

window.newGame = function() {
    document.getElementById('new-game-modal')?.classList.remove('hidden');
};

window.openMapEditor = async function() {
    const res = await fetch("/metropoly/api/editor/begin", { method: "POST" });
    const data = await res.json();
    if (data.success) {
        window.game.state = data.game;
        document.getElementById('map-editor-modal')?.classList.remove('hidden');
        window.game.updateUI();
    }
};

window.endTurn = async function() {
    const res = await fetch("/metropoly/api/end_turn", { method: "POST" });
    const data = await res.json();
    if (data.success) {
        window.game.state = data.game;
        window.game.renderBoard();
        window.game.updateUI();
    }
};

window.handleTileClick = async function(x, y) {
    const res = await fetch("/metropoly/api/map_click", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ x: x, y: y })
    });
    const data = await res.json();
    window.game.state = data.game;
    window.game.renderBoard();
    window.game.updateUI();
};

window.showAbout = () => document.getElementById('about-modal')?.classList.remove('hidden');
window.closeAbout = () => document.getElementById('about-modal')?.classList.add('hidden');
window.showContents = () => document.getElementById('help-modal')?.classList.remove('hidden');
window.closeHelp = () => document.getElementById('help-modal')?.classList.add('hidden');

/* =========================================================
 * 4. EVENT BINDINGS & INITIALIZATION
 * ======================================================= */

window.onload = async () => {
    await window.game.init();

    // Bind non-menu buttons
    document.getElementById("btn-roll")?.addEventListener("click", async () => {
        const res = await fetch("/metropoly/api/roll", { method: "POST" });
        const data = await res.json();
        if (data.steps) {
            window.game.execSviraj("KOCKA.WAV");
            for (const step of data.steps) {
                window.game.state.players[window.game.state.curpl].x = step.x;
                window.game.state.players[window.game.state.curpl].y = step.y;
                window.game.execSviraj("FIGURA.WAV");
                window.game.renderPlayers();
                await new Promise(r => setTimeout(r, 300));
            }
        }
        window.game.state = data.game;
        window.game.renderBoard();
        window.game.updateUI();
    });

    document.getElementById("btn-end-turn")?.addEventListener("click", window.endTurn);

    // Key Shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT') return;
        const key = e.key.toLowerCase();
        const s = window.game.state.shortcuts || [];
        if (key === s[4] || (s[4] === ' ' && e.code === 'Space')) {
            e.preventDefault();
            window.endTurn();
        }
    });
};

// Step 1: Open the Setup Dialog (what you currently have)
window.openMapEditor = function() {
    document.getElementById('map-editor-modal').classList.remove('hidden');
};

// Step 2: User clicks OK on Setup -> Show the Toolbar & enable Mode 33
window.confirmEditorSetup = async function() {
    const x = document.getElementById('editor-new-x').value;
    const y = document.getElementById('editor-new-y').value;
    const map = document.getElementById('editor-map-combo').value;

    // Call Python to set clkMode = 33 (Map Editor)
    const res = await fetch("/metropoly/api/editor/begin", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ x: x, y: y, map: map })
    });
    
    const data = await res.json();
    if (data.success) {
        window.game.state = data.game;
        // Close setup box
        document.getElementById('map-editor-modal').classList.add('hidden');
        // Show the Toolbar
        document.getElementById('map-editor-tools').classList.remove('hidden');
        // Redraw map with grid lines
        window.game.renderBoard();
        console.log("⚓ Map Editor Toolbar Active.");
    }
};

// Step 3: Handle Tool Selection
window.selectEditorTool = function(toolId, element) {
    // Replicates OptionSelectedTool(Index).Value = True
    window.game.state.mapCurrentTool = toolId;
    
    // UI Visual: remove 'active' from all, add to this one
    document.querySelectorAll('.tool-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    
    window.game.execSviraj('FIGURA.WAV'); // Tick sound
};

// Step 4: Handle the Menu command "Exit Map Editor"
window.exitMapEditor = async function() {
    const res = await fetch("/metropoly/api/editor/end", { method: "POST" });
    const data = await res.json();
    if (data.success) {
        window.game.state = data.game;
        document.getElementById('map-editor-tools').classList.add('hidden');
        window.game.renderBoard();
        window.game.updateUI();
        console.log("🚪 Map Editor Closed.");
    }
};

window.saveMapDialog = function() {
    // 1. Set the Caption from lngg(58) - handled via Python state
    document.getElementById('open-save-title').innerText = window.game.state.lang_dict.menu.save_map || "Save Map";
    
    // 2. Set default filename
    document.getElementById('os-filename').value = "my.map";
    
    // 3. Mark the OK button with a special 'mode' attribute
    const okBtn = document.getElementById('os-ok-btn');
    okBtn.innerText = "Save";
    okBtn.onclick = window.confirmSaveMap; // Custom handler for map saving
    
    document.getElementById('open-save-modal').classList.remove('hidden');
};

window.confirmSaveMap = async function() {
    const filename = document.getElementById('os-filename').value;
    if (!filename) return alert("Please enter a name.");

    const res = await fetch("/metropoly/api/save_map", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ filename: filename })
    });

    const data = await res.json();
    if (data.success) {
        window.game.state = data.game;
        window.closeOpenSave();
        console.log("⚓ Map saved and map list refreshed.");
    }
};

