// Light Phone — e-ink home screen list for Scriptable
// Add as a LARGE widget. Each row is its own tap target.

// ── Look ──────────────────────────────────────────────────────────────
const PAPER = "#d6d5d0";   // e-ink paper
const INK   = "#141414";   // e-ink ink
const SIZE  = 21;          // row text size

// "auto"  = paper in Light Mode, inverted in Dark Mode (follows the Focus)
// "light" = always e-ink paper
// "dark"  = always inverted  (true black, easiest on an OLED battery)
const MODE = "auto";

// ── Routing ───────────────────────────────────────────────────────────
// true  = every row goes through Shortcuts. Always works. Brief flash of
//         the Shortcuts app on each launch.
// false = use the native URL scheme where one is defined below (instant,
//         no flash), falling back to Shortcuts where it's null.
const FORCE_SHORTCUTS = true;

// [label, shortcut name, native scheme or null]
const TOOLS = [
  ["PHONE",        "LP Phone",        "mobilephone://"],
  ["MESSAGES",     "LP Messages",     "sms://"],
  ["WHATSAPP",     "LP WhatsApp",     "whatsapp://"],
  ["SPOTIFY",      "LP Spotify",      "spotify://"],
  ["MAPS",         "LP Maps",         "maps://"],   // Google: comgooglemaps://
  ["ALARM",        "LP Alarm",        "mobiletimer://"],
  ["WEALTHSIMPLE", "LP Wealthsimple", null],
  ["CAMERA",       "LP Camera",       null],
  ["WALLET",       "LP Wallet",       "shoebox://"],
];

// ── Build ─────────────────────────────────────────────────────────────
const paper = new Color(PAPER);
const ink   = new Color(INK);

let bg, fg;
if (MODE === "dark")       { bg = ink;   fg = paper; }
else if (MODE === "light") { bg = paper; fg = ink;   }
else                       { bg = Color.dynamic(paper, ink);
                             fg = Color.dynamic(ink, paper); }

function target(shortcutName, scheme) {
  if (!FORCE_SHORTCUTS && scheme) return scheme;
  return "shortcuts://run-shortcut?name=" + encodeURIComponent(shortcutName);
}

const w = new ListWidget();
w.backgroundColor = bg;
w.setPadding(14, 18, 14, 18);

for (const [label, shortcutName, scheme] of TOOLS) {
  const row = w.addStack();
  row.layoutHorizontally();
  row.centerAlignContent();
  row.setPadding(4, 0, 4, 0);
  row.url = target(shortcutName, scheme);   // per-row tap target

  const t = row.addText(label);
  t.font = new Font("AvenirNext-Medium", SIZE);
  t.textColor = fg;
  t.leftAlignText();
  t.lineLimit = 1;
  t.minimumScaleFactor = 0.7;

  row.addSpacer();                          // stretch the tap target full width
}

if (config.runsInWidget) Script.setWidget(w);
else await w.presentLarge();                // preview inside Scriptable
Script.complete();
