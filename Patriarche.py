import random
import re

# --- V35: VARIATION ADJECTIVALE ET NETTOYAGE DES GNs DE BASE ---
NOMBRE_DE_PHRASES_SOUHAITE = 100
MAX_PROFONDEUR_RECURSIVITE_CN = 1
MAX_PROFONDEUR_RECURSIVITE_SUB = 0 
# ---------------------------------------------------------------------------------------------

# ===================================================================
# --- SECTION 1: VOCABULAIRE & INFRASTRUCTURE SÉMANTIQUE (V35) ---
# ===================================================================

# Groupes Nominaux Définis Masc. Sing. (MS) - EXPANSION MASSIVE
GN_MS_BASE = [
    "médium", "imaginaire", "support", "sujet", "geste", "protocole", "dispositif", "écart", "signal", "format", 
    "vecteur", "schème", "contexte", "diagramme", "médioscope", "robot-orchestre", "flux", "champ", "prisme", 
    "opérateur", "régime", "artefact", "réseau", "corps", "palimpseste", "sillage", "décentrement", 
    "horizon d'attente", "simulacre", "moment", "temps réel", "principes", "interstice", "paradigme", 
    "substrat", "référentiel", "effet-mémoire", "système", "seuil", "rapport au monde", "mythe", 
    "appareil conceptuel", "temps-image", "devenir-machine", "impératif", "cycle", "espace", "signifié", 
    "processus", "mode d'existence", "espace discursif", "chiffre de l'oubli", "terrain", "concept", 
    "référentiel ontologique", "modèle", "flux de données", "territoire affectif", "langage machinique", 
    "horizon phénoménologique", "cadre d'interprétation", "préalable", "objet-frontière", "code source", 
    "protocole d'échange", "fétichisme du médium", "mécanisme de visée", "temps hétérogène", "potentiel ontologique", 
    "geste d'inscription", "récepteur", "savoir-faire", "temps sériel", "alliage", "pigment", "granit", "velours", 
    "plâtre", "cuivre", "acier", "bitume", "fusain", "monochrome", "verre", "faisceau", "carbone", "soufre", 
    "mercure", "marbre", "silicium", "quartz", "béton", "lin", "étalon", "cristal", "souffle", "fétiche", 
    "automaton", "grain", "burin", "fauve", "faciès", "regard", "miroir", "halos", "stroboscope", "clavier", 
    "écran-total", "scrupule", "vertige", "poids", "clivage", "cliché", "négatif", "positif", "déclic", 
    "obturateur", "lentille", "foyer", "spectre", "fantôme", "cadastre", "vestige", "décombres", "fossile", 
    "sédiment", "atlas", "blason", "poussière", "reflet", "monolithe", "incendie", "linceul", "sacre", 
    "faste", "fief", "frontispice", "grimoire", "haillon", "hiéroglyphe", "ilot", "indice", "jargon", 
    "labyrinthe", "levier", "manuscrit", "masque", "mémorial", "monument", "noyau", "obus", "oracle", 
    "orgue", "oscillo", "pacte", "panoptique", "pavillon", "périple", "phare", "pilier", "pivot", 
    "plomb", "poing", "portique", "prodige", "prophète", "radar", "rayon", "rebut", "relais", 
    "rempart", "revers", "rite", "rouage", "sanctuaire", "scaphandre", "scel", "sémaphore", "seuil", 
    "socle", "sommet", "soubassement", "spectre", "stèle", "stéréotype", "stylet", "tabernacle", 
    "talisman", "tambour", "tamis", "témoin", "temple", "tenon", "terminus", "théâtre", "timbre", 
    "torse", "totem", "trajet", "trésor", "trépied", "trophée", "tronc", "tube", "tunnel", "typo"
]

# Groupes Nominaux Définis Fém. Sing. (FS) - EXPANSION MASSIVE
GN_FS_BASE = [
    "sphère", "trace", "médiatisation", "technologie", "médiologie", "médiation", "transmission", 
    "instance", "opération", "structure", "circulation", "interface", "occurrence", "archive", 
    "sémiose", "texture", "matrice", "surface", "stabilisation", "condition", "boucle de rétroaction", 
    "strate", "situation", "neurosphère", "réversibilité", "rupture", "dimension", "réflexivité", 
    "échelle", "vérité du sujet", "condition de possibilité", "infrastructure", "logique interne", 
    "puissance d'agir", "forme-mémoire", "tension", "sémantique de l'objet", "historicité", 
    "grammaire du visible", "phénoménologie de l'écran", "temporalité", "dérive", "chimère", 
    "hégémonie de l'image", "cartographie", "posture", "contingence", "dématérialisation", "évidence", 
    "réappropriation", "force-travail", "esthétique", "agence", "problématique", "dynamique", 
    "fiction théorique", "modalité d'accès", "pratique curatoriale", "économie de l'attention", 
    "zone de friction", "poétique de l'archive", "surface d'inscription", "mémoire", "fiction", 
    "catégorie", "critique", "structure d'accueil", "potentialité", "connaissance", 
    "puissance de déconstruction", "condition liminale", "matrice d'interférence", "pratique de l'écart", 
    "politique du code", "visée", "structure de pouvoir", "rhétorique du flux", "relation de tension", 
    "dynamique d'obsolescence", "matière", "céramique", "soie", "pâte", "scorie", "résine", "laque", 
    "gouache", "tempéra", "encre", "patine", "rouille", "dorure", "sculpture", "gravure", "fresque", 
    "vitesse", "inertie", "lucidité", "prothèse", "rétine", "pupille", "lucarne", "vision", "aura", 
    "idole", "icône", "relique", "onde", "fréquence", "fibre", "pellicule", "bobine", "cassette", 
    "membrane", "peau", "chair", "cendre", "poussière", "buée", "transparence", "opacité", "ombre", 
    "abîme", "alcôve", "allégorie", "amarante", "ambre", "amorce", "amplitude", "ampoule", "ancre", 
    "angoisse", "antenne", "apocalypse", "apparence", "arête", "armature", "armure", "asphalte", 
    "astuce", "atopie", "atrophiée", "attente", "aube", "auréole", "autopsie", "balafre", "balise", 
    "barrière", "bascule", "bavure", "béance", "bible", "biographie", "blessure", "bordure", 
    "bosse", "bouche", "boue", "brèche", "brise", "brisure", "broussaille", "brulure", "brume", 
    "cadence", "calamine", "calligraphie", "carcasse", "caresse", "caricature", "cascade", 
    "catastrophe", "caverne", "cécité", "cellule", "cendre", "cérémonie", "chaîne", "chair", 
    "chaleur", "chambre", "charpente", "charnière", "châsse", "chausse-trape", "chimie", 
    "chronique", "chrysalide", "cicatrice", "cire", "citadelle", "clarté", "cloche", "cloison", 
    "colonne", "combustion", "comète", "communion", "complicité", "compression", "conque", 
    "conquête", "constellation", "corrosion", "couche", "coulisse", "coupure", "couronne", 
    "crevasse", "crise", "cristallisation", "croûte", "cruauté", "crypte", "cuirasse", "cupule", 
    "cure", "cuve", "cybernétique", "cytologie", "dague", "décadence", "décharge", "déchirure", 
    "déclinaison", "déclive", "déconfiture", "découpe", "défaite", "défiguration", "dépouille", 
    "désuétude", "diagonale", "diaphanéité", "dictature", "digue", "dilatation", "disparition", 
    "dissection", "distance", "distorsion", "divination", "dogme", "douleur", "draperie", 
    "dualité", "ductilité", "durée", "ébène", "écorce", "écritoire", "écriture", "effigie", 
    "effraction", "élasticité", "élégie", "ellipse", "émanation", "empathie", "empreinte", 
    "emprise", "émulsion", "enceinte", "enclume", "énergie", "énigme", "entaille", "entité", 
    "entrave", "enveloppe", "enzyme", "épitaphe", "épreuve", "érosion", "errance", "erreur", 
    "esquisse", "essence", "étoffe", "étincelle", "étreinte", "étude", "évocation", "exigence", 
    "existence", "exostose", "expansion", "extase", "extériorité", "extraction", "fable", 
    "façade", "facette", "faille", "falaise", "falsification", "famine", "fêlure", "femme", 
    "fente", "ferraille", "ferveur", "fibre", "fièvre", "figure", "filiation", "fissure", 
    "flamme", "flèche", "fleur", "fluidité", "fluorescence", "fluxion", "folie", "fondation", 
    "fontaine", "force", "forge", "forme", "formule", "fosse", "foudre", "fouille", "foulure", 
    "fracture", "fragilité", "fragmentation", "frange", "frayeur", "friche", "friction", 
    "frivolité", "frontière", "fugue", "fulgurance", "fumée", "fureur", "fusion", "galerie", 
    "gangue", "gêne", "genèse", "géologie", "géométrie", "germination", "gestalt", "gestation", 
    "glace", "glaise", "glissade", "gloire", "glu", "grâce", "gradation", "graphie", "grappe", 
    "gratitude", "gravité", "griffe", "grille", "grimace", "grisaille", "grotte", "guérison", 
    "guilde", "guillotine", "hantise", "harpe", "hâte", "hauteur", "hélice", "herbe", "hérésie", 
    "herse", "heure", "hiérarchie", "histoire", "homélie", "honte", "horreur", "hostilité", 
    "houle", "huile", "humeur", "humidité", "humilité", "hydre", "hymne", "hypnose", "hystérie"
]

# Groupes Nominaux Définis Masc. Pluriel (MP)
GN_MP_BASE = [
    "rituels", "systèmes d'encodage", "appareils", "matériaux et outils", "régimes de visibilité", 
    "protocoles", "dispositifs", "réseaux de neurones", "affects", "objets", "figures de l'altérité", 
    "modes de présence", "gestes de déconstruction", "processus d'indexation", "mécanisms de contrôle", 
    "énoncés", "supports d'enregistrement", "modes d'intermédiation", "acteurs", "codes binaires", 
    "espaces de projection", "indices", "concepts", "régimes d'historicité", "corps", "paradoxes", 
    "schèmes perceptifs", "outils d'analyse", "moments", "vecteurs", "pigments", "métaux", "cristaux", 
    "atomes", "bits", "pixels", "signaux", "éclats", "débris", "ruines", "monuments", "écrans", 
    "câbles", "tubes", "engrenages", "ressorts", "automatismes", "calculs", "algorithmes", "codes", 
    "regards", "visages", "cadavres", "spectres", "miroirs", "reflets", "doubles", "clones", "abrasifs", 
    "aciers", "agrégats", "aimants", "ajustements", "alambics", "aléas", "alvéoles", "amalgames", 
    "ambres", "amidons", "anneaux", "anodes", "antidotes", "appas", "apprêts", "arcanes", "archives", 
    "argents", "armements", "arpents", "artifices", "aspérités", "assemblages", "atours", "attributs", 
    "augures", "avatars", "aveux", "axes", "azimuths", "bagnes", "balanciers", "balayages", "baldaquins", 
    "ballasts", "bandeaux", "banquets", "baptêmes", "barreaux", "bassins", "bâtiments", "battements", 
    "baumes", "beffrois", "berceaux", "besoins", "biais", "bijoux", "bilans", "binoculaires", 
    "blocs", "blasons", "bobinages", "bolides", "bombements", "bonheurs", "bords", "bossages", 
    "boucliers", "bouillons", "boulons", "bouquets", "bourreaux", "boutons", "boyaux", "brancards", 
    "bras", "brasages", "braseros", "brillants", "brins", "broyages", "bruits", "brulots", "brunissements"
]

# Groupes Nominaux Définis Fém. Pluriel (FP)
GN_FP_BASE = [
    "narrations", "données", "archéologies", "dynamiques", "temporalités", "frontières", 
    "conditions de production", "cycles d'information", "écritures", "séries", "instances", 
    "traces", "postures", "logiques", "puissances", "matrices", "conditions d'apparition", 
    "ruptures", "stratégies", "conditions de réception", "matières", "couleurs", "ombres", 
    "fibres", "scories", "cendres", "pierres", "machines", "caméras", "optiques", "lentilles", 
    "archives", "mémoires", "fictions", "vérités", "illusions", "images", "icônes", "idoles", 
    "ondes", "particules", "empreintes", "mues", "peaux", "strates", "abrasions", "absences", 
    "abstractions", "académies", "accélérations", "acclimatations", "acrimonies", "actions", 
    "activités", "adhérences", "admirations", "adresses", "adulations", "affinités", "affres", 
    "agitations", "agonies", "agressions", "aiguilles", "ailes", "aimantations", "ajustures", 
    "alarmes", "alchimies", "algues", "aliénations", "alliances", "allégories", "allures", 
    "alvéoles", "ambitions", "ambres", "amertumes", "amitiés", "amitiés", "amours", "ampoules", 
    "amplitudes", "analogies", "analyses", "anatomies", "ancres", "anecdotes", "angoisses", 
    "animosités", "annales", "annuaires", "anomalies", "antennes", "anticipations", "antiquités", 
    "anxiétés", "apathies", "apocalypses", "apologies", "apparitions", "apparences", "appartenances"
]

# Mapping des GNs de base (inchangé)
GN_BASE_MAP = {}
def map_gn_bases(gn_list, g, n):
    for gn in gn_list: GN_BASE_MAP[gn] = {'g': g, 'n': n}

map_gn_bases(GN_MS_BASE, 'm', 's')
map_gn_bases(GN_FS_BASE, 'f', 's')
map_gn_bases(GN_MP_BASE, 'm', 'p')
map_gn_bases(GN_FP_BASE, 'f', 'p')

GNDefini = list(GN_BASE_MAP.keys())
GNIndefini_Singulier = [gn for gn, info in GN_BASE_MAP.items() if info['n'] == 's']
GNIndefini_Pluriel = [gn for gn, info in GN_BASE_MAP.items() if info['n'] == 'p']
GNIndefini = GNIndefini_Singulier + GNIndefini_Pluriel
GNComplexe = GNDefini

