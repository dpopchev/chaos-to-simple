# Complicated on the How: decoupling, cohesion, FP vs OO, CQS

## Coupling multiplies, cohesion adds {paths=512}

- Coupling: a flag crossing a boundary. The other side branches on it: x
- Cohesion: bits that change together live together. Their count stays local: +
- The refrain: a boundary that passes values adds paths; one that passes flags multiplies them

## Object with a mutable total

```{.python include=05-how/s05_how/oo_checkout.py snippet=oo}
```

## The bit nobody wrote down

```{.python include=05-how/tests/test_oo_order.py snippet=order-bit}
```

::: notes
Temporal coupling: the call order is a decision, and it lives in every caller. Frozen
dataclasses and pure functions put the order in the expression, where it is one path.
:::

## Command Query Separation draws the seam

- Query: `discounted_goods(goods, coupon, member, today) -> Money`, pure, asks nothing of the world
- Command: `gateway.charge(total) -> Charged | Declined`, an effect, answers with a value
- Never both in one method: `apply_coupon() -> bool` mutated and answered

## The answers the world may give

```{.python include=05-how/s05_how/ports.py snippet=results}
```

## The ports

```{.python include=05-how/s05_how/ports.py snippet=ports}
```

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
