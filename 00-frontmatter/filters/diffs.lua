-- diffs.lua: colour the lines of a diff block under its bold caption.
--
--   ```{.diff include=build/04-what/fix.diff}
--   ```
--
-- Runs after include-code-files.lua, so the block text is already filled. Line 1 is the caption
-- (vA -> vB) and is set bold. Each later line is wrapped by its first character: - in \diffdel,
-- + in \diffadd, ~ in \diffchg, and a line starting ... or equal to --- in \diffcut; a context line stays plain.
-- The block becomes a fancyvrb Verbatim (backslash and the two braces are command characters).
-- The fontsize is \snippetsize and the four macros are in preamble.tex.

local ESCAPES = { ["\\"] = "\\textbackslash{}", ["{"] = "\\{", ["}"] = "\\}" }

local function has_class(cb, class)
  for _, c in ipairs(cb.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function escape(text)
  return (text:gsub("[\\{}]", ESCAPES))
end

-- A body line starting with --- is diffcut, but a removed line whose text itself starts with --
-- is - plus that text, so the rule tests the whole trimmed line == "---", never the prefix.
local function macro_of(line)
  if line:sub(1, 3) == "..." or line:match("^%s*(.-)%s*$") == "---" then
    return "diffcut"
  end
  local first = line:sub(1, 1)
  if first == "-" then
    return "diffdel"
  elseif first == "+" then
    return "diffadd"
  elseif first == "~" then
    return "diffchg"
  end
  return nil
end

local function diff_block(cb)
  local rows = {}
  local number = 0
  for line in (cb.text .. "\n"):gmatch("([^\n]*)\n") do
    number = number + 1
    local row = escape(line)
    if number == 1 then
      row = "\\textbf{" .. row .. "}"
    else
      local macro = macro_of(line)
      if macro and row:match("%S") then
        row = "\\" .. macro .. "{" .. row .. "}"
      end
    end
    rows[#rows + 1] = row
  end
  while #rows > 1 and rows[#rows] == "" do
    rows[#rows] = nil
  end
  local tex = "\\begin{Verbatim}[commandchars=\\\\\\{\\},fontsize=\\snippetsize]\n"
    .. table.concat(rows, "\n") .. "\n\\end{Verbatim}"
  return pandoc.RawBlock("latex", tex)
end

-- A beamer frame holding a Verbatim must be fragile: the frame heading ahead of each
-- top-level diff block gets the class, so no slide source carries it.
-- Blocks inside a Div (the columns of a frame) are reached by recursion.
local heading

local function convert(list)
  local blocks = {}
  for _, block in ipairs(list) do
    if block.t == "Header" then
      heading = block
    elseif block.t == "CodeBlock" and has_class(block, "diff") then
      block = diff_block(block)
      if heading and not has_class(heading, "fragile") then
        heading.classes:insert("fragile")
      end
    elseif block.t == "Div" then
      block.content = convert(block.content)
    end
    blocks[#blocks + 1] = block
  end
  return blocks
end

function Pandoc(doc)
  heading = nil
  doc.blocks = convert(doc.blocks)
  return doc
end
