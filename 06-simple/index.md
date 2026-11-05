# 06 Core and shell: clear responsibilities make the next change easier to contain

## We calculate the offer without carrying out the order {paths=512}


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

## Agreed promises now have concrete examples and traceable evidence {paths=72}

\footnotesize I1 shipping eligibility uses the discounted goods; I2 the disputed reading has a decision and an owner; I3 unavailable stock prevents payment

```{.text include=build/06-simple/cards.txt}
```

\vspace{-4pt}

\footnotesize 64 core paths, 8 shell worlds, 2 named regression checks and 1 recorded decision

```{.text include=build/data/splits.txt}
```

two examples now have named regression checks; the dispute has a recorded decision and owner

\thread{5}

::: notes
Each card reads agreed example, customer outcome, passing check; I2 closes by a decision with its owner.
512 became 72: 64 core paths plus 8 shell worlds, nothing deleted, every decision moved to the place that owns it.
:::

## Raising the member discount to 15% leaves shipping untouched {paths=72}

![](build/06-simple/responsibilities-offer-pricing.png){width=70%}

```{.diff include=build/06-simple/member15.diff cap=10}
```

\footnotesize shipping eligibility may move; shipping applies its own rule to the new value, unchanged

::: notes
Marketing changes the member discount: pricing and marketing agree; shipping applies its own rule to the new value; the factor changes, the signature and the contract stay.
:::

## A stable payment contract lets us replace the provider {paths=72}

![](build/06-simple/responsibilities-offer-payment.png){width=70%}

```{.python include=06-simple/s06_simple/other_gateway.py start-line=24 end-line=28}
```

\vspace{-0.4em}

\scriptsize we reduced unnecessary coordination, not business relationships

\thread{4}

::: notes
Operations changes the payment provider: operations and the shell owner agree; the core, pricing and shipping are untouched; the adapter maps the provider's answer to Charged | Declined and pyright stays at zero errors.
:::

## The digital-only delivery charge lands in shipping as a fourth bit, 16 paths {paths=72}

\vspace{0.6em}

```{.text include=01-bits/data/squeeze.txt}
```

for this example we change the delivery-charge policy for a digital-only order

\begingroup\scriptsize separate decisions, not shown: mixed baskets, gift wrap on a digital item, stock reservation, digital delivery, tax treatment\par\endgroup

```{.diff include=build/06-simple/seventh.diff cap=12}
```

::: notes
Marketing's seventh request, digital books: it has a place to start, shipping.
For this example we change the delivery-charge policy for a digital-only order; mixed baskets, gift wrap on a digital item, stock reservation, digital delivery and tax treatment are separate decisions, not shown.
The small diff is the shipping change; the next frame shows its highlight.
:::

## The next if starts with ownership and discovery {paths=72}

![](build/06-simple/responsibilities-offer-shipping.png){width=70%}

\vspace{-0.4em}

\thread{5}

\theline{One more if is cheap}{Ask whose decision it is, what it needs to know and what else it may change; then the next if has a place to start.}

::: notes
The compact picture shows the highlighted shipping box; the full picture is build/06-simple/responsibilities.png.
I no longer ask only where to put the next if. I ask whose decision it is, what information it needs, and what else it is allowed to change.
:::
