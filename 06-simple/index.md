# Simple: functional core, imperative shell

## Cut along the seam {paths=512}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="52%"}

```{.python include=06-simple/s06_simple/core.py snippet=price}
```

:::
::: {.column width="48%"}

```{.diff include=build/06-simple/seam.diff cap=28}
```

:::
::::

the only change: the pure part moves out

::: notes
The pure part moves out into price, and the shell keeps the three calls.
Nothing else changed: same decisions, one place each.
:::

## Sixty-four paths, three invariants: 192 tests {paths=512}

\fvset{fontsize=\scriptsize}

```{.python include=06-simple/tests/test_core_paths.py snippet=from-bits}
```

```{.text include=build/06-simple/pytest-core-summary.txt}
```

::: notes
The core has no if of its own, every bit stays where it was named.
64 paths, one test each, three invariants per path, and the count is measured.
:::

## Eight worlds, four outcomes {paths=512}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="55%"}

```{.python include=06-simple/s06_simple/worlds.py snippet=eight}
```

:::
::: {.column width="45%"}

```{.text include=build/06-simple/worlds.txt}
```

:::
::::

::: notes
Eight shell worlds collapse to four outcomes.
No charge when stock is gone, no mail when the card is refused.
:::

## The wounds close by name {paths=512}

\fvset{fontsize=\scriptsize}

```{.text include=build/06-simple/postmortem.txt}
```

```{.text include=build/06-simple/wounds.txt}
```

every wound closes by name; the seam made each decision local

::: notes
I1 and I3 close by name, each wound is now a test with its own name.
The core has no if of its own, so neither wound can come back through a decision.
:::

## The number {paths=72}

![](build/06-simple/paths.png){height=65%}

```{.text include=build/data/splits.txt}
```

No decision is ever deleted, only moved

::: notes
512 against 72: branch coverage was 100% before and after.
Nothing was deleted, every decision only moved to the place that owns it.
:::

## Epilogue: marketing's seventh if {paths=72}

\fvset{fontsize=\scriptsize}

```{.text include=01-bits/data/squeeze.txt}
```

:::: {.columns}
::: {.column width="60%"}

\fvset{fontsize=\tiny}

```{.diff include=build/06-simple/seventh.diff cap=18}
```

```{.text include=build/06-simple/epilogue.txt}
```

:::
::: {.column width="40%"}

![](build/06-simple/epilogue.png){height=60%}

:::
::::

\theline{One more if is cheap}{Decisions in the core, effects in the shell. The next if costs 8, not 512.}

::: notes
Marketing's seventh if lands in shipping, one bit in one context: +8, not +512.
The core stays untouched, the new decision sits in one place with its own tests.
:::
