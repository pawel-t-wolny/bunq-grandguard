import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Path } from 'react-native-svg';
import { RainbowBlob } from '../components/RainbowBlob';
import { TopChrome } from '../components/TopChrome';
import { PrimaryCTA } from '../components/PrimaryCTA';
import { PurpleWash } from '../components/PurpleWash';
import { ACCENT_BLUE, BG_PURPLE } from '../constants/colors';

interface Props {
  onBack?: () => void;
  onContinue?: () => void;
  onSkip?: () => void;
}

const TRUST_ITEMS: Array<[string, string]> = [
  ['No spam', 'We never share your number.'],
  ['Code expires in 10 min', 'For your safety.'],
];

export function PhoneScreen({ onBack, onContinue, onSkip }: Props) {
  const insets = useSafeAreaInsets();
  const [phone, setPhone] = useState('');
  const canContinue = phone.trim().length >= 4;

  return (
    <View style={styles.root}>
      <RainbowBlob opacity={0.35} />
      <PurpleWash />
      <TopChrome
        progress={2}
        total={6}
        onBack={onBack}
        onSkip={onSkip}
        showSkip
      />

      <View
        style={[
          styles.content,
          { paddingTop: insets.top + 126, paddingBottom: insets.bottom + 30 },
        ]}
      >
            <Text style={styles.title}>what's your number?</Text>
            <Text style={styles.subtitle}>
              We text you a 6-digit code. Standard carrier rates apply.
            </Text>

            <View style={styles.inputPill}>
              <View style={styles.countryBlock}>
                <View style={styles.flag}>
                  <View style={[styles.flagStripe, { backgroundColor: '#AE1C28' }]} />
                  <View style={[styles.flagStripe, { backgroundColor: '#fff' }]} />
                  <View style={[styles.flagStripe, { backgroundColor: '#21468B' }]} />
                </View>
                <Text style={styles.country}>NL +31</Text>
                <Svg width={10} height={6} viewBox="0 0 10 6">
                  <Path
                    d="M1 1l4 4 4-4"
                    stroke="rgba(255,255,255,0.6)"
                    strokeWidth={1.5}
                    strokeLinecap="round"
                    fill="none"
                  />
                </Svg>
              </View>
              <TextInput
                style={styles.number}
                value={phone}
                onChangeText={setPhone}
                keyboardType="phone-pad"
                autoFocus
                returnKeyType="done"
                onSubmitEditing={() => canContinue && onContinue?.()}
                selectionColor={ACCENT_BLUE}
              />
            </View>

            <View style={styles.trustList}>
              {TRUST_ITEMS.map(([title, subtitle]) => (
                <View key={title} style={styles.trustCard}>
                  <View style={styles.trustIcon}>
                    <Svg width={12} height={10} viewBox="0 0 12 10">
                      <Path
                        d="M1 5l3 3L11 1"
                        stroke={ACCENT_BLUE}
                        strokeWidth={1.8}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        fill="none"
                      />
                    </Svg>
                  </View>
                  <View style={styles.trustTextWrap}>
                    <Text style={styles.trustTitle}>{title}</Text>
                    <Text style={styles.trustSubtitle}>{subtitle}</Text>
                  </View>
                </View>
              ))}
            </View>

            <View style={styles.spacer} />

        <PrimaryCTA onPress={onContinue} disabled={!canContinue}>
          Send code
        </PrimaryCTA>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: BG_PURPLE,
    overflow: 'hidden',
  },
  content: {
    ...StyleSheet.absoluteFillObject,
    flex: 1,
    paddingHorizontal: 28,
    zIndex: 5,
  },
  title: {
    fontSize: 34,
    fontWeight: '700',
    letterSpacing: -0.8,
    lineHeight: 37,
    color: '#fff',
  },
  subtitle: {
    marginTop: 12,
    fontSize: 16,
    color: 'rgba(255,255,255,0.6)',
    lineHeight: 23,
  },
  inputPill: {
    marginTop: 36,
    backgroundColor: 'rgba(255,255,255,0.06)',
    borderWidth: 1.5,
    borderColor: ACCENT_BLUE,
    borderRadius: 20,
    paddingHorizontal: 18,
    paddingVertical: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    shadowColor: ACCENT_BLUE,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.4,
    shadowRadius: 4,
    elevation: 3,
  },
  countryBlock: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingRight: 14,
    borderRightWidth: 1,
    borderRightColor: 'rgba(255,255,255,0.15)',
  },
  flag: {
    width: 26,
    height: 18,
    borderRadius: 2,
    overflow: 'hidden',
  },
  flagStripe: {
    flex: 1,
  },
  country: {
    fontSize: 18,
    fontWeight: '500',
    color: '#fff',
  },
  number: {
    flex: 1,
    fontSize: 22,
    fontWeight: '500',
    letterSpacing: 0.3,
    color: '#fff',
    padding: 0,
  },
  trustList: {
    marginTop: 20,
    gap: 10,
  },
  trustCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    backgroundColor: 'rgba(255,255,255,0.03)',
    borderRadius: 14,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  trustIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: 'rgba(30,155,255,0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  trustTextWrap: {
    flex: 1,
  },
  trustTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
  trustSubtitle: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.5)',
  },
  spacer: {
    flex: 1,
  },
});
