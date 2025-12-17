import streamlit as st
import requests
import pandas as pd
import json

# Configuration de la page
st.set_page_config(
    page_title="Bank Churn API Tester",
    page_icon="🏦",
    layout="wide"
)

# URL de l'API (à remplacer par la vôtre si différente)
API_BASE_URL = "https://bank-churn.ashybay-fc2e9f26.westeurope.azurecontainerapps.io"
PREDICT_URL = f"{API_BASE_URL}/predict"
BATCH_URL = f"{API_BASE_URL}/predict/batch"
HEALTH_URL = f"{API_BASE_URL}/health"

# Titre de l'application
st.title("🏦 Bank Churn Prediction API Tester")
st.markdown("Testez les prédictions de défection client via votre API FastAPI hébergée sur Azure.")

# Section 1 : Vérification de l'état de l'API
st.header("📡 Vérification de l'API")

if st.button("Vérifier la santé de l'API"):
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            st.success(f"✅ API en ligne - Modèle chargé : {health_data['model_loaded']}")
        else:
            st.error(f"❌ API retourne une erreur : {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Impossible de joindre l'API : {e}")

# Section 2 : Prédiction individuelle
st.header("👤 Prédiction pour un client unique")
st.markdown("Remplissez les caractéristiques d'un client pour obtenir une prédiction.")

# Création de deux colonnes pour l'organisation
col1, col2 = st.columns(2)

with col1:
    st.subheader("Informations démographiques")
    credit_score = st.slider("Credit Score", 300, 850, 650)
    age = st.slider("Age", 18, 100, 35)
    tenure = st.slider("Ancienneté (années)", 0, 10, 5)
    
    st.subheader("Informations géographiques")
    geography_germany = st.checkbox("Client allemand", value=False)
    geography_spain = st.checkbox("Client espagnol", value=False)
    
    # Logique géographique (un seul pays peut être sélectionné)
    if geography_germany and geography_spain:
        st.warning("Un client ne peut pas être à la fois allemand et espagnol.")
        geography_spain = False

with col2:
    st.subheader("Informations financières")
    balance = st.number_input("Solde du compte (€)", min_value=0.0, value=50000.0, step=1000.0)
    num_products = st.slider("Nombre de produits", 1, 4, 2)
    estimated_salary = st.number_input("Salaire estimé (€)", min_value=0.0, value=75000.0, step=1000.0)
    
    st.subheader("Statut client")
    has_cr_card = st.checkbox("Possède une carte de crédit", value=True)
    is_active_member = st.checkbox("Membre actif", value=True)

# Préparation des données pour l'API
customer_data = {
    "CreditScore": credit_score,
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": num_products,
    "HasCrCard": 1 if has_cr_card else 0,
    "IsActiveMember": 1 if is_active_member else 0,
    "EstimatedSalary": estimated_salary,
    "Geography_Germany": 1 if geography_germany else 0,
    "Geography_Spain": 1 if geography_spain else 0
}

# Affichage des données JSON
with st.expander("📄 Voir les données envoyées à l'API (format JSON)"):
    st.json(customer_data)

