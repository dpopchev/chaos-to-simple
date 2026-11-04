# 08 Backup: the mechanisms behind the seam, for the Q&A

## The call order is a bit nobody wrote down, giving 45 against 44 from the same inputs {paths=512}

```{.python heading-file=build/05-how/tests-order.txt include=05-how/tests/test_oo_order.py snippet=order-bit}
```

\begingroup\footnotesize 05-how/tests/test_oo_order.py: the call order of the next frame's class, tested by make test K=TestCallOrder\par\endgroup

::: notes
The call order is a bit nobody wrote down: 45 against 44 from the same inputs.
Live demo: make test K=TestCallOrder. The first test follows the rule, the second one differs.
:::

## A class hid the call order in its state, the same bug as I3 in pricing {paths=512}

```{.python heading-file=build/05-how/oo.txt include=05-how/s05_how/oo_checkout.py snippet=oo}
```

\begingroup\footnotesize 05-how/s05_how/oo_checkout.py in pricing; tested by test_oo_order.py\par\endgroup

same bug, pricing edition: the order hidden in state

::: notes
Past me reached for a class, so the order of the steps hid in its state.
Each method reads and changes the same fields, and the call sequence became a bit nobody could see.
It is the same bug as I3, pricing edition.
:::

## Command Query Separation draws the seam by making every answer a value {paths=512}

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

## A sum type per answer and a Protocol per port: the fakes satisfy them with no inheritance, pyright says so {paths=512}

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

## Each effect answers with a value, so reserve runs first and every answer is matched {paths=512}


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

## Dependencies point inward: the shell imports the ports and the contexts, no context imports a port {paths=512}

![](build/05-how/imports.png){width=90%}

```{.text heading="names imported, counted from the files" include=build/05-how/imports.txt}
```

the What does not know the world: a context returns a value and asks nothing

::: notes
The table is counted from the import lines of the files, never typed.
The shell imports the ports and the contexts. The contexts import neither the ports nor the shell: zero under ports on every context row.
:::

## Passing values across a boundary adds paths you can count, passing flags multiplies them {paths=512}

\footnotesize

| move | sign | in this talk |
|---|---|---|
| guard clause | + 1 | `max(total, 0)` in pricing |
| `elif` / `match` over a sum type | + k | `Zone` in `base_fee` |
| extract a pure function that returns a value | + | `shipping_fee` returns the fee |
| pass a flag across a boundary | x | subtotal into the threshold (I1) |
| mutable state read in a later step | hidden x | `self.total`, 45 against 44 |
| `try`/`except` around I/O inside the rules | hidden x | the log nobody reads (I3) |

::: notes
The moves table: each move adds a path or hides one.
Guard clauses and sum types add paths you can count; flags and mutable state hide them.
:::

## Request carries every decision in and Priced every result out, so the core never sees a port and the shell never sees a rule {paths=512}


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
Request holds every decision the core needs: the skus, the coupon, the member flag, the zone, the VAT id. Priced holds every result that comes back out: goods, shipping, total. The core never sees a port, the shell never sees a rule. Outcome is the shell's own answer, Accepted or Rejected, a value too.
:::

## Every one of 64 paths holds three invariants, so the core runs 192 tests {paths=512}


```{.python heading-file=build/06-simple/tests-core.txt include=06-simple/tests/test_core_paths.py snippet=from-bits}
```

06-simple/tests/test_core_paths.py: 64 paths x 3 invariants, tested by itself; the other two invariants in the file

```{.text include=build/06-simple/pytest-core-summary.txt}
```

::: notes
The core has no if of its own, every bit stays where it was named.
64 paths, one test each, three invariants per path, and the count is measured.
:::

## Eight shell worlds collapse to four outcomes, with no charge when stock is gone {paths=512}


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

## Five ifs and one match live in three contexts, none in the core, and the shell holds three matches at the edge {paths=512}


:::: {.columns}
::: {.column width="42%"}

![](build/06-simple/ifs.png){width=100%}

:::
::: {.column width="58%"}

![](build/06-simple/imports.png){width=100%}

:::
::::

cohesion: a rule changes in one module; decoupling: the shell imports the core and the ports, the core imports no port

::: notes
Five ifs and one match live in the three contexts: pricing two ifs, shipping two ifs and a match over the Zone sum type, tax one if. core.py holds none; shell.py holds no if and keeps its three matches at the edge. The right figure draws the imports: the shell imports the core and the ports, the core imports the three contexts, no context imports a port. Live demo: git grep -n 'if ' 06-simple/s06_simple/shell.py returns only the docstring that states the house rule.
:::

## The split cuts 512 paths to 72 while branch coverage stays at 100% as before {paths=72}

![](build/06-simple/paths.png){width=72%}

```{.text include=build/data/splits.txt}
```

No decision is ever deleted, only moved

\footnotesize assumes each context tested alone against its contract and the shell against fakes; the integration checks are separate; the payoff is clearer ownership and local reasoning, not a guaranteed cut in effort

::: notes
512 against 72: branch coverage was 100% before and after.
Nothing was deleted, every decision only moved to the place that owns it.
:::

## The seventh if costs 8 paths in the contexts and 512 in one function, under the same assumptions {paths=72}

```{.text include=build/06-simple/epilogue.txt}
```

![](build/06-simple/epilogue.png){width=60%}

\footnotesize assumes each context tested alone against its contract and the shell against fakes; the integration checks are separate; the payoff is clearer ownership and local reasoning, not a guaranteed cut in effort

::: notes
The same seventh if, counted three ways: one function doubles to 1024 (+512), core and shell add 64, contexts and shell add 8.
:::