# Sujets spéciaux
GNPersonnel = [{"v": "nous", "n": "p", "g": "m"}, {"v": "on", "n": "s", "g": "m"}]
GNImpersonnel = [{"v": "il", "n": "s", "g": "m"}]
GNPresentatif = [{"v": "il y a", "n": "s", "g": "m"}]

# Verbes Transitifs
GVTransitif = {
    "réorganiser": {"s": "réorganise", "p": "réorganisent"}, "interroger": {"s": "interroge", "p": "interrogent"},
    "activer": {"s": "active", "p": "activent"}, "configurer": {"s": "configure", "p": "configurent"},
    "articuler": {"s": "articule", "p": "articulent"}, "conditionner": {"s": "conditionne", "p": "conditionnent"},
    "inscrire": {"s": "inscrit", "p": "inscrivent"}, "déplacer": {"s": "déplace", "p": "déplacent"},
    "générer": {"s": "génère", "p": "génèrent"}, "produire": {"s": "produit", "p": "produisent"},
    "moduler": {"s": "module", "p": "modulent"}, "stabiliser": {"s": "stabilise", "p": "stabilisent"},
    "indexer": {"s": "indexe", "p": "indexent"}, "transférer": {"s": "transfère", "p": "transfèrent"}, 
    "reformuler": {"s": "reformule", "p": "reforment"}, "encadrer": {"s": "encadre", "p": "encadrent"},
    "intégrer": {"s": "intègre", "p": "intègrent"}, "traduire": {"s": "traduit", "p": "traduisent"},
    "lier": {"s": "lie", "p": "lient"}, "distribuer": {"s": "distribue", "p": "distribuent"},
    "manifester": {"s": "manifeste", "p": "manifestent"}, "saisir": {"s": "saisit", "p": "saisissent"},
    "gérer": {"s": "gère", "p": "gèrent"}, "fonder": {"s": "fonde", "p": "fondent"},
    "actualiser": {"s": "actualise", "p": "actualisent"}, "déconstruire": {"s": "déconstruit", "p": "déconstruisent"},
    "circonscrire": {"s": "circonscrit", "p": "circonscrivent"}, "opacifier": {"s": "opacifie", "p": "opacifient"},
    "contingenter": {"s": "contingente", "p": "contingentent"}, "médiatiser": {"s": "médiatise", "p": "médiatisent"}, 
    "historiciser": {"s": "historicise", "p": "historicisent"}, "cartographier": {"s": "cartographie", "p": "cartographient"}, 
    "dévoiler": {"s": "dévoile", "p": "dévoilent"}, "interpeller": {"s": "interpelle", "p": "interpellent"}, 
    "formaliser": {"s": "formalise", "p": "formalisent"}, "essentialiser": {"s": "essentialise", "p": "essentialisent"}, 
    "paradoxaliser": {"s": "paradoxalise", "p": "paradoxalisent"}, "subjectiviser": {"s": "subjectivise", "p": "subjectivisent"}, 
    "reconfigurer": {"s": "reconfigure", "p": "reconfigurent"}, "subvertir": {"s": "subvertit", "p": "subvertissent"}, 
    "encrypter": {"s": "encrypte", "p": "encryptent"}, "potentialiser": {"s": "potentialise", "p": "potentialisent"}, 
    "problématiser": {"s": "problématise", "p": "problématisent"}, "réifier": {"s": "réifie", "p": "réifient"}, 
    "dénaturaliser": {"s": "dénaturalise", "p": "dénaturalisent"}, "soutenir": {"s": "soutient", "p": "soutiennent"},
    "abraser": {"s": "abrase", "p": "abrasent"}, "calciner": {"s": "calcine", "p": "calcinent"}, 
    "corroder": {"s": "corrode", "p": "corrodent"}, "ciseler": {"s": "cisèle", "p": "cisèlent"},
    "vitrifier": {"s": "vitrifie", "p": "vitrifient"}, "magnétiser": {"s": "magnétise", "p": "magnétisent"},
    "sculpter": {"s": "sculpte", "p": "sculptent"}, "éroder": {"s": "érode", "p": "érodent"},
    "affirmer": {"s": "affirme", "p": "affirment"}, "montrer": {"s": "montre", "p": "montrent"},
    "postuler": {"s": "postule", "p": "postulent"}, "suggérer": {"s": "suggère", "p": "suggèrent"}, "démontrer": {"s": "démontre", "p": "démontrent"},
}

GVAttributif = {
    "être": {"s": "est", "p": "sont"}, "sembler": {"s": "semble", "p": "semblent"},
    "apparaître": {"s": "apparaît", "p": "apparaissent"}, "demeurer": {"s": "demeure", "p": "demeurent"},
    "rester": {"s": "reste", "p": "restent"}, "devenir": {"s": "devient", "p": "deviennent"}, 
}

GVIntransitif = {
    "émerger": {"s": "émerge", "p": "émergent"}, "persister": {"s": "persiste", "p": "persistent"},
    "circuler": {"s": "circule", "p": "circulent"}, "résider": {"s": "réside", "p": "résident"}, 
    "advenir": {"s": "advient", "p": "adviennent"}, "se déployer": {"s": "se déploie", "p": "se déploient"}, 
    "subsister": {"s": "subsiste", "p": "subsistent"}, "opérer": {"s": "opère", "p": "opèrent"},
}

GVIntroductif = GVTransitif
GVModal = {"devoir": {"s": "doit", "p": "doivent"}, "pouvoir": {"s": "peut", "p": "peuvent"}, "falloir": {"s": "faut", "p": "faut"}}
GVConditionnel = {"permettre": {"s": "permettrait", "p": "permettraient"}}
GVReflexifAttributif = {
    "se constituer": {"s": "se constitue", "p": "se constituent"}, "se définir": {"s": "se définit", "p": "se définissent"}, 
    "se manifester": {"s": "se manifeste", "p": "se manifestent"}, "se reconfigurer": {"s": "se reconfigure", "p": "se reconfigurent"},
    "s'inscrire": {"s": "s'inscrit", "p": "s'inscrivent"}, "s'avérer": {"s": "s'avère", "p": "s'avèrent"}, 
    "se déployer": GVIntransitif["se déployer"],
}

GVModalPersonal = {"devoir": GVModal["devoir"], "pouvoir": GVModal["pouvoir"]}
GVModalImpersonal = {"falloir": GVModal["falloir"]}

# Verbes Passifs et Infinitifs
VERBES_PASSIFS = { 
    "conditionner": "conditionné", "intégrer": "intégré", "structurer": "structuré", "archiver": "archivé", "analyser": "analysé", 
    "transférer": "transféré", "distribuer": "distribué", "moduler": "modulé", "gérer": "géré", 
    "produire": "produit", "lier": "lié", "médiatiser": "médiatisé", "historiciser": "historicisé", 
    "cartographier": "cartographié", "dévoiler": "dévoilé", "formaliser": "formalisé", 
    "problématiser": "problématisé", "réifier": "réifié", "circonscrire": "circonscrit", 
    "déconstruire": "déconstruit", "subvertir": "subverti", "abraser": "abrasé", "vitrifier": "vitrifié"
}
GVPassif = {k: v for k, v in VERBES_PASSIFS.items()}
GVInfinitifTransitif = list(GVTransitif.keys())
GVInfinitifIntransitif = list(GVIntransitif.keys())
GVInfinitif = GVInfinitifTransitif + GVInfinitifIntransitif

# Liste des conjugaisons 'nous'
GV_PERSONNEL_NOUS_EXPLICIT = {
    k: v["p"].replace("ent", "ons") for k, v in GVTransitif.items() if "p" in v
}
GV_PERSONNEL_NOUS_EXPLICIT.update({
    "être": "sommes", "devenir": "devenons", "avoir": "avons", "pouvoir": "pouvons", "devoir": "devons"
})

