# 08 Backup: the mechanisms and the evidence behind the seam

## Agreement on the What and certainty on the How guide each move {paths=64}

:::: {.columns align=center}
::: {.column width="58%"}

![](build/08-backup/stacey-overview.png){height=80%}

:::
::: {.column width="42%"}

\input{build/08-backup/zones.tex}

\footnotesize

- The Who line: stakeholders decide above it, developers below; the grey band is collaboration: none in Simple, most of Chaos.
- The arrows: the talk's movement, 01 to 06.

:::
::::

::: notes
Read the matrix from the origin: both axes start certain. The arrows are the route of the talk,
from 01 to 06, and the footer counter is still ? until each section sets it. The agenda strip
returns on the section pages. The grey band is collaboration: none in Simple, where the Who line
stands alone, and widening through Complicated and Complex to most of Chaos.
:::

## Changing the call order changes the price: 45 against 44 {paths=512}

```{.python heading-file=build/05-how/tests-order.txt include=05-how/tests/test_oo_order.py snippet=order-bit}
```

\begingroup\footnotesize 05-how/tests/test_oo_order.py: the call order of the next frame's class, tested by make test K=TestCallOrder\par\endgroup

::: notes
The call order is a bit nobody wrote down: 45 against 44 from the same inputs.
Live demo: make test K=TestCallOrder. The first test follows the rule, the second one differs.
:::

## This mutable checkout leaves discount order to its callers {paths=512}

```{.python heading-file=build/05-how/oo.txt include=05-how/s05_how/oo_checkout.py snippet=oo}
```

\begingroup\footnotesize 05-how/s05_how/oo_checkout.py in pricing; tested by test_oo_order.py\par\endgroup

same bug, pricing edition: the order hidden in state

::: notes
Past me reached for a class, so the order of the steps hid in its state.
Each method reads and changes the same fields, and the call sequence became a bit nobody could see.
It is the same bug as I3, pricing edition.
:::

## Explicit outcome values make the three effects easier to handle and match {paths=512}

:::: {.columns}
::: {.column width="50%"}

query: returns a value, changes nothing

command: changes the world, answers with a value

the seam: where asking ends and doing begins

```{.python heading="the answers" include=05-how/s05_how/ports.py snippet=types}
```

:::
::: {.column width="50%"}

```{.python heading-file=build/05-how/ports-code.txt include=05-how/s05_how/ports.py snippet=ports}
```

:::
::::

make every answer a value

\begingroup\footnotesize 05-how/s05_how/ports.py in fulfilment; tested by test_ports.py\par\endgroup

::: notes
Command query separation: a query asks, a command answers with a value, never both.
Every answer is a value the caller can match on, so the order stops living in state.
:::

## Protocols accept compatible fakes without inheritance: pyright reports zero errors {paths=512}

:::: {.columns}
::: {.column width="55%"}

```{.python heading-file=build/05-how/fakes-code.txt include=05-how/s05_how/fakes.py snippet=fakes cap=28}
```

:::
::: {.column width="45%"}

```{.text heading="uv run pyright fakes.py test_ports.py" include=build/05-how/pyright.txt}
```

\begingroup\footnotesize FakeGateway: Charged | Declined\par FakeInventory: Reserved | OutOfStock\par FakeMailer: the same shape, Sent | Bounced, in fakes.py\par\endgroup

:::
::::

::: notes
Each answer is its own type: Charged or Declined, Reserved or OutOfStock, Sent or Bounced.
A fake is a plain class with the same method. It never inherits from the port, and pyright accepts it anyway: zero errors.
The test doubles carry one bit each, so a shell test can enumerate the world.
:::

## Stock reservation must succeed before payment is attempted {paths=512}


:::: {.columns}
::: {.column width="45%"}

![](build/05-how/ports.png){height=60%}

\begingroup\footnotesize 05-how/s05_how/checkout_v5.py in fulfilment; tested by test_checkout_v5.py and test_i3.py\par\endgroup

:::
::: {.column width="55%"}

```{.diff include=build/05-how/v5.diff cap=28}
```

:::
::::

above the first match every line is a value; below it three answers, reserve first: that is the seam

::: notes
The ports picture sits beside the v4-to-v5 diff. Reserve goes first, and every answer is matched.
The diff is only the seam, so the picture and the code say the same thing.
:::

## Pricing, shipping and tax import no provider port; only the shell does {paths=512}

![](build/05-how/imports.png){width=88%}

```{.text heading="names imported, counted from the files" include=build/05-how/imports.txt}
```

the What does not know the world: a context returns a value and asks nothing

::: notes
The table is counted from the import lines of the files, never typed.
The shell imports the ports and the contexts. The contexts import neither the ports nor the shell: zero under ports on every context row.
:::

## Explicit contracts limit the knowledge crossing each boundary {paths=512}

