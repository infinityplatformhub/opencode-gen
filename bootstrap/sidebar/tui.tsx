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
        if (!disposed) { setTicket(next); setState(selected.visibility === "private" ? "CURRENT · private" : "CURRENT") }
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
      <box flexDirection="row" justifyContent="space-between" gap={1}>
        <text fg={theme.text.muted}>{ticket() ? state() : "CURRENT"}</text>
        <Show when={ticket()}>{(value) => <text fg={value().status === "blocked" ? theme.text.feedback.warning.base : theme.text.muted}>{value().status === "blocked" ? "!" : "●"} {value().statusLabel}</text>}</Show>
      </box>
      <Show when={!ticket()}><text fg={theme.text.muted}>{state()}</text></Show>
      <Show when={ticket()}>{(value) => <>
        <box>
          <text fg={theme.text.base} maxHeight={2}><b>{value().title}</b></text>
          <Show when={value().id}><text fg={theme.text.muted} wrapMode="none" truncate>{value().id}</text></Show>
        </box>
        <Show when={value().current && value().status !== "done"}><text fg={theme.text.base} maxHeight={2}>{value().current}</text></Show>
        <Show when={value().checkpoint}><box><text fg={theme.text.muted}>Checkpoint</text><text fg={theme.text.muted} maxHeight={2}>{value().checkpoint}</text></box></Show>
        <Show when={value().blocker && !/^(none|ไม่มี|—)$/i.test(value().blocker)}><box><text fg={theme.text.muted}>Blocked</text><text fg={theme.text.base} maxHeight={2}>{value().blocker}</text></box></Show>
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
