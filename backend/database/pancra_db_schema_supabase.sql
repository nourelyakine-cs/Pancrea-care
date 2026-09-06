-- ============================================================================
-- SCHÉMA cancer_pancreas_db — VERSION SUPABASE / POSTGRESQL
-- (conversion de pancra_db_schema.sql, remarks de remarque.md appliqués)
--
-- EXÉCUTION : Supabase Dashboard -> SQL Editor -> coller tout le script -> Run
--             (le script est transactionnel : tout réussit ou rien n'est créé)
--
-- PRÉREQUIS : PostgreSQL >= 13 (Supabase en fournit 15+).
-- Les contraintes CHECK sont TOUJOURS appliquées par PostgreSQL.
--
-- CONVENTION CLINIQUE : pour les booléens critiques (cholestase,
-- extension_ganglionnaire_distance, metastases_presentes), NULL = donnée
-- manquante => le moteur de règles doit BLOQUER la décision concernée.
--
-- NOTE ENUMS : les types *_t sont extensibles via ALTER TYPE ... ADD VALUE ;
-- une valeur ne peut PAS être retirée d'un enum (prévoir VARCHAR si besoin
-- de vocabulaire librement évolutif).
-- ============================================================================

BEGIN;

-- ============================================================================
-- TYPES ÉNUMÉRÉS (équivalents des ENUM MySQL)
-- ============================================================================

CREATE TYPE public.t_sexe                   AS ENUM ('M','F','inconnu');
CREATE TYPE public.t_contexte_usage         AS ENUM ('adjuvant','neoadjuvant','localement_avance',
                                                     'metastatique_1ere_ligne','metastatique_2eme_ligne',
                                                     'metastatique_3eme_ligne','maintenance','chimioradiotherapie');
CREATE TYPE public.t_statut_dossier         AS ENUM ('ouvert','clos','archive');
CREATE TYPE public.t_degre_parente          AS ENUM ('premier_degre','deuxieme_degre','troisieme_degre_ou_plus','inconnu');
CREATE TYPE public.t_statut_mutation        AS ENUM ('mute','non_mute');
CREATE TYPE public.t_contexte_evaluation    AS ENUM ('diagnostic','pre_neoadjuvant','restaging','pre_chirurgie',
                                                     'adjuvant','surveillance','recidive');
CREATE TYPE public.t_etat_nutritionnel      AS ENUM ('normal','denutrition_moderee','denutrition_severe','inconnu');
CREATE TYPE public.t_diabete                AS ENUM ('absent','recent_moins_2ans','ancien','inconnu');
CREATE TYPE public.t_severite               AS ENUM ('mineure','majeure');
CREATE TYPE public.t_statut_lewis           AS ENUM ('exprime','a_b_negatif','inconnu');
CREATE TYPE public.t_statut_dpd             AS ENUM ('normal','deficit_partiel','deficit_complet','non_teste');
CREATE TYPE public.t_type_imagerie          AS ENUM ('TDM','IRM');
CREATE TYPE public.t_localisation_tumorale  AS ENUM ('tete_crochet','corps_queue','inconnu');
CREATE TYPE public.t_contact_vaisseau       AS ENUM ('absent','lt180','ge180');
CREATE TYPE public.t_contact_art_hepatique  AS ENUM ('absent','court_sans_envahissement','envahissant');
CREATE TYPE public.t_contact_vms_vp         AS ENUM ('absent','lt180_sans_irregularite','ge180_ou_irregularite',
                                                     'occlusion_reconstructible','occlusion_non_reconstructible');
