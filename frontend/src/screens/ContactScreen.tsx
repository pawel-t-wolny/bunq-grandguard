import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Pressable,
  TouchableOpacity,
  ImageBackground,
  Alert,
  Linking,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import * as Contacts from 'expo-contacts';
import Svg, { Path, Circle } from 'react-native-svg';
import { TopChrome } from '../components/TopChrome';
import { PrimaryCTA } from '../components/PrimaryCTA';
import {
  ACCENT_BLUE,
  BG_PURPLE,
  IOS_BLUE,
  IOS_GREEN,
  SHEET_BG,
  SHEET_ROW,
} from '../constants/colors';

interface Props {
  onBack?: () => void;
  onContinue?: () => void;
}

const BUNQ_NAME = 'Bunq';
const BUNQ_PHONE = '+3197010253347';

const WHY_ITEMS: Array<[string, string]> = [
  ['🛡️', 'Texts stay out of spam'],
  ['📞', "You see when it's us calling"],
  ['🔒', "We'll never text a link"],
];

export function ContactScreen({ onBack, onContinue }: Props) {
  const insets = useSafeAreaInsets();
  const [sheetOpen, setSheetOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    if (saving) return;
    setSaving(true);
    try {
      const { status } = await Contacts.requestPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert(
          'Contacts access needed',
          'Enable contacts access in Settings to save Bunq.',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Open Settings', onPress: () => Linking.openSettings() },
          ],
        );
        return;
      }

      await Contacts.addContactAsync({
        [Contacts.Fields.ContactType]: Contacts.ContactTypes.Person,
        [Contacts.Fields.FirstName]: BUNQ_NAME,
        [Contacts.Fields.PhoneNumbers]: [
          {
            label: 'mobile',
            number: BUNQ_PHONE,
            isPrimary: true,
          },
        ],
      } as Contacts.Contact);

      setSheetOpen(false);
      setSaved(true);
    } catch (err) {
      Alert.alert(
        'Could not save contact',
        err instanceof Error ? err.message : 'Unknown error',
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <View style={styles.root}>
      <ImageBackground
        source={require('../../assets/bunq-splash.png')}
        resizeMode="cover"
        style={StyleSheet.absoluteFill}
      >
        <LinearGradient
          colors={[
            'rgba(7,6,11,0.92)',
            'rgba(7,6,11,0.4)',
            'rgba(7,6,11,0.55)',
            'rgba(7,6,11,0.92)',
          ]}
          locations={[0, 0.22, 0.6, 1]}
          style={StyleSheet.absoluteFill}
        />
      </ImageBackground>

      <TopChrome
        progress={3}
        total={6}
        onBack={onBack}
        showSkip={false}
      />

      <View
        style={[
          styles.content,
          { paddingTop: insets.top + 116, paddingBottom: insets.bottom + 30 },
        ]}
      >
        <Text style={styles.title}>save us to{'\n'}your contacts.</Text>
        <Text style={styles.subtitle}>
          So our texts don't get flagged as spam and our calls come through.
          Tap below and confirm on the next screen.
        </Text>

        <View style={styles.contactCard}>
          <BunqAvatar size={60} letterSize={26} />
          <View style={styles.contactInfo}>
            <Text style={styles.contactName}>{BUNQ_NAME}</Text>
            <Text style={styles.contactPhone}>{BUNQ_PHONE}</Text>
          </View>
          <View style={styles.plusBadge}>
            <Svg width={16} height={16} viewBox="0 0 16 16">
              <Path
                d="M8 3v10M3 8h10"
                stroke={ACCENT_BLUE}
                strokeWidth={2}
                strokeLinecap="round"
              />
            </Svg>
          </View>
        </View>

        <View style={styles.whyList}>
          {WHY_ITEMS.map(([emoji, text]) => (
            <View key={text} style={styles.whyRow}>
              <View style={styles.whyIcon}>
                <Text style={styles.whyEmoji}>{emoji}</Text>
              </View>
              <Text style={styles.whyText}>{text}</Text>
            </View>
          ))}
        </View>

        <View style={styles.spacer} />

        {saved ? (
          <View style={styles.savedRow}>
            <View style={styles.savedDot}>
              <Svg width={10} height={8} viewBox="0 0 10 8">
                <Path
                  d="M1 4l3 3 5-6"
                  stroke="#fff"
                  strokeWidth={1.8}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  fill="none"
                />
              </Svg>
            </View>
            <Text style={styles.savedText}>Saved to your contacts</Text>
          </View>
        ) : (
          <View style={styles.requiredRow}>
            <Svg width={12} height={12} viewBox="0 0 12 12">
              <Circle
                cx={6}
                cy={6}
                r={5}
                stroke="rgba(255,255,255,0.4)"
                strokeWidth={1}
                fill="none"
              />
              <Path
                d="M6 3v3.5M6 8.5v.01"
                stroke="rgba(255,255,255,0.5)"
                strokeWidth={1.2}
                strokeLinecap="round"
              />
            </Svg>
            <Text style={styles.requiredText}>Required to continue</Text>
          </View>
        )}

        {saved ? (
          <PrimaryCTA onPress={onContinue}>Continue to transfer</PrimaryCTA>
        ) : (
          <PrimaryCTA onPress={() => setSheetOpen(true)}>
            Add to Contacts
          </PrimaryCTA>
        )}
      </View>

      <NativeContactSheet
        visible={sheetOpen}
        saving={saving}
        onDismiss={() => setSheetOpen(false)}
        onDone={handleSave}
      />
    </View>
  );
}

