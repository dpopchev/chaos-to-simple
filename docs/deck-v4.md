# Deck v4: the review of 2026-11-02

Source: the developer's review of 2026-11-02 and the agreed plan of E-012 (frame map at 2d453f0, 48 pages; plan 50 pages); the blocks below are that review's text, verbatim.

## Per page

```text
p2: The business map show the flow of policy riequets, not just lines depdencies; Is the shp a balck box, black not poopulare choice but if it is black box need be outlined; the page shows opporutnit for Strategic domain discovery, the shop is the core etc the otehr terms were we see payment is some external that can be sourced out
p3 it is not clear what l1 are and is the color codding about, sections? also the paths and reason abot on the bottom of the page need have some connectino as well the numbers, maybe som cymbol of a single line would fit
p4 the showdo effect looks great but the title is alwfu; always put action titile on the top for all slides
[Core Finding / Result] + [Driven By / Because Of] + [Specific Impact / Action Required] for action title whiel in those agenda once you can use simple Topic Title
p6 to p11 need be alinged iwth one another; the diff view was very nice and can use colring also showing the checkout version, lines and expand on the request ocmming also use the same laoyt for all now moving through they dance also we are toalking about policie requetsts/requiremnts not ifs; and should have intro about the path measurment as its already used the main message is simple reqs lead simple solutiosn straightforwards
p12 the build up to have doesnt make sens, the markeiytn gives heads up with new request for plicoy and we need to see path incersases while the easy sthragtfowarsd patchin is misisng; I like the how many tests would you make to be sure but then p13 we are followed with three code snipet and tests cases that alerayd need be spread around the previous pages setting the tempo; we need the two tests both values and all combinations be explored using already the established technique of paths
p14 use the r1 vs r2 framework for marketing finditng out they are missing raveniu and emphisises this discrpetnacy, a lot money is no where to be found backtracking as potential sw foault
p15 drop the reason, its a new test provided by finance and marketing to see if system is working fine, should be ocneected with the r1/r2 framework from previoous page establishg the numbes giving tests results we are expecting them to pass not xfail
p16 is the further exploration of the missing peices and need improve as how tis counted, should be htree layout page transition fo p13 exploring to compleixty space and coverate edge cases and bugs lesson\
p18 we should have resoulved previous conflict and now see the new one -- marketing and logsings are backtracking on diffretn readings and should presetn their requiremnts, requiring joined exploration to settal the policices; there is conflict new between markeint and lgositcs R1 vs R2 for each and theri conflict backtraced to the dev
p19 the matrix is nice but a lot of space and hanfging
p21 nice but mood and the questions doesnt mean much
p22 the room doesnt make much but the transcirpt is nice; this is the attempt of stakeholders conficlt resolution needing to be emphisized on the exploration process and reveiwes in the retor on p23
p23 isnt q4 to q6 also an busines decision somehow, apply the domain straetgic map from earlier and domain exploration sub domain external core etc form domain drivend design techniqes
p24 the left boxex are misisng the connection with teh apths also the scope is just haning; all are nice but maybe spread around previous pages to set the tone
p25 missinc continuit with previous pages
p27 aling the legend lefgt and right; this is ideal show how we are building the donains and a shell of shop core important domaisn and theri mening while producing prots with the external teams
p28-30 are missing the tactical resolution whici si already discussedand actually rediscoverd in the p31 should be other way around, strategic hinch leads to the tacitcal descision or even that tactical descision are discovering the strategic one, the later is even better but not well estalished in the pages
p32 shows the contexts and momvent but hangs on the table; shwos idea of functional core and imperitvie shell and how it alings with ddd suggest ipromvents
p34 support misses this, but the system reg can transformed to tdd and show narrowing down to the BCs; support only rises the flag but not saying where the probelms are we are able because to point to policies owners due to BCs and previous stesp
p35 OOP limitasion and entanglin show throug TDD not just like hits, write test firs p36 sanf and p37 then tdd helps us fidn the better desing CQSPR
p38 the checkout versioning not consistent throught the talk, should be the diff type showgin version trasistnios, like it the most here would like to see it colored - delete red and + added and modificaitons yellow with tilde and breaking dashes for omited where no cahgnes, line numbers not needed
p39 is very nice but the move is missing context need beter epxlained while the table on the right is unreadabel
all from p40 to p39 very nice epsciall showing the wasy how core shell context are helpgin, missing the poitns of decoupling and coheision need be ephiszed and how CQRS withi fucntional shell heped, like post morten examintaion with good decision tactical, still too much code and need be onctex

target talk be 50 pages; should have a call for action to follow my linkding and CraftsamsDay and JournemansDay posts series and reach out if they wan to go over theri specific probelts; qna and then tahnky note to public and organizes
```

