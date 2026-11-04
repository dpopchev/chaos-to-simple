# 05 Seam: decoupling, cohesion, FP vs OO, CQS

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

## I3 charged cards for missing stock because charge ran before reserve {paths=512}


```{.text include=05-how/data/incident.txt}
```

```{.python include=05-how/tests/test_i3.py snippet=i3}
```

```{.text include=build/05-how/i3-run.txt}
```

support raised the flag, the test points at the shell: reserve before charge (q5)

::: notes
I3 comes first, before any design word. Support raised the flag: cards charged for parcels the warehouse did not have.
The test writes the rule down against checkout v4, and the run under it shows the order the code happened to take: charge, then reserve.
:::

\theline{A class will keep it tidy}{A method that does and tells hides a bit. Separate asking from doing; make every answer a value.}
