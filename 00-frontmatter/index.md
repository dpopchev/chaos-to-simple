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

## Business decisions lead checkout from tangled rules to clear responsibilities {paths=?}

![](build/00-frontmatter/agenda-00.png){width=90%}

::: notes
The route, eight stops; we are at 00, the rest fade until we reach them; I1 to I3 mark the incidents. The footer counts code paths from 01.
:::

## Six rules add up to 7 for McCabe and multiply to 64 configurations {paths=?}

::::: {.columns}
:::: {.column width="58%"}

![](build/08-backup/counting.png){height=70%}

::::
:::: {.column width="42%"}

\footnotesize

**configurations = 2^rules**

| pattern | paths | rule |
|---|---|---|
| sequential ifs | 2 x 2 x 2 x 2 x 2 x 2 | each if doubles the paths |
| if / elif / else | 2 + 1 | alternatives add, one branch is taken |
| two ifs written as if/elif | 3, not 4 | the merged branch drops a path |

::::
:::::

\footnotesize

cyclomatic complexity adds: decisions + 1 = 7 (McCabe, 1976), the basis paths a branch suite walks; the rules multiply: 2^6 = 64 input configurations, one per combination of the six conditions; the same six ifs, one sum and one product

::: notes
The arithmetic, for the Q&A. Every rule is one bit, and every bit doubles the
configurations. Walk the diagram left to right: two sequential ifs multiply, 2 x 2, into four
configurations, bits 00 to 11; the if/elif adds, 2 + 1, into three; the general form is the
product of each block's alternatives. Compare with the cyclomatic number: it adds, decisions + 1
= 7, the basis paths a branch suite walks; the rules multiply into 64 configurations.
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
