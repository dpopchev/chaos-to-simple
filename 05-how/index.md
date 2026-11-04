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

## Rules belong together because they answer the same business question {paths=512}


![](build/05-how/cohesion.png){height=42%}

these rules belong together because we discuss and change them together, not because they contain similar Python; cohesion is the name for that

\thread{3}

\theline{A boundary is a technical choice}{A boundary is an agreement about what the other side must know: providers report facts, the shop decides what they mean.}

::: notes
The coupon-then-member decision (q2) is the short illustration: two rules in one pricing calculation, answering one business question.
The groups are candidate model boundaries the departments helped discover, not boundaries a department defines.
:::

## A boundary is an agreement about what the other side must know {paths=512}


:::: {.columns}
::: {.column width="55%"}

```{.python include=05-how/s05_how/warehouse_adapter.py snippet=adapter cap=16}
```

:::
::: {.column width="45%"}

![](build/05-how/ports.png){height=45%}

:::
::::

\begingroup\footnotesize Reserved: the warehouse set the items aside for this order for 15 minutes; the shell depends on Reserved | OutOfStock, never on the JSON; reserve before charge is written in the shell, the type does not enforce it\par\endgroup

we still depend on the warehouse; we no longer need its language everywhere in checkout

\thread{4}
