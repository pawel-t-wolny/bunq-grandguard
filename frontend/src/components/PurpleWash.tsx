import React from 'react';
import { StyleSheet, View } from 'react-native';
import Svg, { Defs, RadialGradient, Stop, Rect } from 'react-native-svg';

export function PurpleWash() {
  return (
    <View style={[StyleSheet.absoluteFillObject, { zIndex: 1 }]} pointerEvents="none">
      <Svg width="100%" height="100%" preserveAspectRatio="none">
        <Defs>
          <RadialGradient id="rg" cx="50%" cy="0%" rx="80%" ry="60%">
            <Stop offset="0%" stopColor="#4A1882" stopOpacity={0.8} />
            <Stop offset="60%" stopColor="#0C0616" stopOpacity={0.95} />
            <Stop offset="100%" stopColor="#0C0616" stopOpacity={1} />
          </RadialGradient>
        </Defs>
        <Rect x={0} y={0} width="100%" height="100%" fill="url(#rg)" />
      </Svg>
    </View>
  );
}
