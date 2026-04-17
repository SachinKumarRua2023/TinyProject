# S7 — React Navigation

> Install first:
> ```bash
> npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs @react-navigation/drawer
> npm install react-native-screens react-native-safe-area-context
> ```

---

## 1. Stack Navigator

> Screens stacked on top of each other. Going forward **pushes**, going back **pops**.  
> Like a deck of cards.

```
┌──────────────────────────┐
│  Stack                   │
│                          │
│  ┌──────────────────┐    │
│  │  Screen C (top)  │    │  ← current screen
│  ├──────────────────┤    │
│  │  Screen B        │    │
│  ├──────────────────┤    │
│  │  Screen A        │    │  ← initial
│  └──────────────────┘    │
│                          │
│  Back → pops top screen  │
└──────────────────────────┘
```

```jsx
// App.js
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { View, Text, Button } from 'react-native';

const Stack = createStackNavigator();

function HomeScreen({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Home Screen</Text>
      <Button title="Go to Details" onPress={() => navigation.navigate('Details')} />
    </View>
  );
}

function DetailsScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
    </View>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

---

## 2. Passing Params Between Screens

> Send data when navigating. Receive it with `route.params`.

```
HomeScreen                     DetailsScreen
─────────────────              ─────────────────
navigate('Details',    ──►     route.params.userId
  { userId: 42 })              route.params.name
  { name: 'Ravi'  }
```

```jsx
// Sending params
navigation.navigate('Details', { userId: 42, name: 'Ravi' });

// Receiving params
function DetailsScreen({ route }) {
  const { userId, name } = route.params;
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>User ID: {userId}</Text>
      <Text>Name: {name}</Text>
    </View>
  );
}
```

---

## 3. Tab Navigator

> Bottom tabs for **top-level screens**. Always visible — switch between sections.

```
┌──────────────────────────┐
│                          │
│    (screen content)      │
│                          │
├──────────────────────────┤
│  🏠 Home  📋 Feed  👤 Me │  ← tab bar
└──────────────────────────┘
```

```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text } from 'react-native';

const Tab = createBottomTabNavigator();

const HomeScreen  = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Home</Text></View>;
const FeedScreen  = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Feed</Text></View>;
const ProfileScreen = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Profile</Text></View>;

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home"    component={HomeScreen} />
        <Tab.Screen name="Feed"    component={FeedScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

---

## 4. Drawer Navigator

> Side menu that **slides in** from the left (or right).  
> Good for secondary navigation, settings, profile.

```
 Drawer closed          Drawer open
┌─────────────┐       ┌────┬──────────┐
│             │       │    │          │
│  Content    │  ──►  │ 🏠 │ Home     │
│             │       │ 📋 │ Feed     │
│  ☰ Menu    │       │ ⚙️ │ Settings │
└─────────────┘       └────┴──────────┘
```

```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { View, Text } from 'react-native';

const Drawer = createDrawerNavigator();

const HomeScreen     = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Home</Text></View>;
const SettingsScreen = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Settings</Text></View>;

export default function App() {
  return (
    <NavigationContainer>
      <Drawer.Navigator>
        <Drawer.Screen name="Home"     component={HomeScreen} />
        <Drawer.Screen name="Settings" component={SettingsScreen} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}
```

---

## 5. Nesting — Tabs Inside Stack (Real-world Pattern)

> Most apps combine navigators. Tabs live **inside** the stack so you can push screens on top of them.

```
NavigationContainer
└── Stack Navigator
    ├── Screen: "Main" → Tab Navigator
    │                    ├── Tab: Home
    │                    └── Tab: Profile
    └── Screen: "Details" (pushed on top of tabs)
```

```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text, Button } from 'react-native';

const Stack = createStackNavigator();
const Tab   = createBottomTabNavigator();

const HomeScreen    = ({ navigation }) => (
  <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}>
    <Text>Home Tab</Text>
    <Button title="Open Details" onPress={() => navigation.navigate('Details', { id: 7 })} />
  </View>
);
const ProfileScreen = () => <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}><Text>Profile Tab</Text></View>;
const DetailsScreen = ({ route }) => (
  <View style={{ flex:1, alignItems:'center', justifyContent:'center' }}>
    <Text>Details — ID: {route.params.id}</Text>
  </View>
);

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home"    component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Main"    component={TabNavigator} options={{ headerShown: false }} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

---

## Quick Reference Cheatsheet

| Navigator       | Use Case                         | Key Method                          |
|-----------------|----------------------------------|-------------------------------------|
| Stack           | Drill-down screens               | `navigation.navigate()`, `goBack()` |
| Bottom Tabs     | Top-level app sections           | `navigation.navigate(tabName)`      |
| Drawer          | Secondary nav / settings         | `navigation.openDrawer()`           |
| Params (send)   | Pass data to next screen         | `navigate('Screen', { key: val })`  |
| Params (receive)| Read data in destination screen  | `route.params.key`                  |
| Nesting         | Tabs + Stack together            | Wrap Tab inside Stack Screen        |
