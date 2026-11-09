> **Superseded on 9 Nov 2026.** The road-sign world below was replaced by a mainstream consumer-app style (see PRODUCT.md, Brand Commitments, and the tokens in `web/ruko.css`, which are the source of truth). Regenerate this file before relying on it.

---
name: Ruko
description: A live scam-call guard that warns before the scammer's next move, drawn as Indian road warning signs.
colors:
  asphalt: "#26282b"
  asphalt-raised: "#303337"
  asphalt-line: "#45494e"
  sign-white: "#fafaf7"
  sign-white-band: "#efeee8"
  sign-line: "#cfcdc4"
  ink: "#141414"
  ink-muted: "#4a4c50"
  stop-red: "#c8102e"
  stop-red-ink: "#a30d25"
  stop-red-dark-mode: "#e0233f"
  hazard-yellow: "#ffc20e"
  hazard-yellow-hover: "#ffd34d"
  hazard-yellow-ink: "#6b4f00"
  safe-green: "#1f7a45"
  safe-green-dark-mode: "#3fbf74"
  night-ground: "#1c1d20"
  night-text: "#f1f0ea"
  night-muted: "#b4b2aa"
typography:
  display:
    fontFamily: "Overpass, Mukta, system-ui, sans-serif"
    fontSize: "clamp(2.6rem, 6.2vw, 4.9rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Overpass, Mukta, system-ui, sans-serif"
    fontSize: "clamp(2rem, 4.4vw, 3.2rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Overpass, Mukta, system-ui, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Overpass, Mukta, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "tnum"
  label:
    fontFamily: "Overpass, Mukta, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 800
    lineHeight: 1.25
  body-hi:
    fontFamily: "Mukta, Overpass, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
rounded:
  sign: "4px"
  plate: "6px"
  board: "8px"
spacing:
  xs: "6px"
  sm: "10px"
  md: "14px"
  lg: "22px"
  section: "clamp(64px, 9vw, 112px)"
components:
  button-primary:
    backgroundColor: "{colors.hazard-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    padding: "0 22px"
    height: "52px"
  button-primary-hover:
    backgroundColor: "{colors.hazard-yellow-hover}"
  button-danger:
    backgroundColor: "{colors.stop-red}"
    textColor: "{colors.sign-white}"
    rounded: "{rounded.sign}"
    padding: "0 22px"
    height: "52px"
  button-ghost:
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    padding: "0 22px"
    height: "52px"
  button-ghost-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.sign-white}"
  button-dark:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.hazard-yellow}"
    rounded: "{rounded.sign}"
    padding: "0 22px"
    height: "52px"
  panel:
    backgroundColor: "{colors.sign-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    padding: "22px"
  hero-plate:
    backgroundColor: "{colors.sign-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.plate}"
    padding: "clamp(24px, 4vw, 44px)"
  ahead-plate:
    backgroundColor: "{colors.hazard-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    padding: "12px 14px"
  ahead-plate-now:
    backgroundColor: "{colors.stop-red}"
    textColor: "{colors.sign-white}"
  field:
    backgroundColor: "{colors.sign-white-band}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
    padding: "12px"
  destination-board:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.night-text}"
    rounded: "{rounded.board}"
    padding: "10px 24px"
---

# Design System: Ruko

## Overview

**Creative North Star: "The Sign Before the Bend"**

Ruko is drawn as Indian road warning signs. A warning sign tells you what is ahead before you reach it; Ruko does the same for the scammer's next move. The page is a road: asphalt bands carry the road and its signs, sign-white bands carry the reading, and a hazard-chevron strip marks the edge between them. Every container is a sign plate (flat, square-ish, with a thin inner rule) and every colour is one of the four sign inks: white, red, yellow, black.

Meaning is carried by colour, not decoration. Red means it is happening now. Yellow means it is ahead, and it is also the colour of the thing you should press. The scam playbook is shown as four cautionary triangles that start unlit (a dashed ghost outline) and light up in sequence (white fill, red edge) as the call moves through them, ending at a red STOP octagon, the brand mark. The persuasive landing uses full asphalt and sign bands; the guard app and family screen keep the same inks and plates in a quieter, single-column register.

The surface is flat. Depth comes from inset rules and the contrast between asphalt and sign-white, never from soft shadows, glass or decorative gradients. Type is heavy Overpass (Highway Gothic lineage) for display and UI, with Mukta carrying Devanagari when the EN/HI toggle is on Hindi.

**Key Characteristics:**
- Asphalt grounds, sign-white reading bands, hazard-chevron strips between them.
- Red only for "now"; yellow for "ahead" and the primary action.
- Cautionary triangles (unlit dashed ghost, lit white with red edge) and a STOP octagon mark.
- Flat sign plates with 4px corners and inset double rules.
- Heavy Overpass (800-900) headings, tabular numerals everywhere, Mukta for Hindi.

## Colors

Four sign inks on two grounds: asphalt for the road, sign-white for reading.

