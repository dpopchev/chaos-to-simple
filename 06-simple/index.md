# 06 Core and shell: functional core, imperative shell

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

## Moving the pure part out into price cuts along the seam and changes nothing else {paths=512}


:::: {.columns}
::: {.column width="52%"}

```{.python heading-file=build/06-simple/price.txt include=06-simple/s06_simple/core.py snippet=price}
```

:::
::: {.column width="48%"}

```{.python heading-file=build/06-simple/shell.txt include=06-simple/s06_simple/shell.py snippet=checkout cap=22}
```

:::
::::

the only change: the pure part moved out; the shell reads request and priced

::: notes
The pure part moves out into price; the shell keeps v9's three matches word for word. If anyone asks for the diff: make build/06-simple/seam.diff -- seven pricing lines out, one line in, the reads renamed.
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

## I1 and I3 each close by name as a test, and the seam keeps both from returning {paths=512}


```{.text include=build/06-simple/postmortem.txt}
```

```{.text include=build/06-simple/wounds.txt}
```

every wound closes by name; the seam made each decision local

::: notes
I1 and I3 close by name, each wound is now a test with its own name.
The core has no if of its own, so neither wound can come back through a decision.
:::

## The split cuts 512 paths to 72 while branch coverage stays at 100% as before {paths=72}

![](build/06-simple/paths.png){width=88%}

```{.text include=build/data/splits.txt}
```

No decision is ever deleted, only moved

::: notes
512 against 72: branch coverage was 100% before and after.
Nothing was deleted, every decision only moved to the place that owns it.
:::

## Marketing's seventh if lands in shipping and costs 8 paths {paths=72}


```{.text include=01-bits/data/squeeze.txt}
```

:::: {.columns}
::: {.column width="60%"}


```{.diff include=build/06-simple/seventh.diff cap=18}
```

\begingroup\footnotesize 06-simple/s06_simple/seventh.py in shipping; tested by test_seventh.py\par\endgroup

```{.text include=build/06-simple/epilogue.txt}
```

:::
::: {.column width="40%"}

![](build/06-simple/epilogue.png){width=100%}

:::
::::

\footnotesize the seventh if is a supporting change, and a supporting change should be cheap; it was not, until the split

\theline{One more if is cheap}{Decisions in the core, effects in the shell. The next if costs 8, not 512.}

::: notes
Marketing's seventh if lands in shipping, one bit in one context: +8, not +512.
The core stays untouched, the new decision sits in one place with its own tests.
The shipping context is supporting, so +8 is what a supporting change should cost.
:::
