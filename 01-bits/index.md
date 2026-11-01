# Six if statements, 64 paths

## Step 0: no ifs {paths=1}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="35%"}

\actor{customer}

```{.text include=build/01-bits/bubble-0.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-0.diff}
```

:::
::::

::: notes
The customer asked for the plain checkout: pick the books, pay, get them shipped. This
skeleton has the three calls and no decision, so the footer reads 1 path. Read the
customer's line aloud: that is all.
:::

## Step 1: one if {paths=2}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="35%"}

\actor{marketing}

```{.text include=build/01-bits/bubble-1.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-1.diff}
```

:::
::::

::: notes
Marketing asked for the autumn coupon: 10 BGN off with the code AUTUMN. The if adds the
first decision, a coupon that is valid until a date, so the footer doubles to 2 paths.
Read the marketing line aloud and ask who thinks it is a small change.
:::

## Step 2: two ifs {paths=4}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="35%"}

\actor{loyalty}

```{.text include=build/01-bits/bubble-2.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-2.diff}
```

:::
::::

::: notes
The loyalty program asked for 10 percent off for members, after the coupon. The second
if adds a decision about membership, so the footer doubles to 4 paths. Read the loyalty
line aloud and point out that the two discounts now stack.
:::

## Step 3: three ifs {paths=8}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="35%"}

\actor{logistics}

```{.text include=build/01-bits/bubble-3.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-3.diff}
```

:::
::::

::: notes
Logistics asked for free shipping from 50 BGN, because carts are left over 5 BGN of
postage. The third if adds a threshold on the subtotal, so the footer doubles to 8 paths.
Read the logistics line aloud and ask the room why the carts are left.
:::

## Step 4: four ifs {paths=16}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="35%"}

\actor{logistics}

```{.text include=build/01-bits/bubble-4.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-4.diff}
```

:::
::::

::: notes
Logistics adds the rate abroad: 20 BGN, not 5, because every parcel to Vienna loses money.
The fourth if sends a second destination down its own path, so the footer doubles to 16
paths. Read the second logistics line aloud and say that the shipping rules now branch twice.
:::

## Step 5: five ifs {paths=32}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="35%"}

\actor{marketing}

```{.text include=build/01-bits/bubble-5.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-5.diff}
```

:::
::::

::: notes
Marketing asked for gift wrap at 3 BGN, with just one more if. The fifth if adds an
optional extra to the total, so the footer doubles to 32 paths. Read the marketing line
aloud, the one that promised just one more if.
:::

## Step 6: six ifs {paths=64}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="35%"}

\actor{accounting}

```{.text include=build/01-bits/bubble-6.txt}
```

\actor{dev}

```{.text include=build/01-bits/bubble-7.txt}
```

\actor{marketing}

```{.text include=build/01-bits/bubble-8.txt}
```

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-6.diff}
```

:::
::::

::: notes
Accounting asked for no VAT on companies with a VAT ID, and legal says this week. The sixth
if adds the VAT rate, so the footer doubles to 64 paths. Read the accounting, dev and
marketing lines aloud, then ask the chat how many tests it takes until you are sure.
:::

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
