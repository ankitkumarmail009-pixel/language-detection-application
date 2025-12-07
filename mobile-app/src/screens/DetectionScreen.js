import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Text,
  ProgressBar,
  Chip,
  ActivityIndicator,
  Snackbar,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { detectLanguage } from '../services/api';
import { saveToHistory } from '../utils/history';
import { theme } from '../theme/theme';

const DetectionScreen = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showError, setShowError] = useState(false);

  const exampleTexts = [
    { lang: 'English', text: "Hello, how are you today? I hope you're doing well." },
    { lang: 'French', text: "Bonjour, comment allez-vous? J'espère que vous allez bien." },
    { lang: 'Spanish', text: 'Hola, ¿cómo estás? Espero que estés bien.' },
    { lang: 'German', text: 'Guten Tag, wie geht es dir? Ich hoffe, es geht dir gut.' },
    { lang: 'Italian', text: "Ciao, come stai? Spero che tu stia bene." },
  ];

  const handleDetect = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      setShowError(true);
      return;
    }

    if (text.trim().length < 3) {
      setError('Text should be at least 3 characters long');
      setShowError(true);
      return;
    }

    setLoading(true);
    setResult(null);
    setError('');

    const response = await detectLanguage(text);

    if (response.success) {
      setResult(response.data);
      // Save to history
      saveToHistory({
        type: 'detection',
        text: text.substring(0, 100),
        language: response.data.language,
        confidence: response.data.confidence,
        timestamp: new Date().toISOString(),
      });
    } else {
      setError(response.error);
      setShowError(true);
    }

    setLoading(false);
  };

  const handleExamplePress = (exampleText) => {
    setText(exampleText);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return theme.colors.success;
    if (confidence >= 0.5) return theme.colors.warning;
    return theme.colors.error;
  };

  const getTopLanguages = () => {
    if (!result || !result.probabilities) return [];
    return Object.entries(result.probabilities)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#6366f1', '#818cf8', '#a5b4fc']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>🌐 Language Detector</Text>
        <Text style={styles.headerSubtitle}>Detect the language of any text</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        {/* Example Texts */}
        <View style={styles.examplesContainer}>
          <Text style={styles.sectionTitle}>Quick Examples</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {exampleTexts.map((example, index) => (
              <Chip
                key={index}
                mode="outlined"
                onPress={() => handleExamplePress(example.text)}
                style={styles.exampleChip}
                textStyle={styles.exampleChipText}
              >
                {example.lang}
              </Chip>
            ))}
          </ScrollView>
        </View>

        {/* Text Input */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Enter Text</Text>
            <TextInput
              mode="outlined"
              multiline
              numberOfLines={6}
              value={text}
              onChangeText={setText}
              placeholder="Type or paste text here..."
              style={styles.textInput}
              disabled={loading}
            />
            <View style={styles.statsContainer}>
              <Text style={styles.statsText}>
                {text.length} characters • {text.split(/\s+/).filter(Boolean).length} words
              </Text>
            </View>
          </Card.Content>
        </Card>

        {/* Detect Button */}
        <Button
          mode="contained"
          onPress={handleDetect}
          loading={loading}
          disabled={loading || !text.trim()}
          style={styles.detectButton}
          contentStyle={styles.buttonContent}
          labelStyle={styles.buttonLabel}
        >
          {loading ? 'Detecting...' : '🔍 Detect Language'}
        </Button>

        {/* Results */}
        {result && (
          <Card style={[styles.card, styles.resultCard]}>
            <Card.Content>
              <Text style={styles.resultTitle}>Detection Result</Text>

              {/* Main Result */}
              <View style={styles.mainResult}>
                <Text style={styles.languageName}>{result.language}</Text>
                <Text style={styles.confidenceLabel}>Confidence</Text>
                <View style={styles.confidenceContainer}>
                  <ProgressBar
                    progress={result.confidence}
                    color={getConfidenceColor(result.confidence)}
                    style={styles.progressBar}
                  />
                  <Text
                    style={[
                      styles.confidenceValue,
                      { color: getConfidenceColor(result.confidence) },
                    ]}
                  >
                    {(result.confidence * 100).toFixed(1)}%
                  </Text>
                </View>
              </View>

              {/* Warning */}
              {result.warning && (
                <View style={styles.warningContainer}>
                  <Text style={styles.warningText}>⚠️ {result.warning}</Text>
                </View>
              )}

              {/* Top Languages */}
              {result.probabilities && (
                <View style={styles.topLanguagesContainer}>
                  <Text style={styles.sectionTitle}>Top 5 Languages</Text>
                  {getTopLanguages().map(([lang, prob], index) => (
                    <View key={index} style={styles.languageItem}>
                      <View style={styles.languageItemHeader}>
                        <Text style={styles.languageItemName}>
                          {index + 1}. {lang}
                        </Text>
                        <Text style={styles.languageItemProb}>
                          {(prob * 100).toFixed(1)}%
                        </Text>
                      </View>
                      <ProgressBar
                        progress={prob}
                        color={theme.colors.primary}
                        style={styles.languageProgressBar}
                      />
                    </View>
                  ))}
                </View>
              )}
            </Card.Content>
          </Card>
        )}

        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={theme.colors.primary} />
            <Text style={styles.loadingText}>Analyzing text...</Text>
          </View>
        )}
      </ScrollView>

      <Snackbar
        visible={showError}
        onDismiss={() => setShowError(false)}
        duration={3000}
        style={styles.snackbar}
      >
        {error}
      </Snackbar>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#ffffff',
    textAlign: 'center',
    opacity: 0.9,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 16,
    paddingBottom: 32,
  },
  examplesContainer: {
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 12,
  },
  exampleChip: {
    marginRight: 8,
    borderColor: theme.colors.primary,
  },
  exampleChipText: {
    fontSize: 12,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  textInput: {
    marginTop: 8,
    backgroundColor: theme.colors.surface,
  },
  statsContainer: {
    marginTop: 8,
    alignItems: 'flex-end',
  },
  statsText: {
    fontSize: 12,
    color: theme.colors.placeholder,
  },
  detectButton: {
    marginBottom: 16,
    borderRadius: 12,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  buttonLabel: {
    fontSize: 16,
    fontWeight: '600',
  },
  resultCard: {
    backgroundColor: theme.colors.surface,
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: 16,
    textAlign: 'center',
  },
  mainResult: {
    alignItems: 'center',
    marginBottom: 20,
  },
  languageName: {
    fontSize: 32,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 12,
  },
  confidenceLabel: {
    fontSize: 14,
    color: theme.colors.placeholder,
    marginBottom: 8,
  },
  confidenceContainer: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  progressBar: {
    flex: 1,
    height: 12,
    borderRadius: 6,
  },
  confidenceValue: {
    fontSize: 18,
    fontWeight: 'bold',
    minWidth: 60,
    textAlign: 'right',
  },
  warningContainer: {
    backgroundColor: '#fef3c7',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  warningText: {
    fontSize: 14,
    color: '#92400e',
  },
  topLanguagesContainer: {
    marginTop: 16,
  },
  languageItem: {
    marginBottom: 12,
  },
  languageItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  languageItemName: {
    fontSize: 14,
    fontWeight: '500',
    color: theme.colors.text,
  },
  languageItemProb: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.primary,
  },
  languageProgressBar: {
    height: 8,
    borderRadius: 4,
  },
  loadingContainer: {
    alignItems: 'center',
    marginTop: 20,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    color: theme.colors.placeholder,
  },
  snackbar: {
    backgroundColor: theme.colors.error,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 4,
  },
});

export default DetectionScreen;

