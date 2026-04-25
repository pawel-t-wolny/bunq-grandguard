import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import Svg, { Path } from 'react-native-svg';
import { TopChrome } from '../components/TopChrome';
import { PurpleWash } from '../components/PurpleWash';
import { RainbowBlob } from '../components/RainbowBlob';
import {
  ACCENT_BLUE,
  BG_PURPLE,
  SUCCESS_GREEN,
  SUCCESS_GREEN_GLOW,
} from '../constants/colors';

interface Props {
  onBack?: () => void;
  onDismiss?: () => void;
}

export function ApprovedScreen({ onBack, onDismiss }: Props) {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.root}>
      <RainbowBlob opacity={0.15} />
      <PurpleWash />

      <View
        pointerEvents="none"
        style={[StyleSheet.absoluteFillObject, styles.greenGlowWrap]}
      >
        <View style={styles.greenGlow} />
      </View>

      <TopChrome
        progress={5}
        total={6}
        onBack={onBack}
        showSkip={false}
      />

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={[
          styles.content,
          { paddingTop: insets.top + 116, paddingBottom: insets.bottom + 30 },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.iconWrap}>
          <View style={styles.iconHalo} />
          <LinearGradient
            colors={['#5DEB8C', SUCCESS_GREEN, '#1E9A43']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.iconCircle}
          >
            <Svg width={48} height={48} viewBox="0 0 48 48">
              <Path
                d="M12 24l8 8 16-18"
                stroke="#fff"
                strokeWidth={4}
                strokeLinecap="round"
                strokeLinejoin="round"
                fill="none"
              />
            </Svg>
          </LinearGradient>
        </View>

        <Text style={styles.title}>transfer{'\n'}complete.</Text>
        <Text style={styles.subtitle}>
          Your money is on its way. The recipient will see it in seconds.
        </Text>

        <Text style={styles.refText}>Reference: BUNQ-OK-5821</Text>

        <View style={styles.spacer} />

        <View style={styles.doneShadow}>
          <TouchableOpacity
            onPress={onDismiss}
            activeOpacity={0.85}
            style={styles.doneBtn}
          >
            <Text style={styles.doneText}>Done</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          onPress={onBack}
          activeOpacity={0.6}
          style={styles.receiptBtn}
        >
          <Text style={styles.receiptText}>View receipt</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: BG_PURPLE,
    overflow: 'hidden',
  },
  greenGlowWrap: {
    zIndex: 2,
    alignItems: 'center',
  },
  greenGlow: {
    position: 'absolute',
    top: 100,
    width: 360,
    height: 360,
    borderRadius: 180,
    backgroundColor: SUCCESS_GREEN_GLOW,
    opacity: 0.6,
    transform: [{ scale: 1.4 }],
  },
  scroll: {
    ...StyleSheet.absoluteFillObject,
    zIndex: 5,
  },
  content: {
    paddingHorizontal: 28,
    flexGrow: 1,
  },
  iconWrap: {
    alignSelf: 'center',
    marginTop: 8,
    width: 96,
    height: 96,
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconHalo: {
    position: 'absolute',
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: SUCCESS_GREEN,
    opacity: 0.25,
  },
  iconCircle: {
    width: 96,
    height: 96,
    borderRadius: 48,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: SUCCESS_GREEN,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.6,
    shadowRadius: 24,
    elevation: 10,
  },
  title: {
    marginTop: 24,
    fontSize: 40,
    fontWeight: '800',
    lineHeight: 42,
    letterSpacing: -1.6,
    color: '#fff',
    textAlign: 'center',
  },
  subtitle: {
    marginTop: 12,
    fontSize: 16,
    color: 'rgba(255,255,255,0.7)',
    lineHeight: 22,
    textAlign: 'center',
  },
  card: {
    marginTop: 22,
    backgroundColor: 'rgba(255,255,255,0.04)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 18,
    paddingHorizontal: 18,
    paddingVertical: 16,
  },
  cardCallout: {
    borderColor: 'rgba(30,155,255,0.35)',
    backgroundColor: 'rgba(30,155,255,0.06)',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  cardIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: 'rgba(48,209,88,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardIconBlue: {
    backgroundColor: 'rgba(30,155,255,0.18)',
  },
  cardEmoji: {
    fontSize: 14,
  },
  cardLabel: {
    fontSize: 11,
    letterSpacing: 1.4,
    fontWeight: '700',
    color: 'rgba(255,255,255,0.7)',
  },
  cardLabelBlue: {
    color: ACCENT_BLUE,
  },
  cardBody: {
    marginTop: 10,
    fontSize: 14,
    color: 'rgba(255,255,255,0.85)',
    lineHeight: 21,
  },
  hintRow: {
    marginTop: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingTop: 12,
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: 'rgba(30,155,255,0.25)',
  },
  hintDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: ACCENT_BLUE,
  },
  hintText: {
    flex: 1,
    fontSize: 12,
    color: 'rgba(255,255,255,0.6)',
    lineHeight: 16,
  },
  refText: {
    marginTop: 16,
    fontSize: 12,
    color: 'rgba(255,255,255,0.45)',
    letterSpacing: 0.5,
    textAlign: 'center',
  },
  spacer: {
    flex: 1,
    minHeight: 24,
  },
  doneShadow: {
    marginTop: 24,
    shadowColor: SUCCESS_GREEN,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 14,
    elevation: 6,
    borderRadius: 28,
  },
  doneBtn: {
    width: '100%',
    height: 56,
    borderRadius: 28,
    backgroundColor: SUCCESS_GREEN,
    justifyContent: 'center',
    alignItems: 'center',
  },
  doneText: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
    letterSpacing: -0.2,
  },
  receiptBtn: {
    marginTop: 12,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  receiptText: {
    color: ACCENT_BLUE,
    fontSize: 15,
    fontWeight: '500',
  },
});
