-- paths-footer.lua: a slide header with the attribute {paths=N} sets the footer
-- counter "paths to reason about" for that slide and the ones after it.
--
--   ## Three numbers {paths=64}
--
-- In beamer output the header is followed by \pathcount{N}, defined in preamble.tex.
-- Other output formats just drop the attribute.

function Header(el)
  local n = el.attributes["paths"]
  if n == nil then
    return nil
  end
  el.attributes["paths"] = nil
  if FORMAT:match("beamer") then
    return { el, pandoc.RawBlock("latex", "\\pathcount{" .. n .. "}") }
  end
  return el
end
