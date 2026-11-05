-- text-exhibits.lua: set every .text exhibit as a Verbatim at the exhibit size.
--
--   ```{.text include=01-bits/data/incident.txt}
--
-- Runs after include-code-files.lua, so every include is already resolved (a heading= block
-- keeps the \snippethead label emitted ahead of it), and after speakers.lua, which sets the
-- .speakers blocks itself. pandoc would set a .text block in Shaded at \snippetsize; here it
-- becomes a fancyvrb Verbatim at \exhibitsize (preamble.tex), its text unchanged. Blocks
-- nested in column Divs count.

local function has_class(el, class)
  for _, c in ipairs(el.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function is_exhibit(cb)
  return has_class(cb, "text") and not has_class(cb, "speakers")
end

local function to_verbatim(cb)
  return pandoc.RawBlock(
    "latex",
    "\\begin{Verbatim}[fontsize=\\exhibitsize]\n" .. cb.text .. "\n\\end{Verbatim}"
  )
end

-- Returns the block with its exhibits converted, and whether it held one.
local function convert(block)
  if block.t == "CodeBlock" then
    if is_exhibit(block) then
      return to_verbatim(block), true
    end
    return block, false
  end
  local found = false
  local walked = pandoc.walk_block(block, {
    CodeBlock = function(cb)
      if is_exhibit(cb) then
        found = true
        return to_verbatim(cb)
      end
      return nil
    end,
  })
  return walked, found
end

-- A beamer frame holding a Verbatim must be fragile, and pandoc marks one only on a CodeBlock
-- it still sees: the frame heading ahead of each converted block gets the class.
function Pandoc(doc)
  local heading
  local blocks = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      heading = block
    else
      local found
      block, found = convert(block)
      if found and heading and not has_class(heading, "fragile") then
        heading.classes:insert("fragile")
      end
    end
    blocks[#blocks + 1] = block
  end
  doc.blocks = blocks
  return doc
end
