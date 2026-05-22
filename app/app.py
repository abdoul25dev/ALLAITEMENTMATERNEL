import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(__file__))
from utils import save_history_to_local_storage, load_history_from_local_storage, clear_local_storage, convert_df_to_excel, preprocess_input

st.set_page_config(
    page_title="Système Prédictif AME - EDS Cameroun",
    page_icon="fas fa-hand-holding-medical",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    try:
        with open("app/styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

load_css()

@st.cache_resource
def load_model_and_cols():
    try:
        model = joblib.load('model/modele_ml_allaitement.joblib')
        model_cols = joblib.load('model/model_columns.joblib')
        return model, model_cols
    except Exception:
        model = joblib.load('../model/modele_ml_allaitement.joblib')
        model_cols = joblib.load('../model/model_columns.joblib')
        return model, model_cols

try:
    model, model_columns = load_model_and_cols()
except Exception as e:
    st.error("Erreur de chargement du modèle d'Intelligence Artificielle.")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = load_history_from_local_storage()
    if not isinstance(st.session_state.history, list):
        st.session_state.history = []

# --- HERO SECTION & DESCRIPTION ---
st.markdown("""
<div class="hero-container">
    <img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80" style="width:100%; height:300px; object-fit:cover; opacity: 0.8;" alt="Hero">
    <div class="hero-overlay">
        <h1 class="hero-title"><i class="fas fa-project-diagram"></i> Plateforme d'Intelligence Artificielle en Santé</h1>
        <p class="hero-subtitle">Prédiction de l'Allaitement Maternel Exclusif au Cameroun (Données EDS 2018)</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander(label="À propos de cette application", expanded=True):
    st.markdown("""
    <div style="font-size: 1.1rem; line-height: 1.6; color: #4A5568;">
        Cette application professionnelle utilise un <strong>modèle de Machine Learning hautement robuste</strong> entraîné sur les données réelles de l'Enquête Démographique et de Santé (EDS) du Cameroun 2018.<br><br>
        <strong>Objectif :</strong> Prédire de manière instantanée si une mère est susceptible de pratiquer l'Allaitement Maternel Exclusif (AME) pour son enfant (âgé de moins de 6 mois), en fonction de son profil socio-démographique, environnemental et de son suivi médical.<br>
        <strong>Utilisation :</strong> Saisissez les caractéristiques du profil dans le formulaire ci-dessous. Le modèle analysera l'ensemble des interactions (âge, éducation, richesse, visites prénatales, lieu d'accouchement...) pour fournir un diagnostic prédictif détaillé.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- FORMULAIRE DE PRÉDICTION ---
st.markdown('<h3><i class="fas fa-clipboard-list" style="color: #2563EB;"></i> Saisie du Profil pour la Prédiction</h3>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<h4><i class="fas fa-user-md" style="color:#3B82F6;"></i> Profil de la Mère</h4>', unsafe_allow_html=True)
        age_mere = st.selectbox("Tranche d'âge de la mère", ['15-24', '25-34', '35-49'])
        education = st.selectbox("Niveau d'éducation le plus élevé", ['Aucune', 'Primaire', 'Secondaire', 'Supérieur'])
        richesse = st.selectbox("Indice de Richesse du foyer", ['Le plus pauvre', 'Pauvre', 'Moyen', 'Riche', 'Le plus riche'])
        
    with col2:
        st.markdown('<h4><i class="fas fa-map-marked-alt" style="color:#10B981;"></i> Environnement</h4>', unsafe_allow_html=True)
        residence = st.selectbox("Milieu de Résidence", ['Urbain', 'Rural'])
        sexe_enfant = st.selectbox("Sexe de l'enfant", ['Masculin', 'Féminin'])
        
    with col3:
        st.markdown('<h4><i class="fas fa-clinic-medical" style="color:#8B5CF6;"></i> Suivi de Santé</h4>', unsafe_allow_html=True)
        visites = st.selectbox("Visites Prénatales (CPON)", ['< 4 visites', '>= 4 visites', 'Inconnu'])
        lieu_accouchement = st.selectbox("Lieu d'Accouchement", ['Domicile', 'Formation Sanitaire', 'Autre'])

    st.markdown('</div>', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    st.write("") 
    predict_clicked = st.button("Analyser et Prédire", use_container_width=True)

# --- RÉSULTAT ET EXPLICATION ---
if predict_clicked:
    input_data = {
        'Age_Mere_Cat': age_mere,
        'Sexe_Enfant': sexe_enfant,
        'Milieu_Residence': residence,
        'Niveau_Education': education,
        'Indice_Richesse': richesse,
        'Lieu_Accouchement_Cat': lieu_accouchement,
        'Visites_Prenatales_Cat': visites
    }
    
    df_processed = preprocess_input(input_data, model_columns)
    prob_ame = model.predict_proba(df_processed)[0][1]
    prediction_class = 1 if prob_ame >= 0.5 else 0
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h3><i class="fas fa-chart-line" style="color: #2563EB;"></i> Résultats de l\'Analyse</h3>', unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        if prediction_class == 1:
            st.markdown(f"""
            <div class="result-box result-high">
                <div class="result-title"><i class="fas fa-shield-virus"></i> Profil Favorable à l'AME</div>
                <div class="result-prob">{prob_ame * 100:.1f} %</div>
                <p style="font-weight: 600;">Probabilité de pratiquer l'Allaitement Exclusif.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown(f"""
            <div class="result-box result-low">
                <div class="result-title"><i class="fas fa-exclamation-circle"></i> Risque d'Abandon de l'AME</div>
                <div class="result-prob">{prob_ame * 100:.1f} %</div>
                <p style="font-weight: 600;">Faible probabilité d'Allaitement Exclusif.</p>
            </div>
            """, unsafe_allow_html=True)
             
    with res_col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("<h4>Interprétation Clinique et Facteurs d'Influence :</h4>", unsafe_allow_html=True)
        if prediction_class == 1:
            st.markdown(f"""
            <p>Notre modèle d'Intelligence Artificielle indique que ce profil présente un <strong>fort potentiel d'adhésion à l'Allaitement Maternel Exclusif</strong>.</p>
            <ul>
                <li><strong>Suivi Prénatal :</strong> Les données (<i>{visites}</i>) et le lieu d'accouchement (<i>{lieu_accouchement}</i>) jouent un rôle protecteur significatif, comme prouvé par l'étude statistique.</li>
                <li><strong>Socio-économique :</strong> L'éducation (<i>{education}</i>) et le niveau de richesse (<i>{richesse}</i>) de ce profil s'alignent avec les groupes démographiques ayant de bonnes pratiques de santé maternelle au Cameroun.</li>
            </ul>
            <p><i>Recommandation : Poursuivre les encouragements et le suivi normal.</i></p>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <p>Notre modèle alerte sur une <strong>probabilité critique de non-respect de l'AME</strong> (introduction précoce d'eau ou d'aliments).</p>
            <ul>
                <li><strong>Facteurs Limitant :</strong> Des combinaisons telles qu'un faible niveau d'éducation (<i>{education}</i>), un accouchement hors structure (<i>{lieu_accouchement}</i>) ou un suivi prénatal insuffisant (<i>{visites}</i>) ont statistiquement réduit les chances de réussite de l'AME selon les données de l'EDS.</li>
                <li><strong>Intervention requise :</strong> Ce profil mère-enfant nécessite une sensibilisation accrue sur l'importance du lait maternel unique durant les 6 premiers mois.</li>
            </ul>
            <p><i>Recommandation : Programmer des visites de suivi rapprochées et des conseils nutritionnels ciblés.</i></p>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
         
    historique_entry = input_data.copy()
    historique_entry['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historique_entry['Probabilité AME'] = f"{prob_ame * 100:.1f} %"
    historique_entry['Prédiction'] = "AME" if prediction_class == 1 else "Non-AME"
    
    st.session_state.history.append(historique_entry)
    save_history_to_local_storage(st.session_state.history)

# --- HISTORIQUE ET EXPORT ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<h3><i class="fas fa-database" style="color:#64748B;"></i> Historique Sécurisé des Prédictions</h3>', unsafe_allow_html=True)
st.markdown("<p style='color: #718096;'><i class='fas fa-info-circle'></i> Cet historique est conservé en local sur votre appareil pour cette session.</p>", unsafe_allow_html=True)

if st.session_state.history and len(st.session_state.history) > 0:
    df_history = pd.DataFrame(st.session_state.history)
    cols = ['Date', 'Prédiction', 'Probabilité AME'] + [c for c in df_history.columns if c not in ['Date', 'Prédiction', 'Probabilité AME']]
    df_history = df_history[cols]
    
    st.dataframe(df_history, use_container_width=True)
    
    col_hist1, col_hist2, col_hist3 = st.columns([1, 1, 2])
    with col_hist1:
        excel_data = convert_df_to_excel(df_history)
        st.download_button(
            label="Télécharger le Rapport Excel",
            data=excel_data,
            file_name=f"Rapport_Predictions_AME_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with col_hist2:
        if st.button("Purger l'historique local", use_container_width=True):
            st.session_state.history = []
            clear_local_storage()
            st.rerun()

if len(st.session_state.history) == 0:
    pass

# --- FOOTER ---
st.markdown("""
<hr style="margin-top: 4rem;">
<div style="text-align: center; color: #A0AEC0; padding-bottom: 2rem; font-size: 0.95rem;">
    <p><i class="fas fa-code"></i> Application d'Intelligence Artificielle développée par <strong>ABDOUL GANIOU TELLY</strong></p>
    <p><i>Étudiant en Master 1 Data Science</i></p>
</div>
""", unsafe_allow_html=True)