# Bouton de prédiction individuelle
if st.button("🔍 Prédire le risque de churn", type="primary"):
    with st.spinner("Envoi de la requête à l'API..."):
        try:
            response = requests.post(PREDICT_URL, json=customer_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Affichage des résultats
                st.success("✅ Prédiction obtenue avec succès !")
                
                # Métriques
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                with col_metric1:
                    st.metric(
                        label="Probabilité de Churn", 
                        value=f"{result['churn_probability']*100:.2f}%",
                        delta=None
                    )
                
                with col_metric2:
                    prediction_text = "💔 Partira" if result['prediction'] == 1 else "💖 Restera"
                    st.metric(label="Prédiction", value=prediction_text)
                
                with col_metric3:
                    # Code couleur pour le niveau de risque
                    risk_color = {
                        "Low": "🟢",
                        "Medium": "🟡", 
                        "High": "🔴"
                    }
                    st.metric(
                        label="Niveau de Risque", 
                        value=f"{risk_color.get(result['risk_level'], '⚪')} {result['risk_level']}"
                    )
                
                # Barre de progression pour la probabilité
                st.progress(float(result['churn_probability']))
                st.caption(f"Probabilité de churn : {result['churn_probability']:.4f}")
                
                # Explication
                st.info(f"""
                **Interprétation** :
                - **Probabilité de churn** : {result['churn_probability']*100:.1f}% de chances que le client quitte la banque
                - **Niveau de risque** : {result['risk_level']} (seuils: <30% = Low, <70% = Medium, ≥70% = High)
                - **Recommandation** : { "Surveillance recommandée" if result['risk_level'] != "Low" else "Client stable"}
                """)
                
            else:
                st.error(f"❌ Erreur de l'API : {response.status_code}")
                try:
                    error_detail = response.json()
                    st.error(f"Détail : {error_detail}")
                except:
                    st.error(f"Réponse texte : {response.text}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur de connexion : {e}")

# Section 3 : Prédiction par lot (batch)
st.header("📊 Prédiction par lot (Batch)")
st.markdown("Téléchargez un fichier CSV avec plusieurs clients ou utilisez l'exemple ci-dessous.")

# Exemple de données
example_data = [
    {
        "CreditScore": 650, "Age": 35, "Tenure": 5, "Balance": 50000,
        "NumOfProducts": 2, "HasCrCard": 1, "IsActiveMember": 1,
        "EstimatedSalary": 75000, "Geography_Germany": 0, "Geography_Spain": 1
    },
    {
        "CreditScore": 720, "Age": 42, "Tenure": 3, "Balance": 120000,
        "NumOfProducts": 3, "HasCrCard": 1, "IsActiveMember": 0,
        "EstimatedSalary": 95000, "Geography_Germany": 1, "Geography_Spain": 0
    },
    {
        "CreditScore": 580, "Age": 28, "Tenure": 1, "Balance": 15000,
        "NumOfProducts": 1, "HasCrCard": 0, "IsActiveMember": 1,
        "EstimatedSalary": 45000, "Geography_Germany": 0, "Geography_Spain": 0
    }
]

# Option 1 : Utiliser les données d'exemple
if st.checkbox("Utiliser les données d'exemple"):
    df_example = pd.DataFrame(example_data)
    st.dataframe(df_example, use_container_width=True)
    batch_data = example_data

# Option 2 : Télécharger un fichier CSV
uploaded_file = st.file_uploader("Ou téléchargez un fichier CSV", type=['csv'])
if uploaded_file is not None:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        st.dataframe(df_uploaded, use_container_width=True)
        
        # Conversion en format API
        required_columns = [
            "CreditScore", "Age", "Tenure", "Balance", "NumOfProducts",
            "HasCrCard", "IsActiveMember", "EstimatedSalary",
            "Geography_Germany", "Geography_Spain"
        ]
        
        # Vérification des colonnes
        missing_columns = [col for col in required_columns if col not in df_uploaded.columns]
        if missing_columns:
            st.error(f"Colonnes manquantes dans le CSV : {', '.join(missing_columns)}")
            batch_data = None
        else:
            batch_data = df_uploaded[required_columns].to_dict('records')
            st.success(f"✅ Fichier chargé : {len(batch_data)} clients")
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
        batch_data = None

# Bouton de prédiction par lot
if st.button("🚀 Lancer la prédiction par lot", type="secondary") and 'batch_data' in locals():
    if batch_data:
        with st.spinner(f"Envoi de {len(batch_data)} clients à l'API..."):
            try:
                response = requests.post(BATCH_URL, json=batch_data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success(f"✅ Batch prédiction réussie ! {result['count']} clients traités")
                    
                    # Création d'un dataframe avec les résultats
                    predictions_df = pd.DataFrame(result['predictions'])
                    
                    # Ajout des données d'entrée pour référence
                    input_df = pd.DataFrame(batch_data)
                    combined_df = pd.concat([input_df, predictions_df], axis=1)
                    
                    # Affichage des résultats
                    st.dataframe(combined_df, use_container_width=True)
                    
                    # Statistiques
                    churn_rate = (combined_df['prediction'].sum() / len(combined_df)) * 100
                    avg_probability = combined_df['churn_probability'].mean() * 100
                    
                    col_stat1, col_stat2 = st.columns(2)
                    with col_stat1:
                        st.metric("Taux de churn prédit", f"{churn_rate:.1f}%")
                    with col_stat2:
                        st.metric("Probabilité moyenne", f"{avg_probability:.1f}%")
                    
                    # Option de téléchargement
                    csv = combined_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Télécharger les résultats (CSV)",
                        data=csv,
                        file_name="batch_predictions_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"❌ Erreur de l'API : {response.status_code}")
                    st.error(f"Détail : {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erreur de connexion : {e}")
    else:
        st.warning("Veuillez d'abord charger ou générer des données.")

# Section 4 : Informations techniques
with st.expander("🔧 Informations techniques et débogage"):
    # URLs de l'API
    st.markdown(f"""
    **URLs de l'API** :
    - Base : `{API_BASE_URL}`
    - Health Check : `{HEALTH_URL}`
    - Prédiction unique : `{PREDICT_URL}`
    - Prédiction batch : `{BATCH_URL}`
    - Documentation : `{API_BASE_URL}/docs`
    """)
    
    # Section 1 : Structure des données requises
    st.markdown("**Structure des données requises :**")
    st.code("""{
  "CreditScore": 650,
  "Age": 35,
  "Tenure": 5,
  "Balance": 50000,
  "NumOfProducts": 2,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 75000,
  "Geography_Germany": 0,
  "Geography_Spain": 1
}""", language="json")
    
    # Section 2 : Format de réponse attendu
    st.markdown("**Format de réponse attendu (prédiction unique) :**")
    st.code("""{
  "churn_probability": 0.2543,
  "prediction": 0,
  "risk_level": "Low"
}""", language="json")
    
    # Section 3 : Tests d'URL
    st.markdown("---")
    st.markdown("**Tests de connexion à l'API**")
    
    # Boutons pour tester les endpoints
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Tester /health", use_container_width=True, key="test_health"):
            with st.spinner("Test de /health en cours..."):
                try:
                    response = requests.get(HEALTH_URL, timeout=10)
                    
                    # Afficher le résultat
                    st.code(
                        f"URL: {HEALTH_URL}\n"
                        f"Status: {response.status_code}\n"
                        f"Response: {response.text}",
                        language="json"
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Endpoint /health fonctionnel !")
                        # Afficher les données formatées
                        try:
                            health_data = response.json()
                            st.json(health_data)
                        except:
                            pass
                    else:
                        st.error(f"❌ Erreur {response.status_code} sur /health")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erreur de connexion : {e}")
    
    with col2:
        if st.button("🔮 Tester /predict (GET)", use_container_width=True, key="test_predict_get"):
            with st.spinner("Test de /predict en cours..."):
                try:
                    # Essayer une requête GET sur /predict (devrait retourner 405 Method Not Allowed)
                    response = requests.get(PREDICT_URL, timeout=10)
                    
                    st.code(
                        f"URL: {PREDICT_URL}\n"
                        f"Méthode: GET\n"
                        f"Status: {response.status_code}\n"
                        f"Response: {response.text}",
                        language="text"
                    )
                    
                    if response.status_code == 405:
                        st.success("✅ Endpoint /predict protégé : GET non autorisé (comme attendu)")
                    elif response.status_code == 200:
                        st.info("⚠️ GET autorisé sur /predict (inattendu)")
                    else:
                        st.warning(f"⚠️ Status inattendu : {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erreur de connexion : {e}")
    
    # Test POST sur /predict avec données d'exemple
    st.markdown("**Test POST avec données :**")
    
    if st.button("📤 Tester /predict (POST avec données)", type="primary", key="test_predict_post"):
        with st.spinner("Envoi de données à /predict..."):
            # Données de test
            test_data = {
                "CreditScore": 650,
                "Age": 35,
                "Tenure": 5,
                "Balance": 50000,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 75000,
                "Geography_Germany": 0,
                "Geography_Spain": 1
            }
            
            try:
                # Afficher les données envoyées
                st.markdown("**Données envoyées :**")
                st.json(test_data)
                
                # Envoyer la requête POST
                response = requests.post(PREDICT_URL, json=test_data, timeout=30)
                
                # Afficher les résultats
                st.markdown("**Réponse de l'API :**")
                st.code(
                    f"URL: {PREDICT_URL}\n"
                    f"Méthode: POST\n"
                    f"Status: {response.status_code}\n"
                    f"Temps de réponse: {response.elapsed.total_seconds():.2f}s",
                    language="text"
                )
                
                if response.status_code == 200:
                    st.success("✅ Prédiction réussie !")
                    try:
                        prediction_result = response.json()
                        st.json(prediction_result)
                        
                        # Afficher une interprétation
                        st.info(f"""
                        **Interprétation** :
                        - Probabilité de churn : **{prediction_result['churn_probability']*100:.1f}%**
                        - Prédiction : **{"💔 Partira" if prediction_result['prediction'] == 1 else "💖 Restera"}**
                        - Niveau de risque : **{prediction_result['risk_level']}**
                        """)
                    except:
                        st.text(f"Réponse brute: {response.text}")
                        
                elif response.status_code == 422:
                    st.error("❌ Erreur de validation des données")
                    st.text(response.text)
                elif response.status_code == 503:
                    st.error("❌ Modèle non chargé sur le serveur")
                else:
                    st.error(f"❌ Erreur {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Timeout : l'API n'a pas répondu dans les délais")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erreur de connexion : {e}")
            except Exception as e:
                st.error(f"❌ Erreur inattendue : {e}")
    
    # Test manuel d'une URL personnalisée
    st.markdown("---")
    st.markdown("**Test manuel d'une URL :**")
    
    col_url, col_btn = st.columns([3, 1])
    with col_url:
        custom_url = st.text_input(
            "URL personnalisée à tester :",
            value=HEALTH_URL,
            key="custom_url_input"
        )
    with col_btn:
        test_method = st.selectbox(
            "Méthode :",
            ["GET", "POST"],
            key="test_method_select"
        )
    
    if st.button("🚀 Tester l'URL personnalisée", key="test_custom"):
        if custom_url.strip():
            with st.spinner(f"Test {test_method} en cours..."):
                try:
                    if test_method == "GET":
                        response = requests.get(custom_url, timeout=10)
                    else:  # POST
                        response = requests.post(custom_url, json=test_data, timeout=10)
                    
                    st.code(
                        f"URL: {custom_url}\n"
                        f"Méthode: {test_method}\n"
                        f"Status: {response.status_code}\n"
                        f"Temps: {response.elapsed.total_seconds():.2f}s\n\n"
                        f"Headers:\n{json.dumps(dict(response.headers), indent=2)}\n\n"
                        f"Body:\n{response.text}",
                        language="text"
                    )
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erreur : {e}")
        else:
            st.warning("⚠️ Veuillez entrer une URL")

# Pied de page
st.divider()
st.caption("Bank Churn Prediction API Tester - Interface développée avec Streamlit")