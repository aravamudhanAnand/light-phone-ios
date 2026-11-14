# Light Phone mode for iPhone

The [Light Phone](https://www.thelightphone.com/) gets something right: a phone made to
sit in your pocket rather than in your hand. This does the same thing to an iPhone you
already own — no second device needed in order to own less.

The home screen becomes a plain list of app names in large e-ink-style type. No icons,
no colour, nothing moving. One press switches it on. The same press gives you your
ordinary phone back.

![The same iPhone in normal mode and in Light Phone Focus](assets/screenshots/same-phone.png)

Both halves are real captures from my own phone, a minute apart. One widget on one Home
Screen page, selected by a Focus. The generated preview below shows the two colour
schemes:

![The home screen, light and inverted](assets/previews/light-vs-dark.png)

No jailbreak, no app to install besides [Scriptable](https://scriptable.app) (free).

Built and verified on an **iPhone 16, iOS 26.6.2** — both routing paths tapped through
end to end: a row with a native URL scheme, and a row falling back to Shortcuts. Widget
tap handling and Focus behaviour both shift between iOS releases, so treat everything
here as confirmed on that combination and worth re-checking on another.
Everything here is a widget script, a set of generated images, and a configuration
walkthrough.

---

## Why a widget, and not icons

The obvious approach is to give each app a custom icon containing its name, set against
a matching wallpaper so the icon squares disappear. I built that first. It doesn't work,
for a reason that's worth stating plainly:

**A home-screen icon is capped at about 60pt.** A word rendered inside one comes out
*smaller* than the stock app label beneath it, and the 96pt row pitch scatters the words
into a grid. It reads as a sparse page of icons, not a list.

![Widget list next to the icon-tile attempt](assets/previews/widget-vs-tiles.png)

A Large widget gets a ~338×354pt canvas. Nine rows fit at 21pt with tight leading, and
`WidgetStack.url` makes each row its own tap target. That's the whole trick: the Light
Phone look needs a canvas the icon grid can't give you.

The icon-tile assets ship here anyway, under `assets/tiles/`, for anyone who'd rather not
install Scriptable.

---

## What's here

```
widget/LightPhone.js        the widget — edit the TOOLS list and you're done
tools/generate_assets.py    regenerates every image for your own app list
assets/wallpapers/          flat e-ink backgrounds, light and inverted
assets/tiles/               word tiles + blank tiles for the icon route
assets/previews/            the mockups above
docs/SETUP.md               the full walkthrough: Focus, grayscale, Screen Time
docs/URL-SCHEMES.md         how rows route, and how to find schemes for your apps
docs/FIELD-NOTES.md         what building this on a real device turned up
docs/BUILT-WITH-AI.md       the agent-assisted workflow, and where it went wrong
assets/screenshots/         real captures from the phone this runs on
```

---

## Install

Roughly ten minutes.

**1. Shortcuts — only for rows that need them.** Five of the nine default rows open their
app through a native URL scheme and need no setup at all. The other four have no known
scheme, so make one shortcut each — a single `Open App` action — named exactly
`LP Tesla`, `LP Wealthsimple`, `LP Yahoo Finance`, `LP Camera`.

See [docs/URL-SCHEMES.md](docs/URL-SCHEMES.md) to swap in your own apps, including a
ten-second way to test whether an app has a usable scheme.

**2. Widget.** Install Scriptable, add a new script, paste in the *contents* of
[`widget/LightPhone.js`](widget/LightPhone.js), name it `Light Phone`. Add a **Large**
Scriptable widget to an empty Home Screen page and point it at that script.

> On the phone, open the file on GitHub and tap the **copy-raw** button in the file
> toolbar — the two-overlapping-squares icon. Pasting the file's *link* into Scriptable
> gives you `SyntaxError: Unexpected token`, because Scriptable tries to run the URL as
> code.

**3. Wallpaper.** Save `assets/wallpapers/wallpaper-light.png` (or `-dark`) to Photos and
set it as your wallpaper. On a phone, open the file on GitHub and long-press the image to
save it. Turn off Depth Effect and remove every Lock Screen widget.

**4. Focus.** Build a custom Focus that shows only that one Home Screen page and allows
notifications from nobody. Full settings in [docs/SETUP.md](docs/SETUP.md).

**5. Grayscale.** Accessibility → Display & Text Size → Color Filters → Grayscale, then a
Shortcuts automation to flip it with the Focus.

**6. The lock.** Screen Time Downtime with only your nine apps allowed, and a Screen Time
passcode that isn't your device passcode. Without this step the mode is decoration — you
can still swipe to App Library. With it, there's a real gap between impulse and access.

---

## Make it yours

The nine rows that ship here are the ones I actually run. Yours will be different, and
swapping them is a single edit — the rest of the repo follows from this array.

Edit `TOOLS` at the top of `LightPhone.js` — label, shortcut name, optional native URL
scheme. A scheme means one less app launch; `null` routes through Shortcuts instead. See
[docs/URL-SCHEMES.md](docs/URL-SCHEMES.md) for how to find and test one:

```js
const TOOLS = [
  ["PHONE",    "LP Phone",    "mobilephone://"],
  ["NOTES",    "LP Notes",    null],
];
```

Two settings sit above it:

| Setting | Options | Effect |
|---|---|---|
| `MODE` | `"auto"` / `"light"` / `"dark"` | `auto` follows system appearance, so the widget flips with your Focus |
| `FORCE_SHORTCUTS` | `true` / `false` | `false` (default) uses a native scheme where one is defined, falling back to Shortcuts. `true` routes everything through Shortcuts — one launch slower, and inert until every shortcut exists, but immune to Apple retiring a scheme |

Then regenerate the images to match:

```bash
pip install -r requirements.txt
python3 tools/generate_assets.py --words PHONE MESSAGES NOTES MUSIC MAPS
```

The generator picks **one** type size for the whole set, large enough that the longest
word still fits. Sizing each tile independently is what made the first attempt look
ragged. Words over nine characters break onto two balanced lines. `--paper` and `--ink`
take any hex pair, `--wallpaper-size` any `WxH`.

---

## What iOS won't let you automate

Worth knowing before you imagine shipping this as an app:

- **No app can** set your wallpaper, rearrange the Home Screen, create or activate a Focus,
  or toggle grayscale. Those stay manual, which is why step 3 through 5 are instructions
  rather than code.
- **Blocking is the one automatable part**, via `FamilyControls` / `ManagedSettings`. It
  needs Apple's Family Controls distribution entitlement, granted per target and reportedly
  slow to arrive.
- The Shortcuts **Set Wallpaper** action exists but has been unreliable since iOS 18, so
  this repo doesn't lean on it. Pair a wallpaper with a Focus-linked Lock Screen instead.

Tested on iOS 18. Earlier versions lack per-Focus Home Screen pages, which the whole
approach depends on.

## Licence

MIT — see [LICENSE](LICENSE).
