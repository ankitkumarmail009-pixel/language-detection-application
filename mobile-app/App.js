import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Screens
import DetectionScreen from './src/screens/DetectionScreen';
import TranslationScreen from './src/screens/TranslationScreen';
import BatchScreen from './src/screens/BatchScreen';
import HistoryScreen from './src/screens/HistoryScreen';

// Theme
import { theme } from './src/theme/theme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function DetectionStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="DetectionMain" 
        component={DetectionScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

function TranslationStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="TranslationMain" 
        component={TranslationScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

function BatchStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="BatchMain" 
        component={BatchScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

function HistoryStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="HistoryMain" 
        component={HistoryScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <StatusBar style="light" />
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;

              if (route.name === 'Detect') {
                iconName = focused ? 'translate' : 'translate';
              } else if (route.name === 'Translate') {
                iconName = focused ? 'google-translate' : 'google-translate';
              } else if (route.name === 'Batch') {
                iconName = focused ? 'file-multiple' : 'file-multiple-outline';
              } else if (route.name === 'History') {
                iconName = focused ? 'history' : 'history';
              }

              return <Icon name={iconName} size={size} color={color} />;
            },
            tabBarActiveTintColor: '#6366f1',
            tabBarInactiveTintColor: 'gray',
            headerShown: false,
            tabBarStyle: {
              backgroundColor: '#ffffff',
              borderTopWidth: 1,
              borderTopColor: '#e5e7eb',
              paddingBottom: 5,
              paddingTop: 5,
              height: 60,
            },
          })}
        >
          <Tab.Screen name="Detect" component={DetectionStack} />
          <Tab.Screen name="Translate" component={TranslationStack} />
          <Tab.Screen name="Batch" component={BatchStack} />
          <Tab.Screen name="History" component={HistoryStack} />
        </Tab.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}

