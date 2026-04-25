import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import { ACCENT_BLUE } from '../constants/colors';

interface Props {
  color?: string;
  height?: number;
}

export function BlinkingCursor({ color = ACCENT_BLUE, height = 22 }: Props) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const t = setInterval(() => setVisible(v => !v), 500);
    return () => clearInterval(t);
  }, []);

  return (
    <View
      style={{
        width: 2,
        height,
        backgroundColor: color,
        marginLeft: 2,
        opacity: visible ? 1 : 0,
      }}
    />
  );
}
