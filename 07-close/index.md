## Six beliefs gave way: we made the rules explicit together and tests protected each step {paths=72}

\small

- A green badge means tested -> Coverage counts edges; bugs live in combinations. Count the configurations before you trust the badge.
- A bug is fixed with a test -> Before fixing the How, check whether the What is agreed.
- Counting makes it worse -> You cannot shrink a count you have not made; the bigger number is the first good news.
- Naming is cosmetics -> Every if was somebody's rule. Write it down, give it a home, pass values between homes.
- A boundary is a technical choice -> A boundary is an agreement about what the other side must know: providers report outcomes, the shop decides.
- One more if is cheap -> It was never just one more if: it was another business rule to understand. Ask whose decision it is, what it needs to know, what else it may change.

**We made the business rules explicit together, used tests to protect each step, and discovered useful boundaries along the way.**

::: notes
read the learned column only
:::

## These choices already have names: shared language, functional core, command-query separation {paths=72}

\begingroup\footnotesize

| what we did | its name | what it does not claim |
|---|---|---|
| one sentence per rule, one owner per home | domain-driven design: ubiquitous language, bounded contexts | a full strategic design; these are candidate boundaries |
| calculation apart from effects | functional core, imperative shell | DDD's core subdomain: that one is pricing |
| the offer apart from placing the order | command-query separation: a query answers, a command acts and reports | a CQRS architecture: one store here, no read model |

the names came after the decisions; the two earlier talks (DDD, CQRS and TDD) are the long version
\endgroup

::: notes
Name them once, now that the room has seen the decisions.
:::

## Q&A: where is the next hidden decision in your checkout? {paths=72}

:::::: {.columns}
::: {.column width="55%"}

- \mbox{\footnotesize\url{github.com/dpopchev/chaos-to-simple}}\
  slides, every snippet tested; make test runs them all
- \mbox{\footnotesize\url{linkedin.com/in/dimitar-popchev-b87074142}}\
  the CraftsmansDay and JourneymansDay post series: one section at a time
- bring your checkout: reach out and we go over your story
- the two earlier talks: metaprogramming; DDD, CQRS and TDD

:::
::: {.column width="45%"}

\vfill

thank you: to you, for the questions; to DEV.BG and the Python user group, for the stage

:::
::::::

::: notes
- "64 tests is overkill": parametrize or Hypothesis make them free; invariants, not expectations.
- "Where does async or the ORM go": shell concerns; the core does not change.
- "What about exceptions": a fourth answer nobody wrote down; sum types make it a value.
- "How do I convince my team": count the paths of one of their functions, show 2 tests at 100%.
- "Does this scale beyond one function": every bit doubles the paths of one function; the split adds, 72 -> 136.
- "Where does the digital-books if go": replay the chat answer.
- Live demo 1: make test K=TestCallOrder, for 45 against 44.
- Live demo 2: show build/01-bits/grid.png, then make test K=two_ifs.
- Stop here; leave the slide up while people leave.
:::
