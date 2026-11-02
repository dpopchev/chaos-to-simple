# Sources for the BOOM label

Question: which published source states the ratio between a first proof of concept
and delivery, and what numbers does it give?

Hypothesis: a citable source exists with a ratio near eight to one.

| title | author | year | claim in one line | link |
|---|---|---|---|---|
| The Mythical Man-Month, ch. 1 "The Tar Pit" | Frederick P. Brooks, Jr. | 1975 (1995 anniversary edition read) | "a programming product costs at least three times as much as a debugged program with the same function"; a programming system component "at least three times as much as a stand-alone program"; the programming systems product: "It costs nine times as much." | https://archive.org/stream/MythicalManMonth/Brooks%201974%20The%20Mythical%20Man-Month-%20Essays%20on%20Software%20Engineering%2C%20Anniversary%20Edition%20%282nd%20Edition%29_djvu.txt |
| Live-Data Prototypes vs. Production | Marty Cagan (SVPG) | 2012 | "As just a rough guide, I find a live-data prototype to be somewhere between 20% and 50% of the work of building production software." (production 2x to 5x the prototype) | https://svpg.com/live-data-prototypes-vs-production |
| Ralph Stacey's Agreement & Certainty Matrix | Brenda Zimmerman | 2001 | No ratio and no effort or cost figure: the page describes the zones only. | https://plexusinstitute.org/edgeware/archive/think/main_aides3.html |

No source read states eight to one. The nearest is Brooks: about 3x per step, 9x from
a program to a programming systems product.

Not verified (seen only in search summaries or secondary pages, no primary page read):

- the ninety-ninety rule, credited to Tom Cargill and printed in Jon Bentley's
  "Bumper-Sticker Computer Science", Communications of the ACM 28(9), 1985: the last
  10% of the code takes the other 90% of the time (about 2x);
- Ralph Stacey's own text (Strategic Management and Organisational Dynamics, 1996 and
  later editions): no copy was read, so no claim is made for it.

Decision: the BOOM label quotes Brooks, The Mythical Man-Month, ch. 1 "The Tar Pit" (1975): a
programming systems product costs nine times the program; labels.csv boom_quote reads
"9x the program (Brooks 1975)"; the 8:1 hunch is not used, since no source read states it.
