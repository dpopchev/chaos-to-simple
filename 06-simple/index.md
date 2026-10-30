# Simple: functional core, imperative shell

## The picture {paths=512}

- Core: six bits, pure functions, values in and values out, composed from three contexts
- Shell: three effects, one call into the core, a `match` per answer
- Between them: the seam from section 05

## The core

```{.python include=06-simple/s06_simple/core.py snippet=price}
```

::: notes
No if of its own. It composes pricing, shipping and tax. The bits are where they were
named: 4 + 8 + 2 if you count by context, 64 if you count the core as one function.
:::

## Sixty-four paths, one test each

```{.python include=06-simple/tests/test_core_paths.py snippet=from-bits}
```

::: notes
Invariants, not expectations: discounts never add, free shipping iff discounted goods
reach 50, VAT never reduces. The ten green cards are separate named tests.
:::

## We counted them

```{.text include=build/06-simple/pytest.txt}
```

## The shell

```{.python include=06-simple/s06_simple/shell.py snippet=checkout}
```

::: notes
House rule: no if on a domain field. Reserve, charge, send; every answer is a sum type and
every match is exhaustive. None of this knows what a coupon is.
:::

## Eight worlds, four outcomes

```{.python include=06-simple/tests/test_shell.py snippet=eight}
```

::: notes
2^3 configurations of the fakes. The guards collapse them to four outcomes, and the test
proves the collapse: no charge when the stock is gone, no mail when the card is refused.
:::

## The number {paths=72}

![](build/06-simple/paths.png){height=75%}

::: notes
512 against 72, and 22 if you count by context. Branch coverage was 100% before and 100%
after: it never measured this. The refrain, one last time: a boundary that passes values
adds paths; one that passes flags multiplies them.
:::