function BunqAvatar({
  size,
  letterSize,
}: {
  size: number;
  letterSize: number;
}) {
  return (
    <LinearGradient
      colors={['#2FA84A', '#1887B8', '#C33534', '#F4D42A']}
      locations={[0, 0.4, 0.7, 1]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Text
        style={{
          fontSize: letterSize * 1.6,
          fontWeight: '800',
          color: '#fff',
          letterSpacing: -2,
          lineHeight: letterSize * 1.6,
        }}
      >
        B
      </Text>
    </LinearGradient>
  );
}

interface SheetProps {
  visible: boolean;
  saving: boolean;
  onDismiss: () => void;
  onDone: () => void;
}

function NativeContactSheet({ visible, saving, onDismiss, onDone }: SheetProps) {
  const slide = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.spring(slide, {
      toValue: visible ? 1 : 0,
      useNativeDriver: true,
      damping: 22,
      stiffness: 180,
      mass: 1,
    }).start();
  }, [visible, slide]);

  const translateY = slide.interpolate({
    inputRange: [0, 1],
    outputRange: [800, 0],
  });

  const overlayOpacity = slide.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 0.55],
  });

  return (
    <>
      <Animated.View
        pointerEvents={visible ? 'auto' : 'none'}
        style={[
          StyleSheet.absoluteFillObject,
          {
            zIndex: 10,
            backgroundColor: 'black',
            opacity: overlayOpacity,
          },
        ]}
      >
        <Pressable style={StyleSheet.absoluteFillObject} onPress={onDismiss} />
      </Animated.View>

      <Animated.View
        style={[styles.sheet, { transform: [{ translateY }] }]}
      >
        <View style={styles.sheetHeader}>
          <TouchableOpacity onPress={onDismiss} hitSlop={10} disabled={saving}>
            <Text style={styles.sheetCancel}>Cancel</Text>
          </TouchableOpacity>
          <Text style={styles.sheetTitle}>New Contact</Text>
          <TouchableOpacity onPress={onDone} hitSlop={10} disabled={saving}>
            <Text style={[styles.sheetDone, saving && styles.sheetDoneDisabled]}>
              {saving ? 'Saving…' : 'Done'}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.sheetAvatar}>
          <BunqAvatar size={100} letterSize={42} />
          <Text style={styles.addPhoto}>add photo</Text>
        </View>

        <View style={styles.sheetSection}>
          <View style={styles.sheetGroup}>
            <View style={styles.sheetRow}>
              <Text style={styles.sheetValue}>{BUNQ_NAME}</Text>
            </View>
            <View style={[styles.sheetRow, styles.sheetRowLast]}>
              <Text style={styles.sheetPlaceholder}>Last name</Text>
            </View>
          </View>
        </View>

        <View style={styles.sheetSection}>
          <View style={styles.sheetGroup}>
            <View style={styles.phoneRow}>
              <View style={styles.phoneIconBadge}>
                <Svg width={12} height={12} viewBox="0 0 14 14">
                  <Path
                    d="M4 2h2l1 3-2 1c.5 2 2 3.5 4 4l1-2 3 1v2c0 1-1 2-2 2C6 13 1 8 1 4c0-1 1-2 2-2z"
                    fill="#fff"
                  />
                </Svg>
              </View>
              <Text style={styles.phoneLabel}>mobile</Text>
              <Text style={styles.phoneNumber}>{BUNQ_PHONE}</Text>
            </View>
            <View style={[styles.addRow, styles.sheetRowLast]}>
              <PlusCircle />
              <Text style={styles.addText}>add phone</Text>
            </View>
          </View>
        </View>

        <View style={styles.sheetSection}>
          <View style={styles.sheetGroup}>
            <View style={styles.addRow}>
              <PlusCircle />
              <Text style={styles.addText}>add email</Text>
            </View>
          </View>
        </View>
      </Animated.View>
    </>
  );
}

