-- story.lua: render the storyboard's request box.
--
--   ::: request
--   ...
--   :::
--
-- A Div with class request becomes the request box (the colour and the box are in preamble.tex).
-- A code block with classes diff and python is left alone: diffs.lua, which runs after this
-- filter, renders it as every other diff, a grey heading over green and red text.

local function has_class(el, class)
  for _, c in ipairs(el.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function convert(list)
  local blocks = {}
  for _, block in ipairs(list) do
    if block.t == "Div" and has_class(block, "request") then
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
  doc.blocks = convert(doc.blocks)
  return doc
end