# Dictionnaire Morphologique des Adjectifs (Expansion massive)
ADJ_MORPHOLOGY = {
    "ambivalent": {"m": {"s": "ambivalent", "p": "ambivalents"}, "f": {"s": "ambivalente", "p": "ambivalentes"}},
    "latent": {"m": {"s": "latent", "p": "latents"}, "f": {"s": "latente", "p": "latentes"}},
    "contingent": {"m": {"s": "contingent", "p": "contingents"}, "f": {"s": "contingente", "p": "contingentes"}},
    "critique": {"m": {"s": "critique", "p": "critiques"}, "f": {"s": "critique", "p": "critiques"}},
    "dialectique": {"m": {"s": "dialectique", "p": "dialectiques"}, "f": {"s": "dialectique", "p": "dialectiques"}},
    "paradoxal": {"m": {"s": "paradoxal", "p": "paradoxaux"}, "f": {"s": "paradoxale", "p": "paradoxales"}},
    "spectral": {"m": {"s": "spectral", "p": "spectraux"}, "f": {"s": "spectrale", "p": "spectrales"}},
    "haptique": {"m": {"s": "haptique", "p": "haptiques"}, "f": {"s": "haptique", "p": "haptiques"}},
    "liminal": {"m": {"s": "liminal", "p": "liminaux"}, "f": {"s": "liminale", "p": "liminales"}},
    "granulaire": {"m": {"s": "granulaire", "p": "granulaires"}, "f": {"s": "granulaire", "p": "granulaires"}},
    "métallique": {"m": {"s": "métallique", "p": "métalliques"}, "f": {"s": "métallique", "p": "métalliques"}},
    "oxydé": {"m": {"s": "oxydé", "p": "oxydés"}, "f": {"s": "oxydée", "p": "oxydées"}},
    "bitumineux": {"m": {"s": "bitumineux", "p": "bitumineux"}, "f": {"s": "bitumineuse", "p": "bitumineuses"}},
    "amarante": {"m": {"s": "amarante", "p": "amarantes"}, "f": {"s": "amarante", "p": "amarantes"}},
    "opaque": {"m": {"s": "opaque", "p": "opaques"}, "f": {"s": "opaque", "p": "opaques"}},
    "diaphane": {"m": {"s": "diaphane", "p": "diaphanes"}, "f": {"s": "diaphane", "p": "diaphanes"}},
    "cathodique": {"m": {"s": "cathodique", "p": "cathodiques"}, "f": {"s": "cathodique", "p": "cathodiques"}},
    "visqueux": {"m": {"s": "visqueux", "p": "visqueux"}, "f": {"s": "visqueuse", "p": "visqueuses"}},
    "numérique": {"m": {"s": "numérique", "p": "numériques"}, "f": {"s": "numérique", "p": "numériques"}},
    "obsolète": {"m": {"s": "obsolète", "p": "obsolètes"}, "f": {"s": "obsolète", "p": "obsolètes"}},
    "vitrifié": {"m": {"s": "vitrifié", "p": "vitrifiés"}, "f": {"s": "vitrifiée", "p": "vitrifiées"}},
    "abject": {"m": {"s": "abject", "p": "abjects"}, "f": {"s": "abjecte", "p": "abjectes"}},
    "abrupt": {"m": {"s": "abrupt", "p": "abrupts"}, "f": {"s": "abrupte", "p": "abruptes"}},
    "abscons": {"m": {"s": "abscons", "p": "abscons"}, "f": {"s": "absconse", "p": "absconses"}},
    "acerbe": {"m": {"s": "acerbe", "p": "acerbes"}, "f": {"s": "acerbe", "p": "acerbes"}},
    "acide": {"m": {"s": "acide", "p": "acides"}, "f": {"s": "acide", "p": "acides"}},
    "acéré": {"m": {"s": "acéré", "p": "acérés"}, "f": {"s": "acérée", "p": "acérées"}},
    "adamantin": {"m": {"s": "adamantin", "p": "adamantins"}, "f": {"s": "adamantine", "p": "adamantines"}},
    "adroit": {"m": {"s": "adroit", "p": "adroits"}, "f": {"s": "adroite", "p": "adroites"}},
    "advenu": {"m": {"s": "advenu", "p": "advenus"}, "f": {"s": "advenue", "p": "advenues"}},
    "aérien": {"m": {"s": "aérien", "p": "aériens"}, "f": {"s": "aérienne", "p": "aériennes"}},
    "affable": {"m": {"s": "affable", "p": "affables"}, "f": {"s": "affable", "p": "affables"}},
    "affecté": {"m": {"s": "affecté", "p": "affectés"}, "f": {"s": "affectée", "p": "affectées"}},
    "affuté": {"m": {"s": "affuté", "p": "affutés"}, "f": {"s": "affutée", "p": "affutées"}},
    "agile": {"m": {"s": "agile", "p": "agiles"}, "f": {"s": "agile", "p": "agiles"}},
    "agité": {"m": {"s": "agité", "p": "agités"}, "f": {"s": "agitée", "p": "agitées"}},
    "agonisant": {"m": {"s": "agonisant", "p": "agonisants"}, "f": {"s": "agonisante", "p": "agonisantes"}},
    "agraire": {"m": {"s": "agraire", "p": "agraires"}, "f": {"s": "agraire", "p": "agraires"}},
    "aimanté": {"m": {"s": "aimanté", "p": "aimantés"}, "f": {"s": "aimantée", "p": "aimantées"}},
    "aisé": {"m": {"s": "aisé", "p": "aisés"}, "f": {"s": "aisée", "p": "aisées"}},
    "albâtre": {"m": {"s": "albâtre", "p": "albâtres"}, "f": {"s": "albâtre", "p": "albâtres"}},
    "alchimique": {"m": {"s": "alchimique", "p": "alchimiques"}, "f": {"s": "alchimique", "p": "alchimiques"}},
    "aléatoire": {"m": {"s": "aléatoire", "p": "aléatoires"}, "f": {"s": "aléatoire", "p": "aléatoires"}},
    "alenti": {"m": {"s": "alenti", "p": "alentis"}, "f": {"s": "alentie", "p": "alenties"}},
    "aliéné": {"m": {"s": "aliéné", "p": "aliénés"}, "f": {"s": "aliénée", "p": "aliénées"}},
    "aligné": {"m": {"s": "aligné", "p": "alignés"}, "f": {"s": "alignée", "p": "alignées"}},
    "allègre": {"m": {"s": "allègre", "p": "allègres"}, "f": {"s": "allègre", "p": "allègres"}},
    "allongé": {"m": {"s": "allongé", "p": "allongés"}, "f": {"s": "allongée", "p": "allongées"}},
    "alluvial": {"m": {"s": "alluvial", "p": "alluviaux"}, "f": {"s": "alluviale", "p": "alluviales"}},
    "alourdi": {"m": {"s": "alourdi", "p": "alourdis"}, "f": {"s": "alourdie", "p": "alourdies"}},
    "altier": {"m": {"s": "altier", "p": "altiers"}, "f": {"s": "altière", "p": "altières"}},
    "altéré": {"m": {"s": "altéré", "p": "altérés"}, "f": {"s": "altérée", "p": "altérées"}},
    "alvéolé": {"m": {"s": "alvéolé", "p": "alvéolés"}, "f": {"s": "alvéolée", "p": "alvéolées"}},
    "amalgamé": {"m": {"s": "amalgamé", "p": "amalgamés"}, "f": {"s": "amalgamée", "p": "amalgamées"}},
    "amande": {"m": {"s": "amande", "p": "amandes"}, "f": {"s": "amande", "p": "amandes"}},
    "ambiant": {"m": {"s": "ambiant", "p": "ambiants"}, "f": {"s": "ambiante", "p": "ambiantes"}},
    "ambigu": {"m": {"s": "ambigu", "p": "ambigus"}, "f": {"s": "ambigüe", "p": "ambigües"}},
    "ambré": {"m": {"s": "ambré", "p": "ambrés"}, "f": {"s": "ambrée", "p": "ambrées"}},
    "amorphe": {"m": {"s": "amorphe", "p": "amorphes"}, "f": {"s": "amorphe", "p": "amorphes"}},
    "amorti": {"m": {"s": "amorti", "p": "amortis"}, "f": {"s": "amortie", "p": "amorties"}},
    "ample": {"m": {"s": "ample", "p": "amples"}, "f": {"s": "ample", "p": "amples"}},
    "amplifié": {"m": {"s": "amplifié", "p": "amplifiés"}, "f": {"s": "amplifiée", "p": "amplifiées"}},
    "ampoulé": {"m": {"s": "ampoulé", "p": "ampoulés"}, "f": {"s": "ampoulée", "p": "ampoulées"}},
    "amputé": {"m": {"s": "amputé", "p": "amputés"}, "f": {"s": "amputée", "p": "amputées"}},
    "amusé": {"m": {"s": "amusé", "p": "amusés"}, "f": {"s": "amusée", "p": "amusées"}},
    "anachronique": {"m": {"s": "anachronique", "p": "anachroniques"}, "f": {"s": "anachronique", "p": "anachroniques"}},
    "analytique": {"m": {"s": "analytique", "p": "analytiques"}, "f": {"s": "analytique", "p": "analytiques"}},
    "ancestral": {"m": {"s": "ancestral", "p": "ancestraux"}, "f": {"s": "ancestrale", "p": "ancestrales"}},
    "ancien": {"m": {"s": "ancien", "p": "anciens"}, "f": {"s": "ancienne", "p": "anciennes"}},
    "anecdotique": {"m": {"s": "anecdotique", "p": "anecdotiques"}, "f": {"s": "anecdotique", "p": "anecdotiques"}},
    "anéanti": {"m": {"s": "anéanti", "p": "anéantis"}, "f": {"s": "anéantie", "p": "anéanties"}},
    "angulaire": {"m": {"s": "angulaire", "p": "angulaires"}, "f": {"s": "angulaire", "p": "angulaires"}},
    "angusticlave": {"m": {"s": "angusticlave", "p": "angusticlaves"}, "f": {"s": "angusticlave", "p": "angusticlaves"}},
    "animal": {"m": {"s": "animal", "p": "animaux"}, "f": {"s": "animale", "p": "animales"}},
    "animé": {"m": {"s": "animé", "p": "animés"}, "f": {"s": "animée", "p": "animées"}},
    "annulaire": {"m": {"s": "annulaire", "p": "annulaires"}, "f": {"s": "annulaire", "p": "annulaires"}},
    "anobli": {"m": {"s": "anobli", "p": "anoblis"}, "f": {"s": "anoblie", "p": "anoblies"}},
    "anodin": {"m": {"s": "anodin", "p": "anodins"}, "f": {"s": "anodine", "p": "anodines"}},
    "anomal": {"m": {"s": "anomal", "p": "anomaux"}, "f": {"s": "anomale", "p": "anomales"}},
    "anonyme": {"m": {"s": "anonyme", "p": "anonymes"}, "f": {"s": "anonyme", "p": "anonymes"}},
    "anorganique": {"m": {"s": "anorganique", "p": "anorganiques"}, "f": {"s": "anorganique", "p": "anorganiques"}},
    "anormal": {"m": {"s": "anormal", "p": "anormaux"}, "f": {"s": "anormale", "p": "anormales"}},
    "antédiluvien": {"m": {"s": "antédiluvien", "p": "antédiluviens"}, "f": {"s": "antédiluvienne", "p": "antédiluviennes"}},
    "antérieur": {"m": {"s": "antérieur", "p": "antérieurs"}, "f": {"s": "antérieure", "p": "antérieures"}},
    "anthropomorphe": {"m": {"s": "anthropomorphe", "p": "anthropomorphes"}, "f": {"s": "anthropomorphe", "p": "anthropomorphes"}},
    "antique": {"m": {"s": "antique", "p": "antiques"}, "f": {"s": "antique", "p": "antiques"}},
    "apathique": {"m": {"s": "apathique", "p": "apathiques"}, "f": {"s": "apathique", "p": "apathiques"}},
    "aperturé": {"m": {"s": "aperturé", "p": "aperturés"}, "f": {"s": "aperturée", "p": "aperturées"}},
    "apocalyptique": {"m": {"s": "apocalyptique", "p": "apocalyptiques"}, "f": {"s": "apocalyptique", "p": "apocalyptiques"}},
    "apocryphe": {"m": {"s": "apocryphe", "p": "apocryphes"}, "f": {"s": "apocryphe", "p": "apocryphes"}},
    "apollinien": {"m": {"s": "apollinien", "p": "apolliniens"}, "f": {"s": "apollinienne", "p": "apolliniennes"}},
    "apostat": {"m": {"s": "apostat", "p": "apostats"}, "f": {"s": "apostate", "p": "apostates"}},
    "apparent": {"m": {"s": "apparent", "p": "apparents"}, "f": {"s": "apparente", "p": "apparentes"}},
    "appauvri": {"m": {"s": "appauvri", "p": "appauvris"}, "f": {"s": "appauvrie", "p": "appauvries"}},
    "appelé": {"m": {"s": "appelé", "p": "appelés"}, "f": {"s": "appelée", "p": "appelées"}},
    "appesanti": {"m": {"s": "appesanti", "p": "appesantis"}, "f": {"s": "appesantie", "p": "appesanties"}},
    "appliqué": {"m": {"s": "appliqué", "p": "appliqués"}, "f": {"s": "appliquée", "p": "appliquées"}},
    "apprécié": {"m": {"s": "apprécié", "p": "appréciés"}, "f": {"s": "appréciée", "p": "appréciées"}},
    "apprivoisé": {"m": {"s": "apprivoisé", "p": "apprivoisés"}, "f": {"s": "apprivoisée", "p": "apprivoisées"}},
    "approché": {"m": {"s": "approché", "p": "approchés"}, "f": {"s": "approchée", "p": "approchées"}},
    "approprié": {"m": {"s": "approprié", "p": "appropriés"}, "f": {"s": "appropriée", "p": "appropriées"}},
    "appuyé": {"m": {"s": "appuyé", "p": "appuyés"}, "f": {"s": "appuyée", "p": "appuyées"}},
    "apre": {"m": {"s": "apre", "p": "apres"}, "f": {"s": "apre", "p": "apres"}},
    "apte": {"m": {"s": "apte", "p": "aptes"}, "f": {"s": "apte", "p": "aptes"}},
    "aquatique": {"m": {"s": "aquatique", "p": "aquatiques"}, "f": {"s": "aquatique", "p": "aquatiques"}},
    "aqueux": {"m": {"s": "aqueux", "p": "aqueux"}, "f": {"s": "aqueuse", "p": "aqueuses"}},
    "aquilin": {"m": {"s": "aquilin", "p": "aquilins"}, "f": {"s": "aquiline", "p": "aquilines"}},
    "arabe": {"m": {"s": "arabe", "p": "arabes"}, "f": {"s": "arabe", "p": "arabes"}},
    "arabesque": {"m": {"s": "arabesque", "p": "arabesques"}, "f": {"s": "arabesque", "p": "arabesques"}},
    "aratoire": {"m": {"s": "aratoire", "p": "aratoires"}, "f": {"s": "aratoire", "p": "aratoires"}},
    "arbitraire": {"m": {"s": "arbitraire", "p": "arbitraires"}, "f": {"s": "arbitraire", "p": "arbitraires"}},
    "arborescent": {"m": {"s": "arborescent", "p": "arborescents"}, "f": {"s": "arborescente", "p": "arborescentes"}},
    "arbustif": {"m": {"s": "arbustif", "p": "arbustifs"}, "f": {"s": "arbustive", "p": "arbustives"}},
    "arcadien": {"m": {"s": "arcadien", "p": "arcadiens"}, "f": {"s": "arcadienne", "p": "arcadiennes"}},
    "archaique": {"m": {"s": "archaique", "p": "archaiques"}, "f": {"s": "archaique", "p": "archaiques"}},
    "archangélique": {"m": {"s": "archangélique", "p": "archangéliques"}, "f": {"s": "archangélique", "p": "archangéliques"}},
    "archetypal": {"m": {"s": "archetypal", "p": "archetypaux"}, "f": {"s": "archetypale", "p": "archetypales"}},
    "architectonique": {"m": {"s": "architectonique", "p": "architectoniques"}, "f": {"s": "architectonique", "p": "architectoniques"}},
    "architectural": {"m": {"s": "architectural", "p": "architecturaux"}, "f": {"s": "architecturale", "p": "architecturales"}},
    "archivé": {"m": {"s": "archivé", "p": "archivés"}, "f": {"s": "archivée", "p": "archivées"}},
    "arctique": {"m": {"s": "arctique", "p": "arctiques"}, "f": {"s": "arctique", "p": "arctiques"}},
    "ardent": {"m": {"s": "ardent", "p": "ardents"}, "f": {"s": "ardente", "p": "ardentes"}},
    "ardoisé": {"m": {"s": "ardoisé", "p": "ardoisés"}, "f": {"s": "ardoisée", "p": "ardoisées"}},
    "ardu": {"m": {"s": "ardu", "p": "ardus"}, "f": {"s": "ardue", "p": "ardues"}},
    "argental": {"m": {"s": "argental", "p": "argentaux"}, "f": {"s": "argentale", "p": "argentales"}},
    "argenté": {"m": {"s": "argenté", "p": "argentés"}, "f": {"s": "argentée", "p": "argentées"}},
    "argileux": {"m": {"s": "argileux", "p": "argileux"}, "f": {"s": "argileuse", "p": "argileuses"}},
    "aride": {"m": {"s": "aride", "p": "arides"}, "f": {"s": "aride", "p": "arides"}},
    "aristocratique": {"m": {"s": "aristocratique", "p": "aristocratiques"}, "f": {"s": "aristocratique", "p": "aristocratiques"}},
    "armé": {"m": {"s": "armé", "p": "armés"}, "f": {"s": "armée", "p": "armées"}},
    "aromatique": {"m": {"s": "aromatique", "p": "aromatiques"}, "f": {"s": "aromatique", "p": "aromatiques"}},
    "arpenté": {"m": {"s": "arpenté", "p": "arpentés"}, "f": {"s": "arpentée", "p": "arpentées"}},
    "arqué": {"m": {"s": "arqué", "p": "arqués"}, "f": {"s": "arquée", "p": "arquées"}},
    "arraché": {"m": {"s": "arraché", "p": "arrachés"}, "f": {"s": "arrachée", "p": "arrachées"}},
    "arrangé": {"m": {"s": "arrangé", "p": "arrangés"}, "f": {"s": "arrangée", "p": "arrangées"}},
    "arrêté": {"m": {"s": "arrêté", "p": "arrêtés"}, "f": {"s": "arrêtée", "p": "arrêtées"}},
    "arrière": {"m": {"s": "arrière", "p": "arrière"}, "f": {"s": "arrière", "p": "arrière"}},
    "arrivé": {"m": {"s": "arrivé", "p": "arrivés"}, "f": {"s": "arrivée", "p": "arrivées"}},
    "arrogant": {"m": {"s": "arrogant", "p": "arrogants"}, "f": {"s": "arrogante", "p": "arrogantes"}},
    "arrondi": {"m": {"s": "arrondi", "p": "arrondis"}, "f": {"s": "arrondie", "p": "arrondies"}},
    "arrosé": {"m": {"s": "arrosé", "p": "arrosés"}, "f": {"s": "arrosée", "p": "arrosées"}},
    "arsenical": {"m": {"s": "arsenical", "p": "arsenicaux"}, "f": {"s": "arsenicale", "p": "arsenicales"}},
    "artériel": {"m": {"s": "artériel", "p": "artériels"}, "f": {"s": "artérielle", "p": "artérielles"}},
    "articulé": {"m": {"s": "articulé", "p": "articulés"}, "f": {"s": "articulée", "p": "articulées"}},
    "artificiel": {"m": {"s": "artificiel", "p": "artificiels"}, "f": {"s": "artificielle", "p": "artificielles"}},
    "artisanal": {"m": {"s": "artisanal", "p": "artisanaux"}, "f": {"s": "artisanale", "p": "artisanales"}},
    "artistique": {"m": {"s": "artistique", "p": "artistiques"}, "f": {"s": "artistique", "p": "artistiques"}},
    "arythmique": {"m": {"s": "arythmique", "p": "arythmiques"}, "f": {"s": "arythmique", "p": "arythmiques"}},
    "ascendant": {"m": {"s": "ascendant", "p": "ascendants"}, "f": {"s": "ascendante", "p": "ascendantes"}},
    "ascétique": {"m": {"s": "ascétique", "p": "ascétiques"}, "f": {"s": "ascétique", "p": "ascétiques"}},
    "aseptique": {"m": {"s": "aseptique", "p": "aseptiques"}, "f": {"s": "aseptique", "p": "aseptiques"}},
    "asexué": {"m": {"s": "asexué", "p": "asexués"}, "f": {"s": "asexuée", "p": "asexuées"}},
    "asocial": {"m": {"s": "asocial", "p": "asociaux"}, "f": {"s": "asociale", "p": "asociales"}},
    "aspectuel": {"m": {"s": "aspectuel", "p": "aspectuels"}, "f": {"s": "aspectuelle", "p": "aspectuelles"}},
    "asphyxié": {"m": {"s": "asphyxié", "p": "asphyxiés"}, "f": {"s": "asphyxiée", "p": "asphyxiées"}},
    "aspirant": {"m": {"s": "aspirant", "p": "aspirants"}, "f": {"s": "aspirante", "p": "aspirantes"}},
    "aspiré": {"m": {"s": "aspiré", "p": "aspirés"}, "f": {"s": "aspirée", "p": "aspirées"}},
    "assemblé": {"m": {"s": "assemblé", "p": "assemblés"}, "f": {"s": "assemblée", "p": "assemblées"}},
    "asservi": {"m": {"s": "asservi", "p": "asservis"}, "f": {"s": "asservie", "p": "asservies"}},
    "assidu": {"m": {"s": "assidu", "p": "assidus"}, "f": {"s": "assidue", "p": "assidues"}},
    "assimilé": {"m": {"s": "assimilé", "p": "assimilés"}, "f": {"s": "assimilée", "p": "assimilées"}},
    "assis": {"m": {"s": "assis", "p": "assis"}, "f": {"s": "assise", "p": "assises"}},
    "associé": {"m": {"s": "associé", "p": "associés"}, "f": {"s": "associée", "p": "associées"}},
    "assombri": {"m": {"s": "assombri", "p": "assombris"}, "f": {"s": "assombrie", "p": "assombries"}},
    "assommant": {"m": {"s": "assommant", "p": "assommants"}, "f": {"s": "assommante", "p": "assommantes"}},
    "assorti": {"m": {"s": "assorti", "p": "assortis"}, "f": {"s": "assortie", "p": "assorties"}},
    "assoupi": {"m": {"s": "assoupi", "p": "assoupis"}, "f": {"s": "assoupie", "p": "assoupies"}},
    "assourdi": {"m": {"s": "assourdi", "p": "assourdis"}, "f": {"s": "assourdie", "p": "assourdies"}},
    "assouvi": {"m": {"s": "assouvi", "p": "assouvis"}, "f": {"s": "assouvie", "p": "assouvies"}},
    "assujetti": {"m": {"s": "assujetti", "p": "assujettis"}, "f": {"s": "assujettie", "p": "assujetties"}},
    "assumé": {"m": {"s": "assumé", "p": "assumés"}, "f": {"s": "assumée", "p": "assumées"}},
    "assuré": {"m": {"s": "assuré", "p": "assurés"}, "f": {"s": "assurée", "p": "assurées"}},
    "astral": {"m": {"s": "astral", "p": "astraux"}, "f": {"s": "astrale", "p": "astrales"}},
    "astrologique": {"m": {"s": "astrologique", "p": "astrologiques"}, "f": {"s": "astrologique", "p": "astrologiques"}},
    "astronomique": {"m": {"s": "astronomique", "p": "astronomiques"}, "f": {"s": "astronomique", "p": "astronomiques"}},
    "astucieux": {"m": {"s": "astucieux", "p": "astucieux"}, "f": {"s": "astucieuse", "p": "astucieuses"}},
    "asymétrique": {"m": {"s": "asymétrique", "p": "asymétriques"}, "f": {"s": "asymétrique", "p": "asymétriques"}},
    "atavique": {"m": {"s": "atavique", "p": "ataviques"}, "f": {"s": "atavique", "p": "ataviques"}},
    "atemporel": {"m": {"s": "atemporel", "p": "atemporels"}, "f": {"s": "atemporelle", "p": "atemporelles"}},
    "athée": {"m": {"s": "athée", "p": "athées"}, "f": {"s": "athée", "p": "athées"}},
    "atlantique": {"m": {"s": "atlantique", "p": "atlantiques"}, "f": {"s": "atlantique", "p": "atlantiques"}},
    "atomique": {"m": {"s": "atomique", "p": "atomiques"}, "f": {"s": "atomique", "p": "atomiques"}},
    "atonal": {"m": {"s": "atonal", "p": "atonaux"}, "f": {"s": "atonale", "p": "atonales"}},
    "atone": {"m": {"s": "atone", "p": "atones"}, "f": {"s": "atone", "p": "atones"}},
    "atrabilaire": {"m": {"s": "atrabilaire", "p": "atrabilaires"}, "f": {"s": "atrabilaire", "p": "atrabilaires"}},
    "atroce": {"m": {"s": "atroce", "p": "atroces"}, "f": {"s": "atroce", "p": "atroces"}},
    "atrophique": {"m": {"s": "atrophique", "p": "atrophiques"}, "f": {"s": "atrophique", "p": "atrophiques"}},
    "attaché": {"m": {"s": "attaché", "p": "attachés"}, "f": {"s": "attachée", "p": "attachées"}},
    "attaqué": {"m": {"s": "attaqué", "p": "attaqués"}, "f": {"s": "attaquée", "p": "attaquées"}},
    "attardé": {"m": {"s": "attardé", "p": "attardés"}, "f": {"s": "attardée", "p": "attardées"}},
    "atteint": {"m": {"s": "atteint", "p": "atteints"}, "f": {"s": "atteinte", "p": "atteintes"}},
    "attentif": {"m": {"s": "attentif", "p": "attentifs"}, "f": {"s": "attentive", "p": "attentives"}},
    "atténué": {"m": {"s": "atténué", "p": "atténués"}, "f": {"s": "atténuée", "p": "atténuées"}},
    "attitré": {"m": {"s": "attitré", "p": "attitrés"}, "f": {"s": "attitré", "p": "attitré"}},
    "attractif": {"m": {"s": "attractif", "p": "attractifs"}, "f": {"s": "attractive", "p": "attractives"}},
    "attrayant": {"m": {"s": "attrayant", "p": "attrayants"}, "f": {"s": "attrayante", "p": "attrayantes"}},
    "attribué": {"m": {"s": "attribué", "p": "attribués"}, "f": {"s": "attribuée", "p": "attribuées"}},
    "atypique": {"m": {"s": "atypique", "p": "atypiques"}, "f": {"s": "atypique", "p": "atypiques"}},
    "auburn": {"m": {"s": "auburn", "p": "auburn"}, "f": {"s": "auburn", "p": "auburn"}},
    "audacieux": {"m": {"s": "audacieux", "p": "audacieux"}, "f": {"s": "audacieuse", "p": "audacieuses"}},
    "au-delà": {"m": {"s": "au-delà", "p": "au-delà"}, "f": {"s": "au-delà", "p": "au-delà"}},
    "audiovisuel": {"m": {"s": "audiovisuel", "p": "audiovisuels"}, "f": {"s": "audiovisuelle", "p": "audiovisuelles"}},
    "auditif": {"m": {"s": "auditif", "p": "auditifs"}, "f": {"s": "auditive", "p": "auditives"}},
    "augmenté": {"m": {"s": "augmenté", "p": "augmentés"}, "f": {"s": "augmentée", "p": "augmentées"}},
    "auguste": {"m": {"s": "auguste", "p": "augustes"}, "f": {"s": "auguste", "p": "augustes"}},
    "aurifère": {"m": {"s": "aurifère", "p": "aurifères"}, "f": {"s": "aurifère", "p": "aurifères"}},
    "auroral": {"m": {"s": "auroral", "p": "auroraux"}, "f": {"s": "aurorale", "p": "aurorales"}},
    "austère": {"m": {"s": "austère", "p": "austères"}, "f": {"s": "austère", "p": "austères"}},
    "austral": {"m": {"s": "austral", "p": "austraux"}, "f": {"s": "australe", "p": "australes"}},
    "authentique": {"m": {"s": "authentique", "p": "authentiques"}, "f": {"s": "authentique", "p": "authentiques"}},
    "autiste": {"m": {"s": "autiste", "p": "autistes"}, "f": {"s": "autiste", "p": "autistes"}},
    "autobiographique": {"m": {"s": "autobiographique", "p": "autobiographiques"}, "f": {"s": "autobiographique", "p": "autobiographiques"}},
    "autocéphale": {"m": {"s": "autocéphale", "p": "autocéphales"}, "f": {"s": "autocéphale", "p": "autocéphales"}},
    "autochtone": {"m": {"s": "autochtone", "p": "autochtones"}, "f": {"s": "autochtone", "p": "autochtones"}},
    "autocrate": {"m": {"s": "autocrate", "p": "autocrates"}, "f": {"s": "autocrate", "p": "autocrates"}},
    "autocritique": {"m": {"s": "autocritique", "p": "autocritiques"}, "f": {"s": "autocritique", "p": "autocritiques"}},
    "autodidacte": {"m": {"s": "autodidacte", "p": "autodidactes"}, "f": {"s": "autodidacte", "p": "autodidactes"}},
    "autogène": {"m": {"s": "autogène", "p": "autogènes"}, "f": {"s": "autogène", "p": "autogènes"}},
    "automate": {"m": {"s": "automate", "p": "automates"}, "f": {"s": "automate", "p": "automate"}},
    "automatique": {"m": {"s": "automatique", "p": "automatiques"}, "f": {"s": "automatique", "p": "automatiques"}},
    "automnal": {"m": {"s": "automnal", "p": "automnaux"}, "f": {"s": "automnale", "p": "automnales"}},
    "autonome": {"m": {"s": "autonome", "p": "autonomes"}, "f": {"s": "autonome", "p": "autonomes"}},
    "autoportrait": {"m": {"s": "autoportrait", "p": "autoportraits"}, "f": {"s": "autoportrait", "p": "autoportrait"}},
    "autorisé": {"m": {"s": "autorisé", "p": "autorisés"}, "f": {"s": "autorisée", "p": "autorisées"}},
    "autoritaire": {"m": {"s": "autoritaire", "p": "autoritaires"}, "f": {"s": "autoritaire", "p": "autoritaires"}},
    "autour": {"m": {"s": "autour", "p": "autour"}, "f": {"s": "autour", "p": "autour"}},
    "autre": {"m": {"s": "autre", "p": "autres"}, "f": {"s": "autre", "p": "autres"}},
    "auxiliaire": {"m": {"s": "auxiliaire", "p": "auxiliaires"}, "f": {"s": "auxiliaire", "p": "auxiliaires"}},
    "avalé": {"m": {"s": "avalé", "p": "avalés"}, "f": {"s": "avalée", "p": "avalées"}},
    "avancé": {"m": {"s": "avancé", "p": "avancés"}, "f": {"s": "avancée", "p": "avancées"}},
    "avant": {"m": {"s": "avant", "p": "avant"}, "f": {"s": "avant", "p": "avant"}},
    "avant-gardiste": {"m": {"s": "avant-gardiste", "p": "avant-gardistes"}, "f": {"s": "avant-gardiste", "p": "avant-gardiste"}},
    "avare": {"m": {"s": "avare", "p": "avares"}, "f": {"s": "avare", "p": "avares"}},
    "avarié": {"m": {"s": "avarié", "p": "avariés"}, "f": {"s": "avariée", "p": "avariées"}},
    "avatar": {"m": {"s": "avatar", "p": "avatars"}, "f": {"s": "avatar", "p": "avatar"}},
    "avenant": {"m": {"s": "avenant", "p": "avenants"}, "f": {"s": "avenante", "p": "avenantes"}},
    "aventureux": {"m": {"s": "aventureux", "p": "aventureux"}, "f": {"s": "aventureuse", "p": "aventureuses"}},
    "avéré": {"m": {"s": "avéré", "p": "avérés"}, "f": {"s": "avérée", "p": "avérées"}},
    "aveugle": {"m": {"s": "aveugle", "p": "aveugles"}, "f": {"s": "aveugle", "p": "aveugles"}},
    "aveuglant": {"m": {"s": "aveuglant", "p": "aveuglants"}, "f": {"s": "aveuglante", "p": "aveuglantes"}},
    "avide": {"m": {"s": "avide", "p": "avides"}, "f": {"s": "avide", "p": "avides"}},
    "avili": {"m": {"s": "avili", "p": "avilis"}, "f": {"s": "avilie", "p": "avilies"}},
    "aviné": {"m": {"s": "aviné", "p": "avinés"}, "f": {"s": "avinée", "p": "avinées"}},
    "avisé": {"m": {"s": "avisé", "p": "avisés"}, "f": {"s": "avisée", "p": "avisées"}},
    "avoué": {"m": {"s": "avoué", "p": "avoués"}, "f": {"s": "avouée", "p": "avouées"}},
    "axial": {"m": {"s": "axial", "p": "axiaux"}, "f": {"s": "axiale", "p": "axiales"}},
    "axiomatique": {"m": {"s": "axiomatique", "p": "axiomatiques"}, "f": {"s": "axiomatique", "p": "axiomatiques"}},
    "azimut": {"m": {"s": "azimut", "p": "azimuts"}, "f": {"s": "azimut", "p": "azimut"}},
    "azur": {"m": {"s": "azur", "p": "azurs"}, "f": {"s": "azur", "p": "azur"}},
    "azuré": {"m": {"s": "azuré", "p": "azurés"}, "f": {"s": "azurée", "p": "azurées"}},
}

