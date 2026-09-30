"""
═══════════════════════════════════════════════════════════════════════════════
COMPARAISON: APPROCHE INTELLIGENTE vs R2RML CLASSIQUE
═══════════════════════════════════════════════════════════════════════════════

Ce script compare deux approches de conversion de données tabulaires en RDF:
1. Baseline Python à mappings statiques (nommée « R2RML Classique » dans le rendu d'origine)
2. Approche Intelligente (découverte automatique + ML + alignement ontologies)
"""

import pandas as pd
import time
from typing import Dict

class R2RMLClassicConverter:
    """
    Implémentation R2RML Classique
    - Mappings manuels prédéfinis
    - Pas de découverte automatique
    - Structure rigide et statique
    """
    
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        self.df.columns = self.df.columns.str.lower().str.replace(" ", "_")
        self.triples = []
        
    def convert_r2rml(self) -> Dict:
        """
        Conversion R2RML classique avec mappings statiques
        
        Retourne:
            Dictionnaire avec métriques de performance
        """
        start_time = time.time()
        
        # R2RML Mapping manuel (statique)
        namespace = "http://example.org/students/"
        
        for idx, row in self.df.iterrows():
            entity_uri = f"{namespace}student_{row['id']}"
            
            # Triplets R2RML basiques (mappings manuels fixes)
            self.triples.append((entity_uri, "rdf:type", f"{namespace}Student"))
            self.triples.append((entity_uri, f"{namespace}id", row['id']))
            self.triples.append((entity_uri, f"{namespace}nom", row['nom']))
            self.triples.append((entity_uri, f"{namespace}age", row['age']))
            self.triples.append((entity_uri, f"{namespace}genre", row['genre']))
            self.triples.append((entity_uri, f"{namespace}filiere", row['filiere']))
            self.triples.append((entity_uri, f"{namespace}universite", row['universite']))
            self.triples.append((entity_uri, f"{namespace}ville", row['ville']))
            self.triples.append((entity_uri, f"{namespace}email", row['email']))
        
        end_time = time.time()
        
        return {
        'approach': 'Baseline Python fixe',
            'triples': len(self.triples),
            'time': end_time - start_time,
            'relations_discovered': 0,  # R2RML ne découvre pas de relations
            'ontology_alignments': 0,   # Pas d'alignement automatique
            'manual_mappings': 'Codés dans la source',
            'ml_used': False,
            'scalability': 'Non évaluée'
        }