### Primary
- **Stop Red** (stop-red): what is happening now. The lit sign edge, the STOP octagon, the full-screen takeover, the danger button, flagged captions and their marked words, the "now" state of the ahead plate, and the family screen when a call turns dangerous. On dark Operate surfaces it brightens to stop-red-dark-mode for legibility. Stop-red-ink is red text on white (takeover button label).

### Secondary
- **Hazard Yellow** (hazard-yellow): what is ahead, and what to press. The primary button, the ahead plate, the hazard chevrons, focus rings, text selection, list markers on asphalt (ticks, diamonds), the listening rule inside the guard octagon, and the one fully yellow setup band. Hazard-yellow-ink is the "watch" risk level as text on light grounds.

### Tertiary
- **Safe Green** (safe-green): the guard is listening and the call is calm. Used for the listening octagon fill, the connected dot and the low risk level only; never decorative. Brightens to safe-green-dark-mode in OS dark mode.

### Neutral
- **Asphalt** (asphalt): the road. Landing nav, hero, family band, footer; the app and family header bars; the guard octagon at rest; code blocks.
- **Asphalt Raised / Asphalt Line** (asphalt-raised, asphalt-line): rules and borders on asphalt.
- **Sign White** (sign-white): sign plates, panels, the hero plate, the proof band, the pressed language option.
- **Sign White Band** (sign-white-band): the page ground under panels, field fills, caption rows.
- **Sign Line** (sign-line): hairlines and the unlit triangle edge on light grounds.
- **Ink / Ink Muted** (ink, ink-muted): text on sign-white and yellow; the destination board ground.
- **Night ground, text, muted** (night-ground, night-text, night-muted): the Operate surfaces' OS dark-mode remap of ground, text and secondary text.

### Named Rules
**The Red Means Now Rule.** Stop red is used only for something happening in this call at this moment. Upcoming danger is yellow. If nothing is happening, no red is on screen except the octagon brand mark.

**The Yellow Is Ahead Rule.** Hazard yellow marks what comes next: the predicted next move, and the next action to take. A yellow plate always says what is ahead or what to do.

**The Sign Band Rule.** On the landing, reading bands stay sign-white in OS dark mode (they reset the tokens locally to light). The asphalt and sign rhythm is the page's structure, not a theme. Only the Operate surfaces (app, family) remap to the night palette.

## Typography

**Display Font:** Overpass, variable 400-900, self-hosted latin (with Mukta, system-ui)
**Body Font:** Overpass (with Mukta, system-ui)
**Devanagari Font:** Mukta 400/600/800, self-hosted latin and devanagari; it becomes the lead family when the page language is Hindi.

**Character:** Overpass descends from Highway Gothic, so headings read like sign legends: heavy, tight and plain. Mukta matches its weight and openness for Hindi.

### Hierarchy
- **Display** (800, clamp(2.6rem, 6.2vw, 4.9rem), 0.98): the hero headline on the white plate. Its second line drops to 0.58em in ink-muted.
- **Headline** (800, clamp(2rem, 4.4vw, 3.2rem), 1.05): section headings, max 20ch. The takeover uses its own clamp(2.25rem, 10vw, 3.25rem) at line-height 1.
- **Title** (800, 1.3rem): playbook step names, board entries (900), app section heads at 1.2rem.
- **Body** (400, 17px, 1.55): running text; ledes at 1.12-1.15rem, max 46-60ch.
- **Label** (700-800, 0.82-0.95rem): call header, connection state, risk level, table heads, sign names under triangles (600, 0.8rem).

### Named Rules
**The Heavy Legend Rule.** Headings and buttons are 800-900 weight with negative tracking (-0.01 to -0.035em). Nothing in the UI is set light or thin.

**The Tabular Rule.** The body sets tabular numerals globally so numbers in results, timelines and risk levels line up.

## Layout

The landing alternates full-bleed bands: asphalt (nav, hero, family, footer), sign-white (playbook, features, proof, business) and one hazard-yellow setup band. Content sits in a 1160px wrap with 20px gutters; bands pad clamp(64px, 9vw, 112px) vertically. Grids are two columns (hero 1.05fr/1fr, family, proof, business) collapsing to one column at 900px; the playbook strip runs four columns separated by 2px vertical rules and becomes a sign-left list on mobile. On mobile the hero's road moves above the plate.

The guard app and family screen are a single 640px column with 14px gaps between panels, an asphalt header bar respecting the safe-area inset, and one job on screen at a time: the stop octagon first, then the signs.

Spacing steps on 6 / 10 / 14 / 22px inside components.

## Elevation & Depth

Flat. There are no ambient or drop shadows. Depth is conveyed by ground contrast (sign-white plate on asphalt, panel on band) and by inset rules drawn with `box-shadow: inset`: a 1px line on panels, a 2px rule on flagged captions and dialogs, and a double rule (ground-coloured gap then ink line) on the hero plate, primary button and destination board, which reads as the border inside a real sign.

