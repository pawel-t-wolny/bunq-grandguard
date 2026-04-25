import React from 'react';
import { Text, TouchableOpacity, StyleSheet, View } from 'react-native';
import { ACCENT_BLUE } from '../constants/colors';

interface Props {
  children: string;
  disabled?: boolean;
  onPress?: () => void;
}

export function PrimaryCTA({ children, disabled = false, onPress }: Props) {
  return (
    <View style={disabled ? undefined : styles.shadow}>
      <TouchableOpacity
        disabled={disabled}
        onPress={onPress}
        activeOpacity={0.85}
        style={[
          styles.btn,
          { backgroundColor: disabled ? 'rgba(30,155,255,0.35)' : ACCENT_BLUE },
        ]}
      >
        <Text style={styles.label}>{children}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  shadow: {
    shadowColor: ACCENT_BLUE,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.35,
    shadowRadius: 12,
    elevation: 6,
    borderRadius: 28,
  },
  btn: {
    width: '100%',
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  label: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
    letterSpacing: -0.2,
  },
});
