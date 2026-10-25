import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

async function api(path, body) {
  const opt = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const r = await fetch(path, opt);
  const data = await r.json().catch(() => ({ ok: false, error: `HTTP ${r.status}` }));
  if (!r.ok || data.ok === false || data.error) throw new Error(data.error || `HTTP ${r.status}`);
  return data;
}

const ui = { mode: "sim", space: "cart", step: 1, state: null, armed: false, realConfirm: 0 };

function say(text, kind = "") { const m = $("#jogMsg"); m.textContent = text; m.className = "msg " + kind; }
function setChecked(buttons, pred) { buttons.forEach(b => b.setAttribute("aria-checked", String(pred(b)))); }

/* ---------------- rail ---------------- */
$$(".mode button").forEach(b => b.onclick = async () => {
  const mode = b.dataset.mode;
  if (mode === ui.mode) return;
  if (mode === "real" && Date.now() - ui.realConfirm > 4000) {
    ui.realConfirm = Date.now();
    $("#robotHint").textContent = "Click Real robot again to drive the physical arm.";
    return;
  }
  try {
    await api("/hub/mode", { mode });
    ui.armed = false; $("#armMotion").checked = false;
    $("#robotHint").textContent = mode === "real" ? "Real robot: mg400-base on :8000 must be connected and enabled." : "";
  } catch (e) { $("#robotHint").textContent = e.message; }
});
$("#speed").oninput = e => $("#speedOut").textContent = e.target.value + " %";
$("#speed").onchange = async e => {
  try { await api("/api/speed", { ratio: +e.target.value }); } catch (err) { $("#robotHint").textContent = err.message; }
};
$("#btnEnable").onclick = () => api("/hub/enable", {}).catch(e => $("#robotHint").textContent = e.message);
$("#btnClear").onclick = () => api("/hub/clear_error", {}).catch(e => $("#robotHint").textContent = e.message);
const stop = () => { stopHold(); api("/hub/stop", {}).then(() => say("Stopped.", "ok")).catch(e => say(e.message, "bad")); };
$("#btnStop").onclick = stop;

