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


:::: {.columns}
::: {.column width="50%"}

```{.diff include=build/04-what/fix.diff cap=18}
```

:::
::: {.column width="50%"}

```{.python heading-file=build/04-what/tests-7.txt include=04-what/tests/test_checkout_stages.py snippet=i1}
```

```{.text include=build/04-what/fix-run.txt}
```

:::
::::

q3 fixed: the threshold reads the discounted goods, a value pricing returns, the first boundary; i1() is the 55 EUR order with the coupon

::: notes
The threshold now reads the discounted goods, so I1 closes.
The diff is the whole fix: one name changes, and the rest of the function stays as it was.
:::

## Shipping owns the dispute's rule and a sum type lets the checker count its bit {paths=512}


```{.text include=build/04-what/dispute.txt}
```

:::: {.columns}
::: {.column width="52%"}

```{.python include=04-what/s04_what/shipping.py snippet=fee heading-file=build/04-what/fee.txt}
```

:::
::: {.column width="48%"}

```{.python include=04-what/tests/test_shipping.py snippet=fee-tests heading-file=build/04-what/tests-fee.txt}
```

:::
::::

the rule belongs to shipping, Zone is a sum type: the checker counts that bit

::: notes
The sentence decided in the room is now a value. coupon.is_valid_on(today), in pricing.py, is the q1 sentence.
The fee is charged on the discounted goods, and no flag carries the decision across contexts.
Zone has two states, so the type is a sum and not a flag: a state with no case is an error, not a silent default.
Live: delete the INTERNATIONAL case in base_fee and run uv run pyright: the type checker counts the bit. Put it back.
:::

## Each bit now has a home in pricing, shipping, tax or shell, named by who asked {paths=512}


:::: {.columns}
::: {.column width="80%"}

```{.python heading-file=build/04-what/code-8.txt include=04-what/s04_what/checkout_v4.py snippet=checkout cap=18}
```

:::
::: {.column width="20%"}

\scriptsize

pricing: \actor{marketing} \actor{loyalty}

shipping: \actor{logistics} \actor{marketing}

tax: \actor{accounting}

shell: \actor{payment} \actor{warehouse} \actor{mailer}

:::
::::

::: notes
The same function now makes three context calls, and its effects are still inline.
Every bit has a home and a face: each context names the people who asked for its rules.
The file is checkout_v4.py if anyone asks; the deck counts versions.
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
