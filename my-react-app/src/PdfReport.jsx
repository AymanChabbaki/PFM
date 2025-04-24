import React from 'react';
import { Page, Text, View, Document, StyleSheet, PDFDownloadLink } from '@react-pdf/renderer';

const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    padding: 40,
  },
  header: {
    marginBottom: 20,
    textAlign: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#7f8c8d',
  },
  section: {
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
    borderBottom: '1px solid #eee',
    paddingBottom: 5,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5,
  },
  label: {
    fontSize: 12,
    color: '#7f8c8d',
    width: '40%',
  },
  value: {
    fontSize: 12,
    color: '#2c3e50',
    width: '60%',
    fontWeight: 'bold',
  },
  price: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#27ae60',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 30,
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 0,
    right: 0,
    textAlign: 'center',
    fontSize: 10,
    color: '#95a5a6',
  },
});

const PdfReport = ({ prediction, formData }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <View style={styles.header}>
        <Text style={styles.title}>Rapport d'Estimation Automobile</Text>
        <Text style={styles.subtitle}>Votre estimation personnalisée</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Détails du Véhicule</Text>
        <View style={styles.row}>
          <Text style={styles.label}>Marque:</Text>
          <Text style={styles.value}>{formData.marque}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Modèle:</Text>
          <Text style={styles.value}>{formData.modele}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Année:</Text>
          <Text style={styles.value}>{formData.annee}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Transmission:</Text>
          <Text style={styles.value}>{formData.transmission}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Carburant:</Text>
          <Text style={styles.value}>{formData.carburant}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Kilométrage:</Text>
          <Text style={styles.value}>{formData.kilometrage} km</Text>
        </View>
      </View>

      <View style={styles.price}>
        <Text>Prix Estimé: {prediction} MAD</Text>
      </View>

      <View style={styles.footer}>
        <Text>Généré on - {new Date().toLocaleDateString()}</Text>
      </View>
    </Page>
  </Document>
);

export default PdfReport;