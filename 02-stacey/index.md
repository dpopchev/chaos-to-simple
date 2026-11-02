# Stacey matrix: agreement on the What, certainty on the How

## I wanted to write a test {paths=64}

Free shipping from 50. Of what?

\actor{marketing}

```{.text include=build/02-stacey/bubble-0.txt}
```

\actor{logistics}

```{.text include=build/02-stacey/bubble-1.txt}
```

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
settles it. The developer's question comes before anyone agreed the rule; agree the What
first.
:::

## Above the line: a decision, not a test {paths=64}

:::: {.columns align=bottom}
::: {.column width="62%"}

![](build/02-stacey/stacey-02.png){height=85%}

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
02 is highlighted, in the Chaos (BOOM) band: joint venture; no boundary; nobody can say how
long. The dispute is a decision for the room, section 03, not a test to write.
:::
