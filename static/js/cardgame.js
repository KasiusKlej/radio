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


function renderImmediately(snapshot) {
    const table = document.getElementById("game-table");
    table.innerHTML = "";

    // 1. Draw Column Placeholders (Z=1)
    snapshot.actors.slots.forEach(slot => {
        if (!slot.visible) return;
        const el = document.createElement("div");

        //el.className = "column-requisite win95-bevel-in";
        el.className = "column-requisite";
        // Logic for changing the costume
        // In FreeCell, home1-4 has backstyle=1 and backcolor=8
        if (slot.backstyle === 1 && slot.backcolor === 8) {
            el.classList.add("style-grey");
        } else {
            // Default Green costume
            el.classList.add("win95-bevel-in"); 
        }
        
        el.style.left = `${slot.left}px`;
        el.style.top = `${slot.top}px`;
        el.style.zIndex = 1;
        table.appendChild(el);
    });

    // 2. Draw Cards (Z=100+)
    snapshot.kup.forEach(col => {
        col.cards.forEach((card, index) => {
            const el = createCardElement(card, col, index);
            table.appendChild(el);
        });
    });

    // 3. Draw Selection Box (Z=1000)
    const sel = snapshot.actors.selector;
    if (sel.visible) {
        const selectorEl = document.createElement("div");
        selectorEl.className = "selection-box";
        // The engine tells us which card is selected
        const cardEl = cardElements[snapshot.selected_card_code];
        if (cardEl) {
            selectorEl.style.left = cardEl.style.left;
            selectorEl.style.top = cardEl.style.top;
            selectorEl.style.zIndex = 1000;
            table.appendChild(selectorEl);
        }
    }


    console.log("=== THEATRE RENDERING START ===");

    snapshot.kup.forEach((col, colIdx) => {
        // 1. Draw Placeholder
        const slotEl = document.createElement("div");
        slotEl.className = "column win95-bevel-in";
        slotEl.dataset.columnId = colIdx;
        slotEl.style.left = `${col.x}px`;
        slotEl.style.top = `${col.y}px`;
        slotEl.style.zIndex = 1;
        table.appendChild(slotEl);

        // 2. Draw Cards in this column
        if (col.cards && col.cards.length > 0) {
            if (colIdx === 8) {
                console.log(`DEBUG: Processing Column 8 [${col.name}]`);
                console.log(`Base Position: X=${col.x}, Y=${col.y}`);
                console.log(`Overlap Stats: OX=${col.overlap_x}, OY=${col.overlap_y}`);
            }

            col.cards.forEach((card, index) => {
                const el = createCardElement(card, col, index);
                table.appendChild(el);
                
                // Detailed Math Debug for Column 8
                if (colIdx === 8 && index < 2) {
                    console.log(` > Card[${index}] (${card.code}): Calculated Left=${el.style.left}, Top=${el.style.top}`);
                }
            });
        }
    });
    console.log("=== THEATRE RENDERING COMPLETE ===");
    



}



// function createCardElement(card, col, index) {
//     const el = document.createElement("div");
//     el.className = `card ${card.face_up ? 'face-up' : 'face-down'}`;
//     el.dataset.cardId = card.code;
    
//     // --- FORCE NUMBERS ---
//     // Ensure overlap is a number. If it's a string or missing, default to 0 or 20.
//     const ox = Number(col.overlap_x) || 0;
//     const oy = Number(col.overlap_y) || 0;
//     const baseX = Number(col.x) || 0;
//     const baseY = Number(col.y) || 0;

//     // --- MATH ---
//     const finalX = baseX + (index * ox);
//     const finalY = baseY + (index * oy);

//     el.style.left = `${finalX}px`;
//     el.style.top = `${finalY}px`;
//     el.style.zIndex = 100 + index;
    
//     // Set Image (using confirmed BMP path)
//     const imgPath = card.face_up 
//         ? `1024x768${card.code}.bmp` 
//         : `1024x768face.bmp`;
        
//     el.style.backgroundImage = `url(/static/cards/${imgPath})`;
    
