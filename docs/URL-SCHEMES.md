# URL schemes

Each row in `TOOLS` can open its app in one of two ways:

```js
["SPOTIFY", "LP Spotify", "spotify://"]   // native scheme — one app launch
["TESLA",   "LP Tesla",   null]            // no scheme — routes via Shortcuts
```

A native scheme is one launch faster. Shortcuts always works but needs a shortcut to
exist first. Neither is more correct; pick per row.

## Test any scheme in ten seconds

iOS URL schemes are mostly undocumented, they change, and **any app can register any
scheme** — so a scheme found on the internet is a guess until you try it on your own
device with your own installed apps.

Open Safari, type the scheme into the address bar, press go.

```
spotify://
```

App opens → put the scheme in `TOOLS`. Nothing happens, or Safari searches for it →
leave `null` and make a shortcut.

Do this before trusting anything in the table below.

## Starting points

Verification status is about *documentation*, not about whether it works on your phone.
Test everything.

### Documented by the vendor

| App | Scheme |
|---|---|
| Google Chrome | `googlechrome://` |
| Google Maps | `comgooglemaps://` |

### Widely used, undocumented

These circulate in the Shortcuts and Scriptable communities and generally work, but Apple
publishes none of them and any of them can stop working after an update.

| App | Scheme |
|---|---|
| Phone | `mobilephone://` |
| Messages | `sms://` |
| Apple Maps | `maps://` |
| Clock | `mobiletimer://` |
| Wallet | `shoebox://` |
| Notes | `mobilenotes://` |
| Music | `music://` |
| Photos | `photos-redirect://` |
| WhatsApp | `whatsapp://` |
| Spotify | `spotify://` |

### No scheme known

Camera has no public scheme. Neither do most third-party finance, banking or
manufacturer apps — Tesla, Wealthsimple and Yahoo Finance among them. Use `null` and a
shortcut.

Camera is reachable from the Lock Screen and Control Center anyway, so consider whether
it needs a row at all.

## When there is no scheme

Set the third field to `null` and make a shortcut named to match the second field:

1. Shortcuts → **+**
2. Search `Open App`, add it
3. Tap the **App** placeholder, pick the app
4. Tap the shortcut's name at the top → **Rename** → type the name from `TOOLS` exactly
5. **Done**

Names are matched character for character. `LP Yahoo Finance` — capital F, single spaces.

## The FORCE_SHORTCUTS flag

```js
const FORCE_SHORTCUTS = false;
```

`false` (default) uses a native scheme wherever one is defined, falling back to Shortcuts
where the field is `null`. Fastest, and works for most rows with no setup.

`true` ignores every scheme and routes all nine rows through Shortcuts. Slower by one app
launch, and inert until every shortcut exists — but immune to Apple retiring a scheme.
Worth flipping if a row suddenly stops working.
