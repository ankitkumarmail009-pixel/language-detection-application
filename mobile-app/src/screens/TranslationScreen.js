import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import {
  TextInput,
  Button,
  Card,
  Text,
  ActivityIndicator,
  Snackbar,
  SegmentedButtons,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { translateText, getSupportedLanguages } from '../services/api';
import { saveToHistory } from '../utils/history';
import { theme } from '../theme/theme';

const TranslationScreen = () => {
  const [text, setText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showError, setShowError] = useState(false);
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('en');
  const [languages, setLanguages] = useState([]);
  const [loadingLanguages, setLoadingLanguages] = useState(true);

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    const response = await getSupportedLanguages();
    if (response.success) {
      const langList = response.data.translation_languages || [];
      setLanguages(langList);
    }
    setLoadingLanguages(false);
  };

  const handleTranslate = async () => {
    if (!text.trim()) {
      setError('Please enter some text to translate');
      setShowError(true);
      return;
    }

    setLoading(true);
    setTranslatedText('');
    setError('');

    const response = await translateText(text, sourceLang, targetLang);

    if (response.success) {
      setTranslatedText(response.data.translated_text);
      // Save to history
      saveToHistory({
        type: 'translation',
        text: text.substring(0, 100),
        translatedText: response.data.translated_text.substring(0, 100),
        sourceLang: response.data.source_language || 'auto',
        targetLang: response.data.target_language,
        timestamp: new Date().toISOString(),
      });
    } else {
      setError(response.error || 'Translation failed');
      setShowError(true);
    }

    setLoading(false);
  };

  const getLanguageCode = (langName) => {
    // Simple mapping - in production, use the full mapping from API
    const langMap = {
      'English': 'en',
      'French': 'fr',
      'Spanish': 'es',
      'German': 'de',
      'Italian': 'it',
      'Portuguese': 'pt',
      'Russian': 'ru',
      'Japanese': 'ja',
      'Chinese': 'zh',
      'Korean': 'ko',
      'Arabic': 'ar',
      'Hindi': 'hi',
    };
    return langMap[langName] || langName.toLowerCase().substring(0, 2);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#f093fb', '#f5576c']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>🌐 Translator</Text>
        <Text style={styles.headerSubtitle}>Translate text between languages</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        {/* Source Language Selection */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Source Language</Text>
            <SegmentedButtons
              value={sourceLang}
              onValueChange={setSourceLang}
              buttons={[
                { value: 'auto', label: 'Auto-detect' },
                { value: 'manual', label: 'Manual' },
              ]}
              style={styles.segmentedButtons}
            />
            {sourceLang === 'manual' && (
              <Text style={styles.note}>
                Manual selection coming soon. Currently using auto-detect.
              </Text>
            )}
          </Card.Content>
        </Card>

        {/* Target Language Selection */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Target Language</Text>
            {loadingLanguages ? (
              <ActivityIndicator />
            ) : (
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                {['English', 'French', 'Spanish', 'German', 'Italian', 'Portuguese', 'Russian', 'Japanese', 'Chinese', 'Korean', 'Arabic', 'Hindi'].map((lang) => (
                  <Button
                    key={lang}
                    mode={targetLang === getLanguageCode(lang) ? 'contained' : 'outlined'}
                    onPress={() => setTargetLang(getLanguageCode(lang))}
                    style={styles.langButton}
                    compact
                  >
                    {lang}
                  </Button>
                ))}
              </ScrollView>
            )}
          </Card.Content>
        </Card>

        {/* Text Input */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Enter Text to Translate</Text>
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

        {/* Translate Button */}
        <Button
          mode="contained"
          onPress={handleTranslate}
          loading={loading}
          disabled={loading || !text.trim()}
          style={styles.translateButton}
          contentStyle={styles.buttonContent}
          labelStyle={styles.buttonLabel}
        >
          {loading ? 'Translating...' : '🌐 Translate'}
        </Button>

        {/* Translation Result */}
        {translatedText && (
          <Card style={[styles.card, styles.resultCard]}>
            <Card.Content>
              <Text style={styles.resultTitle}>Translation</Text>
              <View style={styles.translatedContainer}>
                <Text style={styles.translatedText}>{translatedText}</Text>
              </View>
            </Card.Content>
          </Card>
        )}

        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={theme.colors.primary} />
            <Text style={styles.loadingText}>Translating...</Text>
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
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 12,
  },
  segmentedButtons: {
    marginTop: 8,
  },
  note: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginTop: 8,
    fontStyle: 'italic',
  },
  langButton: {
    marginRight: 8,
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
  translateButton: {
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
  translatedContainer: {
    backgroundColor: '#f0f5ff',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.colors.primary,
  },
  translatedText: {
    fontSize: 16,
    color: theme.colors.text,
    lineHeight: 24,
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
});

export default TranslationScreen;

