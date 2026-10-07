// UI-only parser: do not import server filesystem modules into the TUI bundle.
export function parseTicket(text) {
  const line = (pattern) => (text.match(pattern)?.[1] ?? "").trim().replace(/[\u0000-\u001f\u007f]/g, "").slice(0, 240)
  const heading = line(/^#\s+(.+)$/m)
  const parts = heading.match(/^(\S+)\s+[—–]\s+(.+)$/)
  const rawStatus = line(/^Status:\s*(.+)$/mi).toLowerCase()
  return {
    title: parts?.[2] ?? heading, id: parts?.[1] ?? "",
    status: rawStatus, statusLabel: ({ "in-progress": "Working", open: "Open", blocked: "Blocked", waiting: "Waiting", done: "Closed" })[rawStatus] ?? "Open",
    current: line(/^- Current:\s*(.+)$/mi),
    done: line(/^- Done:\s*(.+)$/mi), next: line(/^- Next:\s*(.+)$/mi),
    checkpoint: line(/^- Checkpoint:\s*(.+)$/mi) || line(/^- Done:\s*(.+)$/mi),
    blocker: line(/^- Blocker:\s*(.+)$/mi),
  }
}
