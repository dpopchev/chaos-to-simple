# 08 Backup: the mechanisms behind the seam, for the Q&A

## The call order is a bit nobody wrote down, giving 45 against 44 from the same inputs {paths=512}

```{.python heading-file=build/05-how/tests-order.txt include=05-how/tests/test_oo_order.py snippet=order-bit}
```

\begingroup\footnotesize 05-how/tests/test_oo_order.py: the call order of the next frame's class, tested by make test K=TestCallOrder\par\endgroup

::: notes
The call order is a bit nobody wrote down: 45 against 44 from the same inputs.
Live demo: make test K=TestCallOrder. The first test follows the rule, the second one differs.
:::

## A class hid the call order in its state, the same bug as I3 in pricing {paths=512}

```{.python heading-file=build/05-how/oo.txt include=05-how/s05_how/oo_checkout.py snippet=oo}
```

\begingroup\footnotesize 05-how/s05_how/oo_checkout.py in pricing; tested by test_oo_order.py\par\endgroup

same bug, pricing edition: the order hidden in state

::: notes
Past me reached for a class, so the order of the steps hid in its state.
Each method reads and changes the same fields, and the call sequence became a bit nobody could see.
It is the same bug as I3, pricing edition.
:::

## Command Query Separation draws the seam by making every answer a value {paths=512}

:::: {.columns}
::: {.column width="50%"}

query: returns a value, changes nothing

command: changes the world, answers with a value

the seam: where asking ends and doing begins

```{.python heading="the answers" include=05-how/s05_how/ports.py snippet=types}
```

:::
::: {.column width="50%"}

```{.python heading-file=build/05-how/ports-code.txt include=05-how/s05_how/ports.py snippet=ports}
```

:::
::::

make every answer a value

\begingroup\footnotesize 05-how/s05_how/ports.py in fulfilment; tested by test_ports.py\par\endgroup

::: notes
Command query separation: a query asks, a command answers with a value, never both.
Every answer is a value the caller can match on, so the order stops living in state.
:::

## A sum type per answer and a Protocol per port: the fakes satisfy them with no inheritance, pyright says so {paths=512}

:::: {.columns}
::: {.column width="55%"}

```{.python heading-file=build/05-how/fakes-code.txt include=05-how/s05_how/fakes.py snippet=fakes cap=28}
```

:::
::: {.column width="45%"}

```{.text heading="uv run pyright fakes.py test_ports.py" include=build/05-how/pyright.txt}
```

\begingroup\footnotesize FakeGateway: Charged | Declined\par FakeInventory: Reserved | OutOfStock\par FakeMailer: the same shape, Sent | Bounced, in fakes.py\par\endgroup

:::
::::

::: notes
Each answer is its own type: Charged or Declined, Reserved or OutOfStock, Sent or Bounced.
A fake is a plain class with the same method. It never inherits from the port, and pyright accepts it anyway: zero errors.
The test doubles carry one bit each, so a shell test can enumerate the world.
:::

## Dependencies point inward: the shell imports the ports and the contexts, no context imports a port {paths=512}

![](build/05-how/imports.png){width=90%}

```{.text heading="names imported, counted from the files" include=build/05-how/imports.txt}
```

the What does not know the world: a context returns a value and asks nothing

::: notes
The table is counted from the import lines of the files, never typed.
The shell imports the ports and the contexts. The contexts import neither the ports nor the shell: zero under ports on every context row.
:::

## Passing values across a boundary adds paths you can count, passing flags multiplies them {paths=512}

\footnotesize

| move | sign | in this talk |
|---|---|---|
| guard clause | + 1 | `max(total, 0)` in pricing |
| `elif` / `match` over a sum type | + k | `Zone` in `base_fee` |
| extract a pure function that returns a value | + | `shipping_fee` returns the fee |
| pass a flag across a boundary | x | subtotal into the threshold (I1) |
| mutable state read in a later step | hidden x | `self.total`, 45 against 44 |
| `try`/`except` around I/O inside the rules | hidden x | the log nobody reads (I3) |

::: notes
The moves table: each move adds a path or hides one.
Guard clauses and sum types add paths you can count; flags and mutable state hide them.
:::
