# Field notes

Things that only surfaced once this ran on a real iPhone. Apple documents none of them.

## iOS dims the Home Screen wallpaper. It does not dim widgets.

The widget's background and the wallpaper file are both `#d6d5d0`, so in theory the card
edge should be invisible. On device it wasn't — a faint rounded rectangle sat behind the
nine words.

Sampling a device screenshot, inside the card against the wallpaper beside it:

| Sample | RGB |
|---|---|
| Card interior | `(211, 210, 206)` |
| Wallpaper, same screenshot | `(199, 198, 196)` |

A ~12/255 gap, about 5%, from two files containing identical values. iOS applies a dim to
the Home Screen wallpaper for icon legibility; widget content is composited after it and
is not dimmed.

There is no setting for this, so the widget compensates: `PAPER` is `#cac9c6`, roughly 5%
below the wallpaper's `#d6d5d0`. Matching the two values exactly is what makes the card
visible.

The measurement is a relative comparison within a single screenshot, so it is unaffected
by any scaling applied to the image. The absolute values may be a few points low.

## Color Filters are invisible to screenshots and to iPhone Mirroring

Grayscale is applied at the display layer, after the framebuffer. Screenshots and
mirroring both capture the frame before it, so a phone running in grayscale produces
full-colour screenshots.

This cost real debugging time: the automation was working and the screenshots said it
wasn't. The same applies to Night Shift, True Tone and Reduce White Point. Verify
display-layer settings by looking at the device.

## A Scriptable widget always launches Scriptable before it opens a URL

A widget's URL can only be opened once its host app has started, so every row costs two
app launches: tap → Scriptable → target app.

This cannot be configured away, and it shapes the design rather than being a bug to fix:

- A row with a native URL scheme is **Scriptable → app**
- A row routed through Shortcuts is **Scriptable → Shortcuts → app**

Hence `FORCE_SHORTCUTS`. Setting it to `false` uses a native scheme wherever one is
defined and falls back to Shortcuts only where none exists, removing one launch from
most rows.

Home Screen tiles are not a way out: an icon added by Shortcuts launches Shortcuts, so it
trades the Scriptable flash for a Shortcuts flash and loses the type size that motivated
the widget in the first place. No zero-hop version of this exists on iOS.

## The routing default was wrong, and the symptom was silence

`FORCE_SHORTCUTS` originally defaulted to `true`, so every row pointed at
`shortcuts://run-shortcut?name=LP%20Phone`. That is robust — it never depends on an
undocumented scheme — but it only works once nine shortcuts exist, and until then every
row does nothing except launch Scriptable.

A first run that is silently inert until fifteen minutes of unrelated manual setup is a
bad default however defensible the reasoning. It now defaults to `false`, so five of the
nine rows work immediately with no Shortcuts involvement at all.

## Unticking the widget's Home Screen page deletes it

Hiding a page sends its app icons to the App Library. A widget has nowhere to go, so the
page and the widget are destroyed rather than hidden.

Worse, the hidden state persists. After rebuilding the widget on a new page, the Focus's
"Choose a Home Screen Page" picker still did not list it, and a full restart did not help
— the page had to be re-ticked in the Home Screen page editor first.

Net effect: a page can be shown only in a Focus, or hidden everywhere, but not hidden
normally and shown in a Focus. Page visibility and Focus page selection read from the
same list.

## What a Focus can and cannot do

Hides **pages**, not apps. With a Focus active and a single page selected:

- Swiping left still reaches the full App Library
- Swiping right still reaches Today View, including any news widget
- The Dock is global and unaffected by Focus
- Screen Time Downtime is schedule-driven and cannot be triggered by a Focus

So a Focus removes the *prompt* but not the *access*. The access controls are Screen Time
or per-app "Hide and Require Face ID", and neither follows the Focus.

## Multi-word labels split at the space

The tile generator originally broke any label over nine characters at its midpoint, which
turned `YAHOO FINANCE` into `YAHOO ` / `FINANCE` — the trailing space throwing the
centring off. It now splits at the space nearest the middle and slugifies filenames
(`yahoo-finance.png`).

## Scriptable runs the editor's contents, not a file reference

Pasting the GitHub *link* to `LightPhone.js` into Scriptable yields
`SyntaxError: Unexpected token`. There is no "load from URL" concept — the editor is the
program, and `https://...` parses as JavaScript. Paste the file's contents.
