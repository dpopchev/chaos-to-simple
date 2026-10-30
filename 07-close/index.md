# Close

## What I should have known from the start {paths=72}

\small

- Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.
- Before fixing the How, check whether the What is agreed.
- You cannot shrink a count you have not made. The bigger number is the first good news.
- Every if was somebody's sentence. Write it down, give it a home, pass values between homes.
- A method that does and tells hides a bit. Separate asking from doing; make every answer a value.
- Decisions in the core, effects in the shell. The next if costs 8, not 512.

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
