# Billionaire Box Backing

This workspace now includes a FreeCAD generator that creates a spreadsheet-parameterized replacement backing for the device. The intent is to keep everything easy to resize once you have real caliper measurements.

## Files

- `BillionaireBoxBacking.FCMacro`: FreeCAD macro entry point.
- `freecad_backing_builder.py`: the actual generator logic.
- `BillionaireBoxBacking.FCStd`: your FreeCAD document; open it, then run the macro.

## What The Generator Builds

- A hollow rectangular back shell with a configurable perimeter wall and back wall.
- Six screw towers with stepped bores:
  - a narrow through-hole for the screw threads
  - a larger recessed shaft for the screw head and screwdriver access
- A three-AA side-by-side tray with divider ribs and a wire notch.
- An exterior battery access opening plus a removable battery cover.
- Two low-flex retaining trays:
  - one for the new rectangular PCB
  - one for the breadboard
- A micro-USB flush-mount opening and a simple interior cradle.
- Two visible keep-out boxes so you can place the motor assembly and the legacy PCB before committing to dimensions.

## Coordinate System

- `X`: left to right across the backing
- `Y`: bottom to top across the backing
- `Z`: depth away from the device body
- `Z = 0` starts at the open face that mates against the main body.

## Usage

1. Open `BillionaireBoxBacking.FCStd` in FreeCAD.
2. Run `BillionaireBoxBacking.FCMacro`.
3. FreeCAD will create or update a spreadsheet named `BackingParams`.
4. Edit the values in `BackingParams` from the UI as you collect measurements.
5. Re-run the macro to rebuild the generated geometry.
6. Verify both generated solids:
  - `BackingShell`
  - `BatteryCover`

## Measurements To Replace First

- Overall shell width, height, and depth
- Actual screw shank diameter and screw head diameter
- Remaining material needed so the existing screws still reach the original threaded posts
- Motor keep-out box
- Legacy PCB keep-out box
- Actual sizes for the add-on PCB, breadboard, and USB receiver

## Printing Workflow

The FreeCAD model should normally be exported to `STL` or `3MF`, then sliced in a printer slicer to generate G-code.

Typical flow:

1. Rebuild the part in FreeCAD.
2. Export both `BackingShell` and `BatteryCover` to `STL` or `3MF`.
3. Open those files in PrusaSlicer, OrcaSlicer, Cura, or another slicer.
4. Generate printer-specific G-code there.

## Current Assumptions

- All default values are placeholders.
- The battery tray is a simple printed holder, not a spring-contact battery cassette.
- The battery door is a separate printed part with a guide plug and overlap lip.
- The PCB and breadboard trays use shallow retaining clips with modest overlap to reduce print flex.
- The USB mount is a generic cradle and will likely need dimension tuning once you know the exact receiver body.


### Previous Chat interactions;
Great! I've never used it before, so help walk me through designing this part. I want to design a replacement back for an electronic device - something like a card shuffler. I don't have my calipers handy, so we will want everything to be easy to resize/move later once I get the measurements. The eventual goal is to 3d print the replacement part, so we will want to make sure it can be translated into g-code or whatever.

The backing has the following properties;
* It is rectangular in shape, and can be up to ~2" deep
* It has 3 screwholes on the left and right sides - these are pass thru for the screw, so needs to be recessed enough that the screws (only about 1/2" long) can still reach the threaded post in the main body. The inner diameter will need to be large enough for the threads to pass through, but small enough that the head remains captured.
* It should have room for a battery compartment that contains 3 AA batteries
* It should ahve a mounting bracket for a flushmount micro-usb receiver

In the internal volume between the new backing and the main body there is a pre-existing motor assembly that needs to be avoided. There is also a small rectangular PCB that controls the motor and connects to the battery & a speaker. With the new model we will want to have a dedicated slot for 2 new components, another rectangular PCB and a small breadboard so that the components can be wired together (both PCB need the signal from the button for instance). 



>> Copilot
Awesome—this is a perfect first FreeCAD project because it rewards a clean parametric setup. Since you don’t have calipers yet, we’ll build this as a fully resizable “master model” driven by a Spreadsheet (so you can plug in real dimensions later and everything updates). We’ll also design it so it exports cleanly to STL/3MF → slicer → G-code for 3D printing.

Below is a guided workflow that’s practical and “future-measurements friendly.” I’ll assume FreeCAD 0.21.x+.

0) Quick plan (what we’re actually building)
Think of the backing as a shell + internal features:

Outer back cover: rectangular plate + perimeter wall (up to ~2" deep)
Screw holes (3 on left + 3 on right):
pass-through for threads
captured head via counterbore/countersink
recess so 1/2" screws still reach posts in main body
Battery compartment for 3×AA (either in-line or side-by-side layout)
Flush-mount micro‑USB receiver bracket
Keep-out volumes: motor assembly + existing PCB space
New slots: a second rectangular PCB + a small breadboard (and wire routing)
We’ll model (5) as “dummy solids” and use them as boolean cut/clearance (so nothing collides).

1) Start the project the right way (parametric from day 1)
1.1 Create a new file and set units
Edit → Preferences → General → Units: set to mm
(Even if you think in inches, printing + CAD is much easier in mm.)
1.2 Add a Spreadsheet (your “parameter panel”)
Switch to Spreadsheet workbench
Create New Spreadsheet
Rename it to: Params
Now we’ll define key parameters. Don’t worry about perfect numbers yet—use placeholders that are easy to revise later.

