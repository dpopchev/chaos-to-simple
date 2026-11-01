# Complicated on the How: decoupling, cohesion, FP vs OO, CQS

## I3: cards charged for parcels the warehouse did not have {paths=512}

\fvset{fontsize=\scriptsize}

```{.text include=05-how/data/incident.txt}
```

```{.text include=build/05-how/effects.txt}
```

## Past me reached for a class {paths=512}

```{.python include=05-how/s05_how/oo_checkout.py snippet=oo}
```

## The bit nobody wrote down {paths=512}

```{.python include=05-how/tests/test_oo_order.py snippet=order-bit}
```

## Command Query Separation draws the seam {paths=512}

```{.python include=05-how/s05_how/ports.py snippet=types}
```

## The ports, as a picture {paths=512}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="45%"}

![](build/05-how/ports.png){height=60%}

:::
::: {.column width="55%"}

```{.diff include=build/05-how/v5.diff}
```

:::
::::

## A boundary that passes values adds paths; one that passes flags multiplies them {paths=512}

\footnotesize

| move | sign |
|---|---|
| guard clause | + 1 |
| `elif` / `match` over a sum type | + k |
| extract a pure function that returns a value | + |
| pass a flag across a boundary | x |
| mutable state read in a later step | hidden x |
| `try`/`except` around I/O inside the rules | hidden x |

![](build/05-how/board.png){height=22%}

\theline{A class will keep it tidy}{A method that does and tells hides a bit. Separate asking from doing; make every answer a value.}
