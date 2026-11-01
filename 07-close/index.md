## What I should have known from the start {paths=72}

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

## Q&A

- The repository: slides, every snippet tested, 64 + 8 tests to run yourself
- The Friday posts: one section at a time, starting with the arithmetic
- The two earlier talks: metaprogramming; DDD, CQRS and TDD

::: notes
- "64 tests is overkill": parametrize or Hypothesis make them free; invariants, not expectations.
- "Where does async or the ORM go": shell concerns; the core does not change.
- "What about exceptions": a fourth answer nobody wrote down; sum types make it a value.
- "How do I convince my team": count the paths of one of their functions, show 2 tests at 100%.
- "Does this scale beyond one function": every bit doubles the paths of one function; the split adds, 72 -> 136.
- "Where does the digital-books if go": replay the chat answer.
- Live demo 1: make test K=test_call_order_is_a_hidden_bit, for 45 against 44.
- Live demo 2: show build/01-bits/tree.png, then make test K=two_ifs.
:::
