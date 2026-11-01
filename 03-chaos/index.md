# From chaos to complex

## The room

![](build/03-chaos/story.png){height=80%}

::: notes
Everyone in one room. One concrete order, told as a story: Maria orders two books with a
coupon to an address in Sofia. Stop at every sentence where the room has a question.
:::

## The six questions

| question | decided |
|---|---|
| What if the coupon expired yesterday? | |
| Does the member discount stack with the coupon, and in which order? | |
| Is the free-shipping threshold checked before or after the discounts? | Decided in the room: after the discount |
| What happens when the payment is declined? | the provider answers Charged / Declined (s0) |
| What happens when the stock is gone after we priced the order? | the warehouse answers Reserved / OutOfStock (s1) |
| What happens when the confirmation email bounces? | the mailer answers Sent / Bounced (s2) |

::: notes
Question 3 was a decision nobody made: marketing wanted before, logistics wanted after, and
the code decided for them (incident I2). The room decided: after the discount.
Chat: which question would you have asked?
:::

## The six questions, as a map

![](build/03-chaos/example_map.png){height=80%}

## The honest count {paths=512}

```{.text include=build/data/counts.txt}
```

::: notes
Nine bits, 512 paths, in one function. Eight times worse than the 64 we counted for the
core alone. That is the first good news: the number is now true.
:::

## First change: a table, not a refactoring

```{.text include=build/03-chaos/rules.txt}
```

- `data/rules.csv`: bit, scope, context, name, rule, code
- `data/examples.csv`: one green card per rule, named like a test
- Checked in next to the code, read by the build

\theline{Counting makes it worse}{You cannot shrink a count you have not made. The bigger number is the first good news.}

::: notes
The cheapest move in the talk. The table is generated from data/rules.csv; the green cards
are data/examples.csv and come back as test names in 06. The counter went up, which is the point.

Say it slowly, then move on. Chaos to complex starts with the count.
:::
