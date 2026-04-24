#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const target = path.join(ROOT, "index.next.html");
const required = [
  "window.GLBFunnel",
  "checkout_success",
  "purchase_success",
  "payment_cta_click",
  "NEXTBASE_TRAVEL_MODE_FULL",
  "id=\"tr-run\"",
  "id=\"glb-mic-btn\"",
  "id=\"t-btn-monthly\"",
  "id=\"link-manage-mini\"",
  "id=\"link-cancel-mini\"",
];

if (!fs.existsSync(target)) {
  process.stderr.write("missing index.next.html\n");
  process.exit(2);
}

const html = fs.readFileSync(target, "utf8");
const missing = required.filter((k) => !html.includes(k));

const maintPath = path.join(ROOT, "glb_maintenance.json");
let maintOk = true;
let maintErr = "";
if (!fs.existsSync(maintPath)) {
  maintOk = false;
  maintErr = "missing glb_maintenance.json";
} else {
  try {
    JSON.parse(fs.readFileSync(maintPath, "utf8"));
  } catch (e) {
    maintOk = false;
    maintErr = "invalid glb_maintenance.json";
  }
}

const report = {
  status: missing.length === 0 && maintOk ? "PASS" : "HOLD",
  missing,
  checked: required,
  maintenance_switch: { ok: maintOk, detail: maintErr || "ok" },
  ts_utc: new Date().toISOString(),
};

process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (missing.length > 0 || !maintOk) process.exit(2);
