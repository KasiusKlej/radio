//cardgame.js
//Rendering faithfully what backend says
//Providing visible cues
//Handling clicks

let selectedCard = null;
let currentGameId = null; // initialized from HTML

document.addEventListener("DOMContentLoaded", () => {
    const gameTable = document.getElementById("game-table");
    currentGameId = gameTable.dataset.gameId;
    console.log("cardgame.js loaded, game ID:", currentGameId);

    // --- Render initial layout ---
    if (typeof initialGameState !== "undefined") {
        renderGame(initialGameState);
    }

    // --- CARD CLICK ---
    document.body.addEventListener("click", (e) => {
        const card = e.target.closest(".card");
        if (!card) return;

        // STOP bubbling to columns
        e.stopPropagation();

        if (selectedCard) selectedCard.classList.remove("selected");

        selectedCard = card;
        card.classList.add("selected");

        console.log("CARD SELECTED", card.dataset.card);
    });

    // --- COLUMN CLICK (event delegation) ---
    document.body.addEventListener("click", (e) => {
        const column = e.target.closest(".column");
        if (!column) return;

        console.log("COLUMN CLICKED", column.dataset.column);

        if (!selectedCard) return console.log("No card selected");

        const payload = {
            game_id: currentGameId,
            card_code: selectedCard.dataset.card,
            from_column: selectedCard.dataset.column,
            to_column: column.dataset.column
        };

        console.log("SENDING MOVE", payload);

        fetch("/cardgames/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log("Move succeeded");
                selectedCard = null;
                renderGame(data.game);
            } else {
                console.log("Invalid move");
                if (selectedCard) selectedCard.classList.remove("selected");
                selectedCard = null;
            }
        })
        .catch(err => console.error("Move error", err));
    });
});

// --- RENDER FUNCTION (VB-AUTHORITATIVE, SCROLL-SAFE ABSOLUTE GEOMETRY) ---
function renderGame(gameState) {
    const gameTable = document.getElementById("game-table");
    const FAN_SCALE = 0.6;   // modern-era correction (VB was tighter)

    if (!gameTable) return;

    gameTable.innerHTML = "";
    gameTable.style.position = "relative";

    const columns = gameState.columns || {};
    const TABLE_INSET = 6;

    // 🔒 Track table extents (flat table, real edges)
    let maxX = 0;
    let maxY = 0;

    Object.entries(columns).forEach(([colId, col]) => {
        if (typeof col.x !== "number" || typeof col.y !== "number") return;

        const colDiv = document.createElement("div");
        colDiv.className = "column";
        colDiv.dataset.column = colId;

        colDiv.style.position = "absolute";
        colDiv.style.left = `${col.x}px`;
        colDiv.style.top  = `${col.y}px`;

        // ---- Base Z-layer (column) ----
        let baseZ = 10;
        if (!Array.isArray(col.cards) || col.cards.length === 0) baseZ = 0;

        colDiv.style.zIndex = baseZ;

        // ---- Placeholder ----
        if (!Array.isArray(col.cards) || col.cards.length === 0) {
            colDiv.classList.add("empty-column");
        }

        // ---- Cards ----
        let colMaxX = col.x;
        let colMaxY = col.y;

        if (Array.isArray(col.cards)) {
            // Sacred overlap vector (renderer only)
            let ox = Number(col.overlap_x || 0);
            let oy = Number(col.overlap_y || 0);

            // Safety
            ox = Number.isFinite(ox) ? ox * FAN_SCALE : 0;
            oy = Number.isFinite(oy) ? oy * FAN_SCALE : 0;

            col.cards.forEach((card, idx) => {
                const img = document.createElement("img");
                img.className = "card";

                img.src = card.face_up
                    ? `/static/cards/${card.image}`
                    : `/static/cards/1024x768face.bmp`;

                img.style.position = "absolute";
                img.style.left = `${idx * ox}px`;
                img.style.top  = `${idx * oy}px`;
                img.style.zIndex = baseZ + idx + 1;

                colDiv.appendChild(img);

                // Track extents (card size is fixed)
                colMaxX = Math.max(colMaxX, col.x + idx * ox + 90);
                colMaxY = Math.max(colMaxY, col.y + idx * oy + 140);
            });
        }

        // Update table extents
        maxX = Math.max(maxX, colMaxX);
        maxY = Math.max(maxY, colMaxY);

        gameTable.appendChild(colDiv);
    });

    // 🔒 FORCE TABLE SIZE (FLAT WORLD, NOT EARTH)
    gameTable.style.width  = `${maxX + TABLE_INSET}px`;
    gameTable.style.height = `${maxY + TABLE_INSET}px`;
}


/* ============================================================
   Card Games – Frontend Theatre Director
   Implements:
   6. Animation pipeline
   7. Safe diff animation
   8. Face-up / face-down transitions
   9. Z-order discipline
  10. Debug overlays
   ============================================================ */

const DEBUG = true;

const table = document.getElementById("table");

/* ---------- STATE ---------- */

