import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Path, Rect } from 'react-native-svg';

interface Props {
  progress?: number;
  total?: number;
  onBack?: () => void;
  showSkip?: boolean;
  onSkip?: () => void;
  label?: string;
}

export function TopChrome({
  progress = 0,
  total = 6,
  onBack,
  showSkip = true,
  onSkip,
  label = 'App Store',
}: Props) {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={[styles.wrap, { paddingTop: Math.max(insets.top, 14) }]}
      pointerEvents="box-none"
    >
      <View style={styles.statusBar} pointerEvents="none">
        <View style={styles.statusLeft}>
          <View style={styles.timeRow}>
            <Text style={styles.timeText}>00:25</Text>
            <Svg width={18} height={13} viewBox="0 0 18 13">
              <Path
                d="M1 11V3M1 7h14a2 2 0 012 2v2M5 7V5a1 1 0 011-1h3a1 1 0 011 1v2"
                stroke="#fff"
                strokeWidth={1.4}
                strokeLinecap="round"
                fill="none"
              />
            </Svg>
          </View>
          <Text style={styles.returnLabel}>◀ {label}</Text>
        </View>

        <View style={styles.statusRight}>
          <Svg width={18} height={11} viewBox="0 0 18 11">
            <Rect x={0} y={7} width={3} height={4} rx={0.6} fill="#fff" />
            <Rect x={4.5} y={5} width={3} height={6} rx={0.6} fill="#fff" />
            <Rect x={9} y={2.5} width={3} height={8.5} rx={0.6} fill="#fff" />
            <Rect x={13.5} y={0} width={3} height={11} rx={0.6} fill="#fff" />
          </Svg>
          <Text style={styles.fiveG}>5G</Text>
          <Battery />
        </View>
      </View>

      <View style={styles.navRow} pointerEvents="box-none">
        {onBack ? (
          <TouchableOpacity
            style={styles.backBtn}
            onPress={onBack}
            hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
          >
            <Svg width={9} height={16} viewBox="0 0 9 16">
              <Path
                d="M7.5 1.5L1.5 8l6 6.5"
                stroke="#fff"
                strokeWidth={1.8}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
            </Svg>
          </TouchableOpacity>
        ) : (
          <View style={styles.placeholder} />
        )}

        <View style={styles.dots} pointerEvents="none">
          {Array.from({ length: total }).map((_, i) => (
            <View
              key={i}
              style={{
                width: i === progress ? 22 : 6,
                height: 6,
                borderRadius: 3,
                backgroundColor:
                  i <= progress ? '#fff' : 'rgba(255,255,255,0.22)',
              }}
            />
          ))}
        </View>

        {showSkip ? (
          <TouchableOpacity
            onPress={onSkip}
            hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
          >
            <Text style={styles.skip}>Skip</Text>
          </TouchableOpacity>
        ) : (
          <View style={styles.placeholder} />
        )}
      </View>
    </View>
  );
}

function Battery() {
  return (
    <View style={batteryStyles.container}>
      <View style={batteryStyles.fill} />
      <Text style={batteryStyles.percent}>62</Text>
      <View style={batteryStyles.nub} />
    </View>
  );
}

const batteryStyles = StyleSheet.create({
  container: {
    width: 28,
    height: 13,
    borderWidth: 1.2,
    borderColor: '#fff',
    borderRadius: 4,
    justifyContent: 'center',
    paddingHorizontal: 1.2,
    position: 'relative',
  },
  fill: {
    width: '62%',
    height: '100%',
    backgroundColor: '#FF9F0A',
    borderRadius: 2,
  },
  percent: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    textAlign: 'center',
    lineHeight: 13,
    fontSize: 9,
    fontWeight: '700',
    color: '#000',
  },
  nub: {
    position: 'absolute',
    right: -3,
    top: 3,
    width: 2,
    height: 5,
    backgroundColor: '#fff',
    borderRadius: 1,
  },
});

const styles = StyleSheet.create({
  wrap: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 20,
  },
  statusBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: 28,
    height: 40,
  },
  statusLeft: {
    gap: 1,
  },
  timeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  timeText: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
  },
  returnLabel: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
    opacity: 0.9,
    marginLeft: 2,
  },
  statusRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingTop: 4,
  },
  fiveG: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
  navRow: {
    marginTop: 8,
    height: 44,
    paddingHorizontal: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  backBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255,255,255,0.08)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholder: {
    width: 36,
  },
  dots: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  skip: {
    color: 'rgba(255,255,255,0.85)',
    fontSize: 16,
    fontWeight: '500',
  },
});
