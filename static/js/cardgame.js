/* ============================================================
   Card Games – Frontend Theatre Director
   ============================================================ */

let prevSnapshot = null;
const cardElements = {}; // Map of cardCode -> DOM Element

document.addEventListener("DOMContentLoaded", () => {
    // --- 1. INITIAL LOAD ---
    if (window.INITIAL_GAME_STATE) {
        onEngineUpdate(window.INITIAL_GAME_STATE);
    }

    // --- 2. THE UNIFIED CLICK HANDLER (Single Click) ---
    // Handles: Selecting a card, moving to a column, or clicking the deck.
    document.addEventListener("click", (e) => {
        const cardEl = e.target.closest(".card");
        const colEl = e.target.closest(".column");

        // If user didn't click a card or a column, ignore.
        if (!colEl && !cardEl) return;

        // Extract IDs
        // If we clicked a card, we use its code. If we clicked a column, code is null.
        const colIdx = colEl ? colEl.dataset.columnId : null;
        const cardCode = cardEl ? cardEl.dataset.cardId : null;

        if (colIdx !== null) {
            handleEngineAction("/cardgames/api/click", {
                col_idx: colIdx,
                card_code: cardCode
            });
        }
    });

    // --- 3. DOUBLE CLICK HANDLER ---
    // Intercepts "Fast Move" wishes.
    document.addEventListener("dblclick", (e) => {
        const cardEl = e.target.closest(".card");
        if (!cardEl) return;

        handleEngineAction("/cardgames/api/double_click", {
            card_code: cardEl.dataset.cardId
        });
    });
});

/**
 * Communicates with the Python Engine and updates the "Theatre" (UI)
 */
function handleEngineAction(url, payload) {
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success || data.ok) {
            onEngineUpdate(data.game);
        } else if (data.error) {
            console.error("Engine Error:", data.error);
        }
    })
    .catch(err => console.error("Network Error:", err));
}

/* ---------- THEATRE UPDATES (Rendering & Animation) ---------- */

function onEngineUpdate(newSnapshot) {
    if (!newSnapshot) return;

    if (!prevSnapshot) {
        renderImmediately(newSnapshot);
    } else {
        animateDiff(prevSnapshot, newSnapshot);
    }
    
    // Update global state tracking
    prevSnapshot = newSnapshot;
    
    // Sync UI selection highlight based on what the Backend says
    updateSelectionUI(newSnapshot);
}

/**
 * Highlights the card that the BACKEND considers selected.
 */
function updateSelectionUI(snapshot) {
    // Remove all existing selections
    document.querySelectorAll(".card.selected").forEach(el => el.classList.remove("selected"));
    
    // If the engine says a card is selected, find it and highlight it
    if (snapshot.selected_card_code) {
        const el = cardElements[snapshot.selected_card_code];
        if (el) el.classList.add("selected");
    }
}


// ============================================================
//  FIXED: renderImmediately + createCardElement
//
//  Problems fixed:
//  1. Old rendering block (sections 1, 2, 3) removed — it was
//     drawing every card directly on #game-table with absolute
//     coords, then the new loop drew them again inside column divs.
//  2. Cards inside a .column div must use RELATIVE coordinates
//     (just index * overlap), because the column div is already
//     absolutely positioned at col.x / col.y.
//  3. createCardElement now takes a `relative` param (default false)
//     so animateDiff keeps using absolute coords on #game-table,
//     while renderImmediately uses relative coords inside columns.
// ============================================================

function createCardElement(card, col, index, relative = false) {
    const el = document.createElement("div");
    el.className = `card ${card.face_up ? 'face-up' : 'face-down'}`;
    el.dataset.cardId = card.code;

    const ox = Number(col.overlap_x) || 0;
    const oy = Number(col.overlap_y) || 0;

    let finalX, finalY;
    if (relative) {
        // Card is a child of its column div — position relative to it
        finalX = index * ox;
        finalY = index * oy;
    } else {
        // Card is a direct child of #game-table — use absolute table coords
        finalX = Number(col.x) + (index * ox);
        finalY = Number(col.y) + (index * oy);
    }

    el.style.left   = `${finalX}px`;
    el.style.top    = `${finalY}px`;
    el.style.zIndex = 100 + index;

    const ext = ".png";
    const imgName = (card.face_up === true || card.face_up === 1)
        ? `1024x768${card.code}${ext}`
        : `1024x768face${ext}`;
    el.style.backgroundImage = `url(/static/cards/${imgName})`;

    cardElements[card.code] = el;
    return el;
}


