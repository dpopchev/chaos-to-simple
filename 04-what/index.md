# Complicated on the What: one language, bounded contexts

## Color-coded, the ifs get names {paths=512}

![](build/04-what/colorcode.png){height=80%}

::: notes
Every line is coloured by who asked for it and by the context that owns it.
The colours show where each if comes from before anyone reads its name.
:::

## The first fix {paths=512}

\fvset{fontsize=\scriptsize}

```{.diff include=build/04-what/fix.diff cap=18}
```

::: notes
The threshold now reads the discounted goods, so I1 closes.
The diff is the whole fix: one name changes, and the rest of the function stays as it was.
:::

## The dispute closes {paths=512}

\fvset{fontsize=\scriptsize}

```{.text include=build/04-what/dispute.txt}
```

```{.python include=04-what/s04_what/shipping.py snippet=fee}
```

Values, never flags.

::: notes
The sentence decided in the room is now a value. coupon.is_valid_on(today), in pricing.py, is the q1 sentence.
The fee is charged on the discounted goods, and no flag carries the decision across contexts.
:::

## A bit as a type {paths=512}

```{.python include=04-what/s04_what/shipping.py snippet=zone}
```

::: notes
Zone has two states, so the type is a sum and not a flag.
The type checker counts this bit: a state with no case is an error, not a silent default.
:::

## Bounded contexts: every bit has a home {paths=512}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="62%"}

```{.diff include=build/04-what/v4.diff cap=30}
```

:::
::: {.column width="38%"}

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

## Bounded contexts, the moves {paths=512}

:::: {.columns}
::: {.column width="50%"}

![](build/04-what/moves.png){height=55%}

:::
::: {.column width="50%"}

![](build/04-what/board.png){height=30%}

:::
::::

::: notes
Each home is a context, and the board shows the nine decisions moved.
None is deleted: each one has a new home and is still on the record.
:::

\theline{Naming is cosmetics}{Every if was somebody's sentence. Write it down, give it a home, pass values between homes.}
