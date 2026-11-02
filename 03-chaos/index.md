# From chaos to complex

## The journey of one order {paths=64}

![](build/03-chaos/diagrams/journey.png){height=80%}

::: notes
One order, one afternoon. Maria buys two books and the coupon goes to Sofia, who places the
order for her. Follow the order left to right: the cart, the coupon, the free-shipping line,
the member discount, the payment, the warehouse, the mail.
The mood drops at every step that raised a question, q1 to q6, in the order the room asked
them. Each drop is a place where the rule was not written down yet.
:::

## The room {paths=64}

\fvset{fontsize=\scriptsize}

```{.text include=03-chaos/data/room.txt cap=18}
```

::: notes
Dev is silent until the end of the chat; the other four departments carry the argument.
Pause before the last line. Chat moment: which question would you have asked?
:::

## The retro {paths=64}

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
::: {.column width="62%"}

![](build/03-chaos/grid-9.png){width=100%}

```{.text include=build/data/counts.txt}
```

:::
::: {.column width="38%"}

![](build/03-chaos/doubling-512.png){width=100%}

:::
::::

::: notes
The grid you saw in 01 was one of eight. The four framed panels are the ones where the
stock is gone. The number is now true: 2^9 = 512. The bigger number is the first good news.
:::

## Nine decisions, none deleted, all moved {paths=512}

![](build/03-chaos/board.png){height=70%}

\theline{Counting makes it worse}{You cannot shrink a count you have not made. The bigger number is the first good news.}

::: notes
Nine decisions came out of the room, one row each on the board. Each one has a sentence and a home.
Coupon: a coupon valid today takes 10 BGN off the goods, in pricing.
Member: a loyalty member gets 10% off, applied after the coupon, in pricing.
Free shipping: shipping is free from 50 BGN of discounted goods, in shipping.
Zone: domestic shipping is 5 BGN, international 20 BGN, in shipping.
Gift wrap: gift wrap adds 3 BGN to the parcel, in shipping.
VAT: orders with a VAT ID are exempt, the rest pay 20 percent, in tax.
Charge, reserve and confirm: the payment, the warehouse and the mailer answer, in shell.
None of the nine is deleted; each one is moved to its home. The board comes back at the end of 04,
at the end of 05 and on the Q&A frame, and every test is green by then.
:::
