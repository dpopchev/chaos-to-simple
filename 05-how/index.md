# 05 Seam: who decides, what is promised, what belongs together

## The price was correct, but the promise to the customer was not kept {paths=512}


```{.text include=05-how/data/incident.txt}
```

![](build/05-how/promise.png){height=38%}

the red test, as evidence: reserve before charge (q5)

```{.text include=build/05-how/i3-run.txt}
```

\thread{1}

::: notes
We now agree how to calculate the order. But a correct total is not the same as an order we can fulfil.
I had treated these as three technical calls. The business saw one promise: an accepted order must mean something.
:::

## Providers report facts, and the shop decides what they mean {paths=512}


```{.text .speakers include=build/05-how/policies.txt}
```

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/05-how/bubble-0.txt}
```

:::
::: {.column width="50%"}

```{.text include=build/05-how/bubble-1.txt}
```

:::
::::

bounced is a provider outcome; keeping an accepted order is the shop's policy; open: release the reservation after a declined payment, not in the shell yet

\thread{2}

::: notes
The exchange is proposed story material, not a transcript. The Fulfilment owner consulted Logistics, Finance and Support before writing the three policies down.
:::

\theline{A class will keep it tidy}{A method that does and tells hides a bit. Separate asking from doing; make every answer a value.}

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
