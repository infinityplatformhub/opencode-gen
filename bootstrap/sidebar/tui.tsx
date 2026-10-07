import { Plugin } from "@opencode/plugin/tui"
import { createEffect, createSignal, onCleanup, Show } from "solid-js"
import { parseTicket } from "./ticket-view.js"

function TicketCard(props: { context: Plugin.Context; sessionID: string }) {
  const [ticket, setTicket] = createSignal<ReturnType<typeof parseTicket>>()
  const [state, setState] = createSignal("No ticket selected")
  createEffect(() => {
    const session = props.context.data.session.get(props.sessionID)
    if (!session) return
    let disposed = false
    let busy = false
    setTicket(undefined)
    async function refresh() {
      if (busy) return
      busy = true
      try {
        const read = async (path: string) => {
          const bytes = await props.context.client.file.read({ path, location: session!.location })
          if (bytes.byteLength > 12288) throw new Error("Oversized sidebar data")
          return new TextDecoder().decode(bytes)
        }
        const selected = JSON.parse(await read(`.ctx/local/sessions/${props.sessionID}.json`))
        if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$/.test(selected.ticket) || !["shared", "private"].includes(selected.visibility)) throw new Error("Invalid selection")
        const folder = selected.visibility === "private" ? ".ctx/local/tickets" : ".ctx/tickets"
        const next = parseTicket(await read(`${folder}/${selected.ticket}.md`))
        if (!disposed) { setTicket(next); setState(selected.visibility === "private" ? "Private ticket" : "Ticket") }
      } catch {
        if (!disposed) { setTicket(undefined); setState("Select a ticket to show progress") }
      } finally { busy = false }
    }
    void refresh()
    // Poll only the mounted card; no model calls, Git subprocesses, or recursive scans.
    const timer = setInterval(() => void refresh(), 5000)
    onCleanup(() => { disposed = true; clearInterval(timer) })
  })
  const theme = props.context.theme
  return (
    <box border={["top"]} borderColor={theme.text.muted} paddingTop={1} gap={1}>
      <text fg={theme.text.base}><b>◈ {state()}</b></text>
      <Show when={ticket()}>{(value) => <>
        <text fg={theme.text.base}>{value().title}</text>
        <text fg={theme.text.muted}>● {value().status || "open"}</text>
        <Show when={value().done}><box><text fg={theme.text.feedback.success.base}><b>✓ Done</b></text><text fg={theme.text.muted}>{value().done}</text></box></Show>
        <Show when={value().next}><box><text fg={theme.text.base}><b>→ Next</b></text><text fg={theme.text.muted}>{value().next}</text></box></Show>
        <Show when={value().blocker && !/^(none|ไม่มี|—)$/i.test(value().blocker)}><box><text fg={theme.text.feedback.warning.base}><b>! Blocked</b></text><text fg={theme.text.muted}>{value().blocker}</text></box></Show>
      </>}</Show>
    </box>
  )
}

export default Plugin.define({
  id: "opencode-gen-sidebar-ui",
  setup(context) {
    context.ui.slot({ append: "sidebar.content", render: (props) => <TicketCard context={context} sessionID={props.sessionID} /> })
  },
})
