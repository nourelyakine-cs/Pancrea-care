import enum


class Sexe(str, enum.Enum):
    M = "M"
    F = "F"
    inconnu = "inconnu"


class ContexteUsage(str, enum.Enum):
    adjuvant = "adjuvant"
    neoadjuvant = "neoadjuvant"
    localement_avance = "localement_avance"
    metastatique_1ere_ligne = "metastatique_1ere_ligne"
    metastatique_2eme_ligne = "metastatique_2eme_ligne"
    metastatique_3eme_ligne = "metastatique_3eme_ligne"
    maintenance = "maintenance"
    chimioradiotherapie = "chimioradiotherapie"


class StatutDossier(str, enum.Enum):
    ouvert = "ouvert"
    clos = "clos"
    archive = "archive"


class DegreParente(str, enum.Enum):
    premier_degre = "premier_degre"
    deuxieme_degre = "deuxieme_degre"
    troisieme_degre_ou_plus = "troisieme_degre_ou_plus"
    inconnu = "inconnu"


class StatutMutation(str, enum.Enum):
    mute = "mute"
    non_mute = "non_mute"


class ContexteEvaluation(str, enum.Enum):
    diagnostic = "diagnostic"
    pre_neoadjuvant = "pre_neoadjuvant"
    restaging = "restaging"
    pre_chirurgie = "pre_chirurgie"
    adjuvant = "adjuvant"
    surveillance = "surveillance"
    recidive = "recidive"


class EtatNutritionnel(str, enum.Enum):
    normal = "normal"
    denutrition_moderee = "denutrition_moderee"
    denutrition_severe = "denutrition_severe"
    inconnu = "inconnu"


class Diabete(str, enum.Enum):
    absent = "absent"
    recent_moins_2ans = "recent_moins_2ans"
    ancien = "ancien"
    inconnu = "inconnu"


class Severite(str, enum.Enum):
    mineure = "mineure"
    majeure = "majeure"


class StatutLewis(str, enum.Enum):
    exprime = "exprime"
    a_b_negatif = "a_b_negatif"
    inconnu = "inconnu"


class StatutDpd(str, enum.Enum):
    normal = "normal"
    deficit_partiel = "deficit_partiel"
    deficit_complet = "deficit_complet"
    non_teste = "non_teste"


class TypeImagerie(str, enum.Enum):
    TDM = "TDM"
    IRM = "IRM"


class LocalisationTumorale(str, enum.Enum):
    tete_crochet = "tete_crochet"
    corps_queue = "corps_queue"
    inconnu = "inconnu"


class ContactVaisseau(str, enum.Enum):
    absent = "absent"
    lt180 = "lt180"
    ge180 = "ge180"


class ContactArtHepatique(str, enum.Enum):
    absent = "absent"
    court_sans_envahissement = "court_sans_envahissement"
    envahissant = "envahissant"


class ContactVmsVp(str, enum.Enum):
    absent = "absent"
    lt180_sans_irregularite = "lt180_sans_irregularite"
    ge180_ou_irregularite = "ge180_ou_irregularite"
    occlusion_reconstructible = "occlusion_reconstructible"
    occlusion_non_reconstructible = "occlusion_non_reconstructible"


class SiteMetastase(str, enum.Enum):
    hepatique = "hepatique"
    peritoneale = "peritoneale"
    pulmonaire = "pulmonaire"
    osseuse = "osseuse"
    autre = "autre"


class StatutBrca(str, enum.Enum):
    mute = "mute"
    non_mute = "non_mute"
    non_teste = "non_teste"


class StatutKras(str, enum.Enum):
    sauvage = "sauvage"
    g12c = "g12c"
    g12d = "g12d"
    g12v = "g12v"
    autre_mute = "autre_mute"
    non_teste = "non_teste"


class StatutMsi(str, enum.Enum):
    mss = "mss"
    msi_h = "msi_h"
    dmmr = "dmmr"
    non_teste = "non_teste"


class Fusion(str, enum.Enum):
    positif = "positif"
    negatif = "negatif"
    non_teste = "non_teste"


class TypeTest(str, enum.Enum):
    panel = "panel"
    germinal = "germinal"
    biopsie_liquide = "biopsie_liquide"
    ihc = "ihc"
    ngs_arn = "ngs_arn"


class ClasseEscat(str, enum.Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"
    non_classe = "non_classe"


class Resecabilite(str, enum.Enum):
    resecable = "resecable"
    borderline = "borderline"
    localement_avance = "localement_avance"
    metastatique = "metastatique"
    inconnu = "inconnu"


class CategorieT(str, enum.Enum):
    T1a = "T1a"
    T1b = "T1b"
    T1c = "T1c"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"
    TX = "TX"


class CategorieN(str, enum.Enum):
    N0 = "N0"
    N1 = "N1"
    N2 = "N2"
    NX = "NX"


class CategorieM(str, enum.Enum):
    M0 = "M0"
    M1 = "M1"


class StadeGlobal(str, enum.Enum):
    IA = "IA"
    IB = "IB"
    IIA = "IIA"
    IIB = "IIB"
    III = "III"
    IV = "IV"
    inconnu = "inconnu"


class Reponse(str, enum.Enum):
    reponse = "reponse"
    stable = "stable"
    progression = "progression"
    non_evaluable = "non_evaluable"


class GradePreuve(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    accord_experts = "accord_experts"


class Operateur(str, enum.Enum):
    egal = "="
    different = "!="
    superieur = ">"
    superieur_egal = ">="
    inferieur = "<"
    inferieur_egal = "<="
    in_ = "in"
    not_in = "not_in"
    est_null = "est_null"
    non_null = "non_null"


class OperateurLiaison(str, enum.Enum):
    ET = "ET"
    OU = "OU"


class TypeConclusion(str, enum.Enum):
    chirurgie = "chirurgie"
    chimio_neoadjuvante = "chimio_neoadjuvante"
    chimio_adjuvante = "chimio_adjuvante"
    chimio_1ere_ligne = "chimio_1ere_ligne"
    chimio_2eme_ligne = "chimio_2eme_ligne"
    chimio_3eme_ligne = "chimio_3eme_ligne"
    chimioradiotherapie = "chimioradiotherapie"
    therapie_ciblee = "therapie_ciblee"
    immunotherapie = "immunotherapie"
    soins_de_support = "soins_de_support"
    drainage_biliaire = "drainage_biliaire"
    surveillance = "surveillance"
    test_moleculaire = "test_moleculaire"
    inclusion_essai = "inclusion_essai"
    discussion_rcp = "discussion_rcp"