# (Note: Les boucles de création de listes ADJ_MS, FS, etc. restent inchangées)
ADJ_MS = []
ADJ_FS = []
ADJ_MP = []
ADJ_FP = []

for base, forms in ADJ_MORPHOLOGY.items():
    if forms['m']['s'] not in ADJ_MS: ADJ_MS.append(forms['m']['s'])
    if forms['f']['s'] not in ADJ_FS: ADJ_FS.append(forms['f']['s'])
    if forms['m']['p'] not in ADJ_MP: ADJ_MP.append(forms['m']['p'])
    if forms['f']['p'] not in ADJ_FP: ADJ_FP.append(forms['f']['p'])

# Adverbes et connecteurs (inchangés)
AdvConnecteur = ["De plus", "Par ailleurs", "En outre", "Dès lors", "Toutefois", "Néanmoins", 
                  "De surcroît", "Nonobstant", "Ainsi", "Également"]
Coordination = ["Or", "De fait", "Aussi", "Cependant", "Inversement", "De ce fait"]
AdvArgumentatif = ["En définitive", "Fondamentalement", "En ce sens", "De manière intrinsèque", 
                   "Subsidiairement", "Globalement", "Épistémologiquement parlant"]
CONNECTEUR_FIX = AdvConnecteur + Coordination + AdvArgumentatif

