# 02 Map: Stacey matrix, agreement on the What, certainty on the How

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

```{.python include=02-stacey/tests/test_readings.py snippet=r1}
```

:::
::::

:::: {.columns}
::: {.column width="47%"}

\actor{logistics}

```{.text include=build/02-stacey/bubble-1.txt}
```

:::
::: {.column width="53%"}

```{.python include=02-stacey/tests/test_readings.py snippet=r2}
```

:::
::::


\begingroup\footnotesize\textit{one function, one reading: the code picked R1 and nobody chose}\par\endgroup
\vspace{-11pt}

\noindent\rule{\linewidth}{0.4pt}

\actor{dev}

```{.text include=build/02-stacey/bubble-2.txt}
```

::: notes
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
the What. The bands Simple, Complicated, Complex and Chaos (BOOM) follow the distance from the
origin. The diagonal is labelled Who: above it stakeholders decide and agree, below it
developers decide. 01 and 02 sit above the diagonal, 03 is on the line, and 04 to 06 sit below.
02 is highlighted, in the Complex band above the line: joint venture; no boundary; nobody can
say how long. The dispute is a decision for the room, section 03, not a test to write.
:::
