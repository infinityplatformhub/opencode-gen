// UI-only parser: do not import server filesystem modules into the TUI bundle.
export function parseTicket(text) {
  const line = (pattern) => (text.match(pattern)?.[1] ?? "").trim().replace(/[\u0000-\u001f\u007f]/g, "").slice(0, 240)
  return {
    title: line(/^#\s+(.+)$/m), status: line(/^Status:\s*(.+)$/mi),
    done: line(/^- Done:\s*(.+)$/mi), next: line(/^- Next:\s*(.+)$/mi),
    blocker: line(/^- Blocker:\s*(.+)$/mi),
  }
}
