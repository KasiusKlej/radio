// static/metropoly/js/wire.js
// ---------------------------
// Wire.js: Connects MetropolyGame engine to the UI

// 1️⃣ Initialize global game
window.game = new MetropolyGame();

// 2️⃣ Cache DOM elements
const board = document.getElementById("game-board");
const btnRoll = document.getElementById("btn-roll");
const btnEndTurn = document.getElementById("btn-end-turn");

const modal = document.getElementById("decision-modal");
const modalText = document.getElementById("modal-text");
const btnYes = document.getElementById("btn-yes");
const btnNo = document.getElementById("btn-no");

const dialogOverlay = document.getElementById("win-dialog-overlay");
const dialogWindow = document.getElementById("win-dialog");
const dialogTitle = document.getElementById("win-dialog-title");
const filenameInput = document.getElementById("win-filename");
const fileList = document.getElementById("win-file-list");

// Dialog state
let currentDialogMode = null; // 'save', 'open', 'save_map'
let dialogCallback = null;

// ---------------------------
// UI RENDERING
// ---------------------------
function renderBoard() {
    board.innerHTML = "";
    const tiles = game.getBoardTiles();

    tiles.forEach(tile => {
        const div = document.createElement("div");
        div.className = "tile";
        div.style.gridColumn = tile.col;
        div.style.gridRow = tile.row;

        // Layers
        ["baseImg", "roadImg", "buildingImg", "flagImg"].forEach(layer => {
            if (tile[layer]) {
                const img = document.createElement("img");
                img.src = tile[layer];
                img.className = "layer-" + layer.replace("Img", "");
                div.appendChild(img);
            }
        });

        // Pawns
        tile.players.forEach((p, i) => {
            const pawn = document.createElement("img");
            pawn.src = p.img;
            pawn.className = `pawn pawn-offset-${i}`;
            div.appendChild(pawn);
        });

        board.appendChild(div);
    });
}

function updateSidebar() {
    const diceContainer = document.getElementById("dice-container");
    diceContainer.innerHTML = "";
    game.dice.forEach(d => {
        const dieImg = document.createElement("img");
        dieImg.src = `static/metropoly/assets/graphics/dice${d}.png`;
        dieImg.className = "die";
        diceContainer.appendChild(dieImg);
    });

    document.getElementById("status-text").textContent = game.getStatusText();
    btnEndTurn.style.display = game.canEndTurn() ? "inline-block" : "none";
}

// ---------------------------
// MODAL HANDLERS
// ---------------------------
function showModal(text, callbackYes, callbackNo) {
    modalText.textContent = text;
    modal.style.display = "block";
    modal.callbackYes = callbackYes;
    modal.callbackNo = callbackNo;
}

function hideModal() {
    modal.style.display = "none";
    modal.callbackYes = null;
    modal.callbackNo = null;
}

btnYes.addEventListener("click", () => { if (modal.callbackYes) modal.callbackYes(); hideModal(); });
btnNo.addEventListener("click", () => { if (modal.callbackNo) modal.callbackNo(); hideModal(); });

// ---------------------------
// WIN95 DIALOG HANDLERS
// ---------------------------
function showDialog(mode, callback) {
    currentDialogMode = mode;
    dialogCallback = callback;

    dialogTitle.textContent = mode === "save" ? "Save Game" :
                              mode === "open" ? "Open Game" :
                              mode === "save_map" ? "Save Map" : "Dialog";

    filenameInput.value = "";
    populateFileList(mode);

    dialogOverlay.classList.remove("hidden");
    dialogWindow.classList.remove("hidden");
}

function closeDialog() {
    dialogOverlay.classList.add("hidden");
    dialogWindow.classList.add("hidden");
    currentDialogMode = null;
    dialogCallback = null;
}

function populateFileList(mode) {
    fileList.innerHTML = "";
    const storageKey = mode === "save_map" ? "metropoly_maps" : "metropoly_saves";
    const files = JSON.parse(localStorage.getItem(storageKey) || "[]");

    files.forEach(f => {
        const li = document.createElement("div");
        li.textContent = f;
        li.className = "win-file-item";
        li.onclick = () => { filenameInput.value = f; };
        li.addEventListener("dblclick", () => confirmDialog());
        fileList.appendChild(li);
    });
}

function confirmDialog() {
    const filename = filenameInput.value.trim();
    if (!filename) return alert("Please enter a file name.");

    switch (currentDialogMode) {
        case "save":
            game.saveGame(filename);
            break;
        case "open":
            game.loadGame(filename);
            break;
        case "save_map":
            game.saveMap(filename);
            break;
        default:
            console.error("Unknown dialog mode:", currentDialogMode);
    }

    if (dialogCallback) dialogCallback(filename);
    closeDialog();
}

// Attach buttons in dialog
document.querySelectorAll("#win-dialog .win-buttons button").forEach(btn => {
    if (btn.textContent === "OK") btn.onclick = confirmDialog;
    else btn.onclick = closeDialog;
});

// Enable click + double-click on file items
fileList.addEventListener("click", e => {
    if (e.target.classList.contains("win-file-item")) {
        fileList.querySelectorAll(".win-file-item").forEach(li => li.classList.remove("selected"));
        e.target.classList.add("selected");
        filenameInput.value = e.target.textContent;
    }
});
fileList.addEventListener("dblclick", e => {
    if (e.target.classList.contains("win-file-item")) {
        filenameInput.value = e.target.textContent;
        confirmDialog();
    }
});

// ---------------------------
// MENU FUNCTIONS
// ---------------------------
function openGameDialog() { showDialog("open"); }
function saveGameDialog() { showDialog("save"); }
function saveMapDialog() { showDialog("save_map"); }

// ---------------------------
// EVENT BINDINGS
// ---------------------------
btnRoll.addEventListener("click", () => { game.rollDice(); renderBoard(); updateSidebar(); });
btnEndTurn.addEventListener("click", () => { game.endTurn(); renderBoard(); updateSidebar(); });

// ---------------------------
// INITIALIZE UI
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    renderBoard();
    updateSidebar();
    console.log("Wire.js connected. Metropoly ready.");
});

// ---------------------------
// EXPORT FUNCTIONS
// ---------------------------
export { openGameDialog, saveGameDialog, saveMapDialog, showDialog, confirmDialog, closeDialog };
