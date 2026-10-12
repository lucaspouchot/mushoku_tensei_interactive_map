# Shared Facts with derived Whereabouts

The app must answer, for any Character and any Story Date, where that Character is. The novels never state this continuously. They state moments: a Character is somewhere, sets off, arrives, is teleported, dies. They also often describe a group doing these things together (Rudeus, Eris and Ruijerd crossing the Demon Continent).

We therefore store only **Facts**, each one dated by Story Dates and backed by Source References, and derive each Character's **Whereabouts** from them:

- A **Presence** is an attestation at a single Story Date, not a stay. A stay is whatever lies between a Presence and the Character's next move.
- A **Journey** is one leg between two Locations, with its own departure and arrival Story Dates. A trip with stops is several Journeys.
- Presence, Journey and Teleport Facts carry a **set of Characters**. One Fact covers a travelling group, so correcting its Story Date corrects it for everyone.
- **In Transit** is not stored. It is the Whereabouts during a Journey that cannot be placed, because its destination is unknown or review marks its timing as contradicting the text.
- Whereabouts is computed on the representative points of Story Dates (ADR 0001). It is one of: at a Location, travelling, In Transit, Unrecorded, Dead, or Off Map. It also carries a precision: an exact point, a point with an uncertainty radius, or somewhere in an area Location.

## Considered Options

- **Presence as a stay with a start and an end.** Rejected: a Story Date's interval already expresses uncertainty, and reading a wide interval as a duration would conflate the two. Stays would also overlap and contradict each other wherever the text is vague.
- **One Fact per Character.** Rejected: a group journey would be copied once per member, and the copies drift apart as soon as one is corrected.
- **Storing each Character's position as a timeline** (precomputed segments). Rejected: it duplicates what the Facts already say, and every corrected Time Cue would need the segments rebuilt by hand.
- **In Transit as a Fact kind of its own.** Rejected: it would duplicate the Journey it describes, and the two could disagree.

## Consequences

- The data build must reject data from which Whereabouts cannot be derived deterministically, unless one of the conflicting Facts is rejected. That covers two Locations at the same point, overlapping Journeys or a Presence during one's own Journey, a Fact before Birth or after Death, a cyclic or dangling relative Time Cue, and an excerpt not found in its passage.
- A Journey's span blocks any other Fact about its Characters. A member who leaves a group ends the shared Journeys, and new ones begin from there.
- The per-Character index the app needs for O(log n) lookups is built at data build time, never stored.