## Storyline

```text
#    Frame    Remark
S1    40 to 46    The climax code is missing. 06 goes from the section page straight to the tests; price() and the final checkout shell never appear, so "cut along the seam" has no picture of the cut. Add one frame "Cut along the seam": price() left (six lines), the shell checkout right, shown as the v5-to-shell diff where the only change is the pure part moving out. Pay for it by merging 41 and 42: the four-line 192 passed output fits under the test class.
S2    35    The bridge sentence is gone again. 05 opens with I3 (effects, charge before reserve) and then spends two frames on a pricing class; without "same bug, pricing edition: the order hidden in state" the audience wonders why the subject changed. Put it back as the frame's caption.
S3    19    The title "The agenda was a map" refers to an earlier deck where the agenda was the Stacey chart. Now the agenda is the strip, so the sentence is false. Rename to the message: "Above the line: a decision, not a test".
S4    16    Three messages on one frame: the grid (2 of 64), the curve (doubling), Rule 1 (x versus +), plus the line. The footer already did the doubling across seven frames; drop the curve here, keep grid left and Rule 1 right. The curve returns in 24 where its jump to 512 is the news.
S5    38 and 43    v5 ends with case Sent() | Bounced(): return Accepted(total) but the worlds table distinguishes "Accepted, confirmed" from "Accepted, not confirmed". Make v5 return Accepted(total, confirmed=True) and Accepted(total, confirmed=False) in two cases so the diff and the table tell the same story.
S6    14    Two messages: the loss and the squeeze. Keep both, but in delivery read the chart, stop, then reveal the bubble (. . . pause); the pause is the beat where the dramatic question is asked.
S7    21    The mood line falls in a straight line, which says "every question hurt equally". Label the axis as the customer's certainty, start flat through the cart step, and let the two effect questions (card, stock) drop more than the rule questions; it then reads as a journey, not a ruler.
```

## Presentation

```text
#    Frame    Remark
P1    12, 18, 31    Two pictograms render as text fallbacks: CODE for Dev and WAREHOUSE for Warehouse. The glyphs are missing from the font the matplotlib renderer loads (regular set instead of solid, or an older FA5). Use terminal and boxes, or load the solid OTF.
P2    5 to 11    The storyboard shows unified-diff hunks, so from step 4 the audience sees nine lines of a twenty-line function; the growth that the footer counts is not visible. Show the full function on every step with the new lines marked +; it fits (twenty lines at the current size).
P3    19    The matrix sits at about 45% of the frame beside the line. Put the line below and let the figure take 85% of the height; the zone texts become legible.
P4    31    Three bare + lines (added blank lines) in the diff. Since every line on the frame is new, show checkout_v4's body as plain code with the caption "checkout_fixed.py -> checkout_v4.py"; no diff markers needed.
P5    29 and 46    The comment # b2, on the discounted goods: the bug, fixed runs to the frame edge twice. Trim to # b2 in shipping.py; the sentence above the code already says it.
P6    38    Title "The ports, as a picture" names the left half; the message is on the right. Rename "Every effect answers with a value".
P7    41 and 42    Same title twice (fixed by the merge in S1).
P8    48    The repo URL wraps mid-word. Give it its own line under the bullet or widen the column.
P9    22    Nineteen lines read in silence is ten seconds the room will not give you. Read Logistics' first line and Marketing's answer aloud, then skip to "Who reads the log?" and the silence; the rest is for the PDF.
P10    all    After S1 and S4 the plan stays at 48 frames, 41 content, 45 minutes. First cuts if the dry run overruns: 21 (journey), 30 (Zone), 37 folded into 38 as a caption.
```

