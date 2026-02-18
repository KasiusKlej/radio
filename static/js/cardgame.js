/* ============================================================
   Card Games – Frontend Theatre Director
   Clean Production Version - February 2026
   ============================================================ */

// ────────────────────────────────────────────────────────────
// GLOBAL STATE
// ────────────────────────────────────────────────────────────
let prevSnapshot = null;
const cardElements = {}; // Map: cardCode → DOM Element


// ────────────────────────────────────────────────────────────
// INITIALIZATION
// ────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    if (window.INITIAL_GAME_STATE) {
        onEngineUpdate(window.INITIAL_GAME_STATE);
    }
    
    attachEventListeners();
});


// ────────────────────────────────────────────────────────────
// EVENT LISTENERS (VB-style event wiring)
// ────────────────────────────────────────────────────────────
function attachEventListeners() {
    // Single Click Handler
    document.addEventListener("click", (e) => {
        const card = e.target.closest(".card");
        const slot = e.target.closest(".column-requisite");
        const table = e.target.id === "game-table";
        
        if (card) {
            // VB: card_Click(Index)
            e.stopPropagation();
            dispatchEvent({
                event_type: "click",
                card_code: card.dataset.cardId,
                col_idx: null
            });
        } else if (slot) {
            // VB: Form_MouseDown (click on empty slot)
            e.stopPropagation();
            dispatchEvent({
                event_type: "click",
                col_idx: slot.dataset.columnId,
                card_code: null
            });
        } else if (table) {
            // VB: Form background click (deselect)
            dispatchEvent({
                event_type: "table_click",
                col_idx: null,
                card_code: null
            });
        }
    });
    
    // Double Click Handler
    document.addEventListener("dblclick", (e) => {
        const card = e.target.closest(".card");
        if (card) {
            // VB: card_DblClick(Index) - Autoplay
            e.stopPropagation();
            dispatchEvent({
                event_type: "dblclick",
                card_code: card.dataset.cardId,
                col_idx: null
            });
        }
    });
}


// ────────────────────────────────────────────────────────────
// NETWORK COMMUNICATION
// ────────────────────────────────────────────────────────────
function dispatchEvent(eventData) {
    const gameTable = document.getElementById("game-table");
    if (!gameTable || !gameTable.dataset.gameId) {
        return; // No active game
    }
    
    fetch("/cardgames/api/click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData)
    })
    .then(res => {
        // Silent fail for table clicks if session expired
        if (res.status === 401 && eventData.event_type === "table_click") {
            return null;
        }
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        return res.json();
    })
    .then(data => {
        if (data && data.game) {
            onEngineUpdate(data.game);
        } else if (data && data.error) {
            console.error("Engine Error:", data.error);
        }
    })
    .catch(err => {
        console.error("Network Error:", err);
    });
}


// ────────────────────────────────────────────────────────────
// RENDERING PIPELINE
// ────────────────────────────────────────────────────────────
function onEngineUpdate(newSnapshot) {
    if (!newSnapshot) return;
    
    if (!prevSnapshot) {
        renderImmediately(newSnapshot);
    } else {
        animateDiff(prevSnapshot, newSnapshot);
    }
    
    prevSnapshot = newSnapshot;
}


function renderImmediately(snapshot) {
    const table = document.getElementById("game-table");
    table.innerHTML = "";
    
    // Clear card registry
    Object.keys(cardElements).forEach(k => delete cardElements[k]);
    
    // ═══════════════════════════════════════════════════════════════════════
    // STEP 1: Draw Column Placeholders (Z=1)
    // ═══════════════════════════════════════════════════════════════════════
    snapshot.actors.slots.forEach(slot => {
        if (!slot.visible) return;
        
        const slotEl = document.createElement("div");
        slotEl.className = "column-requisite";
        slotEl.dataset.columnId = slot.column_index;
        
        // Apply styling based on backstyle/backcolor
        if (slot.backstyle === 1 && slot.backcolor === 8) {
            slotEl.classList.add("style-grey");
        } else {
            slotEl.classList.add("win95-bevel-in");
        }
        
        slotEl.style.left = `${slot.left}px`;
        slotEl.style.top = `${slot.top}px`;
        slotEl.style.zIndex = 1;
        table.appendChild(slotEl);
    });
    
    // ═══════════════════════════════════════════════════════════════════════
    // STEP 2: Draw Cards with ABSOLUTE coordinates (Z=100+)
    // ═══════════════════════════════════════════════════════════════════════
    snapshot.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            const cardEl = createCardElement(card, col, index);
            table.appendChild(cardEl);
            cardElements[card.code] = cardEl;
        });
    });
    
    // ═══════════════════════════════════════════════════════════════════════
    // STEP 3: Draw Selection Box (Z=1000)
    // ═══════════════════════════════════════════════════════════════════════
    renderSelectionBox(snapshot);
}


