# 01 Bits: six policies, 64 paths

## A policy is one bit and every bit doubles the paths: count them before you trust a badge {paths=?}

::::: {.columns}
:::: {.column width="58%"}

![](build/01-bits/counting.png){height=70%}

::::
:::: {.column width="42%"}

\footnotesize

**paths = 2^policies**

| pattern | paths | rule |
|---|---|---|
| sequential ifs | 2 x 2 x 2 x 2 x 2 x 2 | each if doubles the paths |
| if / elif / else | 2 + 1 | alternatives add, one branch is taken |
| two ifs written as if/elif | 3, not 4 | the merged branch drops a path |

::::
:::::

The footer counts from here.

::: notes
Say the rule once: every policy request is one bit, and every bit doubles the paths. Walk the
diagram left to right: two sequential ifs multiply, 2 x 2, into four paths, bits 00 to 11; the
if/elif adds, 2 + 1, into three paths; the general form is the product of each block's
alternatives. Then say that the footer counts from here, starting at 1 for the plain checkout.
:::

## Three calls, two tests and no policy make the plain checkout one path {paths=1}

::: {.request}
\actor{customer}

```{.text include=build/01-bits/bubble-0.txt}
```
:::

::::: {.columns}
::: {.column width="54%"}

```{.diff .python include=build/01-bits/step-0.diff cap=10}
```

:::
::: {.column width="46%"}

```{.diff .python include=build/01-bits/test-0.diff cap=16}
```

:::
:::::

::: notes
The customer asked for the plain checkout: pick the books, pay, get them shipped. The left
column is the skeleton with the three calls and no policy, so the footer reads 1 path. The
right column is the tests, a regular order and an empty cart; both pass on the one path, so
the footer still reads 1 path. Read the customer's line aloud, then say that the tests come
before the policies, not after them.
:::

## The autumn coupon adds the first bit, so the checkout now has 2 paths {paths=2}


::: {.request}
\actor{marketing}

```{.text include=build/01-bits/bubble-1.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-1.diff cap=10}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-1.diff cap=7}
```

:::
::::

::: notes
Marketing asked for the autumn coupon: 10 EUR off with the code AUTUMN. The first policy
request adds a coupon that is valid until a date, so the footer doubles to 2 paths. Read
the marketing line aloud and ask who thinks it is a small change. The diffs show the change
alone, the scope row above it.
:::

## The member discount stacks on the coupon and doubles the checkout to 4 paths {paths=4}


::: {.request}
\actor{loyalty}

```{.text include=build/01-bits/bubble-2.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-2.diff cap=10}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-2.diff cap=7}
```

:::
::::

::: notes
The loyalty program asked for 10 percent off for members, after the coupon. The second
policy request adds a decision about membership, so the footer doubles to 4 paths. Read
the loyalty line aloud and point out that the two discounts now stack. The diffs show the
change alone, the scope row above it.
:::

## Free shipping from 50 EUR adds a third bit and the checkout reaches 8 paths {paths=8}


::: {.request}
\actor{logistics}

```{.text include=build/01-bits/bubble-3.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-3.diff cap=7}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-3.diff cap=11}
```

:::
::::

::: notes
Logistics asked for free shipping from 50 EUR, because carts are left over 5 EUR of
postage. The third policy request adds a threshold on the subtotal, so the footer doubles
to 8 paths. Read the logistics line aloud and ask the room why the carts are left. The
diffs show the change alone, the scope row above it.
:::

## Shipping abroad adds a fourth bit and the checkout reaches 16 paths {paths=16}


::: {.request}
\actor{logistics}

```{.text include=build/01-bits/bubble-4.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-4.diff cap=8}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-4.diff cap=7}
```

:::
::::

::: notes
Logistics adds the rate abroad: 20 EUR, not 5, because every parcel to Vienna loses money.
The fourth policy request sends a second destination down its own path, so the footer
doubles to 16 paths. Read the second logistics line aloud and say that the shipping rules
now branch twice. The diffs show the change alone, the scope row above it.
:::

## Gift wrap, promised as just one more change, brings the checkout to 32 paths {paths=32}


::: {.request}
\actor{marketing}

```{.text include=build/01-bits/bubble-5.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-5.diff cap=10}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-5.diff cap=7}
```

:::
::::

::: notes
Marketing asked for gift wrap at 3 EUR, with just one more change. The fifth policy
request adds an optional extra to the total, so the footer doubles to 32 paths. Read the
marketing line aloud, the one that promised just one more. The diffs show the change alone,
the scope row above it.
:::

## No VAT for companies adds the sixth bit and the checkout reaches 64 paths {paths=64}


::: {.request}
\actor{accounting}

```{.text include=build/01-bits/bubble-6.txt}
```
:::

:::: {.columns}
::: {.column width="45%"}

```{.diff .python include=build/01-bits/test-6.diff cap=10}
```

:::
::: {.column width="55%"}

```{.diff .python include=build/01-bits/step-6.diff cap=7}
```

