# S6 — Lists & Scroll in React Native

---

## 1. ScrollView

> Use for **small, fixed content** that needs to scroll. Renders ALL children at once.  
> ⚠️ Never use ScrollView for long/dynamic lists — use FlatList instead.

```
┌──────────────────┐
│  ScrollView      │
│  ┌────────────┐  │  ← All rendered at once
│  │  Item 1    │  │
│  │  Item 2    │  │
│  │  Item 3    │  │
│  │  Item 4    │  │  ← even off-screen
│  └────────────┘  │
└──────────────────┘
```

```jsx
import { ScrollView, Text, View } from 'react-native';

export default function App() {
  return (
    <ScrollView>
      <Text style={{ padding: 16 }}>Item 1</Text>
      <Text style={{ padding: 16 }}>Item 2</Text>
      <Text style={{ padding: 16 }}>Item 3</Text>
    </ScrollView>
  );
}
```

---

## 2. FlatList

> Use for **long dynamic lists**. Only renders visible items (windowing).  
> **Required props:** `data`, `renderItem`, `keyExtractor`

```
┌──────────────────┐
│  FlatList        │
│  ┌────────────┐  │  ← rendered (visible)
│  │  Item 1    │  │
│  │  Item 2    │  │
│  └────────────┘  │
│  (Items 3–100    │  ← NOT rendered yet
│   virtualized)   │
└──────────────────┘
```

```jsx
import { FlatList, Text, View } from 'react-native';

const DATA = [
  { id: '1', name: 'Apple' },
  { id: '2', name: 'Banana' },
  { id: '3', name: 'Cherry' },
];

export default function App() {
  return (
    <FlatList
      data={DATA}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <Text style={{ padding: 16, borderBottomWidth: 1 }}>{item.name}</Text>
      )}
    />
  );
}
```

---

## 3. keyExtractor

> Tells React which item is which — like a `key` prop.  
> Must return a **unique string** per item.

```
DATA = [ {id:'1',...}, {id:'2',...}, {id:'3',...} ]
         ↓               ↓               ↓
keyExtractor returns: '1'           '2'           '3'
React tracks changes using these keys internally.
```

```jsx
// ✅ From an id field
keyExtractor={(item) => item.id}

// ✅ From index (use only if no unique id)
keyExtractor={(item, index) => index.toString()}
```

---

## 4. Pull-to-Refresh

> Add `refreshControl` prop to FlatList or ScrollView.

```
┌──────────────────┐
│   ↓ Pull down    │  ← user drags down
│                  │
│   ⟳ Loading...  │  ← spinner shows
│                  │
│   ✅ Refreshed   │  ← data reloads
└──────────────────┘
```

```jsx
import { FlatList, RefreshControl, Text } from 'react-native';
import { useState } from 'react';

export default function App() {
  const [refreshing, setRefreshing] = useState(false);
  const [data, setData] = useState(['Item 1', 'Item 2', 'Item 3']);

  const onRefresh = () => {
    setRefreshing(true);
    setTimeout(() => {
      setData(['New Item 1', 'New Item 2']);
      setRefreshing(false);
    }, 1500);
  };

  return (
    <FlatList
      data={data}
      keyExtractor={(item, i) => i.toString()}
      renderItem={({ item }) => <Text style={{ padding: 16 }}>{item}</Text>}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    />
  );
}
```

---

## 5. Empty State

> Always show something when the list is empty — never a blank screen.

```
┌──────────────────┐
│                  │
│       📭         │  ← icon or illustration
│  No items yet    │  ← clear message
│  Add one below   │  ← optional CTA
│                  │
└──────────────────┘
```

```jsx
import { FlatList, Text, View } from 'react-native';

const EmptyState = () => (
  <View style={{ alignItems: 'center', marginTop: 60 }}>
    <Text style={{ fontSize: 40 }}>📭</Text>
    <Text style={{ fontSize: 18, marginTop: 12 }}>No items yet</Text>
  </View>
);

export default function App() {
  const data = []; // empty list

  return (
    <FlatList
      data={data}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <Text>{item.name}</Text>}
      ListEmptyComponent={<EmptyState />}
    />
  );
}
```

---

## 6. SectionList

> Like FlatList but with **grouped sections** — think contacts A, B, C... or settings groups.

```
┌──────────────────┐
│  ── Fruits ──    │  ← section header
│  Apple           │
│  Banana          │
│  ── Veggies ──   │  ← section header
│  Carrot          │
│  Spinach         │
└──────────────────┘
```

```jsx
import { SectionList, Text, View } from 'react-native';

const SECTIONS = [
  { title: 'Fruits',  data: ['Apple', 'Banana'] },
  { title: 'Veggies', data: ['Carrot', 'Spinach'] },
];

export default function App() {
  return (
    <SectionList
      sections={SECTIONS}
      keyExtractor={(item, i) => item + i}
      renderItem={({ item }) => (
        <Text style={{ padding: 12, paddingLeft: 16 }}>{item}</Text>
      )}
      renderSectionHeader={({ section }) => (
        <Text style={{ backgroundColor: '#eee', padding: 8, paddingLeft: 16, fontWeight: '700' }}>
          {section.title}
        </Text>
      )}
    />
  );
}
```

---

## Quick Reference Cheatsheet

| Component      | Use When                              | Key Props                              |
|----------------|---------------------------------------|----------------------------------------|
| `ScrollView`   | Small static content                  | —                                      |
| `FlatList`     | Long dynamic list                     | `data`, `renderItem`, `keyExtractor`   |
| `SectionList`  | Grouped/sectioned list                | `sections`, `renderSectionHeader`      |
| `keyExtractor` | Unique id per row                     | Returns string                         |
| Pull-to-Refresh| Reload data on drag-down              | `refreshControl`, `RefreshControl`     |
| Empty State    | No data                               | `ListEmptyComponent`                   |
