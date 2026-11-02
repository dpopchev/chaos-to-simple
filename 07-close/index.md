## Six beliefs I held at the start each gave way to the lesson I should have known {paths=72}

\small

- A green badge means tested -> Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.
- A bug is fixed with a test -> Before fixing the How, check whether the What is agreed.
- Counting makes it worse -> You cannot shrink a count you have not made. The bigger number is the first good news.
- Naming is cosmetics -> Every if was somebody's sentence. Write it down, give it a home, pass values between homes.
- A class will keep it tidy -> A method that does and tells hides a bit. Separate asking from doing; make every answer a value.
- One more if is cheap -> Decisions in the core, effects in the shell. The next if costs 8, not 512.

::: notes
read the learned column only
:::

## Follow the series one section at a time, then bring your own checkout to review {paths=72}

- \mbox{\footnotesize\url{linkedin.com/in/dpopchev}}
- the CraftsmansDay and JourneymansDay post series: one section at a time
- reach out with your own checkout: we go over your specific problem

::: notes
- The posts take one section at a time; the series is the long version of tonight.
- Bring a function of your own: we count its paths together.
:::

## Q&A: ask anything about the tests, the repository, the posts or the earlier talks {paths=72}

:::::: {.columns}
::: {.column width="45%"}

- \mbox{\footnotesize\url{github.com/dpopchev/chaos-to-simple}}\
  slides, every snippet tested, 64 + 8 tests to run yourself
- The Friday posts: one section at a time, starting with the arithmetic
- The two earlier talks: metaprogramming; DDD, CQRS and TDD

:::
::: {.column width="55%"}

![](build/07-close/board.png){height=70%}

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
:::

## Thank you to the audience for the questions and to DEV.BG for the stage {paths=72}

- to you, for the questions
- to DEV.BG and the Python user group, for the stage

::: notes
Stop here; leave the slide up while people leave.
:::
