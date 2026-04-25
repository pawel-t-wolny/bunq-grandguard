import React from 'react';
import { View } from 'react-native';
import Svg, { Defs, Filter, FeGaussianBlur, Rect, G } from 'react-native-svg';
import { RAINBOW_STRIPES } from '../constants/colors';

interface Props {
  opacity?: number;
}

const VB_WIDTH = 470;
const VB_HEIGHT = 520;
const STRIPE_COUNT = RAINBOW_STRIPES.length;
const STRIPE_W = VB_WIDTH / STRIPE_COUNT;

export function RainbowBlob({ opacity = 0.55 }: Props) {
  return (
    <View
      pointerEvents="none"
      style={{
        position: 'absolute',
        top: -160,
        left: -40,
        right: -40,
        height: VB_HEIGHT,
        opacity,
        zIndex: 0,
      }}
    >
      <Svg
        width="100%"
        height="100%"
        viewBox={`0 0 ${VB_WIDTH} ${VB_HEIGHT}`}
        preserveAspectRatio="xMidYMid slice"
      >
        <Defs>
          <Filter id="blur" x="-20%" y="-20%" width="140%" height="140%">
            <FeGaussianBlur stdDeviation="60" />
          </Filter>
        </Defs>
        <G filter="url(#blur)">
          {RAINBOW_STRIPES.map((c, i) => (
            <Rect
              key={i}
              x={i * STRIPE_W - 2}
              y={0}
              width={STRIPE_W + 4}
              height={VB_HEIGHT}
              fill={c}
            />
          ))}
        </G>
      </Svg>
    </View>
  );
}
