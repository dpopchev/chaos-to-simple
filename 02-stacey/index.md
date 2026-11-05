# 02 Map: Stacey matrix, agreement on the What, certainty on the How

## Engineering reads one sentence two ways: the cart before or after the coupon {paths=64}

Logistics, week 6: "Free shipping from 50."

The code: `if subtotal >= Decimal(50):`. Finance's test: expects 60.00, gets 54.00.

\begingroup\footnotesize

| reading | the threshold reads | 55 EUR with the coupon | said by |
|---|---|---|---|
| R1 the cart before the coupon | 55, ships free | pays 54.00 | marketing: more customers qualify |
| R2 the goods after the coupon | 45, pays 5 | pays 60.00 | logistics: what they pay for |

\endgroup

\begingroup\footnotesize\textit{both readings fit the sentence; the code picked one; nobody chose}\par\endgroup

::: notes
The bridge from the badge to the two voices. The badge said 64 paths and finance's test failed
on one of them: 60.00 expected, 54.00 got, on a 55 EUR order with the coupon. Engineering reads
the code: the condition tests the subtotal, read before the coupon. Then the sentence from week
6, "Free shipping from 50", and asks what 50 is of. Two answers fit. The cart before the coupon
is 55, so it ships free and pays 54.00: marketing's reading. The goods after the coupon are 45,
so the customer pays 5 and the total is 60.00: logistics' reading. Both fit the sentence; the
code picked the first and nobody chose. The next frame lets each of them say so in their own
words, each with a test.
:::

## Marketing and logistics read free shipping differently, so no test settles it {paths=64}


Free shipping from 50. Of what?

\vspace{-6pt}


:::: {.columns}
::: {.column width="47%"}

\actor{marketing}

```{.text include=build/02-stacey/bubble-0.txt}
```

:::
::: {.column width="53%"}

```{.python heading-file=build/02-stacey/tests-6.txt include=02-stacey/tests/test_readings.py snippet=r1}
```

:::
::::

\vspace{4pt}

:::: {.columns}
::: {.column width="47%"}

\actor{logistics}

```{.text include=build/02-stacey/bubble-1.txt}
```

:::
::: {.column width="53%"}

```{.python heading-file=build/02-stacey/tests-6.txt include=02-stacey/tests/test_readings.py snippet=r2}
```

:::
::::


\noindent\rule{\linewidth}{0.4pt}
\vspace{-20pt}

\actor{dev}

```{.text include=build/02-stacey/bubble-2.txt}
```

::: notes
One function, one reading: the code picked R1 and nobody chose.
The rule is the Who diagonal of the next frame: stakeholders above it, developers below.
Both positions are reasonable: marketing counts the subtotal, logistics counts only the
discounted goods, and each is right for its own work. Neither is a How problem, so no test
settles it. Each bubble has its test beside it, and the two tests contradict on one order, so
the room decides, not a test. The developer's question comes before anyone agreed the rule;
agree the What first.
:::

## The shipping dispute sits above the line: a decision for the room, not a test {paths=64}

:::: {.columns align=bottom}
::: {.column width="62%"}

![](build/02-stacey/stacey-02.png){height=80%}

:::
::: {.column width="38%"}

\vfill
\theline{A bug is fixed with a test}{Before fixing the How, check whether the What is agreed.}

:::
::::

::: notes
Read the matrix from the origin: both axes start certain. The x axis is the How, the y axis
the What. The bands Simple, Complicated, Complex and Chaos follow the distance from the
origin. The diagonal is labelled Who: above it stakeholders decide, below it
developers decide. 01 and 02 sit above the diagonal, 03 is on the line, and 04 to 06 sit below.
02 is highlighted, in the Complex band above the line: joint venture; no boundary; nobody can
say how long. The grey wedge is collaboration: one flat wedge from the origin, half of each side of the Who line, so only Simple has a clear boundary. The dispute is a decision for the room, section 03, not a test to write.
:::