function animateDiff(prev, next) {
    // Remove old selection box
    const oldSelector = document.querySelector('.selection-box');
    if (oldSelector) {
        oldSelector.remove();
    }
    
    // Animate card positions
    next.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            const ox = Number(col.overlap_x) || 0;
            const oy = Number(col.overlap_y) || 0;
            const newX = col.x + (index * ox);
            const newY = col.y + (index * oy);
            
            const el = cardElements[card.code];
            
            if (el) {
                // Animate existing card
                el.style.transition = "all 0.35s ease-in-out";
                el.style.left = `${newX}px`;
                el.style.top = `${newY}px`;
                el.style.zIndex = 100 + index;
                
                // Handle face flips
                updateCardFace(el, card);
            } else {
                // Create new card (card was just dealt or moved into view)
                const newEl = createCardElement(card, col, index);
                document.getElementById("game-table").appendChild(newEl);
                cardElements[card.code] = newEl;
            }
        });
    });
    
    // Remove cards that no longer exist
    removeDeletedCards(next);
    
    // Redraw selection box
    renderSelectionBox(next);
}


function createCardElement(card, col, index) {
    const el = document.createElement("div");
    el.className = `card ${card.face_up ? 'face-up' : 'face-down'}`;
    el.dataset.cardId = card.code;
    
    // Calculate absolute position
    const baseX = Number(col.x) || 0;
    const baseY = Number(col.y) || 0;
    const ox = Number(col.overlap_x) || 0;
    const oy = Number(col.overlap_y) || 0;
    
    el.style.left = `${baseX + (index * ox)}px`;
    el.style.top = `${baseY + (index * oy)}px`;
    el.style.zIndex = 100 + index;
    
    // Set card image
    const imgName = card.face_up 
        ? `1024x768${card.code}.png`
        : `1024x768face.png`;
    el.style.backgroundImage = `url(/static/cards/${imgName})`;
    
    return el;
}


function updateCardFace(el, card) {
    if (card.face_up && el.classList.contains('face-down')) {
        el.classList.replace('face-down', 'face-up');
        el.style.backgroundImage = `url(/static/cards/1024x768${card.code}.png)`;
    } else if (!card.face_up && el.classList.contains('face-up')) {
        el.classList.replace('face-up', 'face-down');
        el.style.backgroundImage = `url(/static/cards/1024x768face.png)`;
    }
}


function removeDeletedCards(snapshot) {
    Object.keys(cardElements).forEach(code => {
        const stillExists = snapshot.kup.some(col => 
            col.cards.some(card => card.code === code)
        );
        
        if (!stillExists) {
            const el = cardElements[code];
            if (el && el.parentElement) {
                el.remove();
            }
            delete cardElements[code];
        }
    });
}


function renderSelectionBox(snapshot) {
    const sel = snapshot.actors.selector;
    if (sel.visible && snapshot.selected_card_code) {
        const cardEl = cardElements[snapshot.selected_card_code];
        if (cardEl) {
            const selectorEl = document.createElement("div");
            selectorEl.className = "selection-box";
            selectorEl.style.left = cardEl.style.left;
            selectorEl.style.top = cardEl.style.top;
            selectorEl.style.zIndex = 1000;
            document.getElementById("game-table").appendChild(selectorEl);
        }
    }
}


// ────────────────────────────────────────────────────────────
// MENU ACTIONS
// ────────────────────────────────────────────────────────────
function toggleAutoplay(element) {
    element.classList.toggle("checked");
    const isEnabled = element.classList.contains("checked");
    
    fetch("/cardgames/api/options/autoplay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: isEnabled })
    })
    .then(res => res.json())
    .catch(err => console.error("Autoplay toggle error:", err));
}


function showRules() {
    fetch("/cardgames/api/rules")
        .then(res => {
            if (res.status === 401 || res.status === 404) {
                openMsgBox(
                    "Session Expired", 
                    "Your game session has ended. Please select a game from the menu."
                );
                return null;
            }
            return res.json();
        })
        .then(data => {
            if (data) {
                openMsgBox(`Rules: ${data.title}`, data.text);
            }
        })
        .catch(err => console.error("Rules fetch error:", err));
}


function openMsgBox(title, content) {
    document.getElementById('msgbox-title').innerText = title;
    document.getElementById('msgbox-content').innerText = content;
    document.getElementById('win95-modal-overlay').style.display = 'flex';
}


function closeMsgBox() {
    document.getElementById('win95-modal-overlay').style.display = 'none';
}
