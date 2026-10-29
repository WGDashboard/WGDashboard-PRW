---
description: "Use when writing or editing Vue, JavaScript or TypeScript in the WGDashboard admin/client apps: Composition API, component size, API layer, stores, locale usage."
applyTo: "src/web/**/*.vue, src/web/**/*.js, src/web/**/*.ts"
---
# Vue style – readability first

1. `<script setup>` Composition API only. Pinia stores use the setup syntax of `defineStore`.
2. Templates contain no logic beyond property access. Everything else becomes a named `computed`.
3. Components ≲ 250 lines. Extract composables (`usePeerSorting`, `usePeerFilter`, `usePeerModals`).
4. All HTTP goes through the shared API layer in `src/web/shared` (e.g. `api.peers.update(...)`). No raw `fetch`/`axios` or URL strings in components.
5. `async/await` only. No callback-style helpers.
6. Explicit `defineProps` (with defaults) and `defineEmits`.
7. Descriptive names; no single-letter variables outside trivial `v-for` indexes.
8. Keep component **names and folder structure** aligned with `reference/src/static/app` and `reference/src/static/client`, so features can be compared one-to-one.
9. User-facing text goes through the locale helper with English fallback.

## Example

Legacy pattern:
```vue
<span>{{ peers.filter(p => p.status === 'running').length }} / {{ peers.length }}</span>
```

Rewrite:
```vue
<script setup>
import { computed } from 'vue'

const props = defineProps({
    peers: { type: Array, default: () => [] },
})

const connectedPeerCount = computed(() => {
    let count = 0

    for (const peer of props.peers) {
        if (peer.status === 'running') {
            count += 1
        }
    }

    return count
})
</script>

<template>
    <span>{{ connectedPeerCount }} / {{ props.peers.length }}</span>
</template>
```
