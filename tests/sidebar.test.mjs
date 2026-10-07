import { test } from "node:test"
import assert from "node:assert/strict"
import { mkdtemp, mkdir, writeFile, readFile, rm } from "node:fs/promises"
import { join } from "node:path"
import plugin from "../bootstrap/sidebar/index.js"
import { loadTicket } from "../bootstrap/sidebar/ticket.js"
import { parseTicket } from "../bootstrap/sidebar/ticket-view.js"

test("selection is session-scoped, validates tickets and preserves private visibility", async () => {
  const root = await mkdtemp("/tmp/opencode/sidebar-test-")
  try {
    await mkdir(join(root, ".ctx/local/tickets"), { recursive: true })
    await writeFile(join(root, ".ctx/local/tickets/P-1.md"), "# P-1 — Private work\nStatus: in-progress\n- Done: inspected\n- Next: verify\n- Blocker: none\n")
    let tool
    await plugin.setup({ location: { directory: root }, session: { get: async () => ({ location: { directory: root } }) },
      tool: { transform: async (fn) => fn({ add: (value) => { tool = value } }) } })
    await tool.execute({ ticket: "P-1", visibility: "private" }, { sessionID: "ses_test" })
    assert.deepEqual(JSON.parse(await readFile(join(root, ".ctx/local/sessions/ses_test.json"))), { ticket: "P-1", visibility: "private" })
    await assert.rejects(tool.execute({ ticket: "missing", visibility: "shared" }, { sessionID: "ses_other" }))
    await assert.rejects(loadTicket(root, "../private", "private"))
    const result = await loadTicket(root, "P-1", "private")
    assert.equal(result.next, "verify")
    assert.equal(result.done, "inspected")
  } finally { await rm(root, { recursive: true, force: true }) }
})

test("display parser bounds output and strips terminal control characters", () => {
  const data = parseTicket("# T-1 — Title\nStatus: done\n- Done: " + "x".repeat(1000) + "\n- Next: safe\u001b text\n")
  assert.equal(data.done.length, 240)
  assert.ok(!data.next.includes("\u001b"))
})