### Shadow Vocabulary
- **Panel rule** (`box-shadow: inset 0 0 0 1px var(--line)`): every sign panel.
- **Sign double rule** (`box-shadow: inset 0 0 0 3px var(--sign), inset 0 0 0 5px var(--ink)`): the hero plate; the primary button uses 2px/4px in yellow then ink.
- **Alert rule** (`box-shadow: inset 0 0 0 2px var(--red)`): flagged caption rows; the family status uses 3px yellow when live and 3px white on red when in danger.

### Named Rules
**The Inner Border Rule.** Edges are drawn inside the plate, as on a road sign. Never lift a surface off the ground with a blur.

## Shapes

Square-ish sign plates: 4px corners on buttons, panels, fields, captions, plates and dialogs; 6px on the hero plate, the call box and code blocks; 8px on the destination board. Full circles only for status dots. Phone mockups use 26px corners with a hard 7px bezel ring, standing for the device rather than for the world.

Sign geometry carries meaning: the cautionary triangle (playbook stages, the ahead icon), the STOP octagon (brand mark, takeover, guard button) and the hazard chevron (band divider, a 22px ink strip with yellow chevrons repeating every 24px). Small 45-degree yellow diamonds with an ink ring mark the fact list. Disclosure carets and tick marks are drawn from CSS borders.

## Components

### Buttons
Sign plates you press: heavy, square-ish, 52px tall.
- **Shape:** 4px corners, 2px border in the current colour.
- **Primary:** hazard yellow with ink text and a yellow-then-ink inset double rule; hover lightens to hazard-yellow-hover.
- **Danger:** stop red with white text; reserved for cutting a call or calling 1930.
- **Ghost:** ink border on sign-white; hover and pressed fill ink with sign-white text.
- **Dark:** ink with yellow text, used on the yellow band.
- **Plain:** sign-line border, which darkens to the text colour on hover.
- **States:** 1px press-down on active; 3px hazard-yellow focus outline offset 3px.

### Cards / Containers
- **Panel:** sign-white, 4px corners, 22px padding, 1px inset rule.
- **Hero plate:** sign-white on asphalt, 6px corners, inset double rule.
- **Destination board:** ink ground, 8px corners, inset white double rule, rows of name / description / yellow tag split by 1px lines, like a highway direction board.

### Inputs / Fields
- **Style:** 2px sign-line border, 4px corners, 12px padding, filled with the band colour.
- **Focus:** the border turns to the text colour. Checkboxes are 22px with ink accent.

### Navigation
Sticky asphalt bar, 68px tall, with the octagon logo (900 weight), 700-weight links in a muted sign-white that brighten on hover, the EN/HI toggle and a compact 44px primary button. Links hide below 900px; the CTA hides below 520px.

### Language Toggle
A 2px bordered segmented pair (EN / हि); the pressed option fills sign-white with ink text, in either ground.

### Playbook Signs (signature)
Cautionary triangles generated as SVG (viewBox 100x90) with an inner glyph. Unlit: no fill, a 7px dashed edge in the line colour, glyph in the line colour, muted label. Lit: white fill, solid stop-red edge, ink glyph, full-colour label, entering with a 0.45s scale-in (disabled under reduced motion). Four sit in a row.

### Ahead Plate (signature)
A hazard-yellow plate with an outlined warning-triangle icon and the predicted next move in 700 weight. When the move is happening it turns stop red with white text. Hidden when empty.

### STOP Octagon and Takeover (signature)
The brand mark is a red octagon with a white inner rule and a 900-weight legend. In the app it is the guard button: asphalt at rest with a yellow rule, safe green with a breathing white rule while listening, red in danger. The takeover is a full-screen stop-red field with the octagon, a headline, a white button with red text and an outlined secondary; it can flash three times (disabled under reduced motion).

### Live Captions
Rows on the band colour with 4px corners; a flagged row gets a 2px red inset rule, and the flagged words are red, 800 weight, underlined. On the landing's asphalt they sit in a near-black call box.

## Do's and Don'ts

### Do:
- **Do** put the road on asphalt and the reading on sign-white, and divide them with the hazard-chevron strip.
- **Do** reserve stop red for "happening now" and hazard yellow for "ahead" and the primary action.
- **Do** draw edges as inset rules inside the plate, with 4px corners.
- **Do** show the playbook as cautionary triangles that light from dashed ghost to white with a red edge.
- **Do** set headings and buttons in Overpass at 800-900 and switch to Mukta for Hindi.
- **Do** keep landing reading bands light in OS dark mode; remap only the Operate surfaces.
- **Do** honour reduced motion for every sign light, flash, blink and breathe.

### Don't:
- **Don't** use soft drop shadows, glass or backdrop blur; depth is inset rules and ground contrast.
- **Don't** use decorative colour gradients. Diagonal hazard stripes, as on the setup band, are sign material and allowed.
- **Don't** use red for a warning about the future, or for decoration.
- **Don't** round plates beyond 8px or make pill buttons.
- **Don't** introduce colours outside the four sign inks, the two grounds and the safe green.
