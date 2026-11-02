# Complicated on the What: one language, bounded contexts

## Color-coded, the ifs get names {paths=512}

![](build/04-what/colorcode.png){height=80%}

## The first fix {paths=512}

\fvset{fontsize=\scriptsize}

```{.diff include=build/04-what/fix.diff cap=18}
```

## The dispute closes {paths=512}

\fvset{fontsize=\scriptsize}

```{.python include=04-what/s04_what/pricing.py snippet=coupon}
```

```{.python include=04-what/s04_what/shipping.py snippet=fee}
```

## A bit as a type {paths=512}

```{.python include=04-what/s04_what/shipping.py snippet=zone}
```

## Bounded contexts: every bit has a home {paths=512}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.diff include=build/04-what/v4.diff cap=30}
```

:::
::: {.column width="50%"}

```{.text include=build/04-what/contexts.txt}
```

:::
::::

## Bounded contexts, the moves {paths=512}

:::: {.columns}
::: {.column width="50%"}

![](build/04-what/moves.png){height=55%}

:::
::: {.column width="50%"}

![](build/04-what/board.png){height=30%}

:::
::::

\theline{Naming is cosmetics}{Every if was somebody's sentence. Write it down, give it a home, pass values between homes.}
