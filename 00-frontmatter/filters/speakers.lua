-- speakers.lua: colour the speaker labels of an exhibit block.
--
--   ```{.text .speakers include=03-chaos/data/room.txt}              labels in actor colours
--   ```{.text .speakers highlight=q3 include=build/03-chaos/retro.txt}   and the q3 rows bold
--
-- Runs after include-code-files.lua, so the block text is already filled. The block becomes a
-- fancyvrb Verbatim (backslash and the two braces are command characters) in which each actor
-- label from data/actors.csv (read from the repo root) is wrapped in \textcolor. A label matches
-- in full and by its first word ("Dev (the shop)" and "Dev"), longest first, whole words only.
-- highlight=<id> sets bold the lines from the one starting with <id> to the line before the next
-- one starting with q and a digit. A line opening with "! " is bold too, the mark stripped.
-- The fontsize comes from \fvset, as for any code block.

local ACTORS_CSV = "data/actors.csv"

local function has_class(cb, class)
  for _, c in ipairs(cb.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local function split_csv(line)
  local fields = {}
  for field in (line .. ","):gmatch("([^,]*),") do
    fields[#fields + 1] = field
  end
  return fields
end

-- Returns {{text=, color=}, ...}, longest text first.
local function read_labels()
  local fh = io.open(ACTORS_CSV, "r")
  if not fh then
    error("speakers: cannot open " .. ACTORS_CSV)
  end
  local header
  local seen, labels = {}, {}
  for line in fh:lines() do
    local fields = split_csv(line)
    if not header then
      header = {}
      for i, name in ipairs(fields) do
        header[name] = i
      end
    else
      local label, color = fields[header["label"]], fields[header["color"]]
      local first = label:match("^%S+")
      for _, text in ipairs({ label, first }) do
        if not seen[text] then
          seen[text] = true
          labels[#labels + 1] = { text = text, color = color }
        end
      end
    end
  end
  fh:close()
  table.sort(labels, function(a, b)
    return #a.text > #b.text
  end)
  return labels
end

local ESCAPES = { ["\\"] = "\\textbackslash{}", ["{"] = "\\{", ["}"] = "\\}" }

local function is_word_char(ch)
  return ch ~= "" and ch:match("[%w_]") ~= nil
end

local function colour_line(line, labels)
  local out, i = {}, 1
  while i <= #line do
    local hit
    if not is_word_char(line:sub(i - 1, i - 1)) then
      for _, label in ipairs(labels) do
        local stop = i + #label.text - 1
        if line:sub(i, stop) == label.text and not is_word_char(line:sub(stop + 1, stop + 1)) then
          hit = label
          break
        end
      end
    end
    if hit then
      out[#out + 1] = "\\textcolor[HTML]{" .. hit.color .. "}{" .. hit.text:gsub("[\\{}]", ESCAPES) .. "}"
      i = i + #hit.text
    else
      local ch = line:sub(i, i)
      out[#out + 1] = ESCAPES[ch] or ch
      i = i + 1
    end
  end
  return table.concat(out)
end

local function speakers_block(cb, labels)
  local mark = cb.attributes["highlight"]
  local bold = false
  local rows = {}
  for line in (cb.text .. "\n"):gmatch("([^\n]*)\n") do
    if mark and line:sub(1, #mark) == mark then
      bold = true
    elseif bold and line:match("^q%d") then
      bold = false
    end
    local marked = line:sub(1, 2) == "! "
    if marked then
      line = line:sub(3)
    end
    local row = colour_line(line, labels)
    if (bold or marked) and row:match("%S") then
      row = "\\textbf{" .. row .. "}"
    end
    rows[#rows + 1] = row
  end
  local tex = "\\begin{Verbatim}[commandchars=\\\\\\{\\}]\n" .. table.concat(rows, "\n") .. "\n\\end{Verbatim}"
  return pandoc.RawBlock("latex", tex)
end

-- A beamer frame holding a Verbatim must be fragile: the frame heading ahead of each
-- top-level speakers block gets the class, so no slide source carries it.
function Pandoc(doc)
  local labels
  local heading
  local blocks = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      heading = block
    elseif block.t == "CodeBlock" and has_class(block, "speakers") then
      labels = labels or read_labels()
      block = speakers_block(block, labels)
      if heading and not has_class(heading, "fragile") then
        heading.classes:insert("fragile")
      end
    end
    blocks[#blocks + 1] = block
  end
  doc.blocks = blocks
  return doc
end
