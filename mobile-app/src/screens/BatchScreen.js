import React, { useState } from 'react';
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
  Chip,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { batchDetect } from '../services/api';
import { theme } from '../theme/theme';

const BatchScreen = () => {
  const [text, setText] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showError, setShowError] = useState(false);

  const handleBatchDetect = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      setShowError(true);
      return;
    }

    // Split by newlines
    const texts = text
      .split('\n')
      .map((t) => t.trim())
      .filter((t) => t.length > 0);

    if (texts.length === 0) {
      setError('Please enter at least one line of text');
      setShowError(true);
      return;
    }

    setLoading(true);
    setResults([]);
    setError('');

    const response = await batchDetect(texts);

    if (response.success) {
      setResults(response.data.results || []);
    } else {
      setError(response.error || 'Batch detection failed');
      setShowError(true);
    }

    setLoading(false);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return theme.colors.success;
    if (confidence >= 0.5) return theme.colors.warning;
    return theme.colors.error;
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#43e97b', '#38f9d7']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>📊 Batch Analysis</Text>
        <Text style={styles.headerSubtitle}>Analyze multiple texts at once</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Enter Texts (one per line)</Text>
            <TextInput
              mode="outlined"
              multiline
              numberOfLines={10}
              value={text}
              onChangeText={setText}
              placeholder="Enter multiple texts, one per line:&#10;&#10;Hello, how are you?&#10;Bonjour, comment allez-vous?&#10;Hola, ¿cómo estás?"
              style={styles.textInput}
              disabled={loading}
            />
            <View style={styles.statsContainer}>
              <Text style={styles.statsText}>
                {text.split('\n').filter((l) => l.trim()).length} lines
              </Text>
            </View>
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={handleBatchDetect}
          loading={loading}
          disabled={loading || !text.trim()}
          style={styles.analyzeButton}
          contentStyle={styles.buttonContent}
          labelStyle={styles.buttonLabel}
        >
          {loading ? 'Analyzing...' : '🔍 Analyze All'}
        </Button>

        {results.length > 0 && (
          <View style={styles.resultsContainer}>
            <Text style={styles.resultsTitle}>Results ({results.length})</Text>
            {results.map((result, index) => (
              <Card key={index} style={styles.resultCard}>
                <Card.Content>
                  <Text style={styles.resultText} numberOfLines={2}>
                    {result.text}
                  </Text>
                  <View style={styles.resultInfo}>
                    <Chip
                      mode="flat"
                      style={[
                        styles.languageChip,
                        { backgroundColor: getConfidenceColor(result.confidence) + '20' },
                      ]}
                      textStyle={{ color: getConfidenceColor(result.confidence) }}
                    >
                      {result.language}
                    </Chip>
                    <Text
                      style={[
                        styles.confidenceText,
                        { color: getConfidenceColor(result.confidence) },
                      ]}
                    >
                      {(result.confidence * 100).toFixed(1)}%
                    </Text>
                  </View>
                  {result.warning && (
                    <Text style={styles.warningText}>⚠️ {result.warning}</Text>
                  )}
                </Card.Content>
              </Card>
            ))}
          </View>
        )}

        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={theme.colors.primary} />
            <Text style={styles.loadingText}>Analyzing texts...</Text>
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
    marginBottom: 8,
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
  analyzeButton: {
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
  resultsContainer: {
    marginTop: 8,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: 16,
  },
  resultCard: {
    marginBottom: 12,
    elevation: 1,
  },
  resultText: {
    fontSize: 14,
    color: theme.colors.text,
    marginBottom: 12,
  },
  resultInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  languageChip: {
    height: 32,
  },
  confidenceText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  warningText: {
    fontSize: 12,
    color: theme.colors.warning,
    marginTop: 8,
    fontStyle: 'italic',
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

export default BatchScreen;

