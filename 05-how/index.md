# 05 Seam: the boundary protects a business promise

## A correct price did not guarantee a fulfilled order {paths=512}


```{.text include=05-how/data/incident.txt}
```

:::: {.columns}
::: {.column width="50%"}

red, then green: q5 was decided in the room and not yet in the code when the refunds hit; the full diff is in the backup

```{.python include=build/05-how/i3-run.txt}
```

:::
::: {.column width="50%"}

```{.python heading="the fix (v5): reserve first, every answer a value" include=05-how/s05_how/checkout_v5.py start-line=56 end-line=60}
```

```{.text heading="the regression, green against v5" include=build/05-how/i3-green.txt}
```

:::
::::

\thread{1}

::: notes
We now agree how to calculate the order. But a correct total is not the same as an order we can fulfil.
I had treated these as three technical calls. The business saw one promise: an accepted order must mean something.
The promise picture (reserve before charge) is in the README; the code says it here.
:::

## Providers report facts; Fulfilment decides what the shop does with each answer {paths=512}


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

## Rules answering the same business question belong together: four questions, four homes {paths=512}


![](build/05-how/cohesion.png){width=80%}

\begingroup\footnotesize Rules that change together stay together; cohesion is the name for that -- candidate boundaries the departments helped discover, not bounded contexts proven\par\endgroup

\thread{3}

::: notes
These rules belong together because we change them together, not because the Python looks alike; cohesion is the name for that.
The coupon-then-member decision (q2) is the short illustration: two rules in one pricing calculation, answering one business question.
The groups are candidate model boundaries the departments helped discover, not boundaries a department defines.
:::

## Reserved must mean a 15-minute hold, not just a status word {paths=512}


```{.python include=05-how/s05_how/warehouse_adapter.py snippet=adapter cap=16}
```

\begingroup\footnotesize Reserved: the adapter asks for a 15-minute hold and reads Reserved | OutOfStock, never the JSON; whether the provider honours the hold is a check this talk does not have; reserve-before-charge lives in the shell\par\endgroup

\theline{A boundary is a technical choice}{A boundary is an agreement about what the other side must know: providers report outcomes, the shop decides.}

## The shell connects pure calculations to real-world commitments {paths=512}

![](build/05-how/ports.png){width=70%}

::: notes
We still depend on the warehouse; we no longer need its language everywhere in checkout.
:::

\thread{4}
