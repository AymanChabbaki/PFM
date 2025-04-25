import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './modern.css';
import { ArrowLeft } from "lucide-react";
import { PDFDownloadLink } from '@react-pdf/renderer';
import PdfReport from './PdfReport';
import { FaCar, FaGasPump, FaCogs, FaCalendarAlt, FaRoad, FaTachometerAlt, FaIndustry } from 'react-icons/fa';

const App = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    marque: '',
    modele: '',
    transmission: '',
    puissance_fiscale: '',
    carburant: '',
    kilometrage: '',
    annee: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [marques, setMarques] = useState([]);
  const [modeles, setModeles] = useState([]);
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    axios.get('https://flaskprediction.fly.dev/marques')
      .then(response => setMarques(response.data.marques))
      .catch(() => setMarques(['Renault', 'Peugeot', 'Citroën', 'Dacia', 'Volkswagen']));
  }, []);

  useEffect(() => {
    if (formData.marque) {
      axios.get(`https://flaskprediction.fly.dev/modeles?marque=${formData.marque}`)
        .then(response => {
          setModeles(response.data.modeles);
          if (formData.modele && !response.data.modeles.includes(formData.modele)) {
            setFormData(prev => ({ ...prev, modele: '' }));
          }
        })
        .catch(() => {
          setModeles([]);
          setFormData(prev => ({ ...prev, modele: '' }));
        });
    } else {
      setModeles([]);
      setFormData(prev => ({ ...prev, modele: '' }));
    }
  }, [formData.marque]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('https://flaskprediction.fly.dev/predict', formData);
      setPrediction(response.data.price);
      setShowResult(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors de la prédiction');
    }
    setLoading(false);
  };

  const resetForm = () => {
    setFormData({
      marque: '', modele: '', transmission: '', puissance_fiscale: '', carburant: '', kilometrage: '', annee: ''
    });
    setPrediction(null);
    setShowResult(false);
  };

  return (
    <div className={`modern-app ${darkMode ? 'dark' : 'light'}`}>
      {!showForm ? (
        <section className="intro-section">
          <img
            className="intro-image"
            src="https://cdn.pixabay.com/photo/2022/06/20/21/46/car-7274624_1280.jpg"
            alt="Luxury car"
            loading="eager"
          />
          <div className="intro-content">
            <h1 className="fade-in">Simulez le Prix de Votre Prochaine Voiture</h1>
            <p>Découvrez combien vaudra votre future voiture en quelques clics.</p>
            <button onClick={() => setShowForm(true)}>Estimer Mon Future Voiture Prix</button>
          </div>
          <div className="scroll-indicator">
            <svg style={{
              display: 'block',
              margin: '0 auto'
            }} width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 5v14M19 12l-7 7-7-7" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <footer className="fade-in web">
              Développé par : <br />
              Ayman Chabbaki - <a href="https://www.linkedin.com/in/ayman-chabbaki-10aa80281/">LinkedIn</a> | Afyf Badeddine - <a href="https://www.linkedin.com/in/afyf-badreddine-235a07284/">LinkedIn</a>
              </footer>
          </div>

        </section>
      ) : (
        <>
          <header className="modern-header fade-in">
            <div className="mode-toggle">
              <button onClick={() => setDarkMode(!darkMode)}>
                {darkMode ? '☀️ Light' : '🌙 Dark'}
              </button>
            </div>
            <h1>Estimez le Prix de Votre Future Voiture</h1>
          </header>

          <main className="modern-main fade-in">
            <section className="form-section">
              <form onSubmit={handleSubmit} className="styled-form">
                <button className="back-button" onClick={() => setShowForm(false)}> <ArrowLeft size={15} />Back</button>
                <div className="form-row">
                  <label><FaIndustry /> Marque</label>
                  <select name="marque" value={formData.marque} onChange={handleChange} required>
                    <option value="">Sélectionnez une marque</option>
                    {marques.map(marque => <option key={marque} value={marque}>{marque}</option>)}
                  </select>
                </div>
                <div className="form-row">
                  <label><FaTachometerAlt /> Modèle</label>
                  <select name="modele" value={formData.modele} onChange={handleChange} required disabled={!formData.marque}>
                    <option value="">Sélectionnez un modèle</option>
                    {modeles.map(modele => <option key={modele} value={modele}>{modele}</option>)}
                  </select>
                </div>
                <div className="form-row">
                  <label><FaCogs /> Transmission</label>
                  <select name="transmission" value={formData.transmission} onChange={handleChange} required>
                    <option value="">Sélectionnez une transmission</option>
                    <option value="Manuelle">Manuelle</option>
                    <option value="Automatique">Automatique</option>
                  </select>
                </div>
                <div className="form-row">
                  <label><FaCar /> Puissance Fiscale (CV)</label>
                  <input type="number" name="puissance_fiscale" value={formData.puissance_fiscale} onChange={handleChange} required />
                </div>
                <div className="form-row">
                  <label><FaGasPump /> Carburant</label>
                  <select name="carburant" value={formData.carburant} onChange={handleChange} required>
                    <option value="">Sélectionnez un carburant</option>
                    <option value="Essence">Essence</option>
                    <option value="Diesel">Diesel</option>
                    <option value="Hybride">Autres</option>
                  </select>
                </div>
                <div className="form-row">
                  <label><FaRoad /> Kilométrage</label>
                  <input type="number" name="kilometrage" value={formData.kilometrage} onChange={handleChange} required />
                </div>
                <div className="form-row">
                  <label><FaCalendarAlt /> Année</label>
                  <input type="number" name="annee" value={formData.annee} onChange={handleChange} required />
                </div>
                <div className="form-buttons">
                  <button type="submit" disabled={loading}>{loading ? 'Calcul en cours...' : 'Estimer le prix'}</button>
                  <button type="button" onClick={resetForm}>Réinitialiser</button>
                </div>
              </form>
              {showResult && (
                <div className="result-box pop-in">
                  <h2>Prix estimé: {prediction?.toLocaleString('fr-FR')} MAD</h2>
                  <ul>
                    <li>Marque: {formData.marque}</li>
                    <li>Modèle: {formData.modele}</li>
                    <li>Année: {formData.annee}</li>
                    <li>Transmission: {formData.transmission}</li>
                    <li>Carburant: {formData.carburant}</li>
                    <li>Kilométrage: {formData.kilometrage} km</li>
                  </ul>

                  <div className="pdf-download">
                    <PDFDownloadLink
                      document={<PdfReport prediction={prediction} formData={formData} />}
                      fileName={`estimation_${formData.marque}_${formData.modele}.pdf`}
                      className="pdf-button"
                    >
                      {({ loading }) => (
                        <>
                          {loading ? (
                            'Préparation du PDF...'
                          ) : (
                            <>
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="7 10 12 15 17 10"></polyline>
                                <line x1="12" y1="15" x2="12" y2="3"></line>
                              </svg>
                              Télécharger le Rapport
                            </>
                          )}
                        </>
                      )}
                    </PDFDownloadLink>
                  </div>
                </div>
              )}
            </section>
            <aside className="car-display fade-in">
              <div className="car-container">
                <img src="https://cdn.pixabay.com/photo/2021/11/28/00/27/car-6829156_1280.jpg" alt="3D Car" className="car-image" />
                <div className="car-description">
                  <h3>Votre Voiture de Rêve</h3>
                  <p>Visualisez votre véhicule estimé avec élégance et précision. Une expérience immersive dans le monde automobile moderne.</p>
                </div>
              </div>
            </aside>
          </main>
        </>
      )}
    </div>
  );
};

export default App;