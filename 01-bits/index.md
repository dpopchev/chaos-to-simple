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

\fvset{fontsize=\tiny}

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

:::
::: {.column width="65%"}

```{.diff include=build/01-bits/step-6.diff}
```

:::
::::

::: notes
Accounting asked for no VAT on companies with a VAT ID, and legal says this week. The sixth
if adds the VAT rate, so the footer doubles to 64 paths. Read the accounting line aloud.
:::

## Checkout done {paths=64}

\actor{dev}

```{.text include=build/01-bits/bubble-7.txt}
```

\actor{marketing}

```{.text include=build/01-bits/bubble-8.txt}
```

\vfill

**How many tests would make you sure?**

::: notes
Read the dev and marketing lines aloud, then ask the chat the question and pause.
:::

## Two tests. Coverage says 100% {paths=64}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="54%"}

```{.python include=01-bits/tests/test_chaos.py snippet=two-tests cap=24}
```

:::
::: {.column width="46%"}

![](build/01-bits/coverage-view.png){height=62%}

:::
::::

```{.text include=build/01-bits/coverage-summary.txt}
```

::: notes
Branch coverage counts twelve edges, and both tests take every edge, so the report says
100 percent. The grid shows what it did not count: 2 of 64 combinations ran.
:::

## Finance found it, not the tests {paths=64}

\fvset{fontsize=\scriptsize}

![](build/01-bits/finance.png){height=65%}

\vfill

\actor{marketing}

```{.text include=01-bits/data/squeeze.txt}
```

::: notes
Finance noticed, not the tests: October's four weeks, received shipping income against the
shortfall, 1,214 orders and 6,070 BGN, all in the chart title. Then marketing, the same
morning, asks for one more if, with no idea what the last one cost. Read the bubble after a
pause.
:::

## The path nobody ran {paths=64}

```{.python include=01-bits/tests/test_planted_bug.py snippet=bug}
```

::: notes
Run it live. `make test K=test_chaos` shows 2 passed, `make test K=test_planted_bug` shows
1 xfailed: the bug test sits in its own file, marked xfail, so the suite stays green. Then
`uv run pytest 01-bits/tests/test_planted_bug.py --runxfail`
shows 54.00 against 60.00. The threshold reads the subtotal, not the discounted goods.
:::

## A path is a six-bit number {paths=64}

:::: {.columns}
::: {.column width="50%"}

![](build/01-bits/grid.png){height=52%}

:::
::: {.column width="50%"}

![](build/01-bits/doubling.png){height=52%}

\small

Sequential ifs multiply: 2 x 2 x 2 x 2 x 2 x 2

Alternatives (elif, match) add: 2 + 2 + 2

Two sequential ifs as if/elif: 4 paths become 3

:::
::::

\theline{A green badge means tested}{Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.}

::: notes
Point at 000000 and 111111 on the grid: the two tests, both green. Then point at 000101,
the I1 path, red: the bug. The curve doubled with every request, while the tested
cells stayed at 2.
:::