function PlusCircle() {
  return (
    <View style={styles.plusCircle}>
      <Text style={styles.plusGlyph}>+</Text>
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
    flex: 1,
    paddingHorizontal: 28,
    zIndex: 5,
  },
  title: {
    fontSize: 52,
    fontWeight: '800',
    lineHeight: 50,
    letterSpacing: -2.2,
    color: '#fff',
  },
  subtitle: {
    marginTop: 18,
    fontSize: 16,
    color: 'rgba(255,255,255,0.75)',
    lineHeight: 23,
    maxWidth: 330,
  },
  contactCard: {
    marginTop: 36,
    backgroundColor: 'rgba(7,6,11,0.55)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.18)',
    borderRadius: 22,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  contactInfo: {
    flex: 1,
  },
  contactName: {
    fontSize: 20,
    fontWeight: '600',
    color: '#fff',
  },
  contactPhone: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
    marginTop: 2,
  },
  plusBadge: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(30,155,255,0.22)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  whyList: {
    marginTop: 20,
    gap: 14,
  },
  whyRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  whyIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: 'rgba(7,6,11,0.55)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  whyEmoji: {
    fontSize: 16,
  },
  whyText: {
    fontSize: 15,
    color: 'rgba(255,255,255,0.9)',
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  spacer: {
    flex: 1,
  },
  requiredRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginBottom: 12,
  },
  requiredText: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.65)',
  },
  savedRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginBottom: 12,
  },
  savedDot: {
    width: 18,
    height: 18,
    borderRadius: 9,
    backgroundColor: IOS_GREEN,
    justifyContent: 'center',
    alignItems: 'center',
  },
  savedText: {
    fontSize: 14,
    fontWeight: '600',
    color: IOS_GREEN,
  },
  sheet: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 20,
    backgroundColor: SHEET_BG,
    borderTopLeftRadius: 14,
    borderTopRightRadius: 14,
    paddingBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -10 },
    shadowOpacity: 0.5,
    shadowRadius: 40,
    elevation: 30,
  },
  sheetHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 18,
    paddingTop: 16,
    paddingBottom: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: 'rgba(84,84,88,0.6)',
  },
  sheetCancel: {
    color: IOS_BLUE,
    fontSize: 17,
  },
  sheetTitle: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '600',
  },
  sheetDone: {
    color: IOS_BLUE,
    fontSize: 17,
    fontWeight: '600',
  },
  sheetDoneDisabled: {
    opacity: 0.5,
  },
  sheetAvatar: {
    alignItems: 'center',
    paddingTop: 20,
    paddingBottom: 12,
  },
  addPhoto: {
    color: IOS_BLUE,
    fontSize: 15,
    marginTop: 10,
  },
  sheetSection: {
    paddingHorizontal: 16,
    marginTop: 16,
  },
  sheetGroup: {
    backgroundColor: SHEET_ROW,
    borderRadius: 10,
    overflow: 'hidden',
  },
  sheetRow: {
    paddingHorizontal: 16,
    paddingVertical: 11,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: 'rgba(84,84,88,0.6)',
  },
  sheetRowLast: {
    borderBottomWidth: 0,
  },
  sheetValue: {
    color: '#fff',
    fontSize: 17,
  },
  sheetPlaceholder: {
    color: 'rgba(235,235,245,0.3)',
    fontSize: 17,
  },
  phoneRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 11,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: 'rgba(84,84,88,0.6)',
  },
  phoneIconBadge: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: IOS_GREEN,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  phoneLabel: {
    flex: 1,
    color: '#fff',
    fontSize: 15,
  },
  phoneNumber: {
    color: '#fff',
    fontSize: 17,
  },
  addRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingHorizontal: 16,
    paddingVertical: 11,
  },
  addText: {
    color: IOS_BLUE,
    fontSize: 17,
  },
  plusCircle: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 1.5,
    borderColor: IOS_GREEN,
    justifyContent: 'center',
    alignItems: 'center',
  },
  plusGlyph: {
    color: IOS_GREEN,
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 18,
  },
});
