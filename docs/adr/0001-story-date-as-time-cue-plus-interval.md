# Story Date as Time Cue plus derived interval on a nominal 360-day axis

The novels give only three calendar years (414, 417, 422 of the Armored Dragon Era). They name no months or days. Every other moment comes from ages, Seasons, or offsets like "three weeks later", and the text sometimes contradicts itself.

We therefore store each Story Date as two things:

- the **Time Cue** the text states, which is one of:
  - an absolute year with an optional Season;
  - an offset from another fact's Story Date;
  - a Character's age;
- an **interval [earliest, latest]** derived from that Time Cue, flagged Estimated when it is inferred.

Relative Time Cues chain, so correcting an anchor recomputes everything that depends on it. Interval widths come from a fixed tolerance table, not from case-by-case judgement.

Intervals live on a continuous axis measured in days, with a nominal year of 360 days (12 months of 30 days, 4 Seasons of 90 days, starting in spring). The novels never give the world's year length or the Season in which a year begins. The 360-day year is a modelling convention that keeps month and Season arithmetic exact. It is never shown as a date: the UI shows only years, Seasons, or ranges.

## Considered Options

- **A single date with an "approximate" flag.** Rejected: it hides how wide the uncertainty is. It also loses the anchor, so correcting one date cannot propagate to the dates that depend on it.
- **A discrete axis in Seasons.** Rejected: it cannot hold Journey durations measured in days, and it cannot interpolate a Character's movement between two moments.
- **A 365-day year, or a real calendar.** Rejected: it would claim a precision the text does not have, and 365 days does not split evenly into months or Seasons.

## Consequences

- Each fact also gets an internal representative point inside its interval. The point defaults to the midpoint and shifts to keep a Character's facts in story order. The Timeline Cursor and the movement rule work on these points.
- History shares this calendar, extended backwards. The Previous World does not share it: its own axis is relative to the truck accident and is linked to Story Dates only through World Crossings.