# Variable globale pour l'anaphore
LAST_GN_INFO = None

# ===================================================================
# --- SECTION 2: FONCTIONS GRAMMATICALES V35 (MISES À JOUR) ---
# ===================================================================

def accorder_attribut(attribut_base, sujet_g, sujet_n):
    """Accorde un attribut adjectival ou un participe passé (V35)."""
    if attribut_base in ADJ_MORPHOLOGY:
        try:
            return ADJ_MORPHOLOGY[attribut_base][sujet_g][sujet_n]
        except KeyError:
            pass
            
    attribut = attribut_base
    if sujet_g == 'f' and not attribut.endswith(('e', 'x', 's', 't')): 
        attribut = attribut + ('e' if not attribut.endswith('é') else 'ée')
    if sujet_n == 'p' and not attribut.endswith(('s', 'x', 'aux')):
        if attribut.endswith('al'):
             attribut = attribut[:-2] + 'aux'
        elif attribut.endswith('el') and sujet_g == 'm':
            attribut += 's'
        elif not attribut.endswith('s'):
            attribut += 's'
        
    return attribut.strip().replace('éee', 'ée').replace('éees', 'ées') 

def conjuguer_verbe(verbe_dict, sujet_n, sujet_g="m", verbe_cle=None, voix='active', sujet_v=None):
    """Conjuge un verbe (V35, logique 'nous' inchangée)."""
    
    if verbe_cle is None and verbe_dict:
        verbe_cle = random.choice(list(verbe_dict.keys()))
        
    if sujet_v and sujet_v.lower() == 'nous':
        if verbe_cle.startswith('se ') or verbe_cle.startswith("s'"):
            base_infinitive = re.sub(r"s'|se\s", "", verbe_cle, 1)
        else:
            base_infinitive = verbe_cle

        if base_infinitive in GV_PERSONNEL_NOUS_EXPLICIT:
            return GV_PERSONNEL_NOUS_EXPLICIT[base_infinitive]
        
        else:
            if len(base_infinitive) > 2 and base_infinitive.endswith(('er', 'ir', 're')):
                 return base_infinitive[:-2] + 'ons'
            return base_infinitive + 'ons'
            
    if sujet_v and sujet_v.lower() == 'on':
        sujet_n = 's'
        
    if verbe_cle == 'falloir':
        return verbe_dict[verbe_cle]['s'] 
        
    if voix == 'passive' and verbe_cle in VERBES_PASSIFS:
        participe_base = VERBES_PASSIFS[verbe_cle]
        participe_accorde = accorder_attribut(participe_base, sujet_g, sujet_n)
        conjugation = f"{GVAttributif['être'][sujet_n]} {participe_accorde}"
        return conjugation
    
    if verbe_cle in verbe_dict and sujet_n in verbe_dict[verbe_cle]:
        return verbe_dict[verbe_cle][sujet_n]
    
    if verbe_cle in GVTransitif and sujet_n in GVTransitif[verbe_cle]:
         return GVTransitif[verbe_cle][sujet_n]
    if verbe_cle in GVIntransitif and sujet_n in GVIntransitif[verbe_cle]:
         return GVIntransitif[verbe_cle][sujet_n]
            
    return ""

def eliminer_article_devant_voyelle(text):
    """Gère l'élision l' / d' / qu' / s' / puisqu' / lorsqu' (V35)."""
    
    text = re.sub(r'\s(le|la)\s([aeiouyéèàôêïh])', r" l'\2", text, flags=re.IGNORECASE)
    text = re.sub(r'\sde\s([aeiouyéèàôêïh])', r" d'\1", text, flags=re.IGNORECASE)
    text = re.sub(r'\sque\s([aeiouyéèàôêïh])', r" qu'\1", text, flags=re.IGNORECASE)
    text = re.sub(r'\sse\s([aeiouyéèàôêïh])', r" s'\1", text, flags=re.IGNORECASE)
    text = re.sub(r'\ste\s([aeiouyéèàôêïh])', r" t'\1", text, flags=re.IGNORECASE)
    
    voyelle_start_pattern = r'([aeiouyéèàôêïh])'
    
    text = re.sub(rf'\sparce\s+que\s+{voyelle_start_pattern}', r" parce qu'\1", text, flags=re.IGNORECASE)
    text = re.sub(rf'\slorsque\s+{voyelle_start_pattern}', r" lorsqu'\1", text, flags=re.IGNORECASE)
    text = re.sub(rf'\spuisque\s+{voyelle_start_pattern}', r" puisqu'\1", text, flags=re.IGNORECASE)
    
    text = re.sub(r'\scomme\s+(il|ils)', r" comme \1", text, flags=re.IGNORECASE) 
    
    text = re.sub(r"d'\s+l'", r"d'", text, flags=re.IGNORECASE)
    
    return text

def _get_base_gn_info(gn_base_str):
    return GN_BASE_MAP.get(gn_base_str, {'g': 'm', 'n': 's'}) 

def select_determinant(g, n, type='defini'):
    """Sélectionne le déterminant."""
    if type == 'defini':
        if n == 's': return 'le ' if g == 'm' else 'la '
        else: return 'les '
    elif type == 'indefini':
        if n == 's': return 'un ' if g == 'm' else 'une '
        else: return 'des '
    return ''

def _apply_determinant_and_elision(gn_base_str, g, n, type):
    """Applique le déterminant final et gère l'élision pour 'l''."""
    det = select_determinant(g, n, type)
    
    # Check for vowel start after potential adjectif préposé
    first_word = gn_base_str.split()[0]
    
    if det in ('le ', 'la ') and first_word and first_word[0].lower() in ('a', 'e', 'i', 'o', 'u', 'h', 'y', 'é', 'è', 'à', 'ô', 'ê', 'ï'):
        det = "l'"
            
    return (det + gn_base_str).strip()

# FIX V35: Nouvelle fonction pour obtenir un adjectif de la bonne catégorie
def get_random_adjective_form_from_category(g, n):
    """Sélectionne un adjectif aléatoire de la bonne catégorie G/N."""
    if g == 'm' and n == 's':
        return random.choice(ADJ_MS)
    elif g == 'f' and n == 's':
        return random.choice(ADJ_FS)
    elif g == 'm' and n == 'p':
        return random.choice(ADJ_MP)
    elif g == 'f' and n == 'p':
        return random.choice(ADJ_FP)
    return ""


def generer_gn_recursif_fixed(base_gn_str, type, profondeur=0, allow_recursion=True):
    """Génère le GN complet avec adj. et CN récursifs (V35: utilise les listes d'ADJ catégorisées)."""
    
    gn_info_base = _get_base_gn_info(base_gn_str)
    g, n = gn_info_base['g'], gn_info_base['n']
    
    adjs_post = []
    # FIX V35: Ajout d'un adjectif aléatoire de la bonne catégorie
    if random.random() < 0.4:
        adj_accorde = get_random_adjective_form_from_category(g, n)
        # S'assurer que l'adjectif n'est pas déjà dans le GN de base (nettoyé)
        if adj_accorde.split()[0] not in base_gn_str:
             adjs_post.append(adj_accorde)
    
    gn_final_bare = f"{base_gn_str} {' '.join(adjs_post)}"
        
    if allow_recursion and profondeur < MAX_PROFONDEUR_RECURSIVITE_CN:
        if random.random() < 0.3:
            prefixe_cn = 'de' if random.random() < 0.8 else random.choice(["par"])
            cn_base = random.choice(GNDefini)
            cn_recursif_result = generer_gn_recursif_fixed(cn_base, type='defini', profondeur=profondeur + 1)
            cn_final = formatter_sp_gn_fixed(prefixe_cn, cn_recursif_result)
            gn_final_bare = f"{gn_final_bare} {cn_final}"
        
        if random.random() < 0.2:
            relative = generer_ps_relative(gn_info_base)
            gn_final_bare = f"{gn_final_bare} {relative}"
    
    if type == 'aucun':
        full_gn = gn_final_bare.strip()
    else:
        full_gn = _apply_determinant_and_elision(gn_final_bare, g, n, type)

    return {"v": full_gn.strip(), "g": g, "n": n, "v_bare": gn_final_bare.strip()}


# Le reste des fonctions (get_gn_info, formater_objet_infinitif, etc.) reste inchangé, 
# car elles appellent `generer_gn_recursif_fixed` ou `accorder_attribut` qui gèrent 
# désormais la nouvelle structure des adjectifs.

def generer_gn_coordonne(liste_gn_bases, coord='et'):
    """Génère un GN coordonné (V35)."""
    base1 = random.choice([b for b in liste_gn_bases if GN_BASE_MAP[b]['n'] == 's'])
    base2 = random.choice([b for b in liste_gn_bases if b != base1 and GN_BASE_MAP[b]['n'] == 's'])
    
    gn1_info = generer_gn_recursif_fixed(base1, type='defini', profondeur=0, allow_recursion=False)
    gn2_info = generer_gn_recursif_fixed(base2, type='defini', profondeur=0, allow_recursion=False) 
    
    full_gn = f"{gn1_info['v']} {coord} {gn2_info['v']}" 
    
    return {"v": full_gn.strip(), "g": 'm', "n": 'p', "v_bare": full_gn.strip(), "is_coord": True} 

def get_gn_info(gn_list_or_key=None, type='defini', n=None, g=None, role='subject'):
    """Sélectionne et génère un GN (avec anaphore) (V35)."""
    global LAST_GN_INFO
    
    if role == 'subject' and LAST_GN_INFO and not LAST_GN_INFO.get('is_pronoun') and random.random() < 0.15:
        n_prev = LAST_GN_INFO['n']
        g_prev = LAST_GN_INFO['g']
        
        pron = "il" if g_prev == 'm' and n_prev == 's' else "elle" if g_prev == 'f' and n_prev == 's' else "ils" if n_prev == 'p' and g_prev == 'm' else "elles"
            
        result = {"v": pron, "g": g_prev, "n": n_prev, "v_bare": pron, "is_pronoun": True}
        LAST_GN_INFO = result 
        return result

    if gn_list_or_key == 'GNPersonnel': result = random.choice(GNPersonnel)
    elif gn_list_or_key == 'GNImpersonnel': result = random.choice(GNImpersonnel)
    elif gn_list_or_key == 'GNPresentatif': result = random.choice(GNPresentatif)
    elif gn_list_or_key == 'Coordination': result = generer_gn_coordonne(GNDefini)
    else:
        if isinstance(gn_list_or_key, list):
            base_gn_str = random.choice(gn_list_or_key)
            if gn_list_or_key in [GNDefini, GNComplexe]: type = 'defini'
            elif gn_list_or_key in [GNIndefini_Singulier, GNIndefini_Pluriel, GNIndefini]: type = 'indefini'
        else:
            base_gn_str = gn_list_or_key if gn_list_or_key in GNDefini else random.choice(GNDefini)
            
        gn_info_base = _get_base_gn_info(base_gn_str)
            
        if n is None: n = gn_info_base['n']
        if g is None: g = gn_info_base['g']
            
        result = generer_gn_recursif_fixed(base_gn_str, type=type, profondeur=0)
        
    if role == 'subject' and not result.get('is_pronoun', False) and type == 'defini':
         LAST_GN_INFO = result
    else:
         LAST_GN_INFO = None
            
    return result

def _elide_before_infinitive(infinitive):
    """Vérifie si l'élision doit avoir lieu avant l'infinitif."""
    first_char = infinitive[0].lower()
    return first_char in ('a', 'e', 'i', 'o', 'u', 'h', 'y', 'é', 'è', 'à', 'ô', 'ê', 'ï')

