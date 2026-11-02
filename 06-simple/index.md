# Simple: functional core, imperative shell

## Sixty-four paths, one test each {paths=72}

```{.python include=06-simple/tests/test_core_paths.py snippet=from-bits}
```

## Sixty-four paths, each invariant a test {paths=72}

```{.text include=build/06-simple/pytest-core.txt}
```

## Eight worlds, four outcomes {paths=72}

```{.python include=06-simple/tests/test_shell.py snippet=eight}
```

## The wounds close by name {paths=72}

\fvset{fontsize=\scriptsize}

```{.python include=06-simple/tests/test_examples.py snippet=wound-i1}
```

```{.python include=06-simple/tests/test_shell.py snippet=wound-i3}
```

```{.text include=build/06-simple/wounds.txt}
```

## The number {paths=72}

![](build/06-simple/paths.png){height=65%}

```{.text include=build/data/splits.txt}
```

## Epilogue: marketing's seventh if {paths=72}

\fvset{fontsize=\scriptsize}

:::: {.columns}
::: {.column width="60%"}

STUB: 01-bits/data/squeeze.txt

```{.diff include=build/06-simple/seventh.diff cap=18}
```

```{.text include=build/06-simple/epilogue.txt}
```

:::
::: {.column width="40%"}

![](build/06-simple/epilogue.png){height=65%}

:::
::::

\theline{One more if is cheap}{Decisions in the core, effects in the shell. The next if costs 8, not 512.}
