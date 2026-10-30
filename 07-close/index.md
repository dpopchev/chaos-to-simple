# Close

## What I should have known from the start {paths=72}

- Count paths, not coverage
- Every pattern earns its place by turning a multiplication into an addition
- What-bits in the core, How-bits in the shell

## Where to go from here

- The repository: slides, every snippet tested, 64 + 8 tests to run yourself
- The Friday posts: one section at a time, starting with the arithmetic
- The two earlier talks: metaprogramming; DDD, CQRS and TDD

::: notes
Thank the organisers. Repo link on the slide. Then Q&A.
:::

## Q&A

::: notes
Prepared answers:
- "64 tests is overkill": parametrize or Hypothesis make them free; invariants, not expectations.
- "What about async, frameworks, the ORM": shell concerns; the core does not change.
- "How do I convince my team": count the paths of one of their functions, show 2 tests at 100%.
- "What about exceptions": a fourth answer nobody wrote down; sum types make it a value.
:::