def formater_objet_infinitif(infinitive, objet_info=None, prefixe=""):
    """Formate l'infinitif + objet (V35)."""
    
    objet_str = objet_info['v'] if objet_info else ""
    prefixe_lower = prefixe.lower().strip()
    
    if any(m in prefixe_lower for m in ["doit", "peut", "faut", "peuvent", "doivent", "devons", "pouvons"]): 
        prefixe = prefixe.replace(" de ", " ").replace(" d'", " ")
        return f"{prefixe} {infinitive} {objet_str}".strip()
        
    if any(p in prefixe_lower for p in ["afin de", "afin d'", "permettrait"]):
        prepo = "d'" if _elide_before_infinitive(infinitive) else "de"
        prefixe = prefixe.rstrip(' ,') 
        
        if prefixe_lower.startswith('afin'):
            prefixe_base = "afin"
        elif prefixe_lower.endswith(('trait','rait')): 
            prefixe_base = prefixe.replace(" de", "").replace(" d'", "")
        else:
            prefixe_base = prefixe

        return f"{prefixe_base} {prepo} {infinitive} {objet_str}".strip()

    if prefixe_lower == "pour":
        return f"{prefixe} {infinitive} {objet_str}".strip()

    return f"{prefixe} {infinitive} {objet_str}".strip()


def formatter_sp_gn_fixed(preposition, gn_info):
    """Gère contractions (du, des, au, aux) (V35)."""
    gn_str_bare = gn_info['v_bare'] 
    gn_g, gn_n = gn_info['g'], gn_info['n']
    
    starts_with_vowel = gn_str_bare and gn_str_bare.split()[0][0].lower() in ('a', 'e', 'i', 'o', 'u', 'h', 'y', 'é', 'è', 'à', 'ô', 'ê', 'ï')

    prepo_base = ""
    preposition_lower = preposition.lower().strip()
    
    preposition_to_check = preposition_lower
    if preposition_lower.endswith((" de", " d'")):
        parts = preposition.rsplit(' ', 1)
        prepo_base = parts[0].strip() if len(parts) > 1 else ""
        preposition_to_check = "de"
    elif preposition_lower.endswith((" à", " l'")):
        parts = preposition.rsplit(' ', 1)
        prepo_base = parts[0].strip() if len(parts) > 1 else ""
        preposition_to_check = "à"
    elif preposition_lower in ("de", "à"):
        prepo_base = ""
        
    if preposition_to_check in ("de", "à"):
        
        if preposition_to_check == "de":
            if starts_with_vowel and gn_n == 's':
                final_article_or_contraction = "de l'"
            elif gn_n == 's' and gn_g == 'm': 
                final_article_or_contraction = "du "
            elif gn_n == 's' and gn_g == 'f':
                final_article_or_contraction = "de la "
            elif gn_n == 'p':
                final_article_or_contraction = "des "
            else:
                final_article_or_contraction = "de "
            
            if starts_with_vowel and gn_n == 's' and gn_str_bare.startswith("l'"):
                 return f"{prepo_base} de {gn_str_bare}".strip()
            
            return f"{prepo_base} {final_article_or_contraction}{gn_str_bare}".strip()
            
        elif preposition_to_check == "à":
            if starts_with_vowel:
                final_article_or_contraction = "à l'"
            elif gn_n == 's' and gn_g == 'm':
                final_article_or_contraction = "au "
            elif gn_n == 's' and gn_g == 'f':
                final_article_or_contraction = "à la "
            elif gn_n == 'p':
                final_article_or_contraction = "aux "
            else:
                final_article_or_contraction = "à "
                
            return f"{prepo_base} {final_article_or_contraction}{gn_str_bare}".strip()

    full_gn = _apply_determinant_and_elision(gn_str_bare, gn_g, gn_n, type='defini')
    return eliminer_article_devant_voyelle(f"{preposition} {full_gn}")

def generer_ps_complexe_recursif_fixed(profondeur=0):
    """Génère une proposition subordonnée complète (V35)."""
    
    sujet_info = get_gn_info(random.choice([GNDefini, 'Coordination']), n=random.choice(['s', 'p']), role='subject')
    
    if random.random() < 0.7:
        verbe = conjuguer_verbe(GVTransitif, sujet_info['n'])
        objet_info = get_gn_info(GNIndefini, role='object')
        clause = f"{sujet_info['v']} {verbe} {objet_info['v']}"
    else:
        verbe_key = random.choice(list(GVAttributif.keys()))
        verbe = conjuguer_verbe(GVAttributif, sujet_info['n'], verbe_cle=verbe_key)
        attribut = construire_attribut_correct(sujet_info, verbe_key=verbe_key)
        clause = f"{sujet_info['v']} {verbe} {attribut}"
        
    if profondeur < MAX_PROFONDEUR_RECURSIVITE_SUB and random.random() < 0.2:
        verbe_intro_cle = random.choice(['affirmer', 'montrer', 'démontrer', 'suggérer'])
        verbe_intro = conjuguer_verbe(GVIntroductif, sujet_info['n'], verbe_cle=verbe_intro_cle)
        subordonnee = f" et {verbe_intro} que {generer_ps_complexe_recursif_fixed(profondeur + 1)}"
        clause = f"{clause} {subordonnee}"
            
    return clause.strip()

def generer_ps_relative(gn_sujet_base=None):
    """Génère une relative pour qualifier un GN (V35)."""
    antecedent_n = gn_sujet_base['n']
    
    if random.random() < 0.6: 
        verbe = conjuguer_verbe(GVTransitif, antecedent_n)
        objet_relatif = get_gn_info(GNIndefini, role='object')
        return f" qui {verbe} {objet_relatif['v']}"
    else:
        sujet_relatif = get_gn_info(GNDefini, n=random.choice(['s', 'p']), role='subject')
        verbe = conjuguer_verbe(GVTransitif, sujet_relatif['n']) 
        return f" que {sujet_relatif['v']} {verbe}"

def construire_ps_initiale_clause():
    """Génère une clause subordonnée ou adverbiale pour commencer une phrase (V35)."""
    clause_type = random.choice(['causale', 'temporelle', 'gerondif', 'detache'])
    
    sujet_nominal = get_gn_info(GNDefini, role='subject')
    verbe = conjuguer_verbe(GVTransitif, sujet_nominal['n'])
    objet = get_gn_info(GNIndefini, role='object')
    
    if clause_type == 'causale':
        subordonnee = f"{sujet_nominal['v']} {verbe} {objet['v']}"
        return f"{random.choice(['parce que', 'puisque', 'comme'])} {subordonnee}" 
    elif clause_type == 'temporelle':
        subordonnee = f"{sujet_nominal['v']} {verbe} {objet['v']}"
        return f"{random.choice(['lorsque', 'quand', 'dès que', 'alors que'])} {subordonnee}" 
    elif clause_type == 'gerondif':
        return random.choice(Gerondif)
    elif clause_type == 'detache':
        return random.choice(AdjDetache)
    return ""

def generer_ps_finale_simple():
    """Génère une proposition de finalité simple (V35)."""
    if random.random() < 0.7:
        prefixe = random.choice(["afin de", "pour"])
        infinitive = random.choice(GVInfinitifTransitif)
        objet = get_gn_info(GNDefini, role='object')
        return formater_objet_infinitif(infinitive, objet, prefixe)
    else:
        prefixe = random.choice(["pour que", "afin que"])
        sujet_sub = get_gn_info(GNDefini, role='subject')
        verbe = conjuguer_verbe(GVTransitif, sujet_sub['n']) 
        objet = get_gn_info(GNIndefini, role='object')
        return f"{prefixe} {sujet_sub['v']} {verbe} {objet['v']}"
    
def construire_sp_locatif(preposition=None):
    """Construit un syntagme prépositionnel locatif (V35)."""
    prepo = preposition or random.choice(["dans", "sur", "par", "via"])
    gn_base = random.choice([b for b, i in GN_BASE_MAP.items() if i['n'] == 's']) 
    gn_info = get_gn_info(gn_base, n='s', role='complement')
    return formatter_sp_gn_fixed(prepo, gn_info)

def construire_sp_moyen(preposition=None):
    prepo = preposition or random.choice(["au moyen de", "grâce à", "via"])
    gn_base = random.choice([b for b, i in GN_BASE_MAP.items() if i['n'] == 's'])
    gn_info = get_gn_info(gn_base, n='s', role='complement')
    return formatter_sp_gn_fixed(prepo, gn_info)

def construire_sp_attributif(sujet_info=None):
    """Génère un complément attributif avec 'comme' ou 'en tant que' (V35)."""
    prepo = random.choice(["comme", "en tant que"])
    n_cible = sujet_info['n'] if sujet_info else random.choice(['s', 'p'])
    g_cible = sujet_info['g'] if sujet_info else random.choice(['m', 'f'])
    
    gn_base = random.choice([gn for gn, info in GN_BASE_MAP.items() if info['n'] == n_cible])
    gn_info = generer_gn_recursif_fixed(gn_base, type='indefini', allow_recursion=False)
    
    gn_str_sans_article = gn_info['v_bare'] 
    
    if prepo == "en tant que":
        return f"en tant que {gn_str_sans_article}"
    
    return f"comme {gn_info['v']}"


def construire_attribut_correct(sujet_info, verbe_key=None):
    """Génère un attribut adjectival ou nominal accordé avec le sujet (V35)."""
    attribut_type = random.choice(['adj', 'gn'])
    n_cible = sujet_info['n']
    g_cible = sujet_info['g']
    
    if attribut_type == 'adj':
        # NOTE: Utilise le système de base pour les attributs (qui est toujours accordé par la fonction accorder_attribut)
        adj_base = random.choice(ADJECTIFS_DISPONIBLES) 
        return accorder_attribut(adj_base, g_cible, n_cible)
    else:
        gn_base = random.choice([gn for gn, info in GN_BASE_MAP.items() if info['n'] == n_cible])
        # Utilise le nouveau système de génération de GN pour l'attribut nominal
        gn_attribut = get_gn_info(gn_base, type='indefini', n=n_cible)['v']
        
        if verbe_key in ['être', 'devenir', 'demeurer', 'rester', 'sembler', 'apparaître']:
             return gn_attribut
        else:
             return f"comme {gn_attribut}" 

def construire_opposition(sujet_info):
    """Ajoute une clause d'opposition (V35)."""
    attribut_adj_base = random.choice(ADJECTIFS_DISPONIBLES)
    attribut_adj_accorde = accorder_attribut(attribut_adj_base, sujet_info['g'], sujet_info['n']) 
    
    verbe_etre = conjuguer_verbe(GVAttributif, sujet_info['n'], verbe_cle='être')
    
    if verbe_etre.lower()[0] in ('a', 'e', 'i', 'o', 'u', 'h', 'y', 'é', 'è', 'à', 'ô', 'ê', 'ï'):
         negation = "n'"
    else:
         negation = "ne "

    return f", mais {negation}{verbe_etre} pas {attribut_adj_accorde}" 

# T21 (fixed to ensure subject existence)
T21_fixed = lambda: (
    gn_sujet_reel := get_gn_info(GNIndefini, n=random.choice(['s', 'p']), role='subject'),
    verbe := conjuguer_verbe(GVIntransitif, gn_sujet_reel['n']),
    f"{construire_sp_locatif(preposition='grâce à')}, {gn_sujet_reel['v']} {verbe}."
)[-1]


# ===================================================================
# --- SECTION 3: PATRONS DE PHRASES V35 (T1-T142 INCHANGÉS DANS LA STRUCTURE) ---
# ===================================================================

T = {}

# Patrons T1-T109 (Inchangement)