function renderState(s) {
  ui.state = s; ui.mode = s.mode;
  setChecked($$(".mode button"), b => b.dataset.mode === s.mode);
  document.title = (s.mode === "real" ? "● " : "") + "MG400 Station Hub";
  const r = s.robot || {};
  const pill = $("#robotPill");
  const name = r.mode_name || "unknown";
  pill.textContent = (s.mode === "sim" ? "SIM · " : "") + name + (r.pump_mode && r.pump_mode !== "off" ? " · pump " + r.pump_mode : "");
  pill.className = "pill " + (!r.reachable ? "bad" : r.error || (r.alarm_ids || []).length ? "bad" : r.enabled ? "ok" : "warn");
  const sp = $("#speed");
  sp.max = s.limits.max_speed_ratio;
  if (document.activeElement !== sp && r.speed_ratio) { sp.value = Math.min(r.speed_ratio, sp.max); $("#speedOut").textContent = sp.value + " %"; }
  const p = r.pose || [], j = r.joints || [];
  const f = v => (typeof v === "number" ? v.toFixed(2) : "–");
  ["rx", "ry", "rz", "rr"].forEach((id, i) => $("#" + id).textContent = f(p[i]));
  ["j1", "j2", "j3", "j4"].forEach((id, i) => $("#" + id).textContent = j.length ? j[i].toFixed(2) + "°" : "–");
  $("#pump").textContent = r.pump_mode || "–";
  const seq = s.seq || {};
  $("#task").textContent = seq.error ? "error: " + seq.error : seq.busy ? seq.step : "idle";
  $("#task").style.color = seq.error ? "var(--bad)" : "";
  $$("[data-pump]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.pump === r.pump_mode)));
  const locked = !ui.armed || seq.busy;
  $$(".dial").forEach(d => d.classList.toggle("locked", locked));
  if (s.pose3d) live.target = s.pose3d;
}

async function poll() {
  try { renderState(await api("/hub/state")); }
  catch (e) { $("#robotPill").textContent = "hub unreachable"; $("#robotPill").className = "pill bad"; }
  setTimeout(poll, 200);
}

/* ---------------- jog ---------------- */
const PADS = {
  cart: [
    { hub: "X · Y", keys: { up: ["x", 1, "X+"], down: ["x", -1, "X−"], left: ["y", 1, "Y+"], right: ["y", -1, "Y−"] } },
    { hub: "Z · R", keys: { up: ["z", 1, "Z+"], down: ["z", -1, "Z−"], left: ["r", 1, "R+"], right: ["r", -1, "R−"] } },
  ],
  joint: [
    { hub: "J1 · J2", keys: { left: ["j1", 1, "J1+"], right: ["j1", -1, "J1−"], up: ["j2", -1, "J2−"], down: ["j2", 1, "J2+"] } },
    { hub: "J3 · J4", keys: { up: ["j3", -1, "J3−"], down: ["j3", 1, "J3+"], left: ["j4", 1, "J4+"], right: ["j4", -1, "J4−"] } },
  ],
};
const DIRS = { up: -90, right: 0, down: 90, left: 180 };

function sector(a0, a1, r0, r1) {
  const p = (r, a) => [r * Math.cos(a * Math.PI / 180), r * Math.sin(a * Math.PI / 180)];
  const [x0, y0] = p(r1, a0), [x1, y1] = p(r1, a1), [x2, y2] = p(r0, a1), [x3, y3] = p(r0, a0);
  return `M${x0},${y0} A${r1},${r1} 0 0 1 ${x1},${y1} L${x2},${y2} A${r0},${r0} 0 0 0 ${x3},${y3} Z`;
}

function buildDials() {
  ["#dialA", "#dialB"].forEach((sel, i) => {
    const pad = PADS[ui.space][i], svg = $(sel);
    let html = `<circle class="ring" r="106"/>`;
    for (const [dir, ang] of Object.entries(DIRS)) {
      const [axis, sign, label] = pad.keys[dir];
      const [tx, ty] = [70 * Math.cos(ang * Math.PI / 180), 70 * Math.sin(ang * Math.PI / 180)];
      html += `<path class="key" tabindex="0" role="button" aria-label="${label}" data-axis="${axis}" data-sign="${sign}" d="${sector(ang - 43, ang + 43, 40, 102)}"/>`
            + `<text class="txt" x="${tx}" y="${ty}">${label}</text>`;
    }
    html += `<circle class="hub" r="36"/><text class="hubtxt">${pad.hub}</text>`;
    svg.innerHTML = html;
    svg.querySelectorAll(".key").forEach(k => {
      k.addEventListener("pointerdown", ev => { ev.preventDefault(); k.setPointerCapture(ev.pointerId); press(k); });
      k.addEventListener("pointerup", () => release(k));
      k.addEventListener("pointercancel", () => release(k));
      k.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); jogOnce(k.dataset.axis, +k.dataset.sign); } });
    });
  });
  $("#stepUnit").textContent = ui.space === "cart" ? "mm / °R" : "degrees";
}

let hold = null;
function stopHold() { if (hold) { clearInterval(hold.timer); hold.key?.classList.remove("down"); hold = null; } }
async function jogOnce(axis, sign, step = ui.step) {
  if (!ui.armed) { say("Tick “Motion enabled” first.", "bad"); return false; }
  try {
    const r = await api("/hub/jog", { space: ui.space, axis, delta: sign * step });
    const t = r.target;
    say(t ? `→ X ${t.x.toFixed(1)}  Y ${t.y.toFixed(1)}  Z ${t.z.toFixed(1)}  R ${t.r.toFixed(1)}` : "", "ok");
    return true;
  } catch (e) { say(e.message, "bad"); return false; }
}
function press(k) {
  k.classList.add("down");
  const axis = k.dataset.axis, sign = +k.dataset.sign;
  if (ui.step !== "hold") { jogOnce(axis, sign).finally(() => setTimeout(() => k.classList.remove("down"), 120)); return; }
  stopHold();
  hold = { key: k, timer: setInterval(() => jogOnce(axis, sign, 1).then(ok => { if (!ok) stopHold(); }), 200) };
  jogOnce(axis, sign, 1);
}
function release(k) { if (hold && hold.key === k) stopHold(); }

$$("[data-space]").forEach(b => b.onclick = () => { ui.space = b.dataset.space; setChecked($$("[data-space]"), x => x.dataset.space === ui.space); buildDials(); });
$$("[data-step]").forEach(b => b.onclick = () => {
  ui.step = b.dataset.step === "hold" ? "hold" : +b.dataset.step;
  setChecked($$("[data-step]"), x => x.dataset.step === b.dataset.step);
});
$("#armMotion").onchange = e => { ui.armed = e.target.checked; say(ui.armed ? (ui.mode === "real" ? "Real arm armed. Keep a hand on the e-stop." : "Simulated arm armed.") : ""); };
$$("[data-pump]").forEach(b => b.onclick = () => api("/api/pump", { mode: b.dataset.pump }).catch(e => say(e.message, "bad")));

