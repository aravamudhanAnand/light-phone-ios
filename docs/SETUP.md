# Light Phone mode — iPhone setup

Allowed tools: Phone · WhatsApp · Spotify · Maps · Tesla · Wealthsimple · Yahoo Finance · Camera · Chrome

## Files

- `../widget/LightPhone.js` — Scriptable widget, the e-ink text list (recommended)
- `../assets/wallpapers/` — flat e-ink backgrounds, light and inverted
- `../assets/tiles/words-light/`, `words-dark/` — word tiles, for the icon route
- `../assets/tiles/blank/` — invisible tiles (match the wallpaper exactly)
- `../assets/previews/` — the mockups
- `../tools/generate_assets.py` — regenerate all of the above for your own app list

## 1. The nine shortcuts

The widget routes every row through Shortcuts, so each app needs one tiny shortcut.
Nine of these, ~20 seconds each: Shortcuts → **+** → **Open App** → pick the app →
rename (top of the screen) → Done. The name must match **exactly**.

| Shortcut name     | Open App → |
|-------------------|------------|
| `LP Phone`         | Phone |
| `LP WhatsApp`      | WhatsApp |
| `LP Spotify`       | Spotify |
| `LP Maps`          | Maps (or Google Maps) |
| `LP Tesla`         | Tesla |
| `LP Wealthsimple`  | Wealthsimple |
| `LP Yahoo Finance` | Yahoo Finance |
| `LP Camera`        | Camera |
| `LP Chrome`        | Chrome |

Turn each one's **Show in Share Sheet** off and **Pin to Search** off so they stay out of
your way (shortcut details → the (i) tab).

To kill the Shortcuts flash on a row once you've confirmed its native scheme works:
set `FORCE_SHORTCUTS = false` at the top of `widget/LightPhone.js`. Rows with a scheme listed
then launch instantly; Tesla, Wealthsimple, Yahoo Finance and Camera keep using
Shortcuts either way — none of them has a documented scheme.

## 2. The screen
1. Install **Scriptable** (free, App Store).
2. Scriptable → **+** → paste the *contents* of `widget/LightPhone.js` → name it `Light Phone`.
   On the phone, use GitHub's **copy-raw** button (two overlapping squares, in the file toolbar)
   or the raw URL. Pasting the *link* gives a `SyntaxError` — Scriptable runs whatever is in the editor.
3. Set `assets/wallpapers/wallpaper-light.png` as wallpaper (Photos → share → Use as Wallpaper). Turn **off** Depth Effect and all Lock Screen widgets.
4. Make a new Home Screen page. Long-press → widget **+** → Scriptable → **Large** → choose script `Light Phone`, "When Interacting: Run Script" off.
5. Remove every icon from that page and empty the Dock (drag icons to another page).

**Appearance.** `MODE` at the top of `widget/LightPhone.js`:

- `"auto"` (default) — paper in Light Mode, inverted in Dark Mode. Because the Focus
  carries an Appearance filter, the widget flips with the Focus on its own.
- `"light"` — always e-ink paper
- `"dark"` — always inverted. True black, so on an OLED screen it costs almost no battery.

The wallpaper doesn't follow appearance the way the widget does, so pick the one matching
how you'll mostly run it (`wallpaper-light.png` / `wallpaper-dark.png` in `assets/wallpapers/`). If you want the
pair to switch together, attach `wallpaper-dark.png` to the Lock Screen you link to the
Focus — a Focus-linked Lock Screen swaps the wallpaper when the Focus turns on.

## 3. Grayscale
- Settings → Accessibility → Display & Text Size → **Color Filters** → on → **Grayscale**
- Settings → Accessibility → **Accessibility Shortcut** → Color Filters (triple-click side button to toggle)

## 4. The Focus
Settings → Focus → **+** → Custom → "Light Phone"
- **Apps / People:** allow notifications from nobody and nothing except the few people who must reach you
- **Customize Screens → Home Screen → Custom Pages:** select only the Light Phone page
- **Lock Screen:** plain black/gray, clock only, no widgets
- **Focus Filters:** Appearance → **Light** for paper, **Dark** for inverted; add **Low Power Mode**
- **Options:** Hide Notification Badges on, Dim Lock Screen on

Shortcuts → Automation → **+** → Focus → Light Phone → *Is turned on* → Run Immediately → **Set Color Filters → On**.
Second automation for *Is turned off* → **Set Color Filters → Off**.

Trigger: Action button → Focus → Light Phone, or a Control Center / Lock Screen control, or a daily schedule.

## 5. The lock (otherwise you just swipe to App Library)
Settings → Screen Time:
- **Downtime** → schedule it → **Block at Downtime** on
- **Always Allowed** → exactly: Phone, WhatsApp, Spotify, Maps, Tesla, Wealthsimple, Yahoo Finance, Camera, Chrome
- **Content & Privacy Restrictions → Allowed Apps → Safari: off**
- Set a **Screen Time passcode different from your device passcode**. Write it on paper. Don't memorise it.

Per-app friction without Screen Time: long-press any app → **Hide and Require Face ID** (removes it from Home Screen *and* Search).

## 6. Finishing touches
- Display & Brightness → **Raise to Wake: off**; Always-On Display off; StandBy off
- Sounds & Haptics → silence everything except the ringtone
- Camera and Wallet are both on the Lock Screen already (swipe left / double-click side button),
  so neither strictly needs a row