def generate_comparison_report():
    """
    Génère un rapport comparatif détaillé entre les deux approches
    """
    
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "COMPARAISON: INTELLIGENT vs R2RML CLASSIQUE" + " "*20 + "║")
    print("╚" + "="*78 + "╝\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 1. EXÉCUTION R2RML CLASSIQUE
    # ═══════════════════════════════════════════════════════════════════════
    
    print("1️⃣  BASELINE PYTHON À MAPPINGS FIXES")
    print("─" * 80)
    
    r2rml_converter = R2RMLClassicConverter("etudiants.csv")
    r2rml_results = r2rml_converter.convert_r2rml()
    
    print(f"   ✓ Temps d'exécution: {r2rml_results['time']:.4f}s")
    print(f"   ✓ Triplets générés: {r2rml_results['triples']}")
    print(f"   ✓ Relations découvertes: {r2rml_results['relations_discovered']}")
    print(f"   ✓ Alignements ontologiques: {r2rml_results['ontology_alignments']}")
    print(f"   ✓ Mappings manuels requis: {r2rml_results['manual_mappings']}")
    print(f"   ✓ Machine Learning: {'Oui' if r2rml_results['ml_used'] else 'Non'}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 2. EXÉCUTION DE L'APPROCHE INTELLIGENTE
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n2️⃣  CONVERSION INTELLIGENTE")
    print("─" * 80)
    
    # Correction portfolio: execute réellement le convertisseur intelligent.
    # Le notebook universitaire d'origine utilisait ici des valeurs statiques.
    from intelligent_lod_converter import IntelligentLODConverter
    intelligent_converter = IntelligentLODConverter("etudiants.csv")
    intelligent_graph = intelligent_converter.convert()
    metrics = intelligent_converter.metrics
    discovered = (
        sum(value for key, value in metrics.items() if key.startswith("exact_"))
        + metrics.get("ml_similarity_relations", 0)
        + metrics.get("inferred_relations", 0)
        + metrics.get("dbpedia_links", 0)
    )
    intelligent_results = {
        'approach': 'Approche Intelligente',
        'triples': len(intelligent_graph),
        'time': metrics['execution_time'],
        'relations_discovered': discovered,
        'ontology_alignments': 5,  # FOAF, Schema.org, AIISO, DBpedia, DC
        'manual_mappings': 'Règles et vocabulaires codés dans la source',
        'ml_used': True,
        'scalability': 'Non évaluée au-delà de cet exemple'
    }
    
    print(f"   ✓ Temps d'exécution: {intelligent_results['time']:.4f}s")
    print(f"   ✓ Triplets générés: {intelligent_results['triples']}")
    print(f"   ✓ Relations découvertes: {intelligent_results['relations_discovered']}")
    print(f"   ✓ Alignements ontologiques: {intelligent_results['ontology_alignments']}")
    print(f"   ✓ Mappings manuels requis: {intelligent_results['manual_mappings']}")
    print(f"   ✓ Machine Learning: {'Oui' if intelligent_results['ml_used'] else 'Non'}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 3. TABLEAU COMPARATIF DÉTAILLÉ
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "═"*80)
    print("📊 TABLEAU COMPARATIF DÉTAILLÉ")
    print("═"*80 + "\n")
    
    comparison_data = {
        'Critère': [
            'Triplets RDF',
            'Relations découvertes',
            'Alignement ontologique',
            'Découverte automatique',
            'Machine Learning',
            'Mappings manuels',
            'Enrichissement sémantique',
            'Interopérabilité',
            'Maintenance',
            'Scalabilité',
            'Temps d\'exécution (s)'
        ],
        'R2RML Classique': [
            r2rml_results['triples'],
            r2rml_results['relations_discovered'],
            'Aucun vocabulaire externe',
            'Non',
            'Non',
            r2rml_results['manual_mappings'],
            'Non évalué',
            'Non évaluée',
            'Manuelle',
            r2rml_results['scalability'],
            f"{r2rml_results['time']:.4f}"
        ],
        'Approche Intelligente': [
            intelligent_results['triples'],
            intelligent_results['relations_discovered'],
            f'Oui ({intelligent_results["ontology_alignments"]} ontologies)',
            'Oui (règles + similarité)',
            'Oui (TF-IDF, Clustering)',
            intelligent_results['manual_mappings'],
            'Triplets supplémentaires',
            '5 vocabulaires référencés',
            'Règles codées dans la source',
            intelligent_results['scalability'],
            f"{intelligent_results['time']:.4f}"
        ]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    print(df_comparison.to_string(index=False))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 4. CALCUL DES GAINS
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "═"*80)
    print("📈 ÉCARTS OBSERVÉS SUR L'EXEMPLE FOURNI")
    print("═"*80 + "\n")
    
    triple_gain = ((intelligent_results['triples'] - r2rml_results['triples']) / 
                   r2rml_results['triples'] * 100)
    
    baseline_time = r2rml_results['time']
    time_overhead = (
        (intelligent_results['time'] - baseline_time) / baseline_time * 100
        if baseline_time > 0
        else None
    )
    
    print(f"RÉSULTATS MESURÉS SUR CE JEU DE DIX LIGNES:")
    print(f"   • Enrichissement: +{triple_gain:.1f}% de triplets RDF")
    print(f"   • Relations automatiques: {intelligent_results['relations_discovered']} découvertes (vs 0)")
    print(f"   • Alignement: {intelligent_results['ontology_alignments']} ontologies standard")
    print(f"   • Découverte ML: TF-IDF + Cosine Similarity pour relations sémantiques")
    print(f"   • Configuration: règles et vocabulaires préconfigurés dans le code")
    print(f"   • Vocabulaires référencés: FOAF, Schema.org, AIISO, DBpedia et Dublin Core")
    
    print(f"\nTEMPS D'EXÉCUTION:")
    if time_overhead is None:
        print(f"   • Baseline trop rapide pour calculer un pourcentage fiable; convertisseur enrichi: {intelligent_results['time']:.4f}s")
    else:
        print(f"   • Écart mesuré: {time_overhead:+.1f}%; convertisseur enrichi: {intelligent_results['time']:.4f}s")
    print(f"   • Dépendances: Requiert scikit-learn pour ML")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 5. ANALYSE QUALITATIVE
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "═"*80)
    print("🔬 ANALYSE QUALITATIVE")
    print("═"*80 + "\n")
    
    print("BASELINE PYTHON FIXE:")
    print("   • Ne découvre aucune relation implicite")
    print("   • Ses correspondances sont écrites explicitement dans le code")
    print("   • Elle ne charge ni ne valide un document de mapping R2RML")
    
    print("\nCONVERTISSEUR ENRICHI:")
    print("   • Exécute des règles de relations et une similarité TF-IDF")
    print("   • Référence cinq vocabulaires dans les triplets produits")
    print("   • Ses règles, seuils et correspondances restent préconfigurés dans le code")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 6. RECOMMANDATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "═"*80)
    print("💡 PORTÉE DE LA COMPARAISON")
    print("═"*80 + "\n")
    
    print("Les écarts ci-dessus décrivent uniquement les deux scripts et les dix lignes")
    print("du fichier fourni. Ils ne permettent pas de conclure sur la conformité R2RML,")
    print("la qualité des liens, la maintenance ou les performances à grande échelle.")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 7. CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*30 + "CONCLUSION" + " "*38 + "║")
    print("╚" + "="*78 + "╝\n")
    
    print(f"Sur le jeu fourni, le convertisseur enrichi produit {intelligent_results['triples']}")
    print(f"triplets contre {r2rml_results['triples']} pour la baseline Python et compte")
    print(f"{intelligent_results['relations_discovered']} relations ajoutées par ses règles.")
    print("Cette exécution ne constitue ni un benchmark d'un moteur R2RML conforme au W3C,")
    print("ni une évaluation de passage à l'échelle ou de qualité sémantique.")
    
    print("\n" + "═"*80 + "\n")
    
    # Sauvegarder le rapport
    save_comparison_report(df_comparison, r2rml_results, intelligent_results, triple_gain)
    
    return df_comparison


