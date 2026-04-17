# S5 — UI/UX Principles for Mobile

---

## 1. Touch Targets

> Every tappable element must be **at least 44×44 pts** (Apple HIG) or **48×48 dp** (Material).  
> Fingers are not cursors — give them room.

```
┌─────────────────────────────────┐
│   ❌  Bad touch target          │
│   [tiny btn]  ← 20×20 px       │
│                                 │
│   ✅  Good touch target         │
│   [   Button   ]  ← 48×48 dp   │
└─────────────────────────────────┘
```

```jsx
// ✅ Correct — minimum touch target
<TouchableOpacity style={{ minHeight: 48, minWidth: 48, justifyContent: 'center', alignItems: 'center' }}>
  <Text>Tap Me</Text>
</TouchableOpacity>
```

---

## 2. Spacing System

> Use a **base-8 grid**. All spacing values: `8, 16, 24, 32, 48`.  
> Consistent spacing creates visual rhythm.

```
┌──────────────────────────────┐
│ ←16→ Content ←16→           │  ← horizontal padding
│                              │
│  [Card]     margin-bottom:16 │
│  [Card]     margin-bottom:16 │
│  [Card]                      │
└──────────────────────────────┘
```

```jsx
// ✅ Spacing using base-8 system
const spacing = { xs: 8, sm: 16, md: 24, lg: 32 };

<View style={{ padding: spacing.sm, marginBottom: spacing.sm }}>
  <Text>Content</Text>
</View>
```

---

## 3. Typography Scale

> A type scale creates hierarchy. Use **3 sizes max** per screen.

```
Display  → 32px  Bold    (hero titles)
Title    → 20px  SemiBold (screen headers)
Body     → 16px  Regular  (main content)
Caption  → 12px  Regular  (labels, hints)
```

```jsx
// ✅ Typography scale object
const typography = {
  display: { fontSize: 32, fontWeight: '700' },
  title:   { fontSize: 20, fontWeight: '600' },
  body:    { fontSize: 16, fontWeight: '400' },
  caption: { fontSize: 12, fontWeight: '400' },
};

<Text style={typography.title}>Welcome Back</Text>
<Text style={typography.body}>Here is your summary for today.</Text>
<Text style={typography.caption}>Last updated 5 min ago</Text>
```

---

## 4. Color Theory

> **60-30-10 Rule:**  
> - 60% → Background (neutral)  
> - 30% → Surface / secondary (cards, panels)  
> - 10% → Accent (buttons, highlights)

```
┌─────────────────────────────────────┐
│  Background  #F5F5F5   (60%)        │
│  ┌───────────────────────────────┐  │
│  │  Surface  #FFFFFF   (30%)     │  │
│  │                               │  │
│  │     [ Primary Btn ] (10%)     │  │
│  │       accent: #6200EE         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

```jsx
// ✅ Color system
const colors = {
  background: '#F5F5F5',  // 60%
  surface:    '#FFFFFF',   // 30%
  primary:    '#6200EE',   // 10% accent
  text:       '#1A1A1A',
  textMuted:  '#757575',
};

<View style={{ backgroundColor: colors.background, flex: 1 }}>
  <View style={{ backgroundColor: colors.surface, padding: 16, borderRadius: 8 }}>
    <TouchableOpacity style={{ backgroundColor: colors.primary, padding: 12, borderRadius: 6 }}>
      <Text style={{ color: '#fff', textAlign: 'center' }}>Action</Text>
    </TouchableOpacity>
  </View>
</View>
```

---

## 5. Accessibility Basics

> **A11y is not optional.** Users with disabilities must be able to use your app.

```
accessibilityLabel   → what screen reader reads
accessibilityRole    → "button", "header", "image"
accessibilityHint    → what will happen on tap
```

```jsx
// ✅ Accessible button
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Submit form"
  accessibilityRole="button"
  accessibilityHint="Saves your data and goes to home"
  style={{ backgroundColor: '#6200EE', padding: 16, borderRadius: 8 }}
>
  <Text style={{ color: '#fff' }}>Submit</Text>
</TouchableOpacity>
```

---

## 6. Visual Hierarchy Diagram

```
┌──────────────────────────────┐
│  🔵 Display (32px Bold)      │  ← grabs attention first
│                              │
│  Title (20px SemiBold)       │  ← section context
│                              │
│  Body text (16px) tells the  │  ← readable content
│  user what is happening.     │
│                              │
│  caption • 12px              │  ← least important
└──────────────────────────────┘
```

---

## Quick Reference Cheatsheet

| Concept        | Rule                              |
|----------------|-----------------------------------|
| Touch Target   | Min 48×48 dp                      |
| Spacing        | Multiples of 8 (8,16,24,32...)    |
| Font Sizes     | 32 / 20 / 16 / 12                 |
| Colors         | 60% bg / 30% surface / 10% accent |
| Contrast Ratio | Text ≥ 4.5:1 on background        |
| Accessibility  | Always add `accessibilityLabel`   |