:::
::::

::: notes
Accounting asked for no VAT on companies with a VAT ID, and legal says this week. The sixth
policy request adds the VAT rate, so the footer doubles to 64 paths. Read the accounting
line aloud. The diffs show the change alone, the scope row above it.
:::

## Six policies done and 64 paths live, so how many tests would make you sure? {paths=64}

\actor{dev}

```{.text include=build/01-bits/bubble-7.txt}
```

\actor{marketing}

```{.text include=build/01-bits/bubble-8.txt}
```

```{.text include=build/01-bits/next.txt}
```

\vfill

**How many tests would make you sure?**

::: notes
Read the dev and marketing lines aloud, then ask the chat the question and pause.
:::

## Two tests reach 100% branch coverage yet run only 2 of 64 combinations {paths=64}


:::: {.columns}
::: {.column width="54%"}

```{.python heading-file=build/01-bits/tests-6.txt include=01-bits/tests/test_chaos.py snippet=two-tests cap=24}
```

:::
::: {.column width="46%"}

![](build/01-bits/coverage-view.png){height=60%}

:::
::::

both values of every bit: 100% branch coverage, 2 of 64 combinations

```{.text include=build/01-bits/coverage-summary.txt}
```

::: notes
Branch coverage counts twelve edges, and both tests take every edge, so the report says
100 percent. The grid shows what it did not count: 2 of 64 combinations ran.
:::

## Finance traced 6,070 EUR of missing shipping to orders the coupon took under 50 EUR {paths=64}


```{.text include=01-bits/data/incident.txt cap=8}
```

:::: {.columns}
::: {.column width="58%"}

![](build/01-bits/finance.png){height=40%}

:::
::: {.column width="42%"}

```{.text heading="orders under 50 EUR, by week" include=build/01-bits/cues.txt}
```

:::
::::

**revenue loss: 1,214 orders under 50 EUR after the coupon shipped free, the threshold read the cart before the coupon**

::: notes
Finance noticed, not the tests: October's four weeks, received shipping income against the
shortfall, 1,214 orders and 6,070 EUR nowhere to be found, all in the chart title. The legend
names the two readings: received is the code, R1, marketing's reading of the cart before the
coupon; missing is finance, R2, logistics' reading of what they pay, after the coupon. The
memo is the sheet, not a conclusion: finance's counts and sums, nothing more. Read
the memo, then the chart, then the bold line: the condition, the threshold read the cart
before the coupon. The table is the engineering cue: every free parcel carried the coupon,
none without it, so a rule decided it, not the customers.
:::

## Finance's R2 test expects 60.00 and gets 54.00, a path no test of ours ran {paths=64}

revenue loss: 1,214 orders under 50 EUR after the coupon shipped free, the threshold read the cart before the coupon

the test finance and marketing wrote from it: 60.00

```{.python heading-file=build/01-bits/tests-bug.txt include=01-bits/tests/test_planted_bug.py snippet=bug}
```

```{.text include=build/01-bits/bug-run.txt}
```

::: notes
The slide repeats the condition, then shows a plain test and its run: 54.00 against 60.00. Run it live and it matches.
`make test K=test_chaos` shows 2 passed, `make test K=test_planted_bug` shows 1 xfailed: the
bug test sits in its own file, marked xfail, so the suite stays green. Then
`uv run pytest 01-bits/tests/test_planted_bug.py --runxfail` shows the same 54.00 against
60.00. The threshold reads the subtotal, not the discounted goods.
:::

## Four orders the memo implies: three pass, the coupon order under 60 does not {paths=64}

:::: {.columns}
::: {.column width="62%"}

```{.python heading-file=build/01-bits/tests-memo.txt include=01-bits/tests/test_memo_orders.py snippet=memo-orders cap=18}
```

:::
::: {.column width="38%"}

```{.text heading="make test K=TestMemoOrders --runxfail" include=build/01-bits/memo-run.txt}
```

:::
::::

only the coupon order between 50 and 60 EUR takes the path no test of ours ran

::: notes
Read the memo as a grid: with or without the coupon, under or over 50. Three corners pass; the fourth is finance's order, and it is the only one that fails. The plot said where to look; the tests say which order.
:::

## The badge is 100% branch coverage, it counts edges while every new policy doubles the combinations {paths=64}

:::: {.columns}
::: {.column width="50%"}

![](build/01-bits/grid.png){height=56%}

\small

bits read as the six conditions, left b5 to right b0

:::
::: {.column width="50%"}

![](build/01-bits/grid-growth.png){width=100%}

\small

every policy doubles the grid; the two tests stay in the corners, 000000 and 111111

:::
::::

\theline{A green badge means tested}{Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.}

::: notes
Point at 000000 and 111111 on the grid: the two tests, both green. Then point at 000101,
the I1 path, red: the bug. Walk the strip from 1 cell to 64: each grid doubles, and the
two tests stay in the corners of every one of them.
:::
