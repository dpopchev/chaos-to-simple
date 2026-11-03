# 03 Room: from chaos to complex

## The mood of one order drops at six questions, each a rule nobody wrote down {paths=64}

\begingroup\footnotesize finance traced 6,070 EUR to orders like this one, so the room replayed one order and scored each step: who decided this?\par\endgroup

![](build/03-chaos/diagrams/journey.png){width=90%}

::: notes
One order, one afternoon. Maria buys two books and the coupon goes to Sofia, who places the
order for her. Follow the order left to right: the cart, the coupon, the free-shipping line,
the member discount, the payment, the warehouse, the mail.
The line is how sure the room was. In the retro the room replayed Maria's order step by step
and scored each step: an unwritten rule costs 1, an unhandled answer of an effect costs 2.
It drops at every step that raised a question, q1 to q6, in the order the room asked them.
Each drop is a place where the rule was not written down yet.
:::

## Four departments carry the argument in one room while dev stays silent to the end {paths=64}


```{.text .speakers include=03-chaos/data/room.txt cap=18}
```

the clashes in bold; the outcome: six questions, each with an owner, the action table of the next frame

::: notes
Dev is silent until the end of the chat; the other four departments carry the argument.
Pause before the last line. Chat moment: which question would you have asked?
Reading plan: read the Logistics first line aloud, then the Marketing answer; skip to
'Who reads the log?'; then the silence, and let the room hear it.
:::

## The retro names six business decisions, two core and four in supporting subdomains {paths=64}


```{.text .speakers highlight=q3 include=build/03-chaos/retro.txt cap=18}
```

q3 to q6 are the shop's own answers, supporting; the capability behind q4 to q6 is generic, bought from the providers

::: notes
The subdomain column is the map of page 2: q1 and q2 are core, q3 to q6 supporting; the capability behind q4 to q6 is generic.
Question 3 had two positions: does the coupon that expired on Sunday count on Sunday or on
Monday. The code decided for them, and that is incident I2. The room decided after the
discount, not before it: the rule came last, after the code had already picked one side.
:::

## Counting the nine decisions honestly gives 512 paths, not 64, the first good news {paths=512}


:::: {.columns}
::: {.column width="62%"}

![](build/03-chaos/grid-9.png){width=88%}

\footnotesize same six bits; each answer of the three effects doubles the grid; the two tests still sit in one panel

```{.text include=build/data/counts.txt}
```

:::
::: {.column width="38%"}

![](build/02-stacey/stacey-03.png){width=100%}

\footnotesize the What agreed in the room, the How is now the question: 512 paths

:::
::::

::: notes
The grid you saw in 01 was one of eight. The four framed panels are the ones where the
stock is gone. The number is now true: 2^9 = 512. The bigger number is the first good news.
The right side is the plain matrix of 03, arrows from 01: the What is agreed, the How is open.
:::

## Nine decisions came out of the room, and each moves to a home, none deleted {paths=512}

![](build/03-chaos/board.png){width=65%}

\footnotesize nine rows, nine bits: 2^9 = 512 until every row has a home

\theline{Counting makes it worse}{You cannot shrink a count you have not made. The bigger number is the first good news.}

::: notes
Nine decisions came out of the room, one row each on the board. Each one has a sentence and a home.
Each row is one bit of the honest count; better technical decisions, not fewer rules, bring it down.
Coupon: a coupon valid today takes 10 EUR off the goods, in pricing.
Member: a loyalty member gets 10% off, applied after the coupon, in pricing.
Free shipping: shipping is free from 50 EUR of discounted goods, in shipping.
Zone: domestic shipping is 5 EUR, international 20 EUR, in shipping.
Gift wrap: gift wrap adds 3 EUR to the parcel, in shipping.
VAT: orders with a VAT ID are exempt, the rest pay 20 percent, in tax.
Charge, reserve and confirm: the payment, the warehouse and the mailer answer, in shell.
None of the nine is deleted; each one is moved to its home. The board comes back at the end of 04,
at the end of 05 and on the Q&A frame, and every test is green by then.
:::
