#!/usr/bin/env node
"use strict";

function usage() {
  process.stdout.write(
    "Usage: node tools/utm_link_builder.js --base <url> --source <src> --medium <med> --campaign <name> [--content <content>] [--term <term>]\n"
  );
}

function getArg(name) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return "";
  return String(process.argv[idx + 1] || "").trim();
}

const base = getArg("--base");
const source = getArg("--source");
const medium = getArg("--medium");
const campaign = getArg("--campaign");
const content = getArg("--content");
const term = getArg("--term");

if (!base || !source || !medium || !campaign) {
  usage();
  process.exit(2);
}

let url;
try {
  url = new URL(base);
} catch (e) {
  process.stderr.write("Invalid --base URL\n");
  process.exit(2);
}

url.searchParams.set("utm_source", source);
url.searchParams.set("utm_medium", medium);
url.searchParams.set("utm_campaign", campaign);
if (content) url.searchParams.set("utm_content", content);
if (term) url.searchParams.set("utm_term", term);

process.stdout.write(`${url.toString()}\n`);