\footnotesize

| move | sign | in this talk |
|---|---|---|
| guard clause | + 1 | `max(total, 0)` in pricing |
| `elif` / `match` over a sum type | + k | `Zone` in `base_fee` |
| extract a pure function that returns a value | + | `shipping_fee` returns the fee |
| pass a flag across a boundary | x | subtotal into the threshold (I1) |
| mutable state read in a later step | hidden x | `self.total`, 45 against 44 |
| `try`/`except` around I/O inside the rules | hidden x | the log nobody reads (I3) |

contract: shipping_fee(discounted_goods, zone, gift_wrap) -> Money, so shipping learns the discounted goods, never the coupon -- the concrete contract the title 'Explicit contracts limit the knowledge crossing each boundary' claims; the frame is already \footnotesize from line 129.

::: notes
The moves table: each move adds a path or hides one.
Guard clauses and sum types add paths you can count; flags and mutable state hide them.
:::

## Values carry inputs and results across the calculation boundary {paths=512}


:::: {.columns}
::: {.column width="50%"}

```{.python heading-file=build/06-simple/request.txt include=06-simple/s06_simple/core.py snippet=request cap=18}
```

:::
::: {.column width="50%"}

```{.python heading-file=build/06-simple/outcome.txt include=06-simple/s06_simple/shell.py snippet=outcome cap=12}
```

:::
::::

values in, values out: the seam passes data, never a flag and never an effect

::: notes
Request holds every decision the core needs: the skus, the coupon, the member flag, the zone, the VAT id. Priced holds every result that comes back out: goods, shipping, total. The core never sees a port; the shell sequences the effects and handles their failures, policies of its own. Outcome is the shell's own answer, Accepted or Rejected, a value too.
:::

## Three invariants check 64 configurations in 192 test cases {paths=512}


```{.python heading-file=build/06-simple/tests-core.txt include=06-simple/tests/test_core_paths.py snippet=from-bits}
```

06-simple/tests/test_core_paths.py: 64 paths x 3 invariants, tested by itself; the other two invariants in the file

```{.text include=build/06-simple/pytest-core-summary.txt}
```

::: notes
The core has no if of its own, every bit stays where it was named.
64 paths, one test each, three invariants per path, and the count is measured.
:::

## Eight test worlds produce four explicit order outcomes {paths=512}


:::: {.columns}
::: {.column width="45%"}

```{.python heading-file=build/06-simple/worlds-code.txt include=06-simple/s06_simple/worlds.py snippet=eight}
```

\begingroup\footnotesize 06-simple/s06_simple/worlds.py in fulfilment; tested by test_worlds.py\par\endgroup

:::
::: {.column width="55%"}

```{.text include=build/06-simple/worlds.txt}
```

:::
::::

charged: money moved, declined: attempted and not succeeded; mailed: delivered, bounced: attempted and not delivered

::: notes
Eight shell worlds collapse to four outcomes.
No charge when stock is gone, no mail when the card is refused.
:::

## Pricing, shipping and tax hold every decision of the functional core, core.py only composes {paths=512}


:::: {.columns}
::: {.column width="42%"}

![](build/06-simple/ifs.png){width=100%}

:::
::: {.column width="58%"}

![](build/06-simple/imports.png){width=100%}

:::
::::

cohesion: a rule changes in one module; decoupling: the shell imports core.py and the ports; core.py composes the three contexts and imports no port

::: notes
Five ifs and one match live in the three contexts: pricing two ifs, shipping two ifs and a match over the Zone sum type, tax one if. core.py holds none; shell.py holds no if and keeps its three matches at the edge. The right figure draws the imports: the shell imports the core and the ports, the core imports the three contexts, no context imports a port. Live demo: git grep -n 'if ' 06-simple/s06_simple/shell.py returns only the docstring that states the house rule.
:::

## The split leaves 72 local paths instead of 512, with integration checked separately {paths=72}

![](build/06-simple/paths.png){width=72%}

```{.text include=build/data/splits.txt}
```

No decision is ever deleted, only moved

\footnotesize assumes each context tested alone against its contract and the shell against fakes; the integration checks are separate; the payoff is clearer ownership and local reasoning, not a guaranteed cut in effort

::: notes
512 against 72: branch coverage was 100% before and after.
Nothing was deleted, every decision only moved to the place that owns it.
:::

## The seventh decision adds 8 local paths in shipping, against 512 in one function {paths=72}

```{.text include=build/06-simple/epilogue.txt}
```

![](build/06-simple/epilogue.png){width=60%}

\footnotesize assumes each context tested alone against its contract and the shell against fakes; the integration checks are separate; the payoff is clearer ownership and local reasoning, not a guaranteed cut in effort

::: notes
The same seventh if, counted three ways: one function doubles to 1024 (+512), core and shell add 64, contexts and shell add 8.
:::
