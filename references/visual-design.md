# Color, attention, and conversion design

Use visual design to make the offer legible, credible, and easy to act on. Treat aesthetic choices as context-dependent design decisions; establish conversion impact separately.

## Color theory in an actual interface

Separate hue (color family), lightness/luminance (perceived or measured brightness), and chroma/saturation (color intensity). A hue change alone says little about visibility. Inspect surrounding colors, size, font weight, spacing, imagery, and competing elements.

Use palette relationships deliberately:

| Relationship | Possible use | Check |
| --- | --- | --- |
| Monochromatic | Cohesive surfaces and clear emphasis through lightness | Sufficient differentiation and readable states |
| Analogous | Quiet brand range with restrained accents | Important actions do not disappear into similar colors |
| Complementary | A contrasting action or focal detail | Pair does not vibrate visually or create inaccessible text |
| Neutral foundation plus accent | Content-led page with a clear primary action | Accent is not used for every badge, link, and decoration |
| Semantic status colors | Error, warning, success, and information | Text/icon meaning accompanies color; brand use stays consistent |

Treat 60/30/10 ratios, "one accent," warm/cool mood, and saturated-CTA advice as optional heuristics. Do not force a ratio or replace a working brand system.

The [color research review](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00368/full) describes contextual and methodological limits. Do not encode "blue always creates trust," "red always converts," or a universal buying-color ranking. Generate a hypothesis about contrast, hierarchy, or brand fit that can be checked on the actual page.

## Use semantic design tokens

Map the project's existing tokens to roles: canvas, surface, primary text, secondary text, border, primary action, action text, hover, active, focus, selected, error, warning, success, and disabled.

Keep brand decoration separate from feedback. A destructive action should not look like the normal purchase CTA. A selected annual plan needs a visible label and state, not just a tinted card.

Prefer a dominant action per decision area. Repeat the same primary action after relevant evidence; do not turn the full page into equally weighted buttons. Ensure the color works on every surface where the button appears.

Compute contrast on the final composited foreground/background pair. The bundled contrast command accepts opaque sRGB hex values; it cannot resolve an image, transparency, filter, gradient, or animation. Sample the worst relevant rendered background and inspect real states.

    python3 <skill-dir>/scripts/cro_math.py contrast '#ffffff' '#2563eb'

Under [WCAG 2.2](https://www.w3.org/TR/WCAG22/), normal text generally requires 4.5:1 and large text 3:1; large text means at least 18 pt regular or 14 pt bold. Relevant non-text UI boundaries and indicators generally require 3:1, subject to the criterion's scope and exceptions. Do not round a failing value upward to claim a pass.

## Design the hierarchy around buyer questions

Choose a reading order: outcome, explanation, demonstration/evidence, offer, action. Establish it through typography, spacing, grouping, placement, and contrast together.

- Give the main claim enough space to be read as one thought.
- Group price, billing interval, inclusions, and plan CTA together.
- Keep limitations and recurring commitments readable near the decision.
- Distinguish primary benefits from supporting details.
- Use short section headings that help scanning; avoid generic section labels that convey no substance.
- Make product visuals show the task or result the copy promises.
- Avoid large decorative media that displaces the explanation and action without adding meaning.

Use proximity to communicate relationship, alignment to support comparison, and whitespace to separate decisions. Treat these as composition tools, not automatic persuasion levers.

## Typography and readable density

Reuse established typefaces and avoid unnecessary font requests. Use a clear type scale, comfortable body size and line height, appropriate line length, and enough contrast for supporting text. A typical starting body range of 16–18 CSS px and a text measure around 45–75 characters are design heuristics; adapt to audience, script, device, and existing brand.

Keep prices understandable: preserve currency, quantity unit, billing period, and actual charge. A giant monthly equivalent cannot compensate for unreadably small annual terms.

Use semantic headings, real text rather than essential text in images, and meaningful link names. Avoid clipping longer translated headlines or truncating plan limitations.

## Demonstrate with relevant visuals

Prefer a current product screenshot, annotated workflow, sample output, short optional demo, or a transparent calculator. Caption the useful detail. Use permitted customer assets and redact private information.

Use illustration when it clarifies a concept or supports the brand. Do not make generated interfaces look like proof of a feature the product lacks. Clearly label prototypes and illustrative examples.

Give images dimensions, responsive sizes, useful alternative text when informative, and empty alt for purely decorative imagery. Keep essential meaning available beyond video or animation; provide captions/transcripts as appropriate.

Motion should explain state or guide attention. Respect reduced-motion preferences, avoid autoplay audio, and keep primary information and actions available without waiting for animation. Do not add scroll hijacking or a background video by default.

## Mobile, touch, and accessibility

Read [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for the applicable criteria. Verify keyboard operation, visible focus, meaningful labels, error recovery, zoom, and reflow on the actual path.

At minimum, inspect a narrow phone layout, a representative desktop, long content, and user zoom. Use 320 CSS px reflow as a relevant check, accounting for genuinely two-dimensional content. Do not hide overflow to disguise clipped controls.

WCAG 2.2 AA's minimum pointer target criterion is 24×24 CSS px with exceptions. A larger target such as 44×44 may be a useful design choice; do not falsely call it the universal AA requirement.

For pricing tables, preserve comparable rows and clear plan identities on mobile. Allow appropriate horizontal scrolling for a genuine table, with labels and discoverability; do not make choosing a plan depend on an unreadable compressed grid. A sticky CTA must not obscure inputs, error messages, focused elements, or billing terms.

Localize currency, separators, dates, text direction, and number layout. For RTL, verify logical properties and mixed-direction price strings. Do not assume a Western color association or left-to-right visual priority transfers unchanged.

## Performance supports the journey

Inspect hero image size, fonts, animation work, third-party scripts, layout shifts, and click-to-response delay. Reserve space for changing prices and loading content.

Google's [Web Vitals guidance](https://web.dev/articles/vitals) defines good thresholds at the 75th percentile: LCP at most 2.5 seconds, INP at most 200 ms, and CLS at most 0.1. Separate mobile/desktop field data from a lab run. Treat these as performance checks; they do not forecast revenue.

Choose the smallest implementation that supports the design goal. Prevent analytics and experiment code from breaking the main action. Do not hide important content to improve a synthetic score.

## Visual acceptance

Inspect the actual result, not only source code. Confirm readable offer and terms, consistent primary action, meaningful proof, accessible states, stable layout, and a working path at representative sizes.

A screenshot can verify composition but not keyboard behavior, payment, or field performance. Report the boundary of what was checked. Prefer a concrete before/after change to an aesthetic score such as "9/10 conversion design."