CREATE TYPE public.t_site_metastase         AS ENUM ('hepatique','peritoneale','pulmonaire','osseuse','autre');
CREATE TYPE public.t_statut_brca            AS ENUM ('mute','non_mute','non_teste');
CREATE TYPE public.t_statut_kras            AS ENUM ('sauvage','g12c','g12d','g12v','autre_mute','non_teste');
CREATE TYPE public.t_statut_msi             AS ENUM ('mss','msi_h','dmmr','non_teste');
CREATE TYPE public.t_fusion                 AS ENUM ('positif','negatif','non_teste');
CREATE TYPE public.t_type_test              AS ENUM ('panel','germinal','biopsie_liquide','ihc','ngs_arn');
CREATE TYPE public.t_classe_escat           AS ENUM ('I','II','III','IV','V','non_classe');
CREATE TYPE public.t_resecabilite           AS ENUM ('resecable','borderline','localement_avance','metastatique','inconnu');
CREATE TYPE public.t_categorie_t            AS ENUM ('T1a','T1b','T1c','T2','T3','T4','TX');
CREATE TYPE public.t_categorie_n            AS ENUM ('N0','N1','N2','NX');
CREATE TYPE public.t_categorie_m            AS ENUM ('M0','M1');
CREATE TYPE public.t_stade_global           AS ENUM ('IA','IB','IIA','IIB','III','IV','inconnu');
CREATE TYPE public.t_reponse                AS ENUM ('reponse','stable','progression','non_evaluable');
CREATE TYPE public.t_grade_preuve           AS ENUM ('A','B','C','accord_experts');
CREATE TYPE public.t_operateur              AS ENUM ('=','!=','>','>=','<','<=','in','not_in','est_null','non_null');
CREATE TYPE public.t_operateur_liaison      AS ENUM ('ET','OU');
CREATE TYPE public.t_type_conclusion        AS ENUM ('chirurgie','chimio_neoadjuvante','chimio_adjuvante',
                                                     'chimio_1ere_ligne','chimio_2eme_ligne','chimio_3eme_ligne',
                                                     'chimioradiotherapie','therapie_ciblee','immunotherapie',
                                                     'soins_de_support','drainage_biliaire','surveillance',
                                                     'test_moleculaire','inclusion_essai','discussion_rcp');

-- ============================================================================
-- FONCTION : équivalent du "ON UPDATE CURRENT_TIMESTAMP" de MySQL
-- (à attacher aux tables possédant date_modification)
-- ============================================================================

CREATE OR REPLACE FUNCTION public.set_date_modification()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.date_modification := now();
    RETURN NEW;
END;
$$;

-- ============================================================================
-- 1. ACTEURS — médecin, patient (A.1)
-- ============================================================================

