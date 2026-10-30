# From chaos to complex

## One story, nine sentences {paths=64}

![](build/03-chaos/diagrams/story.png){height=80%}

::: notes
Domain storytelling: actors, work objects, numbered sentences, one concrete case. Tell it
as a story: Maria orders two books with a coupon to an address in Sofia. Stop at every
sentence where the room has a question.
:::

## The questions the story raised

1. What if the coupon expired yesterday?
2. Does the member discount stack with the coupon, in which order?
3. Is the threshold checked before or after the discounts?
4. What if the payment is declined?
5. What if the stock is gone after we priced the order?
6. What if the confirmation bounces?

::: notes
Six red cards. Three about rules we thought we had, three about effects the code calls
without a decision around them. Each one is a bit nobody wrote down.
:::

## Example mapping: the rules we can now count

```{.text include=build/data/rules.txt}
```

::: notes
Yellow story, blue rules, green examples, red questions. The table is generated from
data/rules.csv; the green cards are data/examples.csv and come back as test names in 06.
:::

## The honest count {paths=512}

```{.text include=build/data/counts.txt}
```

::: notes
Nine bits, 512 paths, in one function. We wrote no code in this section. Chaos to complex
means the shape is known; nothing is smaller yet.
:::

## First change: a table, not a refactoring

- `data/rules.csv`: bit, scope, context, name, rule, code
- `data/examples.csv`: one green card per rule, named like a test
- Checked in next to the code, read by the build

::: notes
The cheapest move in the talk. The counter went up, which is the point.
:::