const KEYMAP = { ArrowUp: ["x", 1], ArrowDown: ["x", -1], ArrowLeft: ["y", 1], ArrowRight: ["y", -1],
                 PageUp: ["z", 1], PageDown: ["z", -1], q: ["r", 1], e: ["r", -1] };
addEventListener("keydown", ev => {
  if (ev.key === "Escape") { stop(); return; }
  if (/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName) || $("#tab-jog").hidden || ui.space !== "cart") return;
  const m = KEYMAP[ev.key];
  if (m) { ev.preventDefault(); jogOnce(m[0], m[1], ui.step === "hold" ? 1 : ui.step); }
});

/* ---------------- tabs ---------------- */
$$(".tabs button").forEach(b => b.onclick = () => {
  $$(".tabs button").forEach(x => x.setAttribute("aria-selected", String(x === b)));
  $$(".tab").forEach(t => t.hidden = t.id !== "tab-" + b.dataset.tab);
  if (b.dataset.tab === "picker" && $("#picker").src.endsWith("about:blank")) $("#picker").src = "/picker";
  if (b.dataset.tab === "tests") pollTests();
});

/* ---------------- tests ---------------- */
let queue = [];
function renderTests(tests) {
  const box = $("#testList");
  let anyRunning = false, anyBad = false;
  for (const [key, t] of Object.entries(tests)) {
    let el = box.querySelector(`[data-test="${key}"]`);
    if (!el) {
      el = document.createElement("article");
      el.className = "test"; el.dataset.test = key;
      el.innerHTML = `<h3></h3><button class="ghost run">Run</button><p class="about"></p>
        <div class="res"><span class="chip"></span><span class="sum"></span></div>
        <details><summary>Output</summary><pre></pre></details>`;
      el.querySelector(".run").onclick = () => runTest(key);
      box.appendChild(el);
    }
    el.querySelector("h3").textContent = t.title;
    el.querySelector(".about").textContent = t.about;
    const chip = el.querySelector(".chip");
    chip.className = "chip " + t.status; chip.textContent = t.status;
    el.querySelector(".sum").textContent = t.summary + (t.seconds != null ? `  ·  ${t.seconds} s at ${t.finished}` : "");
    el.querySelector(".run").disabled = t.status === "running";
    const pre = el.querySelector("pre");
    if (pre.textContent !== t.output) pre.textContent = t.output || "(no output yet)";
    anyRunning ||= t.status === "running";
    anyBad ||= t.status === "fail" || t.status === "warn";
  }
  $("#testsDot").hidden = !anyBad;
  return anyRunning;
}
async function runTest(key) {
  try { await api("/hub/tests/run", { name: key }); pollTests(); } catch (e) { alertTest(key, e.message); }
}
function alertTest(key, msg) { const el = $(`[data-test="${key}"] .sum`); if (el) el.textContent = msg; }
$("#runAll").onclick = () => { queue = ["hub", "audit", "dry_run", "dry_run_full", "refit", "tolerance"]; next(); };
async function next() {
  if (!queue.length) return;
  const { tests } = await api("/hub/tests");
  if (Object.values(tests).some(t => t.status === "running")) { setTimeout(next, 1000); return; }
  await runTest(queue.shift());
  setTimeout(next, 1500);
}
let testTimer = null;
async function pollTests() {
  clearTimeout(testTimer);
  try {
    const { tests } = await api("/hub/tests");
    const running = renderTests(tests);
    if (running || !$("#tab-tests").hidden) testTimer = setTimeout(pollTests, running ? 1000 : 4000);
    if (tests.export.status === "pass" && tests.export.finished !== scene.builtAt) { scene.builtAt = tests.export.finished; loadScene(); }
  } catch (e) { testTimer = setTimeout(pollTests, 3000); }
}