T["T1"] = lambda: (
    sujet := get_gn_info(random.choice([GNDefini, 'Coordination']), n=random.choice(['s', 'p']), role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet_defini := get_gn_info(GNDefini, role='object'),
    f"{sujet['v']} {verbe} {objet_defini['v']} {construire_sp_moyen(preposition='par')} {construire_sp_moyen(preposition='grâce à')}."
)[-1]
T["T2"] = lambda: (
    sujet := get_gn_info(GNDefini, n='s', role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle=random.choice(['se définir', 'se manifester'])),
    objet := get_gn_info(GNDefini, role='complement'),
    f"{sujet['v']} {verbe} sur {objet['v']} {generer_ps_relative(_get_base_gn_info(sujet['v_bare']))}."
)[-1]
T["T3"] = lambda: (
    sujet := get_gn_info(GNDefini, n='s', role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNIndefini, role='object'), 
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_moyen()}."
)[-1]
T["T4"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key, sujet_v=sujet['v']), 
    objet_articule := get_gn_info(GNDefini, role='object'),
    ps_explic := generer_ps_finale_simple(),
    f"{sujet['v']} {formater_objet_infinitif('articuler', objet_articule, prefixe=f"{verbe_modal}")} {ps_explic}"
)[-1]
T["T5"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n'], verbe_cle=random.choice(list(GVTransitif.keys())), sujet_v=sujet['v']), 
    objet := get_gn_info(GNIndefini, role='object'),
    ps_explic := generer_ps_finale_simple(),
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_locatif()} {ps_explic}"
)[-1]
T["T6"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVIntransitif, sujet['n'], verbe_cle='persister'), 
    f"{sujet['v']} {verbe} {generer_ps_finale_simple()}."
)[-1]
T["T7"] = lambda: (
    sujet := get_gn_info(GNIndefini, role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=random.choice(['être', 'rester'])),
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='dans')}."
)[-1]
T["T8"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {generer_ps_finale_simple()}."
)[-1]
T["T9"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe_key := random.choice(list(GVAttributif.keys())),
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key), 
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key), 
    f"{sujet['v']} {verbe} {attribut}." 
)[-1]
T["T10"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(VERBES_PASSIFS.keys())),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=verbe_key, voix='passive'),
    ps_explic := construire_sp_attributif(sujet), 
    f"{sujet['v']} {verbe} {ps_explic}."
)[-1]
T["T11"] = lambda: (
    sujet := get_gn_info(GNComplexe, role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle="rester"), 
    objet := get_gn_info(GNDefini, role='complement'), 
    f"{sujet['v']} {verbe} {formatter_sp_gn_fixed('de', objet)}."
)[-1]
T["T12"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {random.choice(['lentement, mais sûrement', 'systématiquement', 'avec prudence'])}."
)[-1]
T["T13"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    cause := get_gn_info(GNIndefini_Pluriel, role='complement'),
    f"{sujet['v']} {verbe} {objet['v']} {formatter_sp_gn_fixed('en raison de', cause)}."
)[-1]
T["T14"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='s', role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n'], sujet_v=sujet['v']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_locatif()}."
)[-1]
T["T15"] = lambda: (
    sujet := get_gn_info(GNIndefini, role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle="se constituer"), 
    attribut := construire_sp_attributif(sujet), 
    f"{sujet['v']} {verbe} {attribut}." 
)[-1]
T["T16"] = lambda: (
    sujet := get_gn_info(GNComplexe, role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNDefini, role='object'), 
    f"{sujet['v']} {verbe} {objet['v']} {generer_ps_finale_simple()}."
)[-1]
T["T17"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    ps_finale := construire_sp_attributif(sujet), 
    f"{sujet['v']} {verbe} {objet['v']} {ps_finale}."
)[-1]
T["T18"] = T["T9"]
T["T19"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']}."
)[-1]
T["T20"] = T["T19"]
T["T21"] = T21_fixed
T["T22"] = lambda: (
    sujet := get_gn_info('GNImpersonnel', n='s', role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle='être'), 
    f"{sujet['v']} {verbe} essentiel que {generer_ps_complexe_recursif_fixed()}."
)[-1]
T["T23"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='s', role='subject'), 
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key, sujet_v=sujet['v']), 
    ps_explic := generer_ps_finale_simple(),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {ps_explic}"
)[-1]
T["T24"] = lambda: (
    sujet := get_gn_info('GNPresentatif', n='s', role='subject'), 
    verbe := conjuguer_verbe(GVIntroductif, get_gn_info('GNPersonnel', n='s')['n'], verbe_cle='montrer'), 
    f"on {verbe} que {sujet['v']} {get_gn_info(GNIndefini, role='object')['v']} {construire_sp_attributif(get_gn_info(GNIndefini, n='s', g='m', role='complement'))}." 
)[-1]
T["T25"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe_key := random.choice(['affirmer', 'montrer', 'postuler', 'suggérer', 'démontrer']),
    verbe := conjuguer_verbe(GVIntroductif, sujet['n'], verbe_cle=verbe_key), 
    f"{sujet['v']} {verbe} que {generer_ps_complexe_recursif_fixed()}." 
)[-1]
T["T26"] = T["T19"]
T["T27"] = T["T25"]
T["T28"] = T["T8"]
T["T29"] = T["T25"]
T["T30"] = lambda: (
    sujet_princ := get_gn_info(GNDefini, role='subject'),
    verbe_princ := conjuguer_verbe(GVTransitif, sujet_princ['n']),
    objet_princ := get_gn_info(GNIndefini, role='object'),
    f"{sujet_princ['v']} {verbe_princ} {objet_princ['v']}."
)[-1]
T["T31"] = T["T19"]
T["T32"] = T["T8"]
T["T33"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNIndefini, role='object'), 
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_locatif()}."
)[-1]
T["T34"] = T["T12"]
T["T35"] = T["T19"]
T["T36"] = lambda: (
    sujet := get_gn_info('GNImpersonnel', n='s', role='subject'), 
    verbe := conjuguer_verbe(GVConditionnel, sujet['n']),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe}")} {generer_ps_finale_simple()}."
)[-1]
T["T37"] = T["T9"]
T["T38"] = T["T25"]
T["T39"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle=random.choice(list(GVReflexifAttributif.keys()))), 
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='dans')} {generer_ps_finale_simple()}."
)[-1]
T["T40"] = T["T33"]
T["T41"] = T["T19"]
T["T42"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {generer_ps_finale_simple()}."
)[-1]
T["T43"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(VERBES_PASSIFS.keys())),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=verbe_key, voix='passive'),
    agent := get_gn_info(GNIndefini, role='complement'), 
    sp_agent := formatter_sp_gn_fixed("par", agent), 
    f"{sujet['v']} {verbe} {sp_agent}." 
)[-1]
T["T44"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVIntransitif, sujet['n']), 
    f"{sujet['v']} {verbe} {construire_opposition(sujet)}."
)[-1]
T["T45"] = T["T19"]
T["T46"] = T["T44"]
T["T47"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle=random.choice(list(GVReflexifAttributif.keys()))), 
    f"{sujet['v']} {verbe} {generer_ps_finale_simple()}." 
)[-1]
T["T48"] = T["T9"]
T["T49"] = T["T19"]
T["T50"] = T["T8"]
T["T51"] = lambda: (
    sujet := get_gn_info(GNIndefini, role='subject'), 
    verbe := conjuguer_verbe({'émerger': GVIntransitif['émerger'], 'circuler': GVIntransitif['circuler'], 'opérer': GVIntransitif['opérer']}, sujet['n']), 
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='dans')}." 
)[-1]
T["T52"] = T["T30"]
T["T53"] = lambda: (
    sujet := get_gn_info('GNImpersonnel', n='s', role='subject'),
    verbe_passif := conjuguer_verbe({'analyser': VERBES_PASSIFS['analyser']}, sujet['n'], sujet['g'], voix='passive'),
    clause := generer_ps_complexe_recursif_fixed(),
    f"{sujet['v']} est analysé que {clause}."
)[-1]
T["T54"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVIntransitif, sujet['n']), 
    f"{sujet['v']} {verbe} {generer_ps_finale_simple()}." 
)[-1]
T["T55"] = T["T43"]
T["T56"] = T["T19"]
T["T57"] = T["T25"]
T["T58"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=random.choice(list(VERBES_PASSIFS.keys())), voix='passive'),
    ps_explic := generer_ps_finale_simple(),
    f"{sujet['v']} {verbe} {construire_sp_attributif(sujet)} {ps_explic}."
)[-1]
T["T59"] = T["T45"]
T["T60"] = lambda: (
    sujet1 := get_gn_info(GNDefini, role='subject'), 
    verbe1 := conjuguer_verbe(GVTransitif, sujet1['n']), 
    objet1 := get_gn_info(GNIndefini, role='object'), 
    sujet2 := get_gn_info(GNDefini, role='subject'), 
    verbe2 := conjuguer_verbe(GVTransitif, sujet2['n']), 
    objet2 := get_gn_info(GNIndefini, role='object'), 
    f"{sujet1['v']} {verbe1} {objet1['v']}, {random.choice(['cependant', 'tandis que', 'alors que'])} {sujet2['v']} {verbe2} {objet2['v']}." 
)[-1]
T["T61"] = T["T19"]
T["T62"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(GVAttributif.keys())),
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    f"{sujet['v']} {verbe} {attribut} {generer_ps_finale_simple()}."
)[-1]
T["T63"] = T["T45"]
T["T64"] = T["T22"]
T["T65"] = T["T45"]
T["T66"] = lambda: (
    sujet := get_gn_info(GNDefini, n='s', role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle='se manifester'), 
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='par')}." 
)[-1]
T["T67"] = T["T15"]
T["T68"] = T["T45"]
T["T70"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {construire_opposition(sujet)}." 
)[-1]
T["T71"] = T["T31"]
T["T72"] = T["T45"]
T["T73"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='s', role='subject'), 
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key, sujet_v=sujet['v']),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {generer_ps_finale_simple()}."
)[-1]
T["T74"] = T["T45"]
T["T75"] = T["T33"]
T["T76"] = lambda: (
    sujet := get_gn_info('Coordination', role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNIndefini, role='object'), 
    f"{sujet['v']} {verbe} {objet['v']}."
)[-1]
T["T77"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle='se déployer'), 
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='dans')}."
)[-1]
T["T78"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key), 
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {generer_ps_finale_simple()}."
)[-1]
T["T79"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], voix='passive'),
    ps_finale := generer_ps_finale_simple(),
    f"{sujet['v']} {verbe} {construire_sp_moyen()} {ps_finale}."
)[-1]
T["T80"] = T["T25"]
T["T81"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n=random.choice(['s', 'p']), role='subject'), # Choix dynamique entre 'nous' et 'on'
    verbe := conjuguer_verbe(GVIntroductif, sujet['n'], sujet_v=sujet['v']), 
    f"{sujet['v']} {verbe} que {generer_ps_complexe_recursif_fixed()}." 
)[-1]
T["T82"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle='demeurer'), 
    attribut := construire_attribut_correct(sujet, verbe_key='demeurer'),
    f"{sujet['v']} {verbe} {attribut} {construire_sp_locatif(preposition='dans')}."
)[-1]
T["T83"] = lambda: (
    sujet := get_gn_info(GNDefini, n='s', role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info('Coordination', role='object'),
    f"{sujet['v']} {verbe} {objet['v']}."
)[-1]
T["T84"] = T["T9"]
T["T85"] = T["T30"] 
T["T86"] = T["T54"]
T["T87"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe({'émerger': GVIntransitif['émerger'], 'circuler': GVIntransitif['circuler'], 'opérer': GVIntransitif['opérer']}, sujet['n']), 
    f"{sujet['v']} {verbe} {construire_sp_locatif(preposition='dans')}."
)[-1]
T["T88"] = T["T70"]
T["T89"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle='apparaître'),
    attribut := construire_attribut_correct(sujet, verbe_key='apparaître'),
    f"{sujet['v']} {verbe} {attribut}."
)[-1]
T["T90"] = T["T60"]
T["T91"] = T["T22"]
T["T92"] = T["T33"]
T["T93"] = lambda: (
    sujet := get_gn_info(GNIndefini_Pluriel, role='subject'),
    verbe := conjuguer_verbe(GVIntransitif, sujet['n'], verbe_cle='advenir'), 
    f"{sujet['v']} {verbe} {generer_ps_finale_simple()}."
)[-1]
T["T94"] = T["T24"]
T["T95"] = T["T43"]
T["T96"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())), 
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key, sujet_v=sujet['v']), 
    f"{sujet['v']} {formater_objet_infinitif('déconstruire', get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {construire_sp_moyen()}."
)[-1]
T["T97"] = T["T75"]
T["T98"] = lambda: (
    sujet := get_gn_info('Coordination', role='subject'),
    verbe_key := random.choice(list(GVAttributif.keys())),
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    f"{sujet['v']} {verbe} {attribut} {generer_ps_finale_simple()}."
)[-1]
T["T99"] = T["T45"]
T["T100"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_moyen()} {construire_opposition(sujet)}."
)[-1]
T["T101"] = T["T10"]
T["T102"] = T["T8"]
T["T103"] = T["T33"]
T["T104"] = T["T36"]
T["T105"] = T["T39"]
T["T106"] = T["T58"]
T["T107"] = T["T7"]
T["T108"] = T["T19"]
T["T109"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'), 
    verbe := conjuguer_verbe(GVIntroductif, sujet['n'], verbe_cle='soutenir', sujet_v=sujet['v']), 
    f"{sujet['v']} {verbe} que {generer_ps_complexe_recursif_fixed()}." 
)[-1]

# --- NOUVEAUX PATRONS UNIQUES T110 - T142 (structure inchangée, utilise V35) ---

# T110: GN transitif avec SP locatif + PS finale.
T["T110"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'), 
    verbe := conjuguer_verbe(GVTransitif, sujet['n']), 
    objet := get_gn_info(GNIndefini, role='object'), 
    f"{sujet['v']} {verbe} {objet['v']} {construire_sp_locatif()} {generer_ps_finale_simple()}."
)[-1]

# T111: Nous/On attributif (être) + attribut + SP locatif.
T["T111"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'), 
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle='être', sujet_v=sujet['v']), 
    attribut := construire_attribut_correct(sujet, verbe_key='être'),
    f"{sujet['v']} {verbe} {attribut} {construire_sp_locatif(preposition='dans')}."
)[-1]

# T112: GN introductif (montrer) que + GN attributif (apparaître).
T["T112"] = lambda: (
    sujet_princ := get_gn_info(GNDefini, role='subject'), 
    verbe_princ := conjuguer_verbe(GVIntroductif, sujet_princ['n'], verbe_cle='montrer'),
    sujet_sub := get_gn_info(GNIndefini, role='object'),
    verbe_sub := conjuguer_verbe(GVAttributif, sujet_sub['n'], verbe_cle='apparaître'),
    attribut := construire_attribut_correct(sujet_sub, verbe_key='apparaître'),
    f"{sujet_princ['v']} {verbe_princ} que {sujet_sub['v']} {verbe_sub} {attribut}." 
)[-1]

# T113: PS initiale (temporelle) + GN passif + SP agent.
T["T113"] = lambda: (
    clause_initiale := construire_ps_initiale_clause(),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(VERBES_PASSIFS.keys())),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=verbe_key, voix='passive'),
    agent := get_gn_info(GNIndefini, role='complement'), 
    sp_agent := formatter_sp_gn_fixed("par", agent), 
    f"{clause_initiale}, {sujet['v']} {verbe} {sp_agent}."
)[-1]

# T114: GN transitif + GN indéfini + PS relative.
T["T114"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n'], verbe_cle='générer'),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {generer_ps_relative(_get_base_gn_info(objet['v_bare']))}."
)[-1]

# T115: GN modal (doit) + Infinitif + SP locatif + SP moyen.
T["T115"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle='devoir'),
    sp_loc := construire_sp_locatif(),
    sp_moyen := construire_sp_moyen(),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {sp_loc} {sp_moyen}."
)[-1]

# T116: PS initiale (adverbe) + GN introductif (suggérer) que + PS complexe.
T["T116"] = lambda: (
    adverbe := random.choice(AdjDetache),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVIntroductif, sujet['n'], verbe_cle='suggérer'),
    f"{adverbe}, {sujet['v']} {verbe} que {generer_ps_complexe_recursif_fixed()}."
)[-1]

# T117: GN attributif (devenir) + attribut + Opposition.
T["T117"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'devenir',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    f"{sujet['v']} {verbe} {attribut} {construire_opposition(sujet)}."
)[-1]

