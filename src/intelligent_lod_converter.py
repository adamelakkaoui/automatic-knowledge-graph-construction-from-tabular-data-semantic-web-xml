import pandas as pd
import numpy as np
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import re
import time
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════
# DÉFINITION DES NAMESPACES ET ONTOLOGIES
# ═══════════════════════════════════════════════════════════════════════════

EX = Namespace("http://example.org/students/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SCHEMA = Namespace("http://schema.org/")
AIISO = Namespace("http://purl.org/vocab/aiiso/schema#")
DBPEDIA = Namespace("http://dbpedia.org/resource/")
DC = Namespace("http://purl.org/dc/elements/1.1/")

class IntelligentLODConverter:
    """
    Convertisseur intelligent de données tabulaires vers Linked Open Data
    
    Fonctionnalités:
    ----------------
    1. Conversion basique CSV → RDF
    2. Découverte automatique de relations (règles + ML)
    3. Alignement multi-ontologies (FOAF, Schema.org, AIISO, DBpedia)
    4. Enrichissement sémantique et inférence
    5. Métriques et rapport détaillé
    """
    
    def __init__(self, csv_file: str, base_uri: str = "http://example.org/students/"):
        """
        Initialise le convertisseur
        
        Args:
            csv_file: Chemin vers le fichier CSV
            base_uri: URI de base pour les entités
        """
        self.csv_file = csv_file
        self.base_uri = base_uri
        self.df = None
        self.g = Graph()
        self.relations_discovered = []
        self.metrics = defaultdict(int)
        self.start_time = None
        
        # Bind namespaces
        self._bind_namespaces()
        
        # Charger les données
        self._load_data()
        
    def _bind_namespaces(self):
        """Lie tous les namespaces au graphe RDF"""
        self.g.bind("ex", EX)
        self.g.bind("foaf", FOAF)
        self.g.bind("schema", SCHEMA)
        self.g.bind("aiiso", AIISO)
        self.g.bind("dbpedia", DBPEDIA)
        self.g.bind("dc", DC)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("owl", OWL)
        self.g.bind("xsd", XSD)
        
    def _load_data(self):
        """Charge et nettoie les données CSV"""
        try:
            self.df = pd.read_csv(self.csv_file, encoding='utf-8')
            # Normaliser les noms de colonnes
            self.df.columns = self.df.columns.str.lower().str.strip().str.replace(" ", "_")
            print(f"✅ Données chargées: {len(self.df)} enregistrements, {len(self.df.columns)} colonnes")
            print(f"   Colonnes: {', '.join(self.df.columns)}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du CSV: {e}")
            raise
    
    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 1: CONVERSION BASIQUE CSV → RDF
    # ═══════════════════════════════════════════════════════════════════════
    
    def basic_rdf_conversion(self):
        """
        Conversion basique avec alignement ontologique complet
        Mappe chaque attribut vers FOAF, Schema.org et AIISO
        """
        print("\n" + "="*80)
        print("ÉTAPE 1: CONVERSION BASIQUE CSV → RDF + ALIGNEMENT ONTOLOGIQUE")
        print("="*80)
        
        for idx, row in self.df.iterrows():
            student_uri = URIRef(EX[f"student_{row['id']}"])
            
            # ─────────────────────────────────────────────────────────────
            # Types (Classes)
            # ─────────────────────────────────────────────────────────────
            self.g.add((student_uri, RDF.type, EX.Student))
            self.g.add((student_uri, RDF.type, FOAF.Person))
            self.g.add((student_uri, RDF.type, SCHEMA.Person))
            self.metrics['types'] += 3
            
            # ─────────────────────────────────────────────────────────────
            # Propriétés de base avec alignement multi-ontologies
            # ─────────────────────────────────────────────────────────────
            
            # ID
            self.g.add((student_uri, EX.studentId, Literal(row['id'], datatype=XSD.integer)))
            self.g.add((student_uri, DC.identifier, Literal(f"student_{row['id']}")))
            
            # Nom
            self.g.add((student_uri, FOAF.name, Literal(row['nom'], datatype=XSD.string)))
            self.g.add((student_uri, SCHEMA.name, Literal(row['nom'], datatype=XSD.string)))
            self.g.add((student_uri, EX.fullName, Literal(row['nom'], datatype=XSD.string)))
            
            # Âge
            self.g.add((student_uri, FOAF.age, Literal(row['age'], datatype=XSD.integer)))
            self.g.add((student_uri, SCHEMA.age, Literal(row['age'], datatype=XSD.integer)))
            self.g.add((student_uri, EX.age, Literal(row['age'], datatype=XSD.integer)))
            
            # Genre
            self.g.add((student_uri, FOAF.gender, Literal(row['genre'])))
            self.g.add((student_uri, SCHEMA.gender, Literal(row['genre'])))
            
            # Email
            self.g.add((student_uri, FOAF.mbox, Literal(f"mailto:{row['email']}")))
            self.g.add((student_uri, SCHEMA.email, Literal(row['email'])))
            
            # Filière (Programme académique)
            self.g.add((student_uri, AIISO.programme_name, Literal(row['filiere'])))
            self.g.add((student_uri, SCHEMA.studiesField, Literal(row['filiere'])))
            self.g.add((student_uri, EX.major, Literal(row['filiere'])))
            
            # Université
            univ_uri = URIRef(EX[f"university_{row['universite'].lower()}"])
            self.g.add((student_uri, SCHEMA.affiliation, univ_uri))
            self.g.add((student_uri, EX.university, Literal(row['universite'])))
            
            # Ville
            self.g.add((student_uri, SCHEMA.homeLocation, Literal(row['ville'])))
            self.g.add((student_uri, EX.city, Literal(row['ville'])))
            
            self.metrics['basic_triples'] += 20  # Approximation
        
        print(f"✅ {len(self.df)} étudiants convertis en RDF")
        print(f"✅ Alignement: FOAF, Schema.org, AIISO, Dublin Core")
        print(f"✅ Types de données: XSD (integer, string)")
        
    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 2: DÉCOUVERTE DE RELATIONS EXACTES (RÈGLES)
    # ═══════════════════════════════════════════════════════════════════════
    
    def discover_exact_relations(self):
        """
        Découvre les relations basées sur égalité exacte
        Relations: sameUniversityAs, sameMajorAs, sameCityAs, sameAgeGroupAs
        """
        print("\n" + "="*80)
        print("ÉTAPE 2: DÉCOUVERTE DE RELATIONS EXACTES (RÈGLES)")
        print("="*80)
        
        relations_count = defaultdict(int)
        
        # ─────────────────────────────────────────────────────────────
        # 1. Même Université
        # ─────────────────────────────────────────────────────────────
        for i, row1 in self.df.iterrows():
            for j, row2 in self.df.iterrows():
                if i < j:
                    s1 = URIRef(EX[f"student_{row1['id']}"])
                    s2 = URIRef(EX[f"student_{row2['id']}"])
                    
                    # Même université
                    if row1['universite'] == row2['universite']:
                        self.g.add((s1, EX.sameUniversityAs, s2))
                        self.g.add((s2, EX.sameUniversityAs, s1))  # Symétrique
                        relations_count['sameUniversity'] += 2
                        self.relations_discovered.append({
                            'type': 'exact',
                            'relation': 'sameUniversityAs',
                            'entity1': row1['nom'],
                            'entity2': row2['nom'],
                            'value': row1['universite']
                        })
                    
                    # Même filière
                    if row1['filiere'] == row2['filiere']:
                        self.g.add((s1, EX.sameMajorAs, s2))
                        self.g.add((s2, EX.sameMajorAs, s1))
                        relations_count['sameMajor'] += 2
                        self.relations_discovered.append({
                            'type': 'exact',
                            'relation': 'sameMajorAs',
                            'entity1': row1['nom'],
                            'entity2': row2['nom'],
                            'value': row1['filiere']
                        })
                    
                    # Même ville
                    if row1['ville'] == row2['ville']:
                        self.g.add((s1, EX.sameCityAs, s2))
                        self.g.add((s2, EX.sameCityAs, s1))
                        relations_count['sameCity'] += 2
                        self.relations_discovered.append({
                            'type': 'exact',
                            'relation': 'sameCityAs',
                            'entity1': row1['nom'],
                            'entity2': row2['nom'],
                            'value': row1['ville']
                        })
                    
                    # Même âge
                    if row1['age'] == row2['age']:
                        self.g.add((s1, EX.sameAgeAs, s2))
                        self.g.add((s2, EX.sameAgeAs, s1))
                        relations_count['sameAge'] += 2
        
        for rel_type, count in relations_count.items():
            print(f"   ✓ {rel_type}: {count} relations")
            self.metrics[f'exact_{rel_type}'] = count
        
        print(f"✅ Total relations exactes: {sum(relations_count.values())}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 3: DÉCOUVERTE PAR SIMILARITÉ (MACHINE LEARNING)
    # ═══════════════════════════════════════════════════════════════════════
    
    def discover_similarity_relations(self, threshold: float = 0.3):
        """
        Découvre les relations basées sur similarité textuelle (TF-IDF)
        Utilise Machine Learning pour trouver des filières similaires
        
        Args:
            threshold: Seuil de similarité (0.0 à 1.0)
        """
        print("\n" + "="*80)
        print("ÉTAPE 3: DÉCOUVERTE PAR SIMILARITÉ (MACHINE LEARNING - TF-IDF)")
        print("="*80)
        print(f"   Seuil de similarité: {threshold}")
        
        # TF-IDF sur les filières
        filieres = self.df['filiere'].astype(str).values
        
        try:
            vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(filieres)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            relations_found = 0
            
            for i in range(len(self.df)):
                for j in range(i+1, len(self.df)):
                    similarity_score = similarity_matrix[i][j]
                    
                    # Si similarité > seuil ET pas identiques
                    if similarity_score > threshold and self.df.iloc[i]['filiere'] != self.df.iloc[j]['filiere']:
                        s1 = URIRef(EX[f"student_{self.df.iloc[i]['id']}"])
                        s2 = URIRef(EX[f"student_{self.df.iloc[j]['id']}"])
                        
                        # Ajouter relation de similarité
                        self.g.add((s1, EX.relatedMajorWith, s2))
                        self.g.add((s2, EX.relatedMajorWith, s1))
                        
                        # Ajouter score de similarité
                        similarity_literal = Literal(round(similarity_score, 3), datatype=XSD.float)
                        blank_node = URIRef(EX[f"similarity_{i}_{j}"])
                        self.g.add((blank_node, RDF.type, EX.SimilarityScore))
                        self.g.add((blank_node, EX.entity1, s1))
                        self.g.add((blank_node, EX.entity2, s2))
                        self.g.add((blank_node, EX.score, similarity_literal))
                        
                        relations_found += 2
                        
                        self.relations_discovered.append({
                            'type': 'ml_similarity',
                            'relation': 'relatedMajorWith',
                            'entity1': self.df.iloc[i]['nom'],
                            'entity2': self.df.iloc[j]['nom'],
                            'value1': self.df.iloc[i]['filiere'],
                            'value2': self.df.iloc[j]['filiere'],
                            'similarity_score': round(similarity_score, 3)
                        })
            
            self.metrics['ml_similarity_relations'] = relations_found
            print(f"✅ {relations_found} relations de similarité découvertes (ML)")
            
            # Afficher quelques exemples
            if self.relations_discovered:
                print("\n   Exemples de similarités détectées:")
                ml_relations = [r for r in self.relations_discovered if r['type'] == 'ml_similarity']
                for rel in ml_relations[:3]:
                    print(f"      • {rel['entity1']} ({rel['value1']}) ↔ {rel['entity2']} ({rel['value2']}) [score: {rel['similarity_score']}]")
        
        except Exception as e:
            print(f"⚠️  Erreur ML: {e}")
            self.metrics['ml_similarity_relations'] = 0
    
    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 4: INFÉRENCES ET RELATIONS DÉRIVÉES
    # ═══════════════════════════════════════════════════════════════════════
    
    def discover_inferred_relations(self):
        """
        Découvre les relations par inférence et extraction de patterns
        1. Email → Université (extraction domaine)
        2. Groupes d'âge (clustering)
        3. Proximité géographique
        """
        print("\n" + "="*80)
        print("ÉTAPE 4: DÉCOUVERTE PAR INFÉRENCE ET EXTRACTION DE PATTERNS")
        print("="*80)
        
        inferred_count = 0
        
        # ─────────────────────────────────────────────────────────────
        # 1. Extraction Email → Université (memberOf)
        # ─────────────────────────────────────────────────────────────
        email_pattern = r'@([a-z-]+)\.invalid'
        university_entities = {}
        
        for idx, row in self.df.iterrows():
            match = re.search(email_pattern, row['email'].lower())
            if match:
                domain = match.group(1)
                student_uri = URIRef(EX[f"student_{row['id']}"])
                univ_uri = URIRef(EX[f"university_{domain}"])
                
                # Créer l'entité université si pas encore créée
                if domain not in university_entities:
                    self.g.add((univ_uri, RDF.type, AIISO.Institution))
                    self.g.add((univ_uri, RDF.type, SCHEMA.EducationalOrganization))
                    self.g.add((univ_uri, RDFS.label, Literal(row['universite'])))
                    self.g.add((univ_uri, SCHEMA.name, Literal(row['universite'])))
                    self.g.add((univ_uri, EX.domain, Literal(domain)))
                    university_entities[domain] = univ_uri
                
                # Lier étudiant → université
                self.g.add((student_uri, AIISO.member_of, univ_uri))
                self.g.add((student_uri, SCHEMA.memberOf, univ_uri))
                inferred_count += 2
                
                self.relations_discovered.append({
                    'type': 'inference',
                    'relation': 'memberOf',
                    'entity1': row['nom'],
                    'entity2': row['universite'],
                    'inferred_from': 'email_domain'
                })
        
        print(f"   ✓ Email → Université: {len(university_entities)} universités créées")
        
        # ─────────────────────────────────────────────────────────────
        # 2. Groupes d'âge (clustering)
        # ─────────────────────────────────────────────────────────────
        self.df['age_group'] = pd.cut(self.df['age'], 
                                       bins=[0, 21, 23, 100], 
                                       labels=['young', 'mid', 'senior'])
        
        age_group_count = 0
        for age_group in self.df['age_group'].unique():
            group_students = self.df[self.df['age_group'] == age_group]
            
            # Créer entité de groupe
            group_uri = URIRef(EX[f"age_group_{age_group}"])
            self.g.add((group_uri, RDF.type, EX.AgeGroup))
            self.g.add((group_uri, RDFS.label, Literal(f"Age Group: {age_group}")))
            
            # Lier étudiants au groupe
            for idx, student in group_students.iterrows():
                student_uri = URIRef(EX[f"student_{student['id']}"])
                self.g.add((student_uri, EX.belongsToAgeGroup, group_uri))
                age_group_count += 1
                
                # Relations entre membres du même groupe
                for idx2, student2 in group_students.iterrows():
                    if idx < idx2:
                        s2 = URIRef(EX[f"student_{student2['id']}"])
                        self.g.add((student_uri, EX.sameAgeGroupAs, s2))
                        inferred_count += 1
        
        print(f"   ✓ Groupes d'âge: {len(self.df['age_group'].unique())} groupes, {age_group_count} memberships")
        
        self.metrics['inferred_relations'] = inferred_count
        print(f"✅ Total relations inférées: {inferred_count}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ÉTAPE 5: ALIGNEMENT AVEC DBPEDIA (VILLES MAROCAINES)
    # ═══════════════════════════════════════════════════════════════════════
    
    def align_with_dbpedia(self):
        """
        Lie les entités locales aux ressources DBpedia
        Mapping des villes marocaines vers DBpedia
        """
        print("\n" + "="*80)
        print("ÉTAPE 5: ALIGNEMENT AVEC DBPEDIA (ONTOLOGIE EXTERNE)")
        print("="*80)
        
        # Mapping villes → DBpedia
        city_dbpedia_mapping = {
            'Fes': 'Fez,_Morocco',
            'Meknes': 'Meknes',
            'Rabat': 'Rabat',
            'Casablanca': 'Casablanca',
            'Marrakech': 'Marrakech'
        }
        
        dbpedia_links = 0
        cities_found = set()
        
        for idx, row in self.df.iterrows():
            city = row['ville']
            
            if city in city_dbpedia_mapping:
                student_uri = URIRef(EX[f"student_{row['id']}"])
                dbpedia_city_uri = URIRef(DBPEDIA[city_dbpedia_mapping[city]])
                
                # Lier à DBpedia
                self.g.add((student_uri, SCHEMA.homeLocation, dbpedia_city_uri))
                self.g.add((student_uri, EX.dbpediaCity, dbpedia_city_uri))
                
                # Ajouter OWL:sameAs pour l'alignement
                local_city = URIRef(EX[f"city_{city.lower()}"])
                self.g.add((local_city, OWL.sameAs, dbpedia_city_uri))
                self.g.add((local_city, RDFS.label, Literal(city)))
                
                dbpedia_links += 2
                cities_found.add(city)
                
                if city not in [r.get('city') for r in self.relations_discovered if r.get('type') == 'dbpedia']:
                    self.relations_discovered.append({
                        'type': 'dbpedia',
                        'relation': 'sameAs',
                        'entity': city,
                        'dbpedia_uri': city_dbpedia_mapping[city]
                    })
        
        self.metrics['dbpedia_links'] = dbpedia_links
        print(f"✅ {dbpedia_links} liens DBpedia créés pour {len(cities_found)} villes")
        print(f"   Villes liées: {', '.join(sorted(cities_found))}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PIPELINE COMPLET
    # ═══════════════════════════════════════════════════════════════════════
    
    def convert(self):
        """Execute le pipeline complet de conversion"""
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "CONVERSION INTELLIGENTE CSV → LOD" + " "*25 + "║")
        print("╚" + "="*78 + "╝")
        
        self.start_time = time.time()
        
        # Exécution des étapes
        self.basic_rdf_conversion()
        self.discover_exact_relations()
        self.discover_similarity_relations(threshold=0.3)
        self.discover_inferred_relations()
        self.align_with_dbpedia()
        
        # Calcul du temps
        self.metrics['execution_time'] = time.time() - self.start_time
        
        return self.g
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXPORTATION ET RAPPORTS
    # ═══════════════════════════════════════════════════════════════════════
    
    def export_rdf(self, base_filename: str = "knowledge_graph_intelligent"):
        """Exporte le graphe RDF en plusieurs formats"""
        print("\n" + "="*80)
        print("EXPORTATION DU GRAPHE RDF")
        print("="*80)
        
        formats = {
            'xml': 'RDF/XML',
            'turtle': 'Turtle (TTL)',
            'n3': 'Notation3 (N3)',
            'nt': 'N-Triples'
        }
        
        for ext, name in formats.items():
            filename = f"{base_filename}.{ext}"
            self.g.serialize(filename, format=ext if ext != 'xml' else 'xml')
            print(f"   ✓ {name}: {filename}")
        
        print(f"\n✅ Graphe exporté avec succès")
        print(f"📊 Triplets RDF totaux: {len(self.g)}")
    
    def generate_statistics_report(self) -> str:
        """Génère un rapport statistique détaillé"""
        report = "\n" + "╔" + "="*78 + "╗\n"
        report += "║" + " "*25 + "RAPPORT STATISTIQUE DÉTAILLÉ" + " "*25 + "║\n"
        report += "╚" + "="*78 + "╝\n\n"
        
        # Statistiques générales
        report += "📊 STATISTIQUES GÉNÉRALES\n"
        report += "─" * 80 + "\n"
        report += f"• Enregistrements traités: {len(self.df)}\n"
        report += f"• Triplets RDF générés: {len(self.g)}\n"
        report += f"• Relations découvertes: {len(self.relations_discovered)}\n"
        report += f"• Temps d'exécution: {self.metrics['execution_time']:.4f}s\n\n"
        
        # Répartition par type de relation
        report += "🔍 RELATIONS DÉCOUVERTES PAR TYPE\n"
        report += "─" * 80 + "\n"
        
        relation_types = defaultdict(int)
        for rel in self.relations_discovered:
            relation_types[rel['type']] += 1
        
        for rel_type, count in sorted(relation_types.items()):
            percentage = (count / len(self.relations_discovered) * 100) if self.relations_discovered else 0
            report += f"• {rel_type.upper():<20}: {count:>4} relations ({percentage:>5.1f}%)\n"
        
        report += "\n"
        
        # Ontologies utilisées
        report += "🌐 ONTOLOGIES ALIGNÉES\n"
        report += "─" * 80 + "\n"
        report += "• FOAF (Friend of a Friend): Person, name, age, mbox, gender\n"
        report += "• Schema.org: Person, EducationalOrganization, affiliation\n"
        report += "• AIISO: Institution, Student, Programme, member_of\n"
        report += "• DBpedia: Entités géographiques (villes marocaines)\n"
        report += "• Dublin Core: identifier, creator, date\n\n"
        
        # Métriques de qualité
        report += "✨ MÉTRIQUES DE QUALITÉ\n"
        report += "─" * 80 + "\n"
        
        triples_per_entity = len(self.g) / len(self.df) if len(self.df) > 0 else 0
        relations_per_entity = len(self.relations_discovered) / len(self.df) if len(self.df) > 0 else 0
        
        report += f"• Triplets par entité: {triples_per_entity:.1f}\n"
        report += f"• Relations par entité: {relations_per_entity:.1f}\n"
        report += f"• Enrichissement sémantique: {'Élevé' if triples_per_entity > 25 else 'Moyen'}\n"
        report += f"• Interopérabilité: 5 ontologies standard\n\n"
        
        # Top relations
        report += "🔝 TOP 10 RELATIONS DÉCOUVERTES\n"
        report += "─" * 80 + "\n"
        
        for i, rel in enumerate(self.relations_discovered[:10], 1):
            if rel['type'] == 'ml_similarity':
                report += f"{i:2}. {rel['entity1']} ↔ {rel['entity2']}\n"
                report += f"    {rel['relation']} | {rel['value1']} ≈ {rel['value2']} (score: {rel['similarity_score']})\n"
            elif rel['type'] == 'exact':
                report += f"{i:2}. {rel['entity1']} ↔ {rel['entity2']}\n"
                report += f"    {rel['relation']} | {rel['value']}\n"
            elif rel['type'] == 'inference':
                report += f"{i:2}. {rel['entity1']} → {rel['entity2']}\n"
                report += f"    {rel['relation']} | Inféré de: {rel['inferred_from']}\n"
        
        return report
    
    def save_report(self, filename: str = "rapport_conversion.txt"):
        """Sauvegarde le rapport dans un fichier"""
        report = self.generate_statistics_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Rapport sauvegardé: {filename}")
        return report


# ═══════════════════════════════════════════════════════════════════════════
# EXÉCUTION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "╔" + "="*85 + "╗")
    print("║" + " "*1 + "Construction automatique de graphes de connaissances à partir de données tabulaires" + " "*1 + "║")
    print("║" + " "*30 + "Projet Web Sémantique" + " "*34 + "║")
    print("╚" + "="*85 + "╝\n")
    
    # Créer le convertisseur
    converter = IntelligentLODConverter("etudiants.csv")
    
    # Exécuter la conversion
    graph = converter.convert()
    
    # Exporter les résultats
    converter.export_rdf("knowledge_graph_intelligent")
    
    # Générer et afficher le rapport
    report = converter.generate_statistics_report()
    print(report)
    
    # Sauvegarder le rapport
    converter.save_report("rapport_conversion.txt")
    
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*25 + "CONVERSION TERMINÉE AVEC SUCCÈS!" + " "*22 + "║")
    print("╚" + "="*78 + "╝\n")
