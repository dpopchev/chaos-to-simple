# 06 Core and shell: the responsibilities make a change safer

## Calculate the offer without carrying out the order: price() {paths=512}


![](build/06-simple/responsibilities-offer.png){width=54%}

```{.python heading-file=build/06-simple/price.txt include=06-simple/s06_simple/core.py snippet=price}
```

\footnotesize the team can discuss and exercise pricing without taking money, reserving stock or sending a message

\thread{3}

::: notes
Business names first: calculate the offer (pricing, shipping, tax), carry out the order (reservation, payment, notification), and the outside capabilities (warehouse, payment provider, mail). The priced result crosses the boundary as a value.
Core subdomain (business differentiation) is not functional core (computation without effects): the supporting shipping rule lives in the functional core too.
The shell has its own obligations: acceptance, rejection and sequencing.
:::

## The business can recognize its promises in the evidence, and the counter falls to 72 {paths=72}

\footnotesize I1 shipping eligibility uses the discounted goods; I2 the disputed reading has a decision and an owner; I3 unavailable stock prevents payment

```{.text include=build/06-simple/cards.txt}
```

\footnotesize 64 core paths, 8 shell worlds, 3 named regression checks

```{.text include=build/data/splits.txt}
```

the tests now record promises the business recognizes; these examples now have named regression checks

\thread{5}

::: notes
Each card reads agreed example, customer outcome, passing check; I2 closes by a decision with its owner.
512 became 72: 64 core paths plus 8 shell worlds, nothing deleted, every decision moved to the place that owns it.
:::

## The next conversation tells us whether the boundaries are useful {paths=72}

\footnotesize who needs to agree, what changes, which contract stays stable?

:::: {.columns}
::: {.column width="44%"}

\footnotesize Marketing changes the member discount

![](build/06-simple/responsibilities-offer-pricing.png){width=58%}

```{.diff include=build/06-simple/member15.diff cap=10}
```

\footnotesize shipping eligibility may move; shipping applies its own rule to the new value, unchanged

:::
::: {.column width="52%"}

\footnotesize Operations changes the payment provider

![](build/06-simple/responsibilities-offer-payment.png){width=58%}

```{.python include=06-simple/s06_simple/other_gateway.py snippet=gateway cap=14}
```

```{.text include=build/06-simple/pyright.txt}
```

:::
::::

\footnotesize we reduced unnecessary coordination, not business relationships

\thread{4}

::: notes
Marketing changes the member discount: pricing and marketing agree; shipping applies its own rule to the new value; the factor changes, the signature and the contract stay.
Operations changes the payment provider: operations and the shell owner agree; the core, pricing and shipping are untouched; the adapter maps the provider's answer to Charged | Declined and pyright stays at zero errors.
:::

## The seventh request has a place to start, not a licence to skip discovery {paths=72}

\vspace{0.6em}

```{.text include=01-bits/data/squeeze.txt}
```

for this example we change the delivery-charge policy for a digital-only order

\begingroup\scriptsize separate decisions, not shown: mixed baskets, gift wrap on a digital item, stock reservation, digital delivery, tax treatment\par\endgroup

:::: {.columns}
::: {.column width="58%"}

```{.diff include=build/06-simple/seventh.diff cap=12}
```

:::
::: {.column width="38%"}

![](build/06-simple/responsibilities-offer-shipping.png){width=100%}

:::
::::

\thread{5}

\theline{One more if is cheap}{Ask whose decision it is, what it needs to know and what else it may change; then the next if has a place to start.}

::: notes
Marketing's seventh request, digital books: it has a place to start, shipping, and it is not a licence to skip discovery.
For this example we change the delivery-charge policy for a digital-only order; mixed baskets, gift wrap on a digital item, stock reservation, digital delivery and tax treatment are separate decisions, not shown.
The small diff is the shipping change; the compact picture shows its highlight; the full picture is build/06-simple/responsibilities.png.
I no longer ask only where to put the next if. I ask whose decision it is, what information it needs, and what else it is allowed to change.
:::
