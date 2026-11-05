## Who is talking: a system type looking for the problem under the five {paths=?}

\small

- Dimitar Popchev: engineering manager, two years, automation flows for the global semiconductor industry (GlobalFoundries)

> There are two classes of system designers. The first, if given five problems will solve them one at a time. The second will come back and announce that these aren't the real problems, and will eventually propose a solution to the single problem which underlies the original five.
>
> -- H. A. Kinslow, NATO Software Engineering Conference, Garmisch 1968; report section 3.2 (Naur and Randell, eds.)

- the Stacey matrix got me into agile: this talk walks it from Chaos to Simple, one business rule at a time
- \mbox{\footnotesize\url{github.com/dpopchev/chaos-to-simple}}\
  \mbox{\footnotesize\url{linkedin.com/in/dimitar-popchev-b87074142}}

\footnotesize

the shop, its people and its dates are reconstructed; the code and its numbers are real and tested

::: notes
Thirty seconds. The quote is the whole talk in one sentence: the five ifs were not the problem.
Then the customer's problem, next frame.
:::

## Every request and every provider outcome lands in one checkout function {paths=?}

![](build/00-frontmatter/business-map-undivided.png){width=100%}

::: notes
Name the nine parts before anyone reads the picture: the customer, the shop, the four
departments on the left (marketing, loyalty program, logistics, accounting) and the
three providers on the right (payment provider, warehouse, mailer). The footer counter
starts at ? because no section has set it yet. The caption is Conway's point: the shape of
the map is the shape of the teams, and the arrows are the calls the code makes. One
function takes every request and every provider outcome; the homes come later, when the
room has decided.
:::

## Business decisions lead checkout from tangled rules to clear responsibilities {paths=?}

![](build/00-frontmatter/agenda-00.png){width=90%}

::: notes
The route, eight stops; we are at 00, the rest fade until we reach them; I1 to I3 mark the incidents. The footer counts code paths from 01.
:::
