-- include-code-files.lua: fill a fenced code block from a file, so a slide never
-- carries a pasted copy of code that the tests do not see.
--
--   ```{.python include=01-bits/s01_bits/chaos.py}                  whole file
--   ```{.python include=01-bits/s01_bits/chaos.py snippet=checkout} between markers
--   ```{.python include=path start-line=3 end-line=9}               by line numbers
--
-- Snippet markers are comment lines in the source:
--   # [snippet: checkout]
--   ...
--   # [/snippet]
-- A trailing step marker, "  # [step: N]", is stripped from every included line.
-- Markers are dropped, the block is dedented, snippets do not nest, and a missing
-- file or marker aborts the build (pandoc exits non-zero on error()). Exception: a
-- missing file renders a block reading "STUB: <path>" with a warning on stderr,
-- unless the environment variable STRICT is set (make STRICT=1), then it errors.
-- Paths are relative to the directory make runs from: the repo root.

local function read_lines(path)
  local fh = io.open(path, "r")
  if not fh then
    error("include-code-files: cannot open " .. path)
  end
  local lines = {}
  for line in fh:lines() do
    lines[#lines + 1] = line:gsub("%s*# %[step: %d%]%s*$", "")
  end
  fh:close()
  return lines
end

local function slice_snippet(lines, name, path)
  local out, inside, found, first = {}, false, false, 1
  local open_marker = "[snippet: " .. name .. "]"
  for number, line in ipairs(lines) do
    if inside and line:find("[/snippet]", 1, true) then
      inside = false
    elseif inside then
      out[#out + 1] = line
    elseif line:find(open_marker, 1, true) then
      inside, found, first = true, true, number + 1
    end
  end
  if not found then
    error("include-code-files: no snippet '" .. name .. "' in " .. path)
  end
  if inside then
    error("include-code-files: snippet '" .. name .. "' in " .. path .. " is not closed")
  end
  return out, first
end

local function slice_lines(lines, first, last)
  local out = {}
  for i = first, math.min(last, #lines) do
    out[#out + 1] = lines[i]
  end
  return out, first
end

local function dedent(lines)
  local min
  for _, line in ipairs(lines) do
    if line:match("%S") then
      local indent = #line:match("^%s*")
      if min == nil or indent < min then
        min = indent
      end
    end
  end
  min = min or 0
  local out = {}
  for _, line in ipairs(lines) do
    out[#out + 1] = line:sub(min + 1)
  end
  return out
end

-- Returns the trimmed lines and how many leading blank lines were dropped.
local function trim_blank_edges(lines)
  local dropped = 0
  while #lines > 0 and not lines[1]:match("%S") do
    table.remove(lines, 1)
    dropped = dropped + 1
  end
  while #lines > 0 and not lines[#lines]:match("%S") do
    table.remove(lines)
  end
  return lines, dropped
end

local function has_class(cb, class)
  for _, c in ipairs(cb.classes) do
    if c == class then
      return true
    end
  end
  return false
end

local LATEX_ESCAPES = {
  ["\\"] = "\\textbackslash{}",
  ["^"] = "\\textasciicircum{}",
  ["~"] = "\\textasciitilde{}",
}

-- The heading text: heading-file= names a built file whose first line is the heading (an
-- unreadable file errors, or reads "STUB: <path>" unless STRICT is set), else heading=.
local function heading_text(cb)
  local path = cb.attributes["heading-file"]
  if path == nil then
    return cb.attributes["heading"]
  end
  cb.attributes["heading-file"] = nil
  local fh = io.open(path, "r")
  if not fh then
    local strict = os.getenv("STRICT")
    if strict == nil or strict == "" then
      io.stderr:write("include-code-files: STUB: " .. path .. "\n")
      return "STUB: " .. path
    end
    error("include-code-files: cannot open " .. path)
  end
  local first = fh:read("l")
  fh:close()
  return first
end

-- A heading= or heading-file= attribute becomes a \snippethead label ahead of the block, the
-- attribute dropped.
local function with_heading(cb)
  local heading = heading_text(cb)
  if heading == nil then
    return cb
  end
  cb.attributes["heading"] = nil
  local escaped = heading:gsub("[\\{}%%#&_%$%^~]", function(ch)
    return LATEX_ESCAPES[ch] or ("\\" .. ch)
  end)
  return { pandoc.RawBlock("latex", "\\snippethead{" .. escaped .. "}"), cb }
end

function CodeBlock(cb)
  local path = cb.attributes["include"]
  if path == nil then
    return nil
  end
  local strict = os.getenv("STRICT")
  if (strict == nil or strict == "") and not io.open(path, "r") then
    io.stderr:write("include-code-files: STUB: " .. path .. "\n")
    cb.text = "STUB: " .. path
    cb.attributes["include"] = nil
    cb.attributes["snippet"] = nil
    cb.attributes["start-line"] = nil
    cb.attributes["end-line"] = nil
    cb.attributes["heading-file"] = nil
    return cb
  end
  local lines = read_lines(path)
  local first = 1
  if cb.attributes["snippet"] then
    lines, first = slice_snippet(lines, cb.attributes["snippet"], path)
  elseif cb.attributes["start-line"] or cb.attributes["end-line"] then
    local start = tonumber(cb.attributes["start-line"] or 1)
    local last = tonumber(cb.attributes["end-line"] or #lines)
    lines, first = slice_lines(lines, start, last)
  end
  local trimmed, dropped = trim_blank_edges(lines)
  lines = dedent(trimmed)
  if has_class(cb, "numberLines") and cb.attributes["startFrom"] == nil then
    cb.attributes["startFrom"] = tostring(first + dropped)
  end
  cb.text = table.concat(lines, "\n")
  cb.attributes["include"] = nil
  cb.attributes["snippet"] = nil
  cb.attributes["start-line"] = nil
  cb.attributes["end-line"] = nil
  return with_heading(cb)
end