//     // Safety: ensure background-size is 100% to fit the 89x132 div
//     el.style.backgroundSize = "100% 100%";
    
//     cardElements[card.code] = el;
//     return el;
// }

function createCardElement(card, col, index) {
    const el = document.createElement("div");
    el.className = `card ${card.face_up ? 'face-up' : 'face-down'}`;
    el.dataset.cardId = card.code;
    
    // VB RECONSTRUCTION MATH
    // 1. Get the base Anchor from the column
    const baseX = Number(col.x);
    const baseY = Number(col.y);
    
    // 2. Get the Overlap (The 'panning' value)
    const ox = Number(col.overlap_x) || 0;
    const oy = Number(col.overlap_y) || 0;

    // 3. Final Absolute Table Position
    // Card 0: baseX + 0
    // Card 1: baseX + ox
    // Card 2: baseX + 2*ox
    const finalX = baseX + (index * ox);
    const finalY = baseY + (index * oy);

    el.style.left = `${finalX}px`;
    el.style.top = `${finalY}px`;
    
    // Z-INDEX: VB used ZOrder. 
    // Requisites (slots) = 1
    // Bottom card = 100
    // Top card = 100 + index
    el.style.zIndex = 100 + index;
    
    // Graphics
    const ext = ".png"; // or .bmp
    let imgName;
    
    if (card.face_up === true || card.face_up === 1) {
        imgName = `1024x768${card.code}${ext}`;
    } else {
        // The Mask! Show the back of the card.
        imgName = `1024x768face${ext}`;
    }
    
    el.style.backgroundImage = `url(/static/cards/${imgName})`;


    return el;
}



function animateDiff(prev, next) {
    next.kup.forEach((col, colIdx) => {
        col.cards.forEach((card, index) => {
            const el = cardElements[card.code];
            if (el) {
                const newX = col.x + (index * (col.overlap_x || 0));
                const newY = col.y + (index * (col.overlap_y || 0));
                
                // If position changed, trigger CSS transition
                el.style.transition = "all 0.35s ease-in-out";
                el.style.left = `${newX}px`;
                el.style.top = `${newY}px`;
                el.style.zIndex = 100 + index;
                
                // Handle flip changes
                if (card.face_up && el.classList.contains('face-down')) {
                    el.classList.replace('face-down', 'face-up');
                    el.style.backgroundImage = `url(/static/cards/1024x768${card.code}.bmp)`;
                }





                // DEBUG 
                const ox = Number(col.overlap_x) || 0;
                const oy = Number(col.overlap_y) || 0;
                const calcX = col.x + (index * ox);
                const calcY = col.y + (index * oy);
                console.log(`--- DEBUG 2: RENDERER MATH (Col 8, Card ${index}) ---`);
                console.log(`Formula: ${col.y} + (${index} * ${oy}) = ${calcY}`);
                console.log(`Resulting Style: Left: ${calcX}px, Top: ${calcY}px`);
    







            } else {
                // Card is new (e.g. redealt), create it
                const newEl = createCardElement(card, col, index);
                document.getElementById("game-table").appendChild(newEl);
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
        const colIdx = card ? card.parentElement.dataset.columnId : slot.dataset.columnId;
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
        const colIdx = card ? card.parentElement.dataset.columnId : slot.dataset.columnId;
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


// document.addEventListener("dblclick", (e) => {
//     const cardEl = e.target.closest(".card");
//     if (!cardEl) return;

//     const colEl = cardEl.closest(".column");
//     const colIdx = colEl ? colEl.dataset.columnId : null;

//     if (colIdx !== null) {
//         // CHANGE THIS: point to /api/click, not /api/double_click
//         handleEngineAction("/cardgames/api/click", {
//             event_type: "dblclick",
//             col_idx: colIdx,
//             card_code: cardEl.dataset.cardId
//         });
//     }
// });

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
        dispatchWish({
            event_type: "dblclick",
            card_code: card.dataset.cardId,
            col_idx: card.parentElement.dataset.columnId
        });
    }
});