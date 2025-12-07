import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  FlatList,
} from 'react-native';
import {
  Card,
  Text,
  Button,
  Chip,
  Divider,
} from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';
import { getHistory, clearHistory } from '../utils/history';
import { theme } from '../theme/theme';

const HistoryScreen = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    const hist = await getHistory();
    setHistory(hist);
  };

  const handleClear = async () => {
    await clearHistory();
    setHistory([]);
  };

  const renderItem = ({ item, index }) => (
    <Card style={styles.historyCard}>
      <Card.Content>
        <View style={styles.historyHeader}>
          <Chip
            mode="flat"
            style={styles.typeChip}
            textStyle={styles.typeChipText}
          >
            {item.type === 'detection' ? '🔍 Detection' : '🌐 Translation'}
          </Chip>
          <Text style={styles.timestamp}>
            {new Date(item.timestamp).toLocaleString()}
          </Text>
        </View>

        <Text style={styles.historyText} numberOfLines={2}>
          {item.text}
        </Text>

        {item.type === 'detection' ? (
          <View style={styles.detectionResult}>
            <Text style={styles.resultLabel}>Language:</Text>
            <Chip
              mode="outlined"
              style={styles.languageChip}
            >
              {item.language}
            </Chip>
            <Text style={styles.confidenceText}>
              {(item.confidence * 100).toFixed(1)}% confidence
            </Text>
          </View>
        ) : (
          <View style={styles.translationResult}>
            <Text style={styles.resultLabel}>Translated:</Text>
            <Text style={styles.translatedText} numberOfLines={2}>
              {item.translatedText}
            </Text>
            <View style={styles.langInfo}>
              <Text style={styles.langInfoText}>
                {item.sourceLang} → {item.targetLang}
              </Text>
            </View>
          </View>
        )}
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fa709a', '#fee140']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>📜 History</Text>
        <Text style={styles.headerSubtitle}>Your detection and translation history</Text>
      </LinearGradient>

      {history.length > 0 && (
        <View style={styles.clearButtonContainer}>
          <Button
            mode="outlined"
            onPress={handleClear}
            style={styles.clearButton}
          >
            Clear History
          </Button>
        </View>
      )}

      {history.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No history yet</Text>
          <Text style={styles.emptySubtext}>
            Your detection and translation history will appear here
          </Text>
        </View>
      ) : (
        <FlatList
          data={history}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          contentContainerStyle={styles.listContainer}
          ItemSeparatorComponent={() => <View style={styles.separator} />}
        />
      )}
    </View>
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
  clearButtonContainer: {
    padding: 16,
    alignItems: 'flex-end',
  },
  clearButton: {
    borderColor: theme.colors.error,
  },
  listContainer: {
    padding: 16,
    paddingBottom: 32,
  },
  historyCard: {
    marginBottom: 12,
    elevation: 2,
  },
  historyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  typeChip: {
    height: 28,
    backgroundColor: theme.colors.primary + '20',
  },
  typeChipText: {
    fontSize: 12,
    color: theme.colors.primary,
  },
  timestamp: {
    fontSize: 11,
    color: theme.colors.placeholder,
  },
  historyText: {
    fontSize: 14,
    color: theme.colors.text,
    marginBottom: 12,
    lineHeight: 20,
  },
  detectionResult: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: 8,
  },
  resultLabel: {
    fontSize: 12,
    color: theme.colors.placeholder,
    marginRight: 4,
  },
  languageChip: {
    height: 28,
  },
  confidenceText: {
    fontSize: 12,
    color: theme.colors.primary,
    fontWeight: '600',
    marginLeft: 'auto',
  },
  translationResult: {
    marginTop: 8,
  },
  translatedText: {
    fontSize: 14,
    color: theme.colors.text,
    fontStyle: 'italic',
    marginTop: 8,
    marginBottom: 8,
    lineHeight: 20,
  },
  langInfo: {
    marginTop: 4,
  },
  langInfoText: {
    fontSize: 12,
    color: theme.colors.primary,
    fontWeight: '500',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  emptyText: {
    fontSize: 20,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: theme.colors.placeholder,
    textAlign: 'center',
  },
  separator: {
    height: 8,
  },
});

export default HistoryScreen;

