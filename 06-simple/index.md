# 06 Core and shell: functional core, imperative shell

## Moving the pure part out into price cuts along the seam and changes nothing else {paths=512}


:::: {.columns}
::: {.column width="52%"}

```{.python include=06-simple/s06_simple/core.py snippet=price}
```

\begingroup\footnotesize 06-simple/s06_simple/core.py price in the core; tested by test_core_paths.py\par\endgroup

:::
::: {.column width="48%"}

```{.text include=build/06-simple/tally-10.txt}
```

```{.diff include=build/06-simple/seam.diff cap=28}
```

\begingroup\footnotesize 06-simple/s06_simple/shell.py in fulfilment; tested by test_shell.py\par\endgroup

:::
::::

the only change: the pure part moves out

::: notes
The pure part moves out into price, and the shell keeps the three calls.
Nothing else changed: same decisions, one place each.
:::

## Every one of 64 paths holds three invariants, so the core runs 192 tests {paths=512}


```{.python include=06-simple/tests/test_core_paths.py snippet=from-bits}
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

```{.python include=06-simple/s06_simple/worlds.py snippet=eight}
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

![](build/06-simple/paths.png){height=61%}

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

![](build/06-simple/epilogue.png){height=54%}

:::
::::

\footnotesize the seventh if is a supporting change, and a supporting change should be cheap; it was not, until the split

\theline{One more if is cheap}{Decisions in the core, effects in the shell. The next if costs 8, not 512.}

::: notes
Marketing's seventh if lands in shipping, one bit in one context: +8, not +512.
The core stays untouched, the new decision sits in one place with its own tests.
The shipping context is supporting, so +8 is what a supporting change should cost.
:::
