# Mushoku Tensei Interactive Map

An interactive world map for the Mushoku Tensei light novel (volumes 1–12), showing where characters are as the reader moves through the story's timeline.

## Language

**World Map**:
The vector map of the whole world, redrawn from volume 4's front-matter illustration as a stack of Map Layers, on which everything is placed.
_Avoid_: Map (ambiguous), background, image

**Map Layer**:
One thematic part of the World Map that can be shown or hidden on its own, such as the land outlines, relief, Routes or settlements.
_Avoid_: Overlay, calque

**Map Style**:
A named look applied to all Map Layers at once (such as minimalist or fantasy) that the reader can switch without changing what the World Map shows.
_Avoid_: Theme, skin

**Color Scheme**:
The light or dark look of the application around the World Map, chosen by the reader or taken from their browser; independent of the Map Style, though a Map Style may offer a dark variant that follows it.
_Avoid_: Theme, dark mode (as a noun for the setting)

**Map Coordinate**:
A point in the World Map's own flat plane, the same whatever Map Style or zoom displays it; not a longitude/latitude.
_Avoid_: Pixel position, lon/lat

**Location**:
A named place in the story, from a continent down to a single building; it lies inside at most one larger Location (a village inside a region), may or may not appear on the World Map, and may be founded or destroyed during the story.
_Avoid_: Place, spot, lieu

**Fact**:
A claim about the story that is dated by one or more Story Dates and backed by at least one Source Reference, such as a Presence, a Journey, a birth or a death.
_Avoid_: Event (reserved for story events), record, entry

**Estimated**:
Said of any value of a Fact (a Story Date, a Map Coordinate, a duration, a Location) inferred rather than stated by the text; it always comes with a justification.
_Avoid_: Guessed, approximate

### Characters

**Character**:
A named person from the novel whose whereabouts and details are tracked over time.
_Avoid_: Personnage, hero, NPC

**Presence**:
One or more Characters being at a Location at a single Story Date, as established by the text; a stay is not a Presence but what lies between Presences and the next move.
_Avoid_: Position, sighting, stay

**Journey**:
A described movement of one or more Characters from one Location to another, one leg only, over a stated or Estimated duration, following a Route when one exists; a trip with stops is several Journeys.
_Avoid_: Trip, travel, path

**Teleport**:
An instantaneous move of a Character from one Location to another, with no Journey in between.
_Avoid_: Warp, jump

**Whereabouts**:
Where a Character is at a given Story Date, derived from their Facts: at a Location, travelling along a Journey, In Transit, Unrecorded, Dead or Off Map; when placed, it is an exact point, a point within a radius, or somewhere in a large Location such as a continent.
_Avoid_: Position, status, location (lowercase)

**Unrecorded**:
The Whereabouts of a Character before their first Fact: they exist, but nothing in the text places them yet.
_Avoid_: Unknown, not born

**Off Map**:
The Whereabouts of a Character at a Location that has no Map Coordinate, nor any larger Location with one, such as the Previous World.
_Avoid_: Hidden, elsewhere

**In Transit**:
The state of a Character during a Journey that cannot be placed without risking a contradiction with the text, because its destination is unknown or its timing does not fit; a state, never a Fact of its own.
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

**Work**:
One published series of books, such as the main Mushoku Tensei series or one of its spin-offs, each with its own volume numbering.
_Avoid_: Series, book (a volume)

**Narrative Position**:
Where a passage sits in the books, by Work, volume, chapter and passage, giving a total reading order within a Work. Readers only ever see the volume and chapter; the passage part is internal and need not match any printed edition.
_Avoid_: Chapter date, reading order

**Source Reference**:
What backs a Fact: a passage of the novels (its Narrative Position and, where possible, the excerpt), an illustration from a volume, or a captured external statement such as a social media post; an external statement may only support Estimated values.
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
