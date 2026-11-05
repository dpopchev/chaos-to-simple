# 03 Room: shared examples turn hidden assumptions into explicit decisions

## Replaying one order reveals six unanswered business questions {paths=64}

\begingroup\footnotesize finance traced 6,070 EUR to orders like this one, so the room replayed one order and scored each step: who decided this?\par\endgroup

![](build/03-chaos/diagrams/journey.png){width=90%}

::: notes
One order, one afternoon. Maria buys two books and the coupon goes to Sofia, who places the
order for her. Follow the order left to right: the cart, the coupon, the free-shipping line,
the member discount, the payment, the warehouse, the mail.
The line is how sure the room was. In the retro the room replayed Maria's order step by step
and scored each step: an unwritten rule costs 1, an unhandled provider outcome costs 2.
It drops at every step that raised a question, q1 to q6, in the order the room asked them.
Each drop is a place where the rule was not written down yet.
:::

## The room surfaces three unwritten rules and three unhandled provider outcomes {paths=64}


```{.text .speakers include=03-chaos/data/room.txt cap=12}
```

the clashes in bold; the shop's calendar: week 16, five days after the memo; the outcome: six questions, each with an owner, the decisions of the next frame

::: notes
Dev is silent until the end of the chat; the other four departments carry the argument.
Pause before the last line. Chat moment: which question would you have asked?
Reading plan: read the Logistics first line aloud, then the Marketing answer; skip to
'Who reads the log?'; then the silence, and let the room hear it.
:::

## Every question gains a rule and an owner: q3 after the discount, Logistics {paths=64}

\moment{AGREED}{q3 decided in the room: the threshold reads the goods after the discount; Logistics owns the rule}

```{.text .speakers highlight=q3 include=build/03-chaos/retro.txt cap=18}
```

q3 to q6 are the shop's own answers, supporting; the capability behind q4 to q6 is generic, bought from the providers

::: notes
The subdomain column is the map of page 2: q1 and q2 are core, q3 to q6 supporting; the capability behind q4 to q6 is generic.
Question 3 had two positions: does the coupon that expired on Sunday count on Sunday or on
Monday. The code decided for them, and that is incident I2. The room decided after the
discount, not before it: the rule came last, after the code had already picked one side.
:::

## Three provider outcomes join the six rules: nine bits, 512 configurations, not 64 {paths=512}


![](build/03-chaos/grid-9.png){width=40%}

\footnotesize same six bits; each outcome of the three effects doubles the grid: 512 modeled configurations, kinds as the map named them; a failed reservation stops the charge and the mail, so fewer paths run than configurations exist

```{.text include=build/data/counts.txt}
```

::: notes
The grid you saw in 01 was one of eight. The four framed panels are the ones where the
stock is gone. The number is now true: 2^9 = 512. The bigger number is the first good news.
The right side is the plain matrix of 03, arrows from 01: the What is agreed, the How is open.
:::

## Every hidden decision is now on the board: nine sentences, their homes still to come {paths=512}

![](build/03-chaos/board.png){width=100%}

\footnotesize a starting inventory: nine rows, nine bits, 2^9 = 512; home, contract and evidence fill in over 04 to 06

\theline{Counting makes it worse}{You cannot shrink a count you have not made; the bigger number is the first good news.}

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
