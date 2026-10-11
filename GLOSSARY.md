# Mushoku Tensei Interactive Map

An interactive world map for the Mushoku Tensei light novel (volumes 1–12), showing where characters are as the reader moves through the story's timeline.

## Language

**World Map**:
The single illustrated map of the whole world (from volume 4's front matter) that serves as the backdrop on which everything is placed.
_Avoid_: Map (ambiguous), background, image

**Map Coordinate**:
A position on the World Map that stays valid whatever the resolution of the illustration used to display it.
_Avoid_: Pixel position

**Location**:
A named place in the story; it may lie inside a larger Location (a village inside a region) and may or may not appear on the World Map.
_Avoid_: Place, spot, lieu

**Estimated**:
Said of any fact (a Map Coordinate, a duration) inferred rather than stated by the text.
_Avoid_: Guessed, approximate

### Characters

**Character**:
A named person from the novel whose whereabouts and details are tracked over time.
_Avoid_: Personnage, hero, NPC

**Presence**:
A Character being at a Location at a given moment, as established by the text.
_Avoid_: Position, sighting

**Journey**:
A described movement of a Character from one Location to another over a stated or Estimated duration, following a Route when one exists.
_Avoid_: Trip, travel, path

**Teleport**:
An instantaneous move of a Character from one Location to another, with no Journey in between.
_Avoid_: Warp, jump

**In Transit**:
The state of a Character known to be travelling whose whereabouts cannot be placed without risking a contradiction with the text.
_Avoid_: Unknown, missing

**Route**:
A path across the World Map that Journeys can follow, such as a road or sea lane.
_Avoid_: Road, path

### Time

**Story Date**:
When something happens in the world's own calendar (Armored Dragon Era years and Seasons), as precise as the text allows, from a single Season to a span of years; the axis of the timeline.
_Avoid_: Date (ambiguous), timestamp

**Armored Dragon Era**:
The world's calendar era, counted in years; the only calendar the text names (years 414, 417, 422).
_Avoid_: ADE in prose, Kōryū era

**Season**:
One of the four quarters of a year, in the order spring, summer, autumn, winter; a winter straddles the turn of the year. Regional periods such as the rainy season or the mating season are Time Cues, not Seasons.
_Avoid_: Month (the text names none)

**Time Cue**:
A statement in the text from which a Story Date is derived: an explicit year or Season, an offset from another fact ("three weeks later"), or a Character's age.
_Avoid_: Timestamp, date hint

**Narrative Position**:
Where a passage sits in the books, by volume, chapter and passage, giving a total reading order. Readers only ever see the volume and chapter; the passage part is internal and need not match any printed edition.
_Avoid_: Chapter date, reading order

**Source Reference**:
The Narrative Position (and, where possible, the excerpt) that backs a fact.
_Avoid_: Citation, provenance, source

**History**:
The world's past before the plot, as the text recounts it; dated in the same calendar as Story Dates, but shown in its own Fresco.
_Avoid_: Lore, backstory

**Period**:
A named span of History as the text names it (the Ancient Age of the Gods, the Chaotic Period, the Armored Dragon Era); Periods follow one another without overlapping. A war covering only part of a Period is an event, not a Period.
_Avoid_: Age, epoch

**Previous World**:
The world Rudeus and Nanahoshi come from (Japan, on Earth); its time cannot be converted into Story Dates.
_Avoid_: Earth timeline, real world

**World Crossing**:
A Character's passage from the Previous World into this one, by reincarnation or summoning, with a departure dated in the Previous World and an arrival dated by Story Date.
_Avoid_: Isekai, transfer

**Fresco**:
A dedicated chronological view, such as History or the Previous World, separate from the Timeline Cursor.
_Avoid_: Timeline (ambiguous)

**Timeline Cursor**:
The control the reader moves along the Story Date axis to choose the moment being viewed.
_Avoid_: Slider, time travel

**Character Selection**:
The set of Characters the reader has chosen to follow on the World Map.
_Avoid_: Filter, party