function renderImmediately(snapshot) {
    const table = document.getElementById("game-table");
    table.innerHTML = "";
    // Reset the cardElements map since we're rebuilding everything
    Object.keys(cardElements).forEach(k => delete cardElements[k]);

    // 1. Draw Column Placeholders (Z=1)
    snapshot.actors.slots.forEach(slot => {
        if (!slot.visible) return;
        const el = document.createElement("div");
        el.className = "column-requisite";
        
        if (slot.backstyle === 1 && slot.backcolor === 8) {
            el.classList.add("style-grey");
        } else {
            el.classList.add("win95-bevel-in"); 
        }
        
        el.style.left = `${slot.left}px`;
        el.style.top = `${slot.top}px`;
        el.style.zIndex = 1;
        table.appendChild(el);
    });

    // 2. Draw Cards (Z=100+) and populate cardElements map
    snapshot.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            const el = createCardElement(card, col, index);
            table.appendChild(el);
            // ✅ FIX: Register card in map BEFORE drawing selector
            cardElements[card.code] = el;
        });
    });

    // 3. Draw Selection Box (Z=1000) — FIXED
    const sel = snapshot.actors.selector;
    if (sel.visible && snapshot.selected_card_code) {
        console.log(`✨ Rendering selection box for card: ${snapshot.selected_card_code}`);
        
        const cardEl = cardElements[snapshot.selected_card_code];
        if (cardEl) {
            const selectorEl = document.createElement("div");
            selectorEl.className = "selection-box";
            
            // Position exactly over the selected card
            selectorEl.style.left = cardEl.style.left;
            selectorEl.style.top = cardEl.style.top;
            selectorEl.style.zIndex = 1000;
            
            table.appendChild(selectorEl);
            console.log(`✅ Selection box rendered at (${cardEl.style.left}, ${cardEl.style.top})`);
        } else {
            console.warn(`⚠️  Card element not found for: ${snapshot.selected_card_code}`);
        }
    }
}



function animateDiff(prev, next) {
    next.kup.forEach((col, colIdx) => {

        // Find the column's wrapper div by its data-column-id.
        // Cards must be moved/created inside this div so their
        // left/top are relative offsets, matching renderImmediately.
        const colEl = document.querySelector(`[data-column-id="${colIdx}"]`);

        col.cards.forEach((card, index) => {
            const ox = Number(col.overlap_x) || 0;
            const oy = Number(col.overlap_y) || 0;

            // Relative offset inside the column div (NOT absolute table coords)
            const newX = index * ox;
            const newY = index * oy;

            const el = cardElements[card.code];

            if (el) {
                // ── Move existing card ──────────────────────────────────
                // Re-parent into the correct column div if it moved columns
                if (el.parentElement !== colEl && colEl) {
                    colEl.appendChild(el);
                }

                el.style.transition = "all 0.35s ease-in-out";
                el.style.left   = `${newX}px`;
                el.style.top    = `${newY}px`;
                el.style.zIndex = 100 + index;

                // Handle face-down → face-up flip
                if (card.face_up && el.classList.contains('face-down')) {
                    el.classList.replace('face-down', 'face-up');
                    el.style.backgroundImage =
                        `url(/static/cards/1024x768${card.code}.png)`;
                }

            } else {
                // ── New card (redealt / just arrived) ───────────────────
                // relative=true so coords are column-relative, not absolute
                const newEl = createCardElement(card, col, index, true);

                if (colEl) {
                    colEl.appendChild(newEl);   // inside column div ✅
                } else {
                    // Fallback: column div missing, go straight to table
                    // (shouldn't happen, but safe to handle)
                    document.getElementById("game-table").appendChild(newEl);
                }
            }
        });
    });
}