/* ---------------- camera ---------------- */
$("#camToggle").onclick = () => {
  const img = $("#camImg"), on = img.hidden;
  img.hidden = !on; $("#camEmpty").hidden = on;
  img.src = on ? "/stream.mjpg?t=" + Date.now() : "";
  $("#camToggle").textContent = on ? "Stop stream" : "Start stream";
};
let shownFrame = null;
async function lastFrame() {
  try {
    const p = await (await fetch("/api/photo")).json();
    if (p.name && p.name !== shownFrame) {
      shownFrame = p.name;
      $("#frameImg").src = "/frames/" + p.name; $("#frameImg").hidden = false;
      $("#frameName").textContent = `Last saved frame: ${p.name} (${p.time})`;
    }
  } catch (e) { /* camera folder may be empty */ }
}
$("#camSnap").onclick = async () => {
  $("#camSnap").disabled = true;
  try { await api("/api/view", {}); await lastFrame(); } catch (e) { $("#frameName").textContent = e.message; }
  $("#camSnap").disabled = false;
};
setInterval(() => { if (!$("#tab-camera").hidden) lastFrame(); }, 2000);
setInterval(() => { const c = ui.state?.camera; if (c) $("#camState").textContent = c.open ? `Camera on, ${c.fps} fps` : (c.error || "Camera closed"); }, 1000);

/* ---------------- 3D stage ---------------- */
const view = $("#view");
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
view.appendChild(renderer.domElement);
const scene3 = new THREE.Scene();
scene3.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
scene3.add(new THREE.HemisphereLight(0xffffff, 0x8a8f96, 0.6));
const sun = new THREE.DirectionalLight(0xffffff, 1.2);
sun.position.set(-600, 1400, 500); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -900, right: 900, top: 900, bottom: -900, near: 100, far: 4000 });
scene3.add(sun);
const camera = new THREE.PerspectiveCamera(38, 1, 5, 20000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
const world = new THREE.Group(); world.rotation.x = -Math.PI / 2; scene3.add(world);
const scene = { nodes: {}, A: null, builtAt: null, root: null };
const live = { target: null };
const to3 = v => new THREE.Vector3(v[0], v[2], -v[1]);

function resize() {
  const w = view.clientWidth, h = view.clientHeight;
  renderer.setSize(w, h); camera.aspect = w / Math.max(1, h); camera.updateProjectionMatrix(); drawStrip();
}
new ResizeObserver(resize).observe(view);
function bg() { scene3.background = new THREE.Color(css("--well")); }
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { bg(); drawStrip(); });

function setCam(kind) {
  const pos = { iso: [1250, -950, 900], top: [250, 0, 1700], side: [250, -1500, 250] }[kind];
  if (kind === "tool") {
    const n = scene.nodes["cup metal"];
    if (!n) return;
    const p = new THREE.Vector3(); n.getWorldPosition(p);
    camera.position.copy(p.clone().add(new THREE.Vector3(140, 60, 140))); controls.target.copy(p);
  } else {
    camera.position.copy(to3(pos)); controls.target.copy(to3([230, 0, kind === "top" ? -150 : 0]));
  }
  camera.up.set(kind === "top" ? 1 : 0, kind === "top" ? 0 : 1, 0);
  controls.update();
}
$$("[data-cam]").forEach(b => b.onclick = () => setCam(b.dataset.cam));

async function loadScene() {
  try {
    const t = Date.now();
    const [gltf, A] = await Promise.all([new GLTFLoader().loadAsync("/viewer/scene.glb?" + t), fetch("/viewer/anim.json?" + t).then(r => r.json())]);
    if (scene.root) world.remove(...world.children);
    const real = {};
    for (const n of A.nodes.map(n => n.name)) real[THREE.PropertyBinding.sanitizeNodeName(n)] = n;
    gltf.scene.traverse(o => { if (real[o.name]) o.name = real[o.name]; });
    const metal = ["cup metal", "cup fitting", "cup flange"];
    gltf.scene.traverse(o => {
      if (!o.isMesh) return;
      const name = o.name, glass = name.startsWith("glass");
      o.geometry = o.geometry.toNonIndexed(); o.geometry.computeVertexNormals();
      o.material = new THREE.MeshStandardMaterial({
        color: A.colors[name] || "#b0b0b0", transparent: glass, opacity: glass ? 0.65 : 1,
        roughness: glass ? 0.1 : name.includes("pipe") || metal.includes(name) ? 0.3 : 0.7,
        metalness: name.includes("pipe") ? 0.9 : metal.includes(name) ? 0.55 : name.startsWith("rakis") ? 0.3 : 0.05,
      });
      o.castShadow = name !== "table"; o.receiveShadow = true;
    });
    scene.nodes = {};
    [...gltf.scene.children].forEach(c => world.add(c));
    world.traverse(o => { if (o.name && !scene.nodes[o.name]) scene.nodes[o.name] = o; });
    scene.A = A; scene.root = gltf.scene;
    applyPose(A.frames[0].s);                // glasses and tool start where the cycle starts
    replay.T = A.frames[A.frames.length - 1].t;
    drawStrip();
    if (!scene.camSet) { setCam("iso"); scene.camSet = true; }
  } catch (e) {
    console.warn("3D scene", e);
  }
}

