# 01 Bits: six policies, 64 paths

## A policy is one bit and every bit doubles the paths: count them before you trust a badge {paths=?}

:::: {.columns}
::: {.column width="58%"}

![](build/01-bits/counting.png){height=70%}

:::
::: {.column width="42%"}

**paths = 2^policies**

Sequential policies multiply: 2 x 2 x 2 x 2 x 2 x 2

Alternatives (elif, match) add: 2 + 2 + 2

Two sequential policies as if/elif: 4 paths become 3

:::
::::

The footer counts from here.

::: notes
Say the rule once: every policy request is one bit, and every bit doubles the paths. Walk the
diagram left to right: two sequential ifs multiply, 2 x 2, into four paths, bits 00 to 11; the
if/elif adds, 2 + 1, into three paths; the general form is the product of each block's
alternatives. Then say that the footer counts from here, starting at 1 for the plain checkout.
:::

## The plain checkout has three calls and no policy, so it has one path {paths=1}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{customer}

```{.text include=build/01-bits/bubble-0.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-0.txt}
```

```{.diff include=build/01-bits/step-0.diff cap=24}
```

:::
::::

::: notes
The customer asked for the plain checkout: pick the books, pay, get them shipped. This
skeleton has the three calls and no policy, so the footer reads 1 path. Read the
customer's line aloud: that is all.
:::

## The autumn coupon adds the first bit, so the checkout now has 2 paths {paths=2}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{marketing}

```{.text include=build/01-bits/bubble-1.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-1.txt}
```

```{.diff include=build/01-bits/step-1.diff cap=7}
```

:::
::::

::: notes
Marketing asked for the autumn coupon: 10 EUR off with the code AUTUMN. The first policy
request adds a coupon that is valid until a date, so the footer doubles to 2 paths. Read
the marketing line aloud and ask who thinks it is a small change. The diff shows the
change alone, one line of context each side.
:::

## The member discount stacks on the coupon and doubles the checkout to 4 paths {paths=4}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{loyalty}

```{.text include=build/01-bits/bubble-2.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-2.txt}
```

```{.diff include=build/01-bits/step-2.diff cap=7}
```

:::
::::

::: notes
The loyalty program asked for 10 percent off for members, after the coupon. The second
policy request adds a decision about membership, so the footer doubles to 4 paths. Read
the loyalty line aloud and point out that the two discounts now stack. The diff shows the change alone, one line of
context each side.
:::

## Free shipping from 50 EUR adds a third bit and the checkout reaches 8 paths {paths=8}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{logistics}

```{.text include=build/01-bits/bubble-3.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-3.txt}
```

```{.diff include=build/01-bits/step-3.diff cap=11}
```

:::
::::

::: notes
Logistics asked for free shipping from 50 EUR, because carts are left over 5 EUR of
postage. The third policy request adds a threshold on the subtotal, so the footer doubles
to 8 paths. Read the logistics line aloud and ask the room why the carts are left. The diff shows the change alone, one line of context
each side.
:::

## Shipping abroad adds a fourth bit and the checkout reaches 16 paths {paths=16}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{logistics}

```{.text include=build/01-bits/bubble-4.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-4.txt}
```

```{.diff include=build/01-bits/step-4.diff cap=7}
```

:::
::::

::: notes
Logistics adds the rate abroad: 20 EUR, not 5, because every parcel to Vienna loses money.
The fourth policy request sends a second destination down its own path, so the footer
doubles to 16 paths. Read the second logistics line aloud and say that the shipping rules
now branch twice. The diff shows the change alone, one line of context each side.
:::

## Gift wrap, promised as just one more change, brings the checkout to 32 paths {paths=32}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{marketing}

```{.text include=build/01-bits/bubble-5.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-5.txt}
```

```{.diff include=build/01-bits/step-5.diff cap=7}
```

:::
::::

::: notes
Marketing asked for gift wrap at 3 EUR, with just one more change. The fifth policy
request adds an optional extra to the total, so the footer doubles to 32 paths. Read the
marketing line aloud, the one that promised just one more. The diff shows the change alone, one line of context
each side.
:::

## No VAT for companies adds the sixth bit and the checkout reaches 64 paths {paths=64}

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="25%"}

\actor{accounting}

```{.text include=build/01-bits/bubble-6.txt}
```

:::
::: {.column width="75%"}

\fvset{fontsize=\scriptsize}

```{.text include=build/01-bits/tally-6.txt}
```

```{.diff include=build/01-bits/step-6.diff cap=7}
```

:::
::::

::: notes
Accounting asked for no VAT on companies with a VAT ID, and legal says this week. The sixth
policy request adds the VAT rate, so the footer doubles to 64 paths. Read the accounting
line aloud. The diff shows the change alone, one line of context each side.
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

\fvset{fontsize=\tiny}

:::: {.columns}
::: {.column width="54%"}

```{.python include=01-bits/tests/test_chaos.py snippet=two-tests cap=24}
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

## Finance traced 6,070 EUR of missing shipping to the checkout, a software fault {paths=64}

\fvset{fontsize=\scriptsize}

finance backtracked the gap to the checkout: a software fault?

![](build/01-bits/finance.png){height=54%}

\vfill

\actor{marketing}

```{.text include=01-bits/data/squeeze.txt}
```

::: notes
Finance noticed, not the tests: October's four weeks, received shipping income against the
shortfall, 1,214 orders and 6,070 EUR nowhere to be found, all in the chart title. The legend
names the two readings: received is the code, R1, marketing's reading of the cart before the
coupon; missing is finance, R2, logistics' reading of what they pay, after the coupon. Read
the chart, stop, then reveal the bubble: marketing, the same morning, asks for one more if,
with no idea what the last one cost.
:::

## Finance's R2 test expects 60.00 and gets 54.00, a path no test of ours ran {paths=64}

the test finance and marketing wrote from R2: 60.00

```{.python include=01-bits/tests/test_planted_bug.py snippet=bug}
```

```{.text include=build/01-bits/bug-run.txt}
```

::: notes
The slide shows a plain test and its run: 54.00 against 60.00. Run it live and it matches.
`make test K=test_chaos` shows 2 passed, `make test K=test_planted_bug` shows 1 xfailed: the
bug test sits in its own file, marked xfail, so the suite stays green. Then
`uv run pytest 01-bits/tests/test_planted_bug.py --runxfail` shows the same 54.00 against
60.00. The threshold reads the subtotal, not the discounted goods.
:::

## A path is a six-bit number, so every new policy doubles the paths to count {paths=64}

:::: {.columns}
::: {.column width="50%"}

![](build/01-bits/grid.png){height=56%}

\small

bits read as the six conditions, left b5 to right b0

:::
::: {.column width="50%"}

\small

Sequential policies multiply: 2 x 2 x 2 x 2 x 2 x 2

Alternatives (elif, match) add: 2 + 2 + 2

Two sequential policies as if/elif: 4 paths become 3

:::
::::

\theline{A green badge means tested}{Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.}

::: notes
Point at 000000 and 111111 on the grid: the two tests, both green. Then point at 000101,
the I1 path, red: the bug.
:::