## Decisions

```text
#    Decision    Recommendation
D1    Storyboard: hunks or the whole function (P2)    Whole function; the growth is the message
D2    Frame 16: drop the curve or split into two frames (S4)    Drop; the footer did the counting
D3    06: add the seam frame by merging 41 and 42 (S1)    Yes; without it the ladder has no last rung
D4    Pictogram fallbacks: fix the glyphs or accept text labels (P1)    Fix; two text boxes among nine icons look like a bug
D5    Dry run date and which cuts are pre-approved (P10)    Tuesday evening with a timer; pre-approve 21 and 30
D6    Keep the believed line on both the section page and the last frame    Keep; setup and payoff are different moments
D7    Slide language stays English for this run    Yes; a language switch two days out is a risk, and the room is Bulgarian-speaking either way
```

## Currency

```text
also change veryhwer EUR not BGN
```

## Frame map

The frame map of build/talk.pdf at 2d453f0 (48 pages) and the planned map at 50 pages, from the agreed plan of E-012. Page 1 is the title page; the six section titles (`# `) are pages of their own; the other pages are the `## ` titles of the `NN-*/index.md` files in sorted order.

```text
page  section  heading today                                   plan
1     title    Python: From chaos to simple ...                 unchanged
2     00       The business map                                 W-105: outlined core, request flow, legend
3     00       Agenda, in the order the bits fall               W-105: I-mark legend, band colours, path glyph
4     01 (s)   Six if statements, 64 paths                      W-119: topic title '01 Bits: ...'
5-11  01       Step 0 .. Step 6                                 W-106: a measurement frame before them, one layout, whole function, tally
12    01       Checkout done                                    W-107: the next doubling over the question
13    01       Two tests. Coverage says 100%                    W-107: both values, 2 of 64
14    01       Finance found it, not the tests                  W-108: R1 against R2, the gap named
15    01       The path nobody ran                              W-108: finance's test, no xfail line, the run captured
16    01       A path is a six-bit number                       W-107: grid left, Rule 1 right, no curve (S4, D2)
17    02 (s)   Stacey matrix ...                                W-119
18    02       I wanted to write a test                         W-109: R1 and R2 tagged, traced to the dev
19    02       The agenda was a map                             W-109: 'Above the line: a decision, not a test' (S3), legible zones, line at the foot
20    03 (s)   From chaos to complex                            W-119
21    03       The journey of one order                         W-110: the customer's certainty (S7); pre-approved cut (D5)
22    03       The room                                         W-110: caption; P9 in the notes
23    03       The retro                                        W-110: subdomain column (core q1-q3, generic q4-q6)
24    03       The honest count                                 W-111: panels named by their shell world, counts as caption
25    03       Nine decisions, none deleted, all moved          W-111: headers from the route, continuity caption
26    04 (s)   Complicated on the What ...                      W-119
27    04       Color-coded, the ifs get names                   W-112: legend 'who asked' left, 'home' right, the ports
28    04       The first fix                                    W-112: caption: the first boundary
29    04       The dispute closes                               W-112: caption: shipping owns it; Zone's sentence folded in
30    04       A bit as a type                                  W-112: PRUNED (D5 pre-approved; pays for the 50 pages)
31    04       Bounded contexts: every bit has a home           W-112: plain body of checkout_v4 under its caption (P4)
32    04       Bounded contexts, the moves                      W-113: full width, core = the What, shell = the How
33    05 (s)   Complicated on the How ...                       W-119
34    05       I3: cards charged ...                            W-114: the test against v4 with its run
35    05       Past me reached for a class                      W-114: after the test frame; S2 caption
36    05       The bit nobody wrote down                        W-114: before the class frame
37    05       Command Query Separation draws the seam          unchanged (P10: fold into 38 only if the dry run overruns)
38    05       The ports, as a picture                          W-115: 'Every effect answers with a value' (P6), v5 confirmed (S5), diff v4 -> v5 (W-104)
39    05       A boundary that passes values ...                W-115: 'in this talk' column, no thumbnail
40    06 (s)   Simple: functional core, imperative shell        W-119
new   06       Cut along the seam                               W-116 (S1, D3)
41-42 06       Sixty-four paths, three invariants: 192 tests x2 W-116: merged into one (P7)
43    06       Eight worlds, four outcomes                      unchanged (S5 lands in v5)
44    06       The wounds close by name                         W-117: the post-mortem table over the run, no snippets
45    06       The number                                       unchanged
46    06       Epilogue: marketing's seventh if                 W-112 trims the b2 comment (P5)
47    07       What I should have known from the start          W-119
new   07       the call to action                               W-118
48    07       Q&A                                              unchanged (P8 landed as W-101)
new   07       the thank-you                                    W-118
```

