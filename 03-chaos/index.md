# From chaos to complex

## The journey of one order {paths=?}

![](build/03-chaos/diagrams/journey.png){height=80%}

::: notes
One order, one afternoon. Maria buys two books and the coupon goes to Sofia, who places the
order for her. Follow the order left to right: the cart, the coupon, the free-shipping line,
the member discount, the payment, the warehouse, the mail.
The mood drops at every step that raised a question, q1 to q6, in the order the room asked
them. Each drop is a place where the rule was not written down yet.
:::

## The room {paths=?}

\fvset{fontsize=\scriptsize}

```{.text include=03-chaos/data/room.txt cap=18}
```

::: notes
Dev is silent until the end of the chat; the other four departments carry the argument.
Pause before the last line. Chat moment: which question would you have asked?
:::

## The retro {paths=?}

\fvset{fontsize=\scriptsize}

```{.text include=build/03-chaos/retro.txt}
```

::: notes
Question 3 had two positions: does the coupon that expired on Sunday count on Sunday or on
Monday. The code decided for them, and that is incident I2. The room decided after the
discount, not before it: the rule came last, after the code had already picked one side.
:::

## The honest count {paths=512}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

![](build/03-chaos/grid-9.png){height=60%}

![](build/03-chaos/doubling-512.png){height=30%}

:::
::: {.column width="50%"}

```{.text include=build/data/counts.txt}
```

:::
::::

## Nine decisions, none deleted, all moved {paths=512}

![](build/03-chaos/board.png){height=70%}

\theline{Counting makes it worse}{You cannot shrink a count you have not made. The bigger number is the first good news.}
