import React, { useRef, useState } from 'react';
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

export function NameScreen({ onBack, onContinue, onSkip }: Props) {
  const insets = useSafeAreaInsets();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const lastRef = useRef<TextInput>(null);

  const canContinue = firstName.trim().length > 0 && lastName.trim().length > 0;

  return (
    <View style={styles.root}>
      <RainbowBlob opacity={0.35} />
      <PurpleWash />
      <TopChrome
        progress={1}
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
        <Text style={styles.title}>nice to meet you.</Text>
        <Text style={styles.subtitle}>
          Enter your full legal name. This stays private and only shows on
          your account.
        </Text>

        <View style={styles.cards}>
          <View style={styles.card}>
            <Text style={styles.label}>FIRST NAME</Text>
            <TextInput
              style={styles.input}
              value={firstName}
              onChangeText={setFirstName}
              autoCapitalize="words"
              autoCorrect={false}
              returnKeyType="next"
              onSubmitEditing={() => lastRef.current?.focus()}
              selectionColor={ACCENT_BLUE}
            />
          </View>

          <View style={styles.card}>
            <Text style={styles.label}>LAST NAME</Text>
            <TextInput
              ref={lastRef}
              style={styles.input}
              value={lastName}
              onChangeText={setLastName}
              autoCapitalize="words"
              autoCorrect={false}
              returnKeyType="done"
              onSubmitEditing={() => canContinue && onContinue?.()}
              selectionColor={ACCENT_BLUE}
            />
          </View>

          <View style={styles.reassurance}>
            <Svg width={14} height={14} viewBox="0 0 14 14">
              <Path
                d="M7 1C4 1 2 3 2 6v2H1v5h12V8h-1V6c0-3-2-5-5-5z"
                stroke="rgba(255,255,255,0.5)"
                strokeWidth={1.2}
                fill="none"
              />
            </Svg>
            <Text style={styles.reassuranceText}>
              Encrypted end-to-end. Only you and bunq can see this.
            </Text>
          </View>
        </View>

        <View style={styles.spacer} />

        <PrimaryCTA onPress={onContinue} disabled={!canContinue}>
          Continue
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
  cards: {
    marginTop: 36,
    gap: 14,
  },
  card: {
    backgroundColor: 'rgba(255,255,255,0.06)',
    borderWidth: 1.5,
    borderColor: 'rgba(255,255,255,0.18)',
    borderRadius: 18,
    paddingHorizontal: 18,
    paddingVertical: 14,
  },
  label: {
    fontSize: 11,
    letterSpacing: 1.4,
    color: 'rgba(255,255,255,0.5)',
    fontWeight: '600',
  },
  input: {
    fontSize: 20,
    fontWeight: '500',
    marginTop: 4,
    color: '#fff',
    padding: 0,
    minHeight: 28,
  },
  reassurance: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 4,
  },
  reassuranceText: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.55)',
  },
  spacer: {
    flex: 1,
  },
});