Suggested starter parameters (placeholders)
In the spreadsheet, enter these labels/values (Column A = name, Column B = value).
Then alias each name (right click cell → Properties → Alias) so we can refer to it in expressions.

Use values like:

L = 160 mm (overall length)
W = 80 mm (overall width)
Depth = 50 mm (≈ 2")
Wall = 2.4 mm (typical printed wall)
Floor = 2.0 mm (base thickness)
Clearance = 0.4 mm (general component clearance)
ScrewEdgeOffset = 10 mm (hole centers from edge)
ScrewSpacing1 = 25 mm
ScrewSpacing2 = 25 mm
(gives 3 holes vertically: offset + spacing1 + spacing2)
ScrewPassDia = 3.4 mm (for M3-ish—placeholder)
HeadDia = 6.5 mm (placeholder head capture)
HeadDepth = 2.0 mm (counterbore depth)
Battery placeholders:

AA_Dia = 14.5 mm
AA_Len = 50.5 mm
BattWall = 2.0 mm
BattClear = 0.6 mm
PCB/breadboard placeholders:

PCB1_L / PCB1_W / PCB1_T (existing board)
PCB2_L / PCB2_W / PCB2_T (new board)
BB_L / BB_W / BB_T (breadboard)
Micro‑USB bracket placeholders:

USB_W = 8.0 mm
USB_H = 3.5 mm
USB_T = 7.0 mm (depth behind face)
USB_Clear = 0.4 mm
✅ Goal: everything in the model references Spreadsheet.Params values, not fixed dimensions.

2) Build the outer shell (Part Design: clean + printable)
2.1 Create the main Body
Switch to Part Design
Create New Body
Create New Sketch on the XY plane (this is your back face)
2.2 Sketch the rectangle (fully constrained)
Draw a rectangle centered on origin (use Rectangle tool)
Constrain it:
Horizontal length = Params.L
Vertical width = Params.W
Center it on origin (symmetry constraints or set midpoint coincident to origin)
Close sketch.

2.3 Create the base plate
Use Pad
Pad length = Params.Floor
Now we have a plate.

2.4 Create the perimeter wall
You have two clean options:

Option A (recommended): Sketch offset and Pad

Select the top face of the plate → New Sketch
Use External Geometry to reference the outer edges
Create an inner rectangle offset inward:
Use constraints so inner dims are:
L - 2*Wall
W - 2*Wall
Close sketch
Use Pad with "Up to face"? Not ideal here.
Better: Pad height = Params.Depth
Then Pocket the interior to create the hollow cavity:
To hollow:

Select the top face (of the wall) → New Sketch
Reference edges and sketch a rectangle:
L - 2*Wall
W - 2*Wall
Pocket depth = Params.Depth (or “Through all” downward)
Option B: Thickness tool

Model a solid block, then use Part → Thickness to shell it
(Sometimes fragile; Option A is more predictable for first-time users.)
At this point: you have a box-like backing: floor + walls.

3) Add screw holes with captured heads (parametric + robust)
We’ll do this using Hole feature (preferred) or sketch+pocket.

3.1 Decide hole layout (left and right, 3 each)
We’ll place 3 on left wall and mirror them to right.

Select the inner face of the left wall (or the outer face—depends where you want recess)
Create New Sketch
Sketch one vertical line of 3 points
Create 3 construction points aligned vertically
Constrain:
X offset from left edge = Params.ScrewEdgeOffset
Y positions:
bottom = Params.ScrewEdgeOffset
middle = Params.ScrewEdgeOffset + Params.ScrewSpacing1
top = Params.ScrewEdgeOffset + Params.ScrewSpacing1 + Params.ScrewSpacing2
Close sketch.

3.2 Use Hole feature (pass-through + counterbore)
Select sketch points
Use Hole:
Type: Counterbore (for captured head)
Hole diameter = Params.ScrewPassDia
Counterbore diameter = Params.HeadDia
Counterbore depth = Params.HeadDepth
Depth: Through all
This creates:

pass-through channel for threads
recessed pocket capturing head
doesn’t overcomplicate the sketch
3.3 Mirror to other side
Use Part Design → Mirror
Mirror plane: YZ plane
Select the Hole feature to mirror
✅ Now you have 6 holes total, fully parametric.

Note on the “recess enough that 1/2” screw reaches post”:
This is why counterbore depth should match the head height (and not be too deep). Later, when you measure:

screw length S
cover thickness at hole T
recess depth R
required engagement E You want: S ≥ (T - R) + E
We’ll set HeadDepth after measuring.
4) Battery compartment for 3×AA (print-friendly)
There are many ways; simplest is a tray that accepts a premade spring-contact holder, or a custom cradle.

