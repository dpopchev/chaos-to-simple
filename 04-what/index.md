# Complicated on the What: one language, bounded contexts

## One language {paths=512}

```{.text include=build/data/rules.txt}
```

::: notes
Same table as in 03, read differently: the last column is code. Every condition is renamed
to the phrase the domain uses. The four red cards about rules are answered in this language.
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

## Contracts are values, never flags

```{.python include=04-what/s04_what/shipping.py snippet=fee}
```

```{.python include=04-what/s04_what/tax.py snippet=vat}
```

::: notes
shipping_fee takes the discounted goods as a Money, not a "coupon_applied" flag. That is
the line between multiplying and adding; section 05 names it.
:::

## Bounded contexts: every bit has a home

| context | bits | paths | owns |
|---|---|---|---|
| pricing | b0 b1 | 4 | `Coupon`, `discounted_goods` |
| shipping | b2 b3 b4 | 8 | `Zone`, `shipping_fee` |
| tax | b5 | 2 | `VatId`, `total_with_vat` |

::: notes
Still 512 in the function nobody has touched yet. But every bit has a name, a home and a
test. The counter does not move in this section; that is honest.
:::
