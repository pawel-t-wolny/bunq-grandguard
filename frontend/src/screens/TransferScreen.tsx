import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import Svg, { Path } from 'react-native-svg';
import { RainbowBlob } from '../components/RainbowBlob';
import { TopChrome } from '../components/TopChrome';
import { PurpleWash } from '../components/PurpleWash';
import { ACCENT_BLUE, BG_PURPLE } from '../constants/colors';
import { checkPaymentForScam } from '../api/fraud';
import { triggerFraudSpecialistCall } from '../api/elevenlabs';

interface Props {
  onBack?: () => void;
  onBlocked?: () => void;
}

const RECIPIENT_NAME = 'Microsoft Tech Support';
const RECIPIENT_IBAN = 'NL45 BUNQ 9420 6913 84';
const AMOUNT_EUROS = '10.000';
const AMOUNT_CENTS = '00';

export function TransferScreen({ onBack, onBlocked }: Props) {
  const insets = useSafeAreaInsets();
  const [processing, setProcessing] = useState(false);
  const cancelled = useRef(false);

  useEffect(() => {
    cancelled.current = false;
    return () => {
      cancelled.current = true;
    };
  }, []);

  const handleTransfer = async () => {
    if (processing) return;
    setProcessing(true);
    try {
      const [result] = await Promise.all([
        checkPaymentForScam(),
        new Promise<void>(resolve => setTimeout(resolve, 1000)),
      ]);
      if (cancelled.current) return;
      if (result.is_scam) {
        triggerFraudSpecialistCall();
        onBlocked?.();
      } else {
        Alert.alert(
          'Transfer sent',
          `€10.000,00 has been sent to ${RECIPIENT_NAME}.`,
        );
      }
    } catch (err) {
      if (cancelled.current) return;
      Alert.alert(
        'Transfer failed',
        err instanceof Error ? err.message : 'Unknown error',
      );
    } finally {
      if (!cancelled.current) setProcessing(false);
    }
  };

  return (
    <View style={styles.root}>
      <RainbowBlob opacity={0.3} />
      <PurpleWash />
      <TopChrome
        progress={4}
        total={6}
        onBack={processing ? undefined : onBack}
        showSkip={false}
      />

      <View
        style={[
          styles.content,
          { paddingTop: insets.top + 116, paddingBottom: insets.bottom + 30 },
        ]}
      >
        <Text style={styles.title}>send transfer.</Text>
        <Text style={styles.subtitle}>
          Review the details below before confirming.
        </Text>

        <View style={styles.recipientCard}>
          <LinearGradient
            colors={['#C33534', '#E4553E', '#F1B12B']}
            locations={[0, 0.5, 1]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.avatar}
          >
            <Text style={styles.avatarLetter}>M</Text>
          </LinearGradient>
          <View style={styles.recipientInfo}>
            <Text style={styles.recipientLabel}>RECIPIENT</Text>
            <Text style={styles.recipientName}>{RECIPIENT_NAME}</Text>
            <Text style={styles.recipientIban}>{RECIPIENT_IBAN}</Text>
          </View>
        </View>

        <View style={styles.amountBlock}>
          <Text style={styles.amountLabel}>AMOUNT</Text>
          <View style={styles.amountRow}>
            <Text style={styles.amountCurrency}>€</Text>
            <Text style={styles.amountWhole}>{AMOUNT_EUROS}</Text>
            <Text style={styles.amountCents}>,{AMOUNT_CENTS}</Text>
          </View>
        </View>

        <View style={styles.memoCard}>
          <Text style={styles.memoIcon}>📝</Text>
          <Text style={styles.memoText}>Add a note (optional)</Text>
        </View>

        <View style={styles.spacer} />

        <View style={styles.feeRow}>
          <Text style={styles.feeLabel}>Transfer fee</Text>
          <Text style={styles.feeValue}>Free</Text>
        </View>
        <View style={styles.feeDivider} />
        <View style={styles.feeRow}>
          <Text style={styles.totalLabel}>Total</Text>
          <Text style={styles.totalValue}>€10.000,00</Text>
        </View>

        <View style={styles.ctaWrap}>
          <TouchableOpacity
            disabled={processing}
            onPress={handleTransfer}
            activeOpacity={0.85}
            style={[
              styles.cta,
              processing && styles.ctaProcessing,
            ]}
          >
            {processing ? (
              <View style={styles.ctaInner}>
                <ActivityIndicator color="#fff" size="small" />
                <Text style={styles.ctaLabel}>Processing…</Text>
              </View>
            ) : (
              <View style={styles.ctaInner}>
                <Text style={styles.ctaLabel}>Transfer</Text>
                <Svg width={16} height={14} viewBox="0 0 16 14">
                  <Path
                    d="M9 1l6 6-6 6M1 7h14"
                    stroke="#fff"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    fill="none"
                  />
                </Svg>
              </View>
            )}
          </TouchableOpacity>
        </View>
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
  recipientCard: {
    marginTop: 28,
    backgroundColor: 'rgba(255,255,255,0.06)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    borderRadius: 22,
    padding: 18,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarLetter: {
    fontSize: 26,
    fontWeight: '800',
    color: '#fff',
    letterSpacing: -1.5,
  },
  recipientInfo: {
    flex: 1,
  },
  recipientLabel: {
    fontSize: 11,
    letterSpacing: 1.4,
    color: 'rgba(255,255,255,0.5)',
    fontWeight: '600',
  },
  recipientName: {
    marginTop: 2,
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  recipientIban: {
    marginTop: 2,
    fontSize: 13,
    color: 'rgba(255,255,255,0.6)',
    letterSpacing: 0.5,
  },
  amountBlock: {
    marginTop: 24,
    paddingHorizontal: 4,
  },
  amountLabel: {
    fontSize: 11,
    letterSpacing: 1.4,
    color: 'rgba(255,255,255,0.5)',
    fontWeight: '600',
  },
  amountRow: {
    marginTop: 6,
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  amountCurrency: {
    fontSize: 36,
    fontWeight: '600',
    color: 'rgba(255,255,255,0.85)',
    marginRight: 4,
  },
  amountWhole: {
    fontSize: 56,
    fontWeight: '800',
    color: '#fff',
    letterSpacing: -2,
    lineHeight: 60,
  },
  amountCents: {
    fontSize: 36,
    fontWeight: '700',
    color: 'rgba(255,255,255,0.6)',
    marginLeft: 2,
  },
  memoCard: {
    marginTop: 20,
    backgroundColor: 'rgba(255,255,255,0.04)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.08)',
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  memoIcon: {
    fontSize: 18,
  },
  memoText: {
    color: 'rgba(255,255,255,0.55)',
    fontSize: 15,
  },
  spacer: {
    flex: 1,
  },
  feeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    paddingHorizontal: 4,
  },
  feeLabel: {
    color: 'rgba(255,255,255,0.55)',
    fontSize: 14,
  },
  feeValue: {
    color: 'rgba(255,255,255,0.85)',
    fontSize: 14,
    fontWeight: '500',
  },
  feeDivider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: 'rgba(255,255,255,0.12)',
    marginHorizontal: 4,
  },
  totalLabel: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
  totalValue: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
  ctaWrap: {
    marginTop: 16,
    shadowColor: ACCENT_BLUE,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.35,
    shadowRadius: 12,
    elevation: 6,
    borderRadius: 28,
  },
  cta: {
    width: '100%',
    height: 56,
    borderRadius: 28,
    backgroundColor: ACCENT_BLUE,
    justifyContent: 'center',
    alignItems: 'center',
  },
  ctaProcessing: {
    backgroundColor: 'rgba(30,155,255,0.45)',
  },
  ctaInner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  ctaLabel: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
    letterSpacing: -0.2,
  },
});