Since you want adaptability and we lack measurements, I recommend:

Approach: make a battery bay volume + mounting bosses
Create a simple rectangular bay sized to a common 3×AA holder footprint OR a custom cradle for 3 cylinders.
Option A (most practical): design for an off-the-shelf 3×AA holder
Pros: easier wiring, reliable contacts, fewer print tolerances. We’ll do:

a rectangular pocket (depth) + strap tabs or screw standoffs.
Option B: print a cradle for 3 AA cylinders
Pros: all-in-one
Cons: you still need contacts, and tolerances matter.

Given your goal (functional replacement cover), I’d start with Option A.

4.1 Build a “battery bay” cut
On the inside face of the floor plate, create a New Sketch
Draw a rectangle where the battery compartment should sit
Constrain its size with spreadsheet parameters:
BattBay_L, BattBay_W, BattBay_Depth (add these)
Pocket it down into the interior space (not through the floor):
Pocket depth = BattBay_Depth
4.2 Add mounting tabs/bosses
Add 2–4 standoffs:
cylinders with pilot holes (if holder screws in)
or flexible clips (later)
For now: do standoffs (easiest to tune later).

5) Bracket for flush-mount micro‑USB receiver
We’ll do a cutout + retention bracket.

5.1 Pick a side
Typically micro‑USB access is on a short edge. Choose where it exits.

5.2 Create a “port cutout” sketch
Select the appropriate wall face → New Sketch
Draw a rectangle (port opening)
Constrain size:
width = USB_W + 2*USB_Clear
height = USB_H + 2*USB_Clear
Position it using offsets from edges (parameters like USB_OffsetFromBottom, USB_OffsetFromSide)
5.3 Pocket through the wall
Pocket: Through all (wall thickness)
5.4 Add a bracket ledge (internal)
Make a small internal shelf so the receiver sits flush and doesn’t slide inward:

On inside wall face, sketch a ledge profile and Pad inward
Or add two small “ears” that pinch the receiver body
Keep it simple now; later you can refine once you measure the receiver.

6) Model the internal “no-go zones” (motor + existing PCB)
This is a huge trick for clean design.

6.1 Create a separate Body called Keepouts
New Body → Keepouts
Create simple shapes representing:
motor assembly volume (box/cylinder union)
existing PCB (simple rectangular prism)
Dimension these with rough placeholders:
Motor_L/W/H
PCB1_L/W/T
6.2 Use them to cut clearance from the cover
Back in your main cover body:

Use Part Design → Subtractive Boolean
Select Keepouts solids
Add an extra clearance offset by making keepouts slightly larger (+ Clearance)
Now your cover can’t accidentally intersect the motor.

7) Add slots for the new PCB + breadboard
7.1 Slot design pattern
For each component, we want:

a base shelf (supports the board)
side rails or a pocket (guides board)
optional: zip-tie holes or screw bosses
Start with rails (printable, tolerant).

7.2 PCB rails
Sketch two long thin rectangles as rails
Pad them up from the floor
Space them to fit PCB2_T + Clearance plus board thickness
7.3 Breadboard pocket
Breadboards vary—so do a rectangular pocket:

Pocket depth ~ 1–2mm so it “keys in”
Include clearance on all sides
7.4 Wire routing channels
Add:

small rectangular channels from battery bay to PCBs
channel from button input area to both boards These can be simple pockets (1.5–2mm deep).
8) Make it printable (critical print constraints)
For FDM printing, add these guidelines to your params (so easy to revise):

Wall: 2.0–2.8mm (multiple of nozzle width is nice: 0.4mm nozzle → 2.4mm = 6 lines)
Floor: 1.6–2.4mm
Fillets: add fillets to reduce stress cracking (especially around screw holes)
Overhangs:
Avoid internal overhangs > 45° unless you plan supports
Use chamfers instead of flat ledges where possible
Screw bosses:
Add ribs if posts are tall (prevents snapping)
Clearance:
printed fit: 0.2–0.5mm depending on printer
9) Export to slicer → G-code
FreeCAD doesn’t generate G-code directly (unless you use Path workbench for CNC). For 3D printing:

Select the final Body
File → Export → STL (or 3MF)
Open in your slicer (PrusaSlicer/Cura/OrcaSlicer)
Slice → export G-code
Tip: Keep the part as one solid manifold body before export.

What I need from you (minimal, to place things sensibly)
Even without calipers, a few “relative” decisions help:

Battery layout:
In-line (3 in a row) or side-by-side (more compact width, more height)?
Where is the micro‑USB opening relative to the device?
On a long edge or short edge?
Screw hole arrangement:
Are the 3 holes vertically aligned on each side, or are they offset?
Do you expect the back to be flat externally, or can it have a bulge for the batteries?
If you answer those 4, I can give you:

a concrete parameter list to paste into your Spreadsheet
an exact modeling sequence (feature tree order) that won’t topo-break later
and a “first-pass” printable geometry plan optimized to be re-measurement-friendly.
Also: what printer/nozzle size are you using (0.4mm typical)? That affects wall defaults.