/* ---------- MENU INTERCEPTORS ---------- */

function toggleAutoplay(element) {
    element.classList.toggle("checked");
    const isEnabled = element.classList.contains("checked");

    handleEngineAction("/cardgames/api/options/autoplay", { 
        enabled: isEnabled 
    });
}

function showRules() {
    fetch("/cardgames/api/rules")
        .then(res => {
            if (res.status === 401 || res.status === 404) {
                openMsgBox("Session Expired", "Your game session has ended. Please select a game from the menu again.");
                return;
            }
            return res.json();
        })
        .then(data => {
            if (data) openMsgBox(`Rules: ${data.title}`, data.text);
        });
}

function openMsgBox(title, content) {
    document.getElementById('msgbox-title').innerText = title;
    document.getElementById('msgbox-content').innerText = content;
    document.getElementById('win95-modal-overlay').style.display = 'flex';
}

function closeMsgBox() {
    document.getElementById('win95-modal-overlay').style.display = 'none';
}




// Unified sender of the The Frontend Wishes
// The Unified Messenger
function dispatchWish(eventData) {
    // If there is no active game ID on the table, don't even send the request
    const gameTable = document.getElementById("game-table");
    if (!gameTable.dataset.gameId) return;

    fetch("/cardgames/api/click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData)
    })
    .then(res => {
        // SILENT FAIL for table clicks if session expired
        if (res.status === 401 && !eventData.col_idx && !eventData.card_code) return; 
        return res.json();
    })
    .then(data => {
        if (data && data.game) onEngineUpdate(data.game);
    })
    .catch(err => console.error("Communication breakdown:", err));
}

// THE STAGE OBSERVERS
document.addEventListener("mousedown", (e) => {
    const card = e.target.closest(".card");
    const slot = e.target.closest(".column-requisite"); // The green/grey pencil-drawn actor
    
    // We send a Mousedown wish if we hit a column or a card
    if (card || slot) {
        //const colIdx = card ? card.parentElement.dataset.columnId : slot.dataset.columnId;
        // Walk up to find the nearest element with data-column-id
        const colEl = e.target.closest("[data-column-id]");
        const colIdx = colEl ? colEl.dataset.columnId : null;
        dispatchWish({
            event_type: "mousedown",
            col_idx: colIdx,
            card_code: card ? card.dataset.cardId : null
        });
    }
});

document.addEventListener("click", (e) => {
    const card = e.target.closest(".card");
    const slot = e.target.closest(".column-requisite");
    const table = e.target.id === "game-table" || e.target.id === "table-scroll";

    if (card || slot) {
        //const colIdx = card ? card.parentElement.dataset.columnId : slot.dataset.columnId;
        // Walk up to find the nearest element with data-column-id
        const colEl = e.target.closest("[data-column-id]");
        const colIdx = colEl ? colEl.dataset.columnId : null;
        dispatchWish({
            event_type: "click",
            col_idx: colIdx,
            card_code: card ? card.dataset.cardId : null
        });
    } else if (table) {
        // User clicked the green background (The Stage Floor)
        dispatchWish({ event_type: "table_click", col_idx: null, card_code: null });
    }
});


// TABLE CLICK (The Green Felt)
document.getElementById("game-table").addEventListener("click", (e) => {
    if (e.target.id === "game-table") {
        dispatchWish({ event_type: "table_click", col_idx: null, card_code: null });
    }
});

// DOUBLE CLICK
document.addEventListener("dblclick", (e) => {
    const card = e.target.closest(".card");
    if (card) {
        // Walk up to find the nearest element with data-column-id
        const colEl = e.target.closest("[data-column-id]");
        const colIdx = colEl ? colEl.dataset.columnId : null;
        dispatchWish({
            event_type: "dblclick",
            card_code: card ? card.dataset.cardId : null,
            col_idx: colIdx
        });        
        
    }
});