function applyPose(s, k = 1) {
  for (const [n, v] of Object.entries(s)) {
    const o = scene.nodes[n];
    if (!o) continue;
    const p = new THREE.Vector3(v[0], v[1], v[2]), q = new THREE.Quaternion(v[3], v[4], v[5], v[6]);
    if (k >= 1) { o.position.copy(p); o.quaternion.copy(q); } else { o.position.lerp(p, k); o.quaternion.slerp(q, k); }
  }
}

/* replay */
const replay = { on: false, playing: true, t: 0, speed: 1, T: 1 };
$$("[data-view]").forEach(b => b.onclick = () => {
  replay.on = b.dataset.view === "replay";
  setChecked($$("[data-view]"), x => x.dataset.view === b.dataset.view);
  $("#replayBar").hidden = !replay.on;
  if (!replay.on && scene.A) applyPose(scene.A.frames[0].s);   // put the glasses back home
  drawStrip();
});
$("#replayPlay").onclick = e => { replay.playing = !replay.playing; e.target.textContent = replay.playing ? "Pause" : "Play"; };
$("#replaySpeed").onchange = e => replay.speed = +e.target.value;
function frameAt(t) {
  const F = scene.A.frames; let lo = 0, hi = F.length - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (F[m].t <= t) lo = m; else hi = m; }
  const a = F[lo], b = F[hi]; return { a, b, k: b.t > a.t ? Math.min(1, Math.max(0, (t - a.t) / (b.t - a.t))) : 0 };
}
const STATUS = { ok: "--ok", close: "--warn", COLLISION: "--bad", event: "--sim" };
function drawStrip() {
  const c = $("#strip canvas"); if (!scene.A || !c.clientWidth) return;
  const w = c.clientWidth, h = c.clientHeight; c.width = w * devicePixelRatio; c.height = h * devicePixelRatio;
  const g = c.getContext("2d"); g.scale(devicePixelRatio, devicePixelRatio);
  const F = scene.A.frames;
  for (let i = 1; i < F.length; i++) {
    g.fillStyle = css(STATUS[scene.A.actions[F[i].a]?.status] || "--ok");
    g.fillRect(F[i - 1].t / replay.T * w, 0, Math.max(1, (F[i].t - F[i - 1].t) / replay.T * w), h);
  }
}
const strip = $("#strip"); let drag = false;
const seek = e => { const r = strip.getBoundingClientRect(); replay.t = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)) * replay.T; };
strip.onpointerdown = e => { drag = true; strip.setPointerCapture(e.pointerId); seek(e); };
strip.onpointermove = e => drag && seek(e);
strip.onpointerup = () => drag = false;

let prev = performance.now();
renderer.setAnimationLoop(now => {
  const dt = Math.min(0.1, (now - prev) / 1000); prev = now;
  if (scene.A) {
    if (replay.on) {
      if (replay.playing) { replay.t += dt * replay.speed; if (replay.t > replay.T) replay.t = 0; }
      const { a, b, k } = frameAt(replay.t);
      const mix = {};
      for (const n of Object.keys(a.s)) {
        const sa = a.s[n], sb = b.s[n] || sa;
        mix[n] = sa.map((v, i) => i < 3 ? v + (sb[i] - v) * k : v);
        const qa = new THREE.Quaternion(...sa.slice(3)), qb = new THREE.Quaternion(...sb.slice(3));
        qa.slerp(qb, k); mix[n].splice(3, 4, qa.x, qa.y, qa.z, qa.w);
      }
      applyPose(mix);
      $("#stripHead").style.left = (replay.t / replay.T * 100) + "%";
      const act = scene.A.actions[(k > 0.5 ? b : a).a];
      $("#replayStep").textContent = act ? act.text : "";
    } else if (live.target) {
      applyPose(live.target, Math.min(1, dt * 12));
    }
  }
  controls.update();
  renderer.render(scene3, camera);
});
window.hub = { snap: () => { renderer.render(scene3, camera); return renderer.domElement.toDataURL("image/png"); }, setCam, replay };

/* ---------------- start ---------------- */
setChecked($$("[data-space]"), b => b.dataset.space === "cart");
setChecked($$("[data-step]"), b => b.dataset.step === "1");
setChecked($$("[data-view]"), b => b.dataset.view === "live");
buildDials(); bg(); resize(); loadScene(); poll(); pollTests();
