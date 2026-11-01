# Six if statements, 64 paths

## Step 0: no ifs {paths=1}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-0.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-0.diff}
```

:::
::::

## Step 1: one if {paths=2}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-1.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-1.diff}
```

:::
::::

## Step 2: two ifs {paths=4}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-2.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-2.diff}
```

:::
::::

## Step 3: three ifs {paths=8}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-3.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-3.diff}
```

:::
::::

## Step 4: four ifs {paths=16}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-4.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-4.diff}
```

:::
::::

## Step 5: five ifs {paths=32}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-5.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-5.diff}
```

:::
::::

## Step 6: six ifs {paths=64}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="50%"}

```{.text include=build/01-bits/bubble-6.txt}
```

:::
::: {.column width="50%"}

```{.diff include=build/01-bits/step-6.diff}
```

:::
::::

## Two tests. Coverage says 100% {paths=64}

\fvset{fontsize=\tiny}

```{.python include=01-bits/tests/test_chaos.py snippet=two-tests cap=24}
```

![](build/01-bits/coverage-view.png){height=20%}

## Finance found it, not the tests {paths=64}

\fvset{fontsize=\scriptsize}

![](build/01-bits/finance.png){height=45%}

STUB: 01-bits/data/squeeze.txt

## The path nobody ran {paths=64}

```{.python include=01-bits/tests/test_chaos.py snippet=bug}
```

## A path is a six-bit number {paths=64}

:::: {.columns}
::: {.column width="50%"}

![](build/01-bits/grid.png){height=65%}

:::
::: {.column width="50%"}

![](build/01-bits/doubling.png){height=65%}

:::
::::

\theline{A green badge means tested}{Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.}
