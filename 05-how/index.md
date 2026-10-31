# Complicated on the How: decoupling, cohesion, FP vs OO, CQS

## I3: cards charged for parcels the warehouse did not have {paths=512}

```{.text include=05-how/data/incident.txt}
```

::: notes
The incident first, before any design word. Cards were charged for parcels the warehouse
did not have. The report is the only spec we have; the code under it is what we changed.
:::

## Past me reached for a class

```{.python include=05-how/s05_how/oo_checkout.py snippet=oo}
```

::: notes
"I'll make it a class and handle it properly." The class holds a mutable total that every
method reads and writes. It looks like the answer to the incident: one place for the rules.
:::

## The bit nobody wrote down

```{.python include=05-how/tests/test_oo_order.py snippet=order-bit}
```

::: notes
The false victory: the test passes for the order the author wrote it in, and the live
run gives 45 where the test expects 44. Temporal coupling: the call order is a decision,
and it lives in every caller. Frozen dataclasses and pure functions put the order in the
expression, where it is one path.
:::

## Command Query Separation draws the seam

- Query: `discounted_goods(goods, coupon, member, today) -> Money`, pure, asks nothing of the world
- Command: `gateway.charge(total) -> Charged | Declined`, an effect, answers with a value
- Never both in one method: `apply_coupon() -> bool` mutated and answered
- The refrain: a boundary that passes values adds paths; one that passes flags multiplies them

## The answers the world may give

\fvset{fontsize=\tiny,baselinestretch=0.9}

```{.python include=05-how/s05_how/ports.py snippet=results}
```

::: notes
Every effect answers with a value. A declined card is a value, not an exception; the
business outcomes are sum types the caller must match.
:::

## The ports

:::: columns
::: {.column width="55%"}
```{.python include=05-how/s05_how/ports.py snippet=ports}
```
:::
::: {.column width="45%"}
![](build/05-how/ports.png){width=100%}
:::
::::

::: notes
Three Protocols, three sum types, no exceptions for business outcomes. The seam is drawn;
nothing is on either side of it yet. Counter still 512.
:::

## Refactoring moves and their sign

| move | sign |
|---|---|
| guard clause | + 1 |
| `elif` / `match` over a sum type | + k |
| extract a pure function that returns a value | + |
| pass a flag across a boundary | x |
| mutable state read in a later step | hidden x |
| `try`/`except` around I/O inside the rules | hidden x |

## Coupling multiplies, cohesion adds

- Coupling: a flag crossing a boundary. The other side branches on it.
- Cohesion: bits that change together live together. Their count stays local.
- Each move in the table either adds a path or hides one; count them before you merge.

A class will keep it tidy

A method that does and tells hides a bit. Separate asking from doing; make every answer a value.
