import { mkdir, writeFile, realpath, rename } from "node:fs/promises"
import { join, sep } from "node:path"
import { randomUUID } from "node:crypto"

// Plugin.define is an identity helper in V2.0.24. A structural definition avoids
// requiring a second installed copy of the server SDK just to register this tool.
export default {
  id: "opencode-gen-sidebar",
  async setup(ctx) {
    await ctx.tool.transform((editor) => {
      editor.add({
        name: "opencode_gen_select_ticket",
        description: "Bind an existing project ticket to this session's sidebar. Does not create or modify the ticket.",
        input: {
          type: "object",
          properties: { ticket: { type: "string" }, visibility: { type: "string", enum: ["shared", "private"] } },
          required: ["ticket", "visibility"], additionalProperties: false,
        },
        async execute(input, context) {
          if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$/.test(input.ticket)) throw new Error("Invalid ticket ID")
          const session = await ctx.session.get({ sessionID: context.sessionID })
          const root = session.location.directory
          if (root !== ctx.location.directory) throw new Error("Select the ticket from its project root")
          const { loadTicket } = await import("./ticket.js")
          await loadTicket(root, input.ticket, input.visibility)
          const folder = join(root, ".ctx/local/sessions")
          const local = await realpath(join(root, ".ctx/local"))
          if (!local.startsWith((await realpath(root)) + sep)) throw new Error("External local storage")
          await mkdir(folder, { recursive: true })
          if (!(await realpath(folder)).startsWith(local + sep)) throw new Error("External session storage")
          const temp = join(folder, `${context.sessionID}.${randomUUID()}.tmp`)
          await writeFile(temp, JSON.stringify(input) + "\n", { flag: "wx", mode: 0o600 })
          await rename(temp, join(folder, `${context.sessionID}.json`))
          return { content: "Ticket selected for this session sidebar." }
        },
      })
    })
  },
}
