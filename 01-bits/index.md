# 01 Bits: six decisions outgrow the confidence of two tests

## We begin with one checkout flow and two tests: one path {paths=1}

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

## The coupon adds a decision without adding a test: 2 paths {paths=2}


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
One breath: the request aloud, the + line, the footer.
Marketing asked for the autumn coupon: 10 EUR off with the code AUTUMN. The first policy
request adds a coupon that is valid until a date, so the footer doubles to 2 paths. Read
the marketing line aloud and ask who thinks it is a small change. The diffs show the change
alone, the scope row above it.
:::

## Member pricing depends on the coupon coming first: 4 paths, two tests {paths=4}


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
One breath: the request aloud, the + line, the footer. The loyalty program asked for 10 percent off for members, after the coupon. The second
policy request adds a decision about membership, so the footer doubles to 4 paths. Read
the loyalty line aloud and point out that the two discounts now stack. The diffs show the
change alone, the scope row above it.
:::

## Free shipping adds a threshold decision to checkout: 8 paths, two tests {paths=8}


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

\footnotesize subtotal is the cart total captured at step 0, before any discount; the threshold reads it

::: notes
One breath: the request aloud, the + line, the footer. Logistics asked for free shipping from 50 EUR, because carts are left over 5 EUR of
postage. The third policy request adds a threshold on the subtotal, so the footer doubles
to 8 paths. Read the logistics line aloud and ask the room why the carts are left. The
diffs show the change alone, the scope row above it.
:::

## International delivery changes the code, not the test total: 16 paths {paths=16}


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

\footnotesize the international fee is set first; the free-shipping line then zeroes it for the test's 50-plus cart, so the total stands

::: notes
One breath: the request aloud, the + line, the footer. Logistics adds the rate abroad: 20 EUR, not 5, because every parcel to Vienna loses money.
The fourth policy request sends a second destination down its own path, so the footer
doubles to 16 paths. Read the second logistics line aloud and say that the shipping rules
now branch twice. The diffs show the change alone, the scope row above it.
:::

## Gift wrap becomes another exception for checkout to manage: 32 paths, two tests {paths=32}


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
One breath: the request aloud, the + line, the footer. Marketing asked for gift wrap at 3 EUR, with just one more change. The fifth policy
request adds an optional extra to the total, so the footer doubles to 32 paths. Read the
marketing line aloud, the one that promised just one more. The diffs show the change alone,
the scope row above it.
:::

## VAT status completes the six decisions: 64 paths, still two tests {paths=64}


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
One breath: the request aloud, the + line, the footer. Accounting asked for no VAT on companies with a VAT ID, and legal says this week. The sixth
policy request adds the VAT rate, so the footer doubles to 64 paths. Read the accounting
line aloud. The diffs show the change alone, the scope row above it.
:::

## I was ready to ship on the strength of two tests {paths=64}

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

## Two tests cover every branch but only 2 of 64 combinations {paths=64}


:::: {.columns}
::: {.column width="54%"}

```{.python heading-file=build/01-bits/tests-6.txt include=01-bits/tests/test_chaos.py snippet=two-tests cap=24}
```

:::
::: {.column width="46%"}

![](build/01-bits/grid.png){height=56%}

\small

bits read as the six conditions, left b5 to right b0

:::
::::

both values of every bit: 100% branch coverage, 2 of 64 combinations; the two tests sit in the corners, 000000 and 111111

```{.text include=build/01-bits/coverage-summary.txt}
```

::: notes
Branch coverage counts twelve edges, and both tests take every edge, so the report says
100 percent. The grid shows what it did not count: 2 of 64 combinations ran.
Point at 000000 and 111111 on the grid: the two tests, both green. Then point at 000101,
the I1 path, red: the bug.
:::

## 1,214 uncharged parcels leave a 6,070 EUR gap against the carrier's bill {paths=64}


```{.text include=01-bits/data/incident.txt cap=8}
```

:::: {.columns}
::: {.column width="58%"}

![](build/01-bits/finance.png){height=40%}

:::
::: {.column width="42%"}

```{.text heading="engineering: October orders, by week" include=build/01-bits/cues.txt}
```

:::
::::

**revenue loss: 1,214 parcels shipped free after the coupon, every one with a cart of 50 EUR or more before it: the threshold read the cart before the coupon**

::: notes
Four steps, in order. First finance's sheet: the memo is the sheet, not a conclusion,
their counts and sums only. Second the chart drawn from it: October's four weeks, received
shipping income against the shortfall, 1,214 parcels and 6,070 EUR nowhere to be found; the
legend is finance's: expected is their count of parcels under 50 EUR at 5 EUR, received is
the income they booked, missing is the difference. Third engineering's breakdown of the same
parcels, headed by its source: every free parcel carried the coupon and had a cart of 50 EUR
or more before it. Last the bold line, the condition: the threshold read the cart before the
coupon, so a rule decided it, not the customers.
:::

## The 55 EUR order fails Logistics' expected price: 60.00 expected, 54.00 paid {paths=64}

\moment{RED}{a test exposes the question: the expected total is Logistics' proposal, not yet the agreed rule}

from the breakdown: 1,214 free parcels, each with the coupon, the cart at 50 EUR or more before it, the goods under 50 after it; one of them: 55 EUR of books, the coupon, domestic

```{.python heading-file=build/01-bits/tests-bug.txt include=01-bits/tests/test_planted_bug.py snippet=bug}
```

```{.text include=build/01-bits/bug-run.txt}
```

::: notes
The order is read off page 16's breakdown table: the cart at 50 EUR or more, the coupon on, the goods under 50 after it. The slide shows a plain test of that order and its run: 54.00 against 60.00. Run it live and it matches.
`make test K=test_chaos` shows 2 passed, `make test K=test_planted_bug` shows 1 xfailed: the
bug test sits in its own file, marked xfail, so the suite stays green. Then
`uv run pytest 01-bits/tests/test_planted_bug.py --runxfail` shows the same 54.00 against
60.00. The threshold reads the subtotal, not the discounted goods.
:::

## The coupon boundary order fails while the memo's other three orders pass {paths=64}

the memo's four boundary orders, not the full grid

:::: {.columns}
::: {.column width="62%"}

```{.python heading-file=build/01-bits/tests-memo.txt include=01-bits/tests/test_memo_orders.py snippet=memo-orders cap=21}
```

:::
::: {.column width="38%"}

```{.text heading="make test K=TestMemoOrders --runxfail" include=build/01-bits/memo-run.txt}
```

:::
::::

only the coupon order with the cart over 50 and the goods under 50 takes the path no test of ours ran

\theline{A green badge means tested}{Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.}

::: notes
Read the memo as a grid: with or without the coupon, under or over 50. Three corners pass; the fourth is finance's order, and it is the only one that fails. The plot said where to look; the tests say which order.
:::