let prevSnapshot = null;
const cardElements = {};   // cardId -> DOM element

/* ---------- ENTRY POINT ---------- */

document.addEventListener("DOMContentLoaded", () => {
    if (window.INITIAL_GAME_STATE) {
        onEngineUpdate(window.INITIAL_GAME_STATE);
    }
});

/* ---------- ENGINE UPDATE ---------- */

function onEngineUpdate(newSnapshot) {
    if (!prevSnapshot) {
        renderImmediately(newSnapshot);
    } else {
        animateDiff(prevSnapshot, newSnapshot);
    }
    prevSnapshot = newSnapshot;
}

/* ---------- SNAPSHOT INDEXING ---------- */

function indexCards(snapshot) {
    const map = {};
    snapshot.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            map[card.code] = {
                col,
                index,
                card
            };
        });
    });
    return map;
}

/* ---------- POSITION COMPUTATION ---------- */

function computeCardPosition(col, index) {
    const baseX = col.custom_x !== -1 ? col.custom_x : window.columnX[col.position];
    const baseY = col.custom_y !== -1 ? col.custom_y : window.columnY[col.position];

    return {
        x: baseX + col.overlap_x * index,
        y: baseY + col.overlap_y * index,
        z: index
    };
}

/* ---------- INITIAL RENDER ---------- */

function renderImmediately(snapshot) {
    table.innerHTML = "";
    snapshot.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            spawnCard(card, col, index, false);
        });
    });

    if (DEBUG) drawDebug(snapshot);
}

/* ---------- DIFF ANIMATION ---------- */

function animateDiff(prev, next) {
    const prevIndex = indexCards(prev);
    const nextIndex = indexCards(next);

    for (const cardId in nextIndex) {
        const prevEntry = prevIndex[cardId];
        const nextEntry = nextIndex[cardId];

        if (!prevEntry) {
            spawnCard(nextEntry.card, nextEntry.col, nextEntry.index, true);
        } else {
            const moved =
                prevEntry.col.cId !== nextEntry.col.cId ||
                prevEntry.index !== nextEntry.index;

            if (moved) {
                animateMove(cardId, prevEntry, nextEntry);
            }

            if (prevEntry.card.face_up !== nextEntry.card.face_up) {
                flipCard(cardId, nextEntry.card.face_up);
            }
        }
    }

    if (DEBUG) drawDebug(next);
}

/* ---------- CARD CREATION ---------- */

function spawnCard(card, col, index, animate) {
    const el = document.createElement("div");
    el.className = "card";
    el.dataset.cardId = card.code;
    el.textContent = DEBUG ? card.code : "";

    table.appendChild(el);
    cardElements[card.code] = el;

    const pos = computeCardPosition(col, index);
    placeCard(el, pos, !animate);

    if (animate) {
        el.style.opacity = "0";
        requestAnimationFrame(() => {
            el.style.transition = "all 0.4s ease";
            el.style.opacity = "1";
        });
    }

    setFace(el, card.face_up);
}

/* ---------- MOVEMENT ---------- */

function animateMove(cardId, from, to) {
    const el = cardElements[cardId];
    if (!el) return;

    const toPos = computeCardPosition(to.col, to.index);

    el.style.zIndex = 1000; // lift during move
    el.style.transition = "all 0.35s ease";

    requestAnimationFrame(() => {
        el.style.left = `${toPos.x}px`;
        el.style.top = `${toPos.y}px`;
    });

    el.addEventListener("transitionend", () => {
        el.style.zIndex = toPos.z;
    }, { once: true });
}

/* ---------- FLIP ---------- */

function flipCard(cardId, faceUp) {
    const el = cardElements[cardId];
    if (!el) return;

    el.classList.add("flipping");
    setTimeout(() => {
        setFace(el, faceUp);
        el.classList.remove("flipping");
    }, 150);
}

function setFace(el, faceUp) {
    el.classList.toggle("face-down", !faceUp);
}

/* ---------- PLACEMENT ---------- */

function placeCard(el, pos, immediate) {
    if (immediate) el.style.transition = "none";

    el.style.left = `${pos.x}px`;
    el.style.top = `${pos.y}px`;
    el.style.zIndex = pos.z;

    if (immediate) {
        requestAnimationFrame(() => {
            el.style.transition = "";
        });
    }
}

/* ---------- DEBUG ---------- */

function drawDebug(snapshot) {
    console.clear();
    snapshot.kup.forEach((col, i) => {
        console.log(
            `Col ${i} (${col.column_name}):`,
            col.cards.map(c => c.code)
        );
    });
}



const autoplayItem = document.getElementById("menu-autoplay");

autoplayItem.addEventListener("click", () => {
    autoplayItem.classList.toggle("checked");

    const enabled = autoplayItem.classList.contains("checked");

    fetch("/api/options/autoplay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled })
    });
});


document.getElementById("menu-autoplay")?.addEventListener("click", function () {
    this.classList.toggle("checked");
    const enabled = this.classList.contains("checked");

    fetch("/api/options/autoplay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled })
    });
});
