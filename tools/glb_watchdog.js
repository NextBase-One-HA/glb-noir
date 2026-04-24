#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const INDEX_NEXT = path.join(ROOT, "index.next.html");
const PAIR_TABLE = path.join(ROOT, "canonical", "language_pair_table.json");
const TRAVEL_CATEGORIES = path.join(ROOT, "canonical", "travel_categories.json");
const LOG_DIR = path.join(ROOT, "logs");
const LATEST_REPORT = path.join(LOG_DIR, "watchdog.latest.json");
const EVENTS_LOG = path.join(LOG_DIR, "watchdog.events.jsonl");

const REQUIRED_SNIPPETS = [
  'id="tr-run"',
  'id="glb-mic-btn"',
  'id="glb-quick-speak"',
  "window.GLBFunnel",
  "summary: function",
];

const FORBIDDEN_SNIPPETS = [
  "micBtn.style.display = 'none'",
  'micBtn.style.display = "none"',
];

function ensureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function safeWrite(p, body) {
  const tmp = `${p}.tmp`;
  fs.writeFileSync(tmp, body, "utf8");
  fs.renameSync(tmp, p);
}

function nowIso() {
  return new Date().toISOString();
}

function hashFileSha256(filePath) {
  const crypto = require("crypto");
  const data = fs.readFileSync(filePath);
  return crypto.createHash("sha256").update(data).digest("hex");
}

function runChecks() {
  const errors = [];
  const warnings = [];
  const details = {};

  if (!fs.existsSync(INDEX_NEXT)) {
    errors.push("missing:index.next.html");
  } else {
    const html = fs.readFileSync(INDEX_NEXT, "utf8");
    details.index_next_sha256 = hashFileSha256(INDEX_NEXT);
    for (const s of REQUIRED_SNIPPETS) {
      if (!html.includes(s)) errors.push(`missing_required_snippet:${s}`);
    }
    for (const s of FORBIDDEN_SNIPPETS) {
      if (html.includes(s)) errors.push(`forbidden_snippet:${s}`);
    }
  }

  for (const p of [PAIR_TABLE, TRAVEL_CATEGORIES]) {
    if (!fs.existsSync(p)) {
      errors.push(`missing:${path.relative(ROOT, p)}`);
      continue;
    }
    try {
      const obj = readJson(p);
      if (p === PAIR_TABLE && (typeof obj !== "object" || Array.isArray(obj))) {
        errors.push("invalid_pair_table_shape");
      }
      if (p === TRAVEL_CATEGORIES && !Array.isArray(obj)) {
        errors.push("invalid_travel_categories_shape");
      }
      details[`${path.basename(p)}_sha256`] = hashFileSha256(p);
    } catch (e) {
      errors.push(`invalid_json:${path.relative(ROOT, p)}`);
    }
  }

  if (errors.length === 0) {
    warnings.push("watchdog_pass");
  }
  return {
    ts_utc: nowIso(),
    status: errors.length === 0 ? "PASS" : "HOLD",
    errors,
    warnings,
    details,
  };
}

function applySafeAutofix() {
  if (!fs.existsSync(INDEX_NEXT)) return { changed: false, changes: [] };
  let html = fs.readFileSync(INDEX_NEXT, "utf8");
  const changes = [];
  for (const s of FORBIDDEN_SNIPPETS) {
    if (html.includes(s)) {
      html = html.split(s).join("// watchdog removed hidden-mic fallback");
      changes.push(`removed:${s}`);
    }
  }
  if (changes.length > 0) {
    safeWrite(INDEX_NEXT, html);
    return { changed: true, changes };
  }
  return { changed: false, changes: [] };
}

function persistReport(report) {
  ensureDir(LOG_DIR);
  safeWrite(LATEST_REPORT, `${JSON.stringify(report, null, 2)}\n`);
  fs.appendFileSync(EVENTS_LOG, `${JSON.stringify(report)}\n`, "utf8");
}

function runOnce({ autofix }) {
  const fix = autofix ? applySafeAutofix() : { changed: false, changes: [] };
  const report = runChecks();
  if (fix.changed) {
    report.autofix = { applied: true, changes: fix.changes };
  }
  persistReport(report);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (report.status !== "PASS") process.exitCode = 2;
}

function watchMode({ autofix, intervalMs }) {
  runOnce({ autofix });
  let running = false;
  let pending = false;
  const trigger = () => {
    if (running) {
      pending = true;
      return;
    }
    running = true;
    try {
      runOnce({ autofix });
    } finally {
      running = false;
      if (pending) {
        pending = false;
        setTimeout(trigger, 100);
      }
    }
  };
  const watchTargets = [
    INDEX_NEXT,
    path.join(ROOT, "canonical"),
  ];
  for (const target of watchTargets) {
    if (!fs.existsSync(target)) continue;
    fs.watch(target, { recursive: true }, () => {
      setTimeout(trigger, intervalMs);
    });
  }
  process.stdout.write(
    `[watchdog] watching GLB files (autofix=${autofix ? "on" : "off"})\n`
  );
  setInterval(() => {}, 1 << 30);
}

function parseArgs(argv) {
  const args = new Set(argv.slice(2));
  const noAutofix = args.has("--no-autofix");
  return {
    watch: args.has("--watch"),
    // Default is immediate fix. Use --no-autofix only when debugging.
    autofix: noAutofix ? false : true,
    intervalMs: 250,
  };
}

const opts = parseArgs(process.argv);
if (opts.watch) {
  watchMode(opts);
} else {
  runOnce(opts);
}
