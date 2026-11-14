# Built with an AI agent

This repo was built end to end in conversation with an LLM coding agent. The commit
trailers say so. This page says what that was actually like, because the interesting part
is not that an AI was used — it is where it failed, and what caught it.

## The division of labour

The agent wrote the widget, the generator and the documentation, and proposed every
configuration step. I ran all of it on an iPhone and reported what happened. Nothing
entered the repo as fact until it had been observed on hardware.

That division mattered more than I expected. The agent cannot see the screen, cannot tap
anything, and has no way to tell a thing that works from a thing that sounds like it
works.

## Four times it was confidently wrong

### Grayscale "wasn't firing"

Focus on, automation configured correctly, every screenshot in full colour. The agent
diagnosed a broken Shortcuts automation, and we worked through the trigger, the action
value and the filter type.

The cause was that **Color Filters are applied below the framebuffer**, so screenshots
and iPhone Mirroring never capture them. Grayscale had been working the entire time.

Caught by looking at the actual phone.

The agent was reasoning carefully about an input that was systematically lying to it. It
had no way to know the capture pipeline drops that layer — and neither did I, until the
device and the screenshot disagreed.

### "Untick the page to hide it"

I asked how to hide the widget's page in normal mode. The agent said a Focus's Custom
Pages setting would override page visibility, so unticking it was safe.

It was not. Hiding a page sends its app icons to the App Library, but a widget has
nowhere to go, so **the page and the widget were destroyed**. The hidden state then
survived a full restart, and the Focus page picker stayed empty afterwards — which looked
like an entirely different bug.

Caught by the widget disappearing.

The failure here was not the wrong answer. It was the absent uncertainty: a guess about
platform behaviour, delivered without hedging, attached to a destructive action.

### A default that did nothing

`FORCE_SHORTCUTS` originally shipped as `true`, routing every row through Shortcuts so it
never depended on an undocumented URL scheme. The reasoning is sound.

It also meant **nothing worked until nine shortcuts existed**, and the symptom of their
absence was silence — a tap opened Scriptable and stopped there. We went through widget
configuration, Scriptable's tap semantics and iOS link handling before the actual cause
surfaced: the shortcuts had never been created.

Caught by me saying "I didn't create the shortcuts."

The agent optimised for robustness and never asked what the first run looks like to
someone who has done nothing yet. It also debugged downward into the code rather than
upward into its own assumptions.

### Three wrong theories about one failure

For that same tap failure, the agent proposed, in order: the widget's `When Interacting`
setting was wrong; per-row links were unsupported on this iOS version; the page needed an
app icon to register. It searched the web and cited sources for the first.

All three were wrong. The setting was already correct, per-row links work, and the page
needed nothing.

Fluent, well-sourced and wrong. The citations raised the confidence of the explanation
without raising its accuracy.

## What it was good at

- **Producing and revising artefacts quickly.** The widget, the generator and every
  document here were written, rewritten and re-scoped as the facts changed, without the
  friction that usually stops documentation from keeping up.
- **Measurement.** The wallpaper-dimming constraint was found by sampling a device
  screenshot and comparing the widget against the background beside it — a 12/255 gap
  from two files holding identical values. That turned "it looks slightly off" into a
  number and a one-line fix.
- **Bookkeeping after a correction.** When a claim turned out to be false it came out of
  the README rather than being quietly softened, and the reasoning went into the commit
  message.

## The takeaway

The agent was fastest at producing things and weakest at knowing whether they were true.
Everything in this repo that is now reliable became reliable because it was run on a
phone and the result contradicted something.

If there is a transferable lesson, it is that the verification layer is the product.
Generation is the cheap part.
