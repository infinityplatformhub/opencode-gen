import { readFile, realpath, stat } from "node:fs/promises"
import { join, sep } from "node:path"
import { parseTicket } from "./ticket-view.js"

export async function loadTicket(root, id, visibility) {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$/.test(id) || !["shared", "private"].includes(visibility)) throw new Error("Invalid ticket selection")
  const base = await realpath(root)
  const path = await realpath(join(base, visibility === "private" ? ".ctx/local/tickets" : ".ctx/tickets", `${id}.md`))
  if (!path.startsWith(base + sep)) throw new Error("External ticket path")
  if ((await stat(path)).size > 12288) throw new Error("Ticket exceeds 12 KiB")
  return parseTicket(await readFile(path, "utf8"))
}