# T118: GN Impersonnel (il faut) + Infinitif + SP attributif (en tant que).
T["T118"] = lambda: (
    sujet := get_gn_info('GNImpersonnel', n='s', role='subject'),
    verbe_modal := conjuguer_verbe(GVModalImpersonal, sujet['n'], verbe_cle='falloir'),
    sp_attributif := construire_sp_attributif(sujet),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {sp_attributif}."
)[-1]

# T119: GN Passif + SP agent + PS finale (pour).
T["T119"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(VERBES_PASSIFS.keys())),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=verbe_key, voix='passive'),
    agent := get_gn_info(GNIndefini, role='complement'),
    sp_agent := formatter_sp_gn_fixed("par", agent),
    ps_finale := generer_ps_finale_simple(),
    f"{sujet['v']} {verbe} {sp_agent} {ps_finale}."
)[-1]

# T120: GN Reflexif (se reconfigurer) + SP locatif + SP moyen.
T["T120"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle='se reconfigurer'),
    sp_loc := construire_sp_locatif(),
    sp_moyen := construire_sp_moyen(),
    f"{sujet['v']} {verbe} {sp_loc} {sp_moyen}."
)[-1]

# T121: PS initiale (causale) + GN transitif GN.
T["T121"] = lambda: (
    clause_initiale := construire_ps_initiale_clause(),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{clause_initiale}, {sujet['v']} {verbe} {objet['v']}."
)[-1]

# T122: Coordination transitif GN + PS relative (que).
T["T122"] = lambda: (
    sujet := get_gn_info('Coordination', role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {generer_ps_relative(sujet)}."
)[-1]

# T123: Nous/On modal + Infinitif transitif GN + PS relative (qui).
T["T123"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe_modal_key := random.choice(list(GVModalPersonal.keys())),
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle=verbe_modal_key, sujet_v=sujet['v']),
    objet := get_gn_info(GNDefini, role='object'),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), objet, prefixe=f"{verbe_modal}")} {generer_ps_relative(_get_base_gn_info(objet['v_bare']))}."
)[-1]

# T124: GN attributif (rester) + attribut + SP moyen.
T["T124"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'rester',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    sp_moyen := construire_sp_moyen(),
    f"{sujet['v']} {verbe} {attribut} {sp_moyen}."
)[-1]

# T125: GN introductif (affirmer) que + GN modal (pouvoir) + Infinitif transitif GN.
T["T125"] = lambda: (
    sujet_princ := get_gn_info(GNDefini, role='subject'),
    verbe_princ := conjuguer_verbe(GVIntroductif, sujet_princ['n'], verbe_cle='affirmer'),
    sujet_sub := get_gn_info(GNIndefini, role='object'),
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet_sub['n'], verbe_cle='pouvoir'),
    f"{sujet_princ['v']} {verbe_princ} que {sujet_sub['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")}."
)[-1]

# T126: GN réflexif (s'avérer) + SP attributif (comme) + PS finale.
T["T126"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle="s'avérer"),
    sp_attributif := construire_sp_attributif(sujet),
    ps_finale := generer_ps_finale_simple(),
    f"{sujet['v']} {verbe} {sp_attributif} {ps_finale}."
)[-1]

# T127: GN attributif (sembler) + attribut + SP locatif + Opposition.
T["T127"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'sembler',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    sp_loc := construire_sp_locatif(),
    f"{sujet['v']} {verbe} {attribut} {sp_loc} {construire_opposition(sujet)}."
)[-1]

# T128: PS initiale (gérondif) + GN modal (peut) + Infinitif transitif GN.
T["T128"] = lambda: (
    gerondif := random.choice(Gerondif),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_modal := conjuguer_verbe(GVModalPersonal, sujet['n'], verbe_cle='pouvoir'),
    f"{gerondif}, {sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")}."
)[-1]

# T129: GN attributif (être) + attribut + PS relative (qui) + SP moyen.
T["T129"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'être',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    ps_relative := generer_ps_relative(sujet),
    sp_moyen := construire_sp_moyen(),
    f"{sujet['v']} {verbe} {attribut} {ps_relative} {sp_moyen}."
)[-1]

# T130: GN réflexif (se constituer) + SP attributif (en tant que) + PS relative.
T["T130"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle='se constituer'),
    sp_attributif := construire_sp_attributif(sujet),
    f"{sujet['v']} {verbe} {sp_attributif} {generer_ps_relative(sujet)}."
)[-1]

# T131: Nous/On introductif (affirmer) que + GN transitif GN.
T["T131"] = lambda: (
    sujet_princ := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe_princ := conjuguer_verbe(GVIntroductif, sujet_princ['n'], verbe_cle='affirmer', sujet_v=sujet_princ['v']),
    sujet_sub := get_gn_info(GNDefini, role='subject'),
    verbe_sub := conjuguer_verbe(GVTransitif, sujet_sub['n']),
    objet_sub := get_gn_info(GNIndefini, role='object'),
    f"{sujet_princ['v']} {verbe_princ} que {sujet_sub['v']} {verbe_sub} {objet_sub['v']}."
)[-1]

# T132: GN Impersonnel (il y a) + GN indéfini + SP locatif.
T["T132"] = lambda: (
    sujet_pres := get_gn_info('GNPresentatif', n='s', role='subject'),
    gn_exist := get_gn_info(GNIndefini, n=random.choice(['s', 'p']), role='object'),
    sp_loc := construire_sp_locatif(),
    f"{sujet_pres['v']} {gn_exist['v']} {sp_loc}."
)[-1]

# T133: GN attributif (apparaître) + attribut + SP attributif (en tant que).
T["T133"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'apparaître',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    sp_attributif := construire_sp_attributif(sujet),
    f"{sujet['v']} {verbe} {attribut} {sp_attributif}."
)[-1]

# T134: PS initiale (adverbe) + GN introductif (montrer) que + PS complexe.
T["T134"] = lambda: (
    adverbe := random.choice(AdjDetache),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVIntroductif, sujet['n'], verbe_cle='montrer'),
    f"{adverbe}, {sujet['v']} {verbe} que {generer_ps_complexe_recursif_fixed()}."
)[-1]

# T135: GN réflexif (s'inscrire) + SP locatif + PS relative (que).
T["T135"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVReflexifAttributif, sujet['n'], verbe_cle="s'inscrire"),
    sp_loc := construire_sp_locatif(),
    f"{sujet['v']} {verbe} {sp_loc} {generer_ps_relative(sujet)}."
)[-1]

# T136: GN transitif GN + SP locatif + Opposition adjectivale.
T["T136"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    sp_loc := construire_sp_locatif(),
    f"{sujet['v']} {verbe} {objet['v']} {sp_loc} {construire_opposition(sujet)}."
)[-1]

# T137: GN passif + SP agent + SP locatif.
T["T137"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := random.choice(list(VERBES_PASSIFS.keys())),
    verbe := conjuguer_verbe(GVPassif, sujet['n'], sujet['g'], verbe_cle=verbe_key, voix='passive'),
    agent := get_gn_info(GNIndefini, role='complement'),
    sp_agent := formatter_sp_gn_fixed("par", agent),
    sp_loc := construire_sp_locatif(),
    f"{sujet['v']} {verbe} {sp_agent} {sp_loc}."
)[-1]

# T138: GN attributif (devenir) + attribut + SP locatif.
T["T138"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'devenir',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    f"{sujet['v']} {verbe} {attribut} {construire_sp_locatif()}."
)[-1]

# T139: GN Impersonnel (il faut) + Infinitif + SP locatif.
T["T139"] = lambda: (
    sujet := get_gn_info('GNImpersonnel', n='s', role='subject'),
    verbe_modal := conjuguer_verbe(GVModalImpersonal, sujet['n'], verbe_cle='falloir'),
    sp_loc := construire_sp_locatif(),
    f"{sujet['v']} {formater_objet_infinitif(random.choice(GVInfinitifTransitif), get_gn_info(GNDefini, role='object'), prefixe=f"{verbe_modal}")} {sp_loc}."
)[-1]

# T140: Nous/On transitif GN + PS relative (qui/que) + Opposition.
T["T140"] = lambda: (
    sujet := get_gn_info('GNPersonnel', n='p', role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n'], sujet_v=sujet['v']),
    objet := get_gn_info(GNIndefini, role='object'),
    ps_relative := generer_ps_relative(sujet),
    f"{sujet['v']} {verbe} {objet['v']} {ps_relative} {construire_opposition(sujet)}."
)[-1]

# T141: GN attributif (rester) + attribut + PS relative (qui).
T["T141"] = lambda: (
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe_key := 'rester',
    verbe := conjuguer_verbe(GVAttributif, sujet['n'], verbe_cle=verbe_key),
    attribut := construire_attribut_correct(sujet, verbe_key=verbe_key),
    f"{sujet['v']} {verbe} {attribut} {generer_ps_relative(sujet)}."
)[-1]

# T142: PS initiale (gérondif) + GN transitif GN + SP locatif.
T["T142"] = lambda: (
    gerondif := random.choice(Gerondif),
    sujet := get_gn_info(GNDefini, role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    sp_loc := construire_sp_locatif(),
    f"{gerondif}, {sujet['v']} {verbe} {objet['v']} {sp_loc}."
)[-1]

T["T143"] = lambda: (
    sujet := get_gn_info('Coordination', role='subject'),
    verbe := conjuguer_verbe(GVTransitif, sujet['n']),
    objet := get_gn_info(GNIndefini, role='object'),
    f"{sujet['v']} {verbe} {objet['v']} {generer_ps_finale_simple()}."
)[-1]
T["T144"] = T["T1"]
T["T145"] = T["T47"]
T["T146"] = T["T25"]
T["T147"] = T["T12"]
T["T148"] = T["T54"]
T["T149"] = T["T4"]
T["T150"] = T["T21"]


# ===================================================================
# --- SECTION 4: FONCTION DE POST-TRAITEMENT ET GÉNÉRATION DE PROSE ---
# ===================================================================

def post_process_phrase(phrase):
    """Effectue le nettoyage final (espaces, élisions, point, doublons) (V35)."""
    
    phrase = re.sub(r'\s+', ' ', phrase).strip()
    phrase = re.sub(r'\s([,.:;?!])', r'\1', phrase)
    
    phrase = re.sub(r"d'\s*l'", r"d'", phrase)
    phrase = re.sub(r"qu'\s*l'", r"qu'", phrase)
    phrase = re.sub(r"'\s+(\w)", r"'\1", phrase)
    phrase = re.sub(r'de de', 'de', phrase) 
    phrase = re.sub(r'(du|des)\s+(du|des)', r'\1', phrase) 
    
    phrase = phrase.replace("ÉGalement", "Également").replace("éGalement", "également")

    phrase = eliminer_article_devant_voyelle(phrase)

    phrase = re.sub(r'(affirme|soutenons|montrons|postule|démontre|suggère|est analysé)\s*,\s*(que)', r'\1 que', phrase, flags=re.IGNORECASE)

    phrase = re.sub(r'([a-z])([A-Z])', r'\1 \2', phrase) 
    phrase = re.sub(r'de(un|une|des)', r'de \1', phrase)
    
    phrase = re.sub(r'\s*,\s*(il|elle|ils|elles|nous|vous)\s*\.\s*$', '.', phrase, flags=re.IGNORECASE)
    phrase = re.sub(r'\s*,\s*(il|elle|ils|elles|nous|vous)\s*$', '', phrase, flags=re.IGNORECASE)
    phrase = re.sub(r'\s+(il|elle|ils|elles|nous|vous)\s*\.\s*$', '.', phrase, flags=re.IGNORECASE)

    if phrase and not phrase.endswith(('.', '?', '!', ':')):
        phrase += '.'
        
    return phrase.strip()

def generate_prose_block():
    """Génère un bloc de texte continu, enchaîné par des connecteurs (V35)."""
    global LAST_GN_INFO
    t_keys = list(T.keys())
    generated_sentences = []
    
    for i in range(NOMBRE_DE_PHRASES_SOUHAITE):
        try:
            LAST_GN_INFO = None 
            
            # Correction: T[random.choice(t_keys)] doit être appelé avec () pour exécuter la lambda.
            raw_phrase_core = T[random.choice(t_keys)]()
            
            prefix = ""
            
            if i > 0 and random.random() < 0.6:
                
                # S'assurer de ne pas doubler les connecteurs/adverbes
                starts_with_forbidden = any(raw_phrase_core.lower().startswith(con.lower().split()[0]) for con in CONNECTEUR_FIX + AdjDetache + Gerondif)
                
                if not starts_with_forbidden:
                    choice_prefix = random.choice(['connector', 'clause', 'adverb'])
                    
                    if choice_prefix == 'connector':
                        prefix = random.choice(AdvConnecteur + Coordination)
                    elif choice_prefix == 'clause':
                        prefix = construire_ps_initiale_clause()
                    elif choice_prefix == 'adverb':
                        prefix = random.choice(AdjDetache + Gerondif)
            
            if prefix and prefix not in AdvConnecteur + Coordination:
                prefix += ','

            final_phrase_raw = f"{prefix} {raw_phrase_core}"
            
            final_phrase_processed = post_process_phrase(final_phrase_raw)
            
            if final_phrase_processed:
                final_phrase = final_phrase_processed.lstrip()
                if final_phrase and final_phrase[0].isalpha():
                    final_phrase = final_phrase[0].upper() + final_phrase[1:]
                
                # Nettoyage des virgules finales avant le point
                final_phrase = final_phrase.rstrip(',').rstrip() 
                if not final_phrase.endswith(('.', '?', '!', ':')):
                     final_phrase += '.'
                
                generated_sentences.append(final_phrase)
            
        except Exception as e:
            # print(f"Erreur de génération à la phrase {i}: {e}")
            pass 
            
    return " ".join(generated_sentences)

prose = generate_prose_block()
print(prose)