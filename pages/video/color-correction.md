---
layout: default
---

# Setup Workspace

It's easier to color correct if you make the selection follow playhead. `Sequence > Selection Follows Playhead` in the top menu.

Open up `Lumetri Scopes` in the Color workspace. You want the `Vectorscope YUV` and the `Waveform (Luma)` open. These show you the color saturation and the exposure. To make them show up you `Rt click` within the scopes window and select them.

For comparing two shots use the comparison view, which is in the program viewer next to my proxies button.

# General Notes

There are technical LUTs for cameras. My Panasonic likely has a LUT for editing in premiere.

Double click on a slider to reset.

`Ctrl + click` on a slider to make minor adjustments.

Settings and effects get applied in the vertical order that they appear.

# Color Correction Rules

If you're going to use a LUT **DO NOT USE IT IN BASIC CORRECTION**. Reason being, the LUT will likely prevent you from correcting your shots. You want all stylistic settings to be applied in the Creative tab under `look`. Don't ever use a Basic Input LUT.

Adjust the exposure so that your clip has proper exposure in the Wavform view.

Only use the temp/tint slider in basic correction for small changes. For larger changes use the color wheels and match section. The second tool allows you to add color to just the midtones so you don't wash out your whites and blacks with color.

You can use an opacity mask to select perfect white colors and make sure that they are actually perfect white in the scopes. You can also check skin tones in the RGB scope the same way. This way you're only looking at one tiny section of the footage and everything else falls away so you can focus.

Skin tones are supposed to fall along the red/yellow guideline in the vectorscope.

Saturation pulls up and down all colors together.  Vibrance pulls the dullest colors the hardest to even all colors out. If your red is too saturated but you want more color then decrease saturation and then increase vibrance.

## Removing washed out blacks/whites

`HSL secondary` gets applied after the creative and color wheels sections. So if after color correction your blacks have color in them like blue or orange, you can selectivley remove those colors from the blacks. You select a hue, saturation, and lumma range that you want to focus on, then you refine that selection area and last apply the color correction, pulling out or pushing in colors of your choice.

## Animating Masks

Create your mask and then select the wrench icon under `mask path` to ensure the preview is available. Then press play and premeire will attempt to track the selected area. This is good for putting a mask on a person's face that is moving.

## Stylistic Notes

Contrast creates a harsh look. Low contrast creates a soft look. For a soft shot set a rule like blacks won't go below 10% and whites won't go above 90%.

Greens and blues create a sci fi harsh look. Reds and orange create a softer look.

## Advanced Workflow

Color correction comes first. You can apply color correction on the master clip which will save you time. All clips from that source will get the color correction at once.

Color Grading comes second and should take place in a seperate layer. `Project View > New Item > Adjustment Layer` insert the new adjustment layer on top of all of your footage and color grade that way. Then you go back and perform color correction on each individual clip again to fix any issues that arise. This way you can adjust each individual clip for errors without having to copy settings from clip to clip.

# Troubleshoot

Mask Edges not showing up - `Program View > Hamburger Menu > Panel Group Settings > Stacked Panel Group`
