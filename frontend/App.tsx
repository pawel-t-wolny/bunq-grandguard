import React, { useState } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { NameScreen } from './src/screens/NameScreen';
import { PhoneScreen } from './src/screens/PhoneScreen';
import { ContactScreen } from './src/screens/ContactScreen';
import { TransferScreen } from './src/screens/TransferScreen';
import { BlockedScreen } from './src/screens/BlockedScreen';
import { TransferLegitScreen } from './src/screens/TransferLegitScreen';
import { ApprovedScreen } from './src/screens/ApprovedScreen';

type Step =
  | 'name'
  | 'phone'
  | 'contact'
  | 'transfer'
  | 'blocked'
  | 'transferLegit'
  | 'approved';

export default function App() {
  const [step, setStep] = useState<Step>('name');

  return (
    <SafeAreaProvider>
      <StatusBar style="light" hidden />
      {step === 'name' && (
        <NameScreen
          onContinue={() => setStep('phone')}
          onSkip={() => setStep('phone')}
        />
      )}
      {step === 'phone' && (
        <PhoneScreen
          onBack={() => setStep('name')}
          onContinue={() => setStep('contact')}
          onSkip={() => setStep('contact')}
        />
      )}
      {step === 'contact' && (
        <ContactScreen
          onBack={() => setStep('phone')}
          onContinue={() => setStep('transfer')}
        />
      )}
      {step === 'transfer' && (
        <TransferScreen
          onBack={() => setStep('contact')}
          onBlocked={() => setStep('blocked')}
        />
      )}
      {step === 'blocked' && (
        <BlockedScreen
          onBack={() => setStep('transfer')}
          onDismiss={() => setStep('transferLegit')}
        />
      )}
      {step === 'transferLegit' && (
        <TransferLegitScreen
          onBack={() => setStep('blocked')}
          onApproved={() => setStep('approved')}
          onBlocked={() => setStep('blocked')}
        />
      )}
      {step === 'approved' && (
        <ApprovedScreen
          onBack={() => setStep('transferLegit')}
          onDismiss={() => setStep('transferLegit')}
        />
      )}
    </SafeAreaProvider>
  );
}
