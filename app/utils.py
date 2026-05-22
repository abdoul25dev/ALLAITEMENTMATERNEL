import pandas as pd
import json
import base64
from io import BytesIO
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

def save_history_to_local_storage(history_list):
    """Sauvegarde l'historique dans le localStorage du navigateur."""
    # Convert list of dicts to JSON string
    json_str = json.dumps(history_list)
    # Inject JS to save
    js_code = f"""
        <script>
            window.localStorage.setItem('allaitement_history', '{json_str}');
        </script>
    """
    components.html(js_code, height=0)

def load_history_from_local_storage():
    """Charge l'historique depuis le localStorage."""
    try:
        # Note: st_javascript execute le JS et retourne le resultat à Python
        data = st_javascript("window.localStorage.getItem('allaitement_history');")
        if data and isinstance(data, str):
            return json.loads(data)
        return []
    except Exception as e:
        return []

def clear_local_storage():
    components.html("<script>window.localStorage.removeItem('allaitement_history');</script>", height=0)

def convert_df_to_excel(df):
    """Convertit un DataFrame pandas en fichier Excel binaire pour le téléchargement."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Historique_Predictions')
        # Ajustement des colonnes
        worksheet = writer.sheets['Historique_Predictions']
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)
    processed_data = output.getvalue()
    return processed_data

def preprocess_input(input_data, model_columns):
    """
    Prend le dictionnaire des entrées du formulaire et génère un DataFrame
    avec le format One-Hot Encoding exact (dummies) attendu par le modèle.
    """
    df_input = pd.DataFrame([input_data])
    # Encodage One-Hot
    df_dummies = pd.get_dummies(df_input)
    
    # Réalignement avec les colonnes du modèle d'entraînement
    # On crée un DF vide avec les bonnes colonnes
    df_final = pd.DataFrame(columns=model_columns)
    # On concatène pour aligner les colonnes (remplit avec NaN)
    df_final = pd.concat([df_final, df_dummies], ignore_index=True)
    # On remplace les NaN par 0 (ou False)
    df_final = df_final.fillna(0)
    
    # On s'assure de l'ordre exact et qu'il n'y a qu'une seule ligne
    df_final = df_final[model_columns].iloc[0:1]
    
    # Force float type
    df_final = df_final.astype(float)
    return df_final