Budget after the plan (data/budget.csv): 00 2/3, 01 13/12, 02 2/3, 03 5/6, 04 5/6, 05 6/6, 06 6/6, 07 4/3 -- 43 content frames, 45 minutes; with the title and six section pages, 50.

## Planned titles

The rule (W-119): every content frame (each `## ` outside 00-frontmatter) carries an action title -- core finding + driven by + impact or action, at least eight words. The title page, the two 00 frames and the six section pages (`# <NN> <route label>: <claim>`, labels from data/route.csv) keep topic titles; 07 has no section page. Pages are those of the 50-page build at e8418df. Q&A and Thank you are worded so each still reads as Q&A and as the thanks.

| page | section | old title | new title |
|---|---|---|---|
| 1 | title | Python: From chaos to simple, one bit at a time | unchanged |
| 2 | 00 | The business map | unchanged |
| 3 | 00 | Agenda, in the order the bits fall | unchanged |
| 4 | 01 (s) | Six if statements, 64 paths | 01 Bits: six policies, 64 paths |
| 5 | 01 | A policy is one bit and every bit doubles the paths: count them before you trust a badge | unchanged |
| 6 | 01 | No policy yet: one path | The plain checkout has three calls and no policy, so it has one path |
| 7 | 01 | Policy 1: the autumn coupon adds one bit: 2^1 paths | The autumn coupon adds the first bit, so the checkout now has 2 paths |
| 8 | 01 | Policy 2: the member discount adds one bit: 2^2 paths | The member discount stacks on the coupon and doubles the checkout to 4 paths |
| 9 | 01 | Policy 3: free shipping from 50 EUR adds one bit: 2^3 paths | Free shipping from 50 EUR adds a third bit and the checkout reaches 8 paths |
| 10 | 01 | Policy 4: shipping abroad adds one bit: 2^4 paths | Shipping abroad adds a fourth bit and the checkout reaches 16 paths |
| 11 | 01 | Policy 5: gift wrap adds one bit: 2^5 paths | Gift wrap, promised as just one more change, brings the checkout to 32 paths |
| 12 | 01 | Policy 6: no VAT for companies adds one bit: 2^6 paths | No VAT for companies adds the sixth bit and the checkout reaches 64 paths |
| 13 | 01 | Checkout done | Six policies done and 64 paths live, so how many tests would make you sure? |
| 14 | 01 | Two tests. Coverage says 100% | Two tests reach 100% branch coverage yet run only 2 of 64 combinations |
| 15 | 01 | Finance found it, not the tests | Finance traced 6,070 EUR of missing shipping to the checkout, a software fault |
| 16 | 01 | The path nobody ran | Finance's R2 test expects 60.00 and gets 54.00, a path no test of ours ran |
| 17 | 01 | A path is a six-bit number | A path is a six-bit number, so every new policy doubles the paths to count |
| 18 | 02 (s) | Stacey matrix: agreement on the What, certainty on the How | 02 Map: Stacey matrix, agreement on the What, certainty on the How |
| 19 | 02 | I wanted to write a test | Marketing and logistics read free shipping differently, so no test settles it |
| 20 | 02 | Above the line: a decision, not a test | The shipping dispute sits above the line: a decision for the room, not a test |
| 21 | 03 (s) | From chaos to complex | 03 Room: from chaos to complex |
| 22 | 03 | The journey of one order | The mood of one order drops at six questions, each a rule nobody wrote down |
| 23 | 03 | The room | Four departments carry the argument in one room while dev stays silent to the end |
| 24 | 03 | The retro | The retro names six business decisions, three core and three in generic subdomains |
| 25 | 03 | The honest count | Counting the nine decisions honestly gives 512 paths, not 64, the first good news |
| 26 | 03 | Nine decisions, none deleted, all moved | Nine decisions came out of the room, and each moves to a home, none deleted |
| 27 | 04 (s) | Complicated on the What: one language, bounded contexts | 04 Homes: one language, bounded contexts |
| 28 | 04 | Color-coded, the ifs get names | Coloring every line by who asked for it shows which context each if belongs to |
| 29 | 04 | The first fix | One renamed value, the discounted goods, closes I1 and draws the first boundary |
| 30 | 04 | The dispute closes | Shipping owns the dispute's rule and a sum type lets the checker count its bit |
| 31 | 04 | Bounded contexts: every bit has a home | Each bit now has a home in pricing, shipping, tax or shell, named by who asked |
| 32 | 04 | Bounded contexts, the moves | All nine decisions moved home: the contexts are the core, the ports are the shell |
| 33 | 05 (s) | Complicated on the How: decoupling, cohesion, FP vs OO, CQS | 05 Seam: decoupling, cohesion, FP vs OO, CQS |
| 34 | 05 | I3: cards charged for parcels the warehouse did not have | I3 charged cards for missing stock because charge ran before reserve |
| 35 | 05 | The bit nobody wrote down | The call order is a bit nobody wrote down, giving 45 against 44 from the same inputs |
| 36 | 05 | Past me reached for a class | A class hid the call order in its state, the same bug as I3 in pricing |
| 37 | 05 | Command Query Separation draws the seam | Command Query Separation draws the seam by making every answer a value |
| 38 | 05 | Every effect answers with a value | Each effect answers with a value, so reserve runs first and every answer is matched |
| 39 | 05 | A boundary that passes values adds paths; one that passes flags multiplies them | Passing values across a boundary adds paths you can count, passing flags multiplies them |
| 40 | 06 (s) | Simple: functional core, imperative shell | 06 Core and shell: functional core, imperative shell |
| 41 | 06 | Cut along the seam | Moving the pure part out into price cuts along the seam and changes nothing else |
| 42 | 06 | Sixty-four paths, three invariants: 192 tests | Every one of 64 paths holds three invariants, so the core runs 192 tests |
| 43 | 06 | Eight worlds, four outcomes | Eight shell worlds collapse to four outcomes, with no charge when stock is gone |
| 44 | 06 | The wounds close by name | I1 and I3 each close by name as a test, and the seam keeps both from returning |
| 45 | 06 | The number | The split cuts 512 paths to 72 while branch coverage stays at 100% as before |
| 46 | 06 | Epilogue: marketing's seventh if | Marketing's seventh if lands in shipping and costs 8 paths, not 512 |
| 47 | 07 | What I should have known from the start | Six beliefs I held at the start each gave way to the lesson I should have known |
| 48 | 07 | Follow the series and bring your own checkout | Follow the series one section at a time, then bring your own checkout to review |
| 49 | 07 | Q&A | Q&A: ask anything about the tests, the repository, the posts or the earlier talks |
| 50 | 07 | Thank you | Thank you to the audience for the questions and to DEV.BG for the stage |