CREATE TABLE public.medecin (
    id_medecin          INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    prenom              VARCHAR(100) NOT NULL,
    email               VARCHAR(255) NOT NULL UNIQUE,
    telephone           VARCHAR(30),
    hopital             VARCHAR(150),                 -- hôpital / établissement d'affectation
    date_creation       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE public.patient (
    id_patient          INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    prenom              VARCHAR(100) NOT NULL,
    date_naissance      DATE,
    sexe                public.t_sexe DEFAULT 'inconnu',
    telephone           VARCHAR(30),
    email               VARCHAR(255),
    adresse             VARCHAR(255),
    date_creation       TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_modification   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_patient_updated
    BEFORE UPDATE ON public.patient
    FOR EACH ROW EXECUTE FUNCTION public.set_date_modification();

-- ============================================================================
-- 2. TABLES DE RÉFÉRENCE (vocabulaires ouverts / évolutifs)
-- ============================================================================

CREATE TABLE public.gene (
-- Cette table contient les gènes connus utilisés dans le système.
    id_gene             INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    code                VARCHAR(30) NOT NULL UNIQUE,      -- BRCA1, BRCA2, PALB2...
    libelle             VARCHAR(120),
    syndrome            VARCHAR(150),                      -- ex. Lynch, Peutz-Jeghers
    cancers_associes    TEXT
);

CREATE TABLE public.comorbidite (
-- Elle contient les maladies/problèmes de santé associés du patient.
    id_comorbidite      INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    code                VARCHAR(30) NOT NULL UNIQUE,
    libelle_fr          VARCHAR(120),
    libelle_en          VARCHAR(120)
);

CREATE TABLE public.protocole_traitement (
-- Elle contient les traitements/protocoles que le système connaît.
    id_protocole        INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    code                VARCHAR(30) NOT NULL UNIQUE,        -- MFOLFIRINOX, GEMCAP...
    libelle_fr          VARCHAR(120),
    libelle_en          VARCHAR(120),
    description         TEXT                                 -- molécules, doses, cycles
);

CREATE TABLE public.protocole_contexte (
-- Un protocole couvre souvent plusieurs contextes d'usage
-- (ex. mFOLFIRINOX : adjuvant ET métastatique_1ere_ligne).
    id_protocole        INT NOT NULL,
    contexte_usage      public.t_contexte_usage NOT NULL,
    PRIMARY KEY (id_protocole, contexte_usage),
    CONSTRAINT fk_protoctx_protocole FOREIGN KEY (id_protocole) REFERENCES public.protocole_traitement(id_protocole) ON DELETE CASCADE
);

CREATE TABLE public.source_referentiel (
-- Elle contient les sources médicales utilisées par le moteur de règles.
    id_source           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    code                VARCHAR(40) NOT NULL UNIQUE,        -- TNCD-2024, JPS-2022...
    titre               VARCHAR(200),
    version             VARCHAR(50),
    date_publication    DATE
);

-- ============================================================================
-- 3. DOSSIER PATIENT (case wrapper) et contexte familial/génétique (A.1)
-- ============================================================================

CREATE TABLE public.dossier_patient (
    id_dossier              INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_patient              INT NOT NULL,
    id_medecin_referent     INT,
    date_creation           TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_modification       TIMESTAMPTZ NOT NULL DEFAULT now(),
    statut                  public.t_statut_dossier NOT NULL DEFAULT 'ouvert',
    -- RESTRICT : pas de suppression physique en cascade ; préférer la clôture /
    -- l'archivage (statut) pour la traçabilité médico-légale.
    CONSTRAINT fk_dossier_patient FOREIGN KEY (id_patient) REFERENCES public.patient(id_patient) ON DELETE RESTRICT,
    CONSTRAINT fk_dossier_medecin FOREIGN KEY (id_medecin_referent) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL
);

CREATE TRIGGER trg_dossier_patient_updated
    BEFORE UPDATE ON public.dossier_patient
    FOR EACH ROW EXECUTE FUNCTION public.set_date_modification();

CREATE TABLE public.antecedent_familial (
-- Elle représente les antécédents familiaux de cancer du pancréas.
    id_antecedent           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_dossier              INT NOT NULL,
    degre_parente           public.t_degre_parente DEFAULT 'inconnu',
    nombre_apparentes       SMALLINT DEFAULT 1,
    type_cancer             VARCHAR(80) DEFAULT 'pancreas',
    CONSTRAINT fk_antecedent_dossier FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE,
    CHECK (nombre_apparentes >= 1)
);

CREATE TABLE public.mutation_germinale (
-- Elle représente les mutations génétiques connues du patient.
-- Convention : absence de ligne pour un gène = gène non testé.
    id_mutation             INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_dossier              INT NOT NULL,
    id_gene                 INT NOT NULL,
    statut                  public.t_statut_mutation NOT NULL DEFAULT 'mute',
    date_test               DATE,
    CONSTRAINT fk_mutation_dossier FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE,
    CONSTRAINT fk_mutation_gene FOREIGN KEY (id_gene) REFERENCES public.gene(id_gene),
    CONSTRAINT uq_mutation UNIQUE (id_dossier, id_gene)
);

-- ============================================================================
-- 4. ÉVALUATION CLINIQUE — un point dans le temps (A.2)
--    Support du parcours longitudinal : diagnostic → néoadjuvant →
--    réévaluation → chirurgie → adjuvant → surveillance → récidive
-- ============================================================================

CREATE TABLE public.evaluation_clinique (
-- C'est l'évaluation de l'état du patient à un moment donné.
    id_evaluation           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_dossier              INT NOT NULL,
    id_medecin_evaluateur   INT,
    date_evaluation         DATE NOT NULL,
    contexte                public.t_contexte_evaluation DEFAULT 'diagnostic',
    ecog                    SMALLINT,                         -- 0-4 ; NULL = inconnu (jamais traité comme 0)
    etat_nutritionnel       public.t_etat_nutritionnel DEFAULT 'inconnu',
    douleur_presente        BOOLEAN,
    intensite_douleur       SMALLINT,                         -- échelle 0-10
    ictere                  BOOLEAN,
    diabete                 public.t_diabete DEFAULT 'inconnu',
    date_creation           TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_evaluation_dossier FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE RESTRICT,
    CONSTRAINT fk_evaluation_medecin FOREIGN KEY (id_medecin_evaluateur) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL,
    CHECK (ecog IS NULL OR ecog BETWEEN 0 AND 4),
    CHECK (intensite_douleur IS NULL OR intensite_douleur BETWEEN 0 AND 10)
);

CREATE TABLE public.evaluation_comorbidite (
-- C'est une table de liaison entre evaluation et comorbidite
    id_evaluation           INT NOT NULL,
    id_comorbidite          INT NOT NULL,
    severite                public.t_severite DEFAULT 'mineure',
    note                    TEXT,
    PRIMARY KEY (id_evaluation, id_comorbidite),
    CONSTRAINT fk_evalcomorb_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE,
    CONSTRAINT fk_evalcomorb_comorbidite FOREIGN KEY (id_comorbidite) REFERENCES public.comorbidite(id_comorbidite)
);

-- ============================================================================
-- 5. BIOLOGIE — saisi, par évaluation (A.3)
-- ============================================================================

CREATE TABLE public.biologie (
-- Elle contient les résultats biologiques.
    id_biologie             INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation           INT NOT NULL,
    ca19_9                  NUMERIC(10,2),                    -- U/mL — seuil clé 500 (critère B, si sans cholestase)
    ca19_9_multiple_lsn     NUMERIC(8,2),                     -- pour situations exceptionnelles (>10N)
    cholestase              BOOLEAN,                          -- NULL = inconnu => BLOQUER l'interprétation du CA19-9 (jamais traité comme FALSE)
    bilirubine              NUMERIC(8,2),                     -- µmol/L — seuil 250 (drainage urgent)
    bilirubine_ratio_lsn    NUMERIC(6,2),                     -- seuil 1.5xLSN (choix protocole métastatique)
    statut_lewis            public.t_statut_lewis DEFAULT 'inconnu',
    statut_dpd              public.t_statut_dpd DEFAULT 'non_teste',
    albuminemie             NUMERIC(5,2),                     -- g/L — seuil indicatif 35
    date_analyse            DATE,
    CONSTRAINT fk_biologie_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE,
    CHECK (ca19_9 IS NULL OR ca19_9 >= 0)
);

-- ============================================================================
-- 6. IMAGERIE — saisi UNIQUEMENT (A.4) — la résécabilité est DÉDUITE,
--    jamais stockée ici (voir donnees_derivees)
-- ============================================================================

CREATE TABLE public.imagerie (
    id_imagerie                        INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation                      INT NOT NULL,
    type_imagerie                      public.t_type_imagerie NOT NULL,  -- TDM/IRM seuls : base du bilan de résécabilité TNCD ; TEP-TDM et écho-endoscopie volontairement exclus (bilans complémentaires)
    date_imagerie                      DATE NOT NULL,          -- TNCD : doit être < 4 semaines avant décision
    localisation_tumorale              public.t_localisation_tumorale DEFAULT 'inconnu',
    taille_tumorale_cm                 NUMERIC(5,2),
    contact_ams                        public.t_contact_vaisseau,
    contact_tronc_coeliaque            public.t_contact_vaisseau,
    contact_art_hepatique              public.t_contact_art_hepatique,
    contact_vms_vp                     public.t_contact_vms_vp,
    extension_ganglionnaire_regionale  BOOLEAN DEFAULT FALSE,  -- loge pancréatique, ne contre-indique PAS la résection
    extension_ganglionnaire_distance   BOOLEAN,                -- hile hépatique, mésentère... ; NULL = inconnu => BLOQUER la décision chirurgicale
    metastases_presentes               BOOLEAN,                -- NULL = inconnu => BLOQUER la décision chirurgicale
    CONSTRAINT fk_imagerie_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE,
    CHECK (taille_tumorale_cm IS NULL OR taille_tumorale_cm > 0)
);

CREATE TABLE public.metastase_localisation (
-- Elle précise où se trouvent les métastases.
    id_metastase        INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_imagerie         INT NOT NULL,
    site                public.t_site_metastase NOT NULL,
    detail              TEXT,
    CONSTRAINT fk_metastase_imagerie FOREIGN KEY (id_imagerie) REFERENCES public.imagerie(id_imagerie) ON DELETE CASCADE,
    CONSTRAINT uq_metastase UNIQUE (id_imagerie, site)
);

-- ============================================================================
-- 7. HISTOLOGIE ET BIOLOGIE MOLÉCULAIRE — saisi (A.6)
-- ============================================================================

CREATE TABLE public.histologie_biologie (
-- Elle contient les résultats histologiques et moléculaires principaux.
    id_histo                INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation           INT NOT NULL,
    preuve_histologique     BOOLEAN DEFAULT FALSE,          -- obligatoire avant tout ttt médical, pas avant chirurgie d'emblée
    statut_brca_germinal    public.t_statut_brca DEFAULT 'non_teste',
    statut_kras             public.t_statut_kras DEFAULT 'non_teste',
    statut_msi_dmmr         public.t_statut_msi DEFAULT 'non_teste',
    fusion_ntrk             public.t_fusion DEFAULT 'non_teste',
    fusion_nrg1             public.t_fusion DEFAULT 'non_teste',
    CONSTRAINT fk_histo_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE,
    CONSTRAINT uq_histo_evaluation UNIQUE (id_evaluation)
);

-- Granularité fine pour la RCP moléculaire (2e/3e ligne, essais cliniques)
CREATE TABLE public.analyse_moleculaire (
-- C'est une version plus détaillée de l'analyse génétique.
    id_analyse              INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation           INT NOT NULL,
    type_test               public.t_type_test,
    gene                    VARCHAR(50),                     -- ex. KRAS
    alteration              VARCHAR(120),                    -- ex. p.G12C
    classe_escat            public.t_classe_escat,
    date_test               DATE,
    reference_rapport       VARCHAR(120),
    CONSTRAINT fk_analysemol_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE
);

-- ============================================================================
-- 8. DONNÉES DÉRIVÉES — calculées par le moteur UNIQUEMENT (A.4bis, A.5)
--    Jamais écrites/modifiées par un utilisateur.
-- ============================================================================

CREATE TABLE public.donnees_derivees (
-- Ce sont les données que le moteur de règles calcule automatiquement.
    id_derive               INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation           INT NOT NULL,
    version_moteur          VARCHAR(20) NOT NULL,
    source_code             VARCHAR(20) NOT NULL DEFAULT 'TNCD-2024',
    source_version          VARCHAR(30) NOT NULL DEFAULT '17/05/2024',
    date_calcul             TIMESTAMPTZ NOT NULL DEFAULT now(),

    resecabilite            public.t_resecabilite DEFAULT 'inconnu',

    categorie_t             public.t_categorie_t,
    categorie_n             public.t_categorie_n,
    categorie_m             public.t_categorie_m,
    stade_global            public.t_stade_global DEFAULT 'inconnu',

    critere_abc_a           VARCHAR(30),                       -- = résécabilité, dupliqué pour lisibilité
    critere_abc_b           BOOLEAN,                           -- CA19-9 > 500 ET SANS cholestase
    critere_abc_c           BOOLEAN,                           -- TODO avant production : trancher le seuil ECOG (>=1 ou >=2)
    sous_categorie_abc      VARCHAR(30),                       -- ex. 'Resecable_A', 'Resecable_AB', 'Resecable_ABC'
    -- Augmentation de sous_categorie_abc à 30 caractères pour éviter les erreurs de troncature des valeurs générées comme 'metastatique_ABC

    justification_calcul    TEXT,                              -- explication lisible du calcul

    CONSTRAINT fk_derive_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE,
    CONSTRAINT uq_derive_version UNIQUE (id_evaluation, version_moteur)
);

-- ============================================================================
-- 9. PARCOURS THÉRAPEUTIQUE (A.7)
-- ============================================================================

CREATE TABLE public.traitement (
-- Elle représente le traitement réellement reçu par le patient.
    id_traitement           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_dossier              INT NOT NULL,
    id_protocole            INT,
    numero_ligne            SMALLINT,                          -- 1, 2, 3...
    date_debut              DATE,
    date_fin                DATE,
    reponse                 public.t_reponse,
    toxicite_residuelle     BOOLEAN DEFAULT FALSE,
    type_toxicite           VARCHAR(120),                      -- ex. neuropathie
    termine_comme_prevu     BOOLEAN,
    notes                   TEXT,
    CONSTRAINT fk_traitement_dossier FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE,
    CONSTRAINT fk_traitement_protocole FOREIGN KEY (id_protocole) REFERENCES public.protocole_traitement(id_protocole),
    CHECK (date_fin IS NULL OR date_debut IS NULL OR date_fin >= date_debut)
);

-- ============================================================================
-- 10. BASE DE CONNAISSANCE — moteur de règles (cœur du CDSS)
-- ============================================================================

CREATE TABLE public.regle (
    id_regle                INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    code_regle              VARCHAR(20) NOT NULL UNIQUE,       -- ex. R01, R02...
    nom                     VARCHAR(120),
    id_source               INT NOT NULL,
    section_reference       VARCHAR(60),                       -- ex. "TNCD 9.5.1"
    grade_preuve            public.t_grade_preuve,
    priorite                INT DEFAULT 100,                   -- plus petit = priorité plus haute
    categorie               VARCHAR(30) DEFAULT 'strategie',
    necessite_rcp           BOOLEAN DEFAULT FALSE,
    actif                   BOOLEAN DEFAULT TRUE,               -- désactivation logique (sans suppression)
    condition_json          JSONB,                              -- SOURCE DE VÉRITÉ : arbre de conditions lu par le moteur
    texte_conclusion        TEXT,                               -- repli voulu si regle_conclusion est vide
    justification           TEXT,
    version                 INT DEFAULT 1,
    date_creation           TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_modification       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_regle_source FOREIGN KEY (id_source) REFERENCES public.source_referentiel(id_source)
);

CREATE TRIGGER trg_regle_updated
    BEFORE UPDATE ON public.regle
    FOR EACH ROW EXECUTE FUNCTION public.set_date_modification();

CREATE INDEX idx_regle_actif_priorite ON public.regle (actif, priorite);

CREATE TABLE public.regle_condition (
-- Cette table décompose les conditions d'une règle (vue lisible/dénombrable).
-- Dérivée de regle.condition_json, qui reste la SEULE source de vérité lue
-- par le moteur : maintenir les deux strictement en cohérence à l'écriture.
    id_condition             INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_regle                 INT NOT NULL,
    attribut                 VARCHAR(80) NOT NULL,             -- ex. "ecog", "ca19_9"
    operateur                public.t_operateur NOT NULL,
    valeur                   VARCHAR(80),
    operateur_liaison        public.t_operateur_liaison DEFAULT 'ET',
    ordre_index              INT DEFAULT 0,
    CONSTRAINT fk_condition_regle FOREIGN KEY (id_regle) REFERENCES public.regle(id_regle) ON DELETE CASCADE
);

CREATE TABLE public.regle_conclusion (
-- Elle contient ce que la règle recommande.
    id_conclusion            INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_regle                 INT NOT NULL,
    type_conclusion          public.t_type_conclusion,
    texte_conclusion         TEXT,
    id_protocole             INT,
    CONSTRAINT fk_conclusion_regle FOREIGN KEY (id_regle) REFERENCES public.regle(id_regle) ON DELETE CASCADE,
    CONSTRAINT fk_conclusion_protocole FOREIGN KEY (id_protocole) REFERENCES public.protocole_traitement(id_protocole)
);

CREATE TABLE public.regle_historique (
-- Elle garde l'historique des modifications des règles.
    id_historique            INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_regle                 INT NOT NULL,
    ancienne_version         JSONB,
    nouvelle_version         JSONB,
    modifie_par              INT,
    date_modification        TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_historique_regle FOREIGN KEY (id_regle) REFERENCES public.regle(id_regle) ON DELETE CASCADE,
    CONSTRAINT fk_historique_medecin FOREIGN KEY (modifie_par) REFERENCES public.medecin(id_medecin)
);

-- ============================================================================
-- 11. DÉCISIONS ET EXPLICABILITÉ — traçabilité complète d'une recommandation
-- ============================================================================

CREATE TABLE public.decision (
    id_decision              INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_evaluation            INT NOT NULL,
    id_derive                INT,
    date_decision            TIMESTAMPTZ NOT NULL DEFAULT now(),
    decide_par               INT,                              -- médecin ayant déclenché le calcul (ou système)
    source_code              VARCHAR(20),
    source_version           VARCHAR(30),
    snapshot_patient         JSONB,                             -- copie immuable des données au moment de la décision
    resume                   TEXT,
    necessite_rcp            BOOLEAN DEFAULT FALSE,
    -- RESTRICT : une décision est une trace médico-légale, jamais supprimée
    -- en cascade ; passer par l'archivage.
    CONSTRAINT fk_decision_evaluation FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE RESTRICT,
    CONSTRAINT fk_decision_derive FOREIGN KEY (id_derive) REFERENCES public.donnees_derivees(id_derive),
    CONSTRAINT fk_decision_medecin FOREIGN KEY (decide_par) REFERENCES public.medecin(id_medecin)
);

CREATE TABLE public.decision_regle_declenchee (
-- Elle permet de savoir quelles règles ont été déclenchées pour produire une décision.
    id_declenchement         INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_decision              INT NOT NULL,
    id_regle                 INT NOT NULL,
    version_regle            INT,
    a_matche                 BOOLEAN DEFAULT TRUE,
    est_alternative          BOOLEAN DEFAULT FALSE,             -- règle concurrente / exception considérée
    valeur_decisive          TEXT,                              -- valeur du paramètre qui a fait pencher la règle
    conditions_snapshot      JSONB,                             -- {attribut: valeur} au moment de l'exécution
    texte_conclusion         TEXT,
    grade_preuve             VARCHAR(20),
    section_reference        VARCHAR(60),
    CONSTRAINT fk_declenchee_decision FOREIGN KEY (id_decision) REFERENCES public.decision(id_decision) ON DELETE CASCADE,
    CONSTRAINT fk_declenchee_regle FOREIGN KEY (id_regle) REFERENCES public.regle(id_regle)
);

CREATE TABLE public.decision_explication (
-- Elle explique la décision étape par étape.
    id_explication           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_decision              INT NOT NULL,
    ordre_etape              INT NOT NULL,
    texte_etape              TEXT NOT NULL,
    CONSTRAINT fk_explication_decision FOREIGN KEY (id_decision) REFERENCES public.decision(id_decision) ON DELETE CASCADE
);

-- ============================================================================
-- 12. RCP — réunion de concertation pluridisciplinaire
-- ============================================================================

CREATE TABLE public.rcp (
-- rcp=Réunion de Concertation Pluridisciplinaire.
    id_rcp                   INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_dossier               INT NOT NULL,
    id_decision              INT,
    date_rcp                 DATE,
    decision_finale          TEXT,
    CONSTRAINT fk_rcp_dossier FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE,
    CONSTRAINT fk_rcp_decision FOREIGN KEY (id_decision) REFERENCES public.decision(id_decision)
);

CREATE TABLE public.rcp_participant (
-- Elle indique quels médecins participent à quelle RCP.
    id_participant           INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_rcp                   INT NOT NULL,
    id_medecin               INT NOT NULL,
    role_dans_rcp            VARCHAR(40),                      -- ex. président, chirurgien, oncologue...
    CONSTRAINT fk_participant_rcp FOREIGN KEY (id_rcp) REFERENCES public.rcp(id_rcp) ON DELETE CASCADE,
    CONSTRAINT fk_participant_medecin FOREIGN KEY (id_medecin) REFERENCES public.medecin(id_medecin),
    CONSTRAINT uq_participant UNIQUE (id_rcp, id_medecin)
);

-- ============================================================================
-- 13. AUDIT — traçabilité générale des actions
-- ============================================================================

CREATE TABLE public.journal_audit (
-- C'est le journal de toutes les actions importantes.
    id_journal               INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    id_medecin               INT,
    action                   VARCHAR(40),                      -- patient_create, evaluation_create, rule_fire, rule_edit, decision_view...
    type_entite              VARCHAR(40),
    id_entite                INT,
    detail                   JSONB,
    date_action              TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_journal_medecin FOREIGN KEY (id_medecin) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL
);

CREATE INDEX idx_journal_medecin ON public.journal_audit (id_medecin);
CREATE INDEX idx_journal_entite  ON public.journal_audit (type_entite, id_entite);

COMMIT;