def save_comparison_report(df_comparison, r2rml_results, intelligent_results, gain):
    """Sauvegarde le rapport de comparaison dans un fichier"""
    
    with open("rapport_comparaison_r2rml.txt", 'w', encoding='utf-8') as f:
        f.write("═"*80 + "\n")
        f.write("RAPPORT DE COMPARAISON: INTELLIGENT vs R2RML CLASSIQUE\n")
        f.write("═"*80 + "\n\n")
        
        f.write("TABLEAU COMPARATIF\n")
        f.write("─"*80 + "\n")
        f.write(df_comparison.to_string(index=False))
        f.write("\n\n")
        
        f.write("RÉSUMÉ DES GAINS\n")
        f.write("─"*80 + "\n")
        f.write(f"• Triplets: {intelligent_results['triples']} vs {r2rml_results['triples']} (+{gain:.1f}%)\n")
        f.write(f"• Relations: {intelligent_results['relations_discovered']} vs {r2rml_results['relations_discovered']}\n")
        f.write(f"• Ontologies: {intelligent_results['ontology_alignments']} vs {r2rml_results['ontology_alignments']}\n")
        f.write(f"• Mappings manuels: {intelligent_results['manual_mappings']} vs {r2rml_results['manual_mappings']}\n")
        f.write("\n")
        
        f.write("CONCLUSION\n")
        f.write("─"*80 + "\n")
        f.write("Ces nombres décrivent uniquement l'exécution sur le jeu fourni. La baseline\n")
        f.write("est une conversion Python fixe, et non l'exécution d'un moteur R2RML.\n")
        f.write("La qualité sémantique et le passage à l'échelle n'ont pas été évalués.\n")
    
    print("📄 Rapport de comparaison sauvegardé: rapport_comparaison_r2rml.txt")


# ═══════════════════════════════════════════════════════════════════════════
# EXÉCUTION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    generate_comparison_report()
