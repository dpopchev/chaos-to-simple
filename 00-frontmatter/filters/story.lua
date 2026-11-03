-- story.lua: render a storyboard block in three shades.
--
--   ```{.diff .python}
--   checkout v0
--   +def f():
--   ```
--
-- A code block carrying both classes diff and python becomes its heading (line 1) as
-- \storyhead, then the body highlighted as Python by pandoc's own highlighter: each body line
-- loses its first character, which chooses the row's background (+ \diffaddbg, - \diffdelbg,
-- a space \diffscope). A Div with class request becomes the request box. The macros and the
-- colours are in preamble.tex. Runs before diffs.lua, which skips the converted block.

local ESCAPES = { ["\\"] = "\\textbackslash{}", ["{"] = "\\{", ["}"] = "\\}" }

local ROW = { ["+"] = "diffaddbg", ["-"] = "diffdelbg" }

local function has_class(el, class)
  for _, c in ipairs(el.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function escape_tex(text)
  return (text:gsub("[\\{}%%#&_%$%^~]", function(ch)
    return ESCAPES[ch] or ("\\" .. ch)
  end))
end

-- The highlighted lines of a Python source, pandoc's tango tokens between the Highlighting tags.
local function highlighted_lines(source)
  local block = pandoc.CodeBlock(source, pandoc.Attr("", { "python" }))
  local tex = pandoc.write(pandoc.Pandoc({ block }), "latex")
  local inner = tex:match("\\begin{Highlighting}%[[^%]]*%]\n(.-)\n?\\end{Highlighting}")
  local lines = {}
  for line in (inner or ""):gmatch("([^\n]*)\n?") do
    lines[#lines + 1] = line
  end
  while #lines > 0 and lines[#lines] == "" and #lines > 1 do
    lines[#lines] = nil
  end
  return lines
end

local function story_block(cb)
  local head, kinds, body = nil, {}, {}
  local number = 0
  for line in (cb.text .. "\n"):gmatch("([^\n]*)\n") do
    number = number + 1
    if number == 1 then
      head = line
    else
      kinds[#kinds + 1] = ROW[line:sub(1, 1)] or "diffscope"
      body[#body + 1] = line:sub(2)
    end
  end
  while #body > 0 and body[#body] == "" do
    body[#body] = nil
    kinds[#kinds] = nil
  end
  local lines = highlighted_lines(table.concat(body, "\n"))
  local rows = {}
  for i, line in ipairs(lines) do
    rows[i] = "\\" .. (kinds[i] or "diffscope") .. "{" .. line .. "}"
  end
  local tex = "\\storyhead{" .. escape_tex(head) .. "}\n"
    .. "\\begin{Verbatim}[commandchars=\\\\\\{\\}]\n"
    .. table.concat(rows, "\n")
    .. "\n\\end{Verbatim}"
  return pandoc.RawBlock("latex", tex)
end

local heading

local function convert(list)
  local blocks = {}
  for _, block in ipairs(list) do
    if block.t == "Header" then
      heading = block
    elseif block.t == "CodeBlock" and has_class(block, "diff") and has_class(block, "python") then
      block = story_block(block)
      if heading and not has_class(heading, "fragile") then
        heading.classes:insert("fragile")
      end
    elseif block.t == "Div" and has_class(block, "request") then
      local out = { pandoc.RawBlock("latex", "\\begin{request}") }
      for _, inner in ipairs(convert(block.content)) do
        out[#out + 1] = inner
      end
      out[#out + 1] = pandoc.RawBlock("latex", "\\end{request}")
      block = pandoc.Div(out)
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
