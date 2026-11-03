# 04 Homes: one language, bounded contexts

## Coloring every line by who asked for it shows which context each if belongs to {paths=512}

![](build/04-what/colorcode.png){height=80%}

::: notes
Every line is coloured by who asked for it and by the context that owns it.
The colours show where each if comes from before anyone reads its name.
The right bar is the home, and the legend names its kind: core, supporting or generic.
This is how the code will move, one home at a time.
:::

## One renamed value, the discounted goods, closes I1 and draws the first boundary {paths=512}

\fvset{fontsize=\scriptsize}

```{.diff include=build/04-what/fix.diff cap=18}
```

one name: discounted goods, a value pricing returns -- the first boundary

::: notes
The threshold now reads the discounted goods, so I1 closes.
The diff is the whole fix: one name changes, and the rest of the function stays as it was.
:::

## Shipping owns the dispute's rule and a sum type lets the checker count its bit {paths=512}

\fvset{fontsize=\scriptsize}

```{.text include=build/04-what/dispute.txt}
```

```{.python include=04-what/s04_what/shipping.py snippet=fee}
```

the rule belongs to shipping, Zone is a sum type: the checker counts that bit

::: notes
The sentence decided in the room is now a value. coupon.is_valid_on(today), in pricing.py, is the q1 sentence.
The fee is charged on the discounted goods, and no flag carries the decision across contexts.
Zone has two states, so the type is a sum and not a flag: a state with no case is an error, not a silent default.
Live: delete the INTERNATIONAL case in base_fee and run uv run pyright: the type checker counts the bit. Put it back.
:::

## Each bit now has a home in pricing, shipping, tax or shell, named by who asked {paths=512}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="75%"}

checkout_fixed.py -> checkout_v4.py

```{.python include=04-what/s04_what/checkout_v4.py snippet=checkout cap=18}
```

:::
::: {.column width="25%"}

pricing: \actor{marketing} \actor{loyalty}

shipping: \actor{logistics} \actor{marketing}

tax: \actor{accounting}

shell: \actor{payment} \actor{warehouse} \actor{mailer}

:::
::::

::: notes
The same function now makes three context calls, and its effects are still inline.
Every bit has a home and a face: each context names the people who asked for its rules.
:::

## All nine decisions moved home: core and supporting the What, generic adapted at the shell {paths=512}

![](build/04-what/moves.png){width=80%}

core and supporting: the What, in three homes; generic: adapted at the shell

::: notes
Pricing is the core; shipping and fulfilment are supporting, so the What spans three homes.
Tax is generic: kept in-house and adapted at the shell, with the payment, warehouse and mailer ports.
None of the nine decisions is deleted: each has a new home and stays on the record.
:::

\theline{Naming is cosmetics}{Every if was somebody's sentence. Write it down, give it a home, pass values between homes.}
