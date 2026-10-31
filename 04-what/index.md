# Complicated on the What: one language, bounded contexts

## One language {paths=512}

```{.text include=build/data/rules.txt}
```

::: notes
Same table as in 03, read differently: the last column is code. Every condition is renamed
to the phrase the domain uses. The four red cards about rules are answered in this language.
:::

## The dispute closes

Free when the discounted goods reach 50. The row is b2 in rules.csv.

```{.python include=04-what/s04_what/shipping.py snippet=fee}
```

::: notes
The sentence was decided in the room, section 03. The value crossing the boundary is the
discounted goods, a Money, not a coupon flag: the fee is decided on what the customer pays
for the goods, so the bug from 03 cannot come back as a flag passed from elsewhere.
:::

## A rule is a phrase, a phrase is a method

```{.python include=04-what/s04_what/pricing.py snippet=coupon}
```

```{.python include=04-what/s04_what/pricing.py snippet=discounted}
```

::: notes
Compare with the chaos version: coupon_valid_until is not None and >= today became
coupon.is_valid_on(today). The order of coupon and member is now a sentence in the rule
and a line in the code. max() hides a decision: say so.
:::

## A bit as a type

```{.python include=04-what/s04_what/shipping.py snippet=zone}
```

::: notes
Two booleans have four states and three of them are legal; a sum type has two. The
type checker counts this bit: remove a case and pyright fails the build.
:::

## Values, never flags

```{.python include=04-what/s04_what/tax.py snippet=vat}
```

::: notes
The line between multiplying and adding; section 05 names it. The fee on slide 2 is the
same move: a Money crosses the boundary, a flag does not.
:::

## Bounded contexts: every bit has a home

```{.text include=build/04-what/contexts.txt}
```

Marketing and loyalty are pricing, logistics is shipping, accounting is tax. The people
who asked are the map of the contexts.

::: notes
Still 512 in the function nobody has touched yet. But every bit has a name, a home and a
test. The counter does not move in this section; that is honest.
:::

## The line

Naming is cosmetics

Every if was somebody's sentence. Write it down, give it a home, pass values between homes.

::: notes
Each home is a context with a name, its bits, its paths and the people who asked. Section
05 takes the values across the homes.
:::
