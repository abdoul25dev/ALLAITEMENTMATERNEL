import pandas as pd
import numpy as np
import os

def generate_dataset(input_file, output_file):
    print("Démarrage de la génération du jeu de données avec noms et valeurs décodés...")
    
    # Dictionnaire de correspondance: Code DHS -> Nom descriptif (en français)
    dhs_to_name = {
        'caseid': 'ID_Enfant',
        'v005': 'Poids_Echantillon',
        'v012': 'Age_Mere_Actuel',
        'v013': 'Groupe_Age_Mere',
        'v024': 'Region',
        'v025': 'Milieu_Residence',
        'v106': 'Niveau_Education',
        'v190': 'Indice_Richesse',
        'b4': 'Sexe_Enfant',
        'b19': 'Age_Enfant_Mois',
        'hw1': 'Age_Enfant_Anthropometrie',
        'm4': 'Duree_Allaitement_Mois',
        'v404': 'Allaitement_Actuel',
        'v409': 'Donne_Eau_Claire',
        'm39': 'Fois_Mange_Solide_Hier',
        'm14': 'Nombre_Visites_Prenatales',
        'm15': 'Lieu_Accouchement',
        'v212': 'Age_Premier_Accouchement',
        'v481': 'Assurance_Maladie',
        'v414s': 'Donne_Nourriture_Solide',
        'v414v': 'Donne_Yaourt'
    }

    try:
        reader = pd.read_stata(input_file, iterator=True)
        metadata = reader.variable_labels()
        value_labels = reader.value_labels()
        
        # On lit sans convertir les catégories pour éviter l'erreur des labels dupliqués de Pandas
        df = pd.read_stata(input_file, convert_categoricals=False)
        print(f"Fichier chargé. Dimensions: {df.shape}")
        
    except Exception as e:
        print(f"Erreur de chargement: {e}")
        return

    cols_to_keep = [col for col in dhs_to_name.keys() if col in df.columns]
    df_subset = df[cols_to_keep].copy()
    
    # Décodage exhaustif des valeurs: Remplacement des codes numériques par leurs labels textuels
    for col in cols_to_keep:
        val_labels_dict = value_labels.get(col, {})
        if val_labels_dict:
            # On mappe les valeurs numériques à leur représentation textuelle
            df_subset[col] = df_subset[col].map(val_labels_dict).fillna(df_subset[col])

    # Renommage des colonnes pour avoir des noms clairs
    df_subset.rename(columns=dhs_to_name, inplace=True)

    # Construction du dictionnaire exhaustif des métadonnées
    meta_list = []
    for col in cols_to_keep:
        nom_descriptif = dhs_to_name[col]
        desc = metadata.get(col, "Non spécifié")
        val_labels_dict = value_labels.get(col, {})
        
        labels_str = "\n".join([f"{k} = {v}" for k, v in val_labels_dict.items()]) if val_labels_dict else "Valeur numérique continue ou texte libre"
        
        meta_list.append({
            "Code_DHS": col,
            "Nom_Variable": nom_descriptif,
            "Description_Officielle": desc,
            "Valeurs_Possibles_et_Encodage": labels_str
        })
        
    df_meta = pd.DataFrame(meta_list)

    print(f"Sauvegarde dans {output_file}...")
    try:
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df_subset.to_excel(writer, sheet_name='data', index=False)
            df_meta.to_excel(writer, sheet_name='metadonnees', index=False)
            
            workbook  = writer.book
            worksheet = writer.sheets['metadonnees']
            wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
            worksheet.set_column('A:B', 20, wrap_format)
            worksheet.set_column('C:C', 50, wrap_format)
            worksheet.set_column('D:D', 60, wrap_format)

        print("Génération réussie : Dataset entièrement décodé et renommé.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")

if __name__ == "__main__":
    INPUT_FILE = "CMKR71FL.DTA"
    OUTPUT_FILE = "dataset_allaitement_edsc2018_decode.xlsx"
    generate_dataset(INPUT_FILE, OUTPUT_FILE)
