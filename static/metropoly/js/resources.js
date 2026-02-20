// static/metropoly/js/resources.js

export const Resources = {
  players: {},        // p1..p7
  tiles: {},          // roads, houses, etc
  flags: {},
  dice: {},
  directions: {},
  gauges: {},
  editorTools: {}
};

function loadImage(path) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = path;
  });
}

// static/metropoly/js/load_resources.js
import { Resources } from "./resources.js";

const BASE = "/static/metropoly/assets/graphics/";

export async function loadResources() {
  /* === PLAYER FIGURES === */
  for (let i = 1; i <= 7; i++) {
    Resources.players[`p${i}`] =
      await loadImage(`${BASE}p${i}.png`);
  }

  /* === ROAD TILES === */
  Object.assign(Resources.tiles, {
    roaddl: await loadImage(`${BASE}roaddl.png`),
    roaddr: await loadImage(`${BASE}roaddr.png`),
    roadlr: await loadImage(`${BASE}roadlr.png`),
    roadud: await loadImage(`${BASE}roadud.png`),
    roadul: await loadImage(`${BASE}roadul.png`),
    roadur: await loadImage(`${BASE}roadur.png`),
    road3n: await loadImage(`${BASE}road3n.png`),
    road3e: await loadImage(`${BASE}road3e.png`),
    road3w: await loadImage(`${BASE}road3w.png`),
    road3s: await loadImage(`${BASE}road3s.png`),
    road4:  await loadImage(`${BASE}road4.png`)
  });

  /* === BUILDINGS === */
  for (let i = 0; i <= 5; i++) {
    Resources.tiles[`house${i}`] =
      await loadImage(`${BASE}h${i}.png`);
  }

  Resources.tiles.school = await loadImage(`${BASE}school.png`);
  Resources.tiles.job    = await loadImage(`${BASE}job.png`);
  Resources.tiles.jail   = await loadImage(`${BASE}jail.png`);

  /* === FLAGS === */
  for (let i = 1; i <= 7; i++) {
    Resources.flags[`flag${i}`] =
      await loadImage(`${BASE}flag${i}.png`);
  }

  /* === DICE === */
  for (let i = 1; i <= 6; i++) {
    Resources.dice[`dice${i}`] =
      await loadImage(`${BASE}dice${i}.png`);
  }

  /* === DIRECTION TILES === */
  Object.assign(Resources.directions, {
    n2: await loadImage(`${BASE}n2.png`),
    n3: await loadImage(`${BASE}n3.png`),
    n4: await loadImage(`${BASE}n4.png`),
    s1: await loadImage(`${BASE}s1.png`),
    s3: await loadImage(`${BASE}s3.png`),
    s4: await loadImage(`${BASE}s4.png`),
    w1: await loadImage(`${BASE}w1.png`),
    w2: await loadImage(`${BASE}w2.png`),
    w4: await loadImage(`${BASE}w4.png`),
    e1: await loadImage(`${BASE}e1.png`),
    e2: await loadImage(`${BASE}e2.png`),
    e3: await loadImage(`${BASE}e3.png`)
  });

  /* === GAUGE === */
  for (let i = 0; i <= 9; i++) {
    Resources.gauges[`gauge${i}`] =
      await loadImage(`${BASE}gaug${i}.png`);
  }

  /* === MAP EDITOR TOOLS === */
  Resources.editorTools = {
    road:   Resources.tiles.roadlr,
    house:  Resources.tiles.house0,
    school: Resources.tiles.school,
    job:    Resources.tiles.job,
    arrow:  Resources.directions.n2
  };
}

