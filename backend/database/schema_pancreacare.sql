-- ============================================================================
-- Schema PostgreSQL de PANCRA - base locale de developpement
--
-- SOURCE DE VERITE UNIQUE du schema applicatif : ce fichier reproduit a
-- l'identique la base locale (22 tables, 31 types enumeres). Il remplace
-- l'ancien schema Supabase et le dossier database/migrations/ : plus de
-- migrations incrementales a rejouer, un seul script cree l'etat final.
--
-- Genere avec :
--   pg_dump --schema-only --no-owner --no-privileges <base>
--
-- Usage : a rejouer UNIQUEMENT sur une base vide (voir
-- pancreacare_local_postgres.ps1). Ne pas executer sur une base contenant
-- deja des donnees.
-- ============================================================================

--
-- PostgreSQL database dump
--


-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: t_categorie_m; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_categorie_m AS ENUM (
    'M0',
    'M1'
);


--
-- Name: t_categorie_n; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_categorie_n AS ENUM (
    'N0',
    'N1',
    'N2',
    'NX'
);


--
-- Name: t_categorie_t; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_categorie_t AS ENUM (
    'T1a',
    'T1b',
    'T1c',
    'T2',
    'T3',
    'T4',
    'TX'
);


--
-- Name: t_classe_escat; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_classe_escat AS ENUM (
    'I',
    'II',
    'III',
    'IV',
    'V',
    'non_classe'
);


--
-- Name: t_contact_art_hepatique; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_contact_art_hepatique AS ENUM (
    'absent',
    'court_sans_envahissement',
    'envahissant'
);


--
-- Name: t_contact_vaisseau; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_contact_vaisseau AS ENUM (
    'absent',
    'lt180',
    'ge180'
);


--
-- Name: t_contact_vms_vp; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_contact_vms_vp AS ENUM (
    'absent',
    'lt180_sans_irregularite',
    'ge180_ou_irregularite',
    'occlusion_reconstructible',
    'occlusion_non_reconstructible'
);


--
-- Name: t_contexte_evaluation; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_contexte_evaluation AS ENUM (
    'diagnostic',
    'pre_neoadjuvant',
    'restaging',
    'pre_chirurgie',
    'adjuvant',
    'surveillance',
    'recidive'
);


--
-- Name: t_degre_parente; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_degre_parente AS ENUM (
    'premier_degre',
    'deuxieme_degre',
    'troisieme_degre_ou_plus',
    'inconnu'
);


--
-- Name: t_diabete; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_diabete AS ENUM (
    'absent',
    'recent_moins_2ans',
    'ancien',
    'inconnu'
);


--
-- Name: t_etat_nutritionnel; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_etat_nutritionnel AS ENUM (
    'normal',
    'denutrition_moderee',
    'denutrition_severe',
    'inconnu'
);


--
-- Name: t_fusion; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_fusion AS ENUM (
    'positif',
    'negatif',
    'non_teste'
);


--
-- Name: t_localisation_tumorale; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_localisation_tumorale AS ENUM (
    'tete_crochet',
    'corps_queue',
    'inconnu'
);


--
-- Name: t_reponse; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_reponse AS ENUM (
    'reponse',
    'stable',
    'progression',
    'non_evaluable'
);


--
-- Name: t_resecabilite; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_resecabilite AS ENUM (
    'resecable',
    'borderline',
    'localement_avance',
    'metastatique',
    'inconnu'
);


--
-- Name: t_role_compte; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_role_compte AS ENUM (
    'medecin',
    'super_admin'
);


--
-- Name: t_severite; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_severite AS ENUM (
    'mineure',
    'majeure'
);


--
-- Name: t_sexe; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_sexe AS ENUM (
    'M',
    'F',
    'inconnu'
);


--
-- Name: t_site_metastase; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_site_metastase AS ENUM (
    'hepatique',
    'peritoneale',
    'pulmonaire',
    'osseuse',
    'autre'
);


--
-- Name: t_stade_global; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_stade_global AS ENUM (
    'IA',
    'IB',
    'IIA',
    'IIB',
    'III',
    'IV',
    'inconnu'
);


--
-- Name: t_statut_brca; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_brca AS ENUM (
    'mute',
    'non_mute',
    'non_teste'
);


--
-- Name: t_statut_compte; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_compte AS ENUM (
    'en_attente',
    'actif',
    'bloque'
);


--
-- Name: t_statut_demande_reinit; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_demande_reinit AS ENUM (
    'en_attente',
    'traitee',
    'annulee'
);


--
-- Name: t_statut_dossier; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_dossier AS ENUM (
    'ouvert',
    'clos',
    'archive'
);


--
-- Name: t_statut_dpd; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_dpd AS ENUM (
    'normal',
    'deficit_partiel',
    'deficit_complet',
    'non_teste'
);


--
-- Name: t_statut_kras; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_kras AS ENUM (
    'sauvage',
    'g12c',
    'g12d',
    'g12v',
    'autre_mute',
    'non_teste'
);


--
-- Name: t_statut_lewis; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_lewis AS ENUM (
    'exprime',
    'a_b_negatif',
    'inconnu'
);


--
-- Name: t_statut_msi; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_msi AS ENUM (
    'mss',
    'msi_h',
    'dmmr',
    'non_teste'
);


--
-- Name: t_statut_mutation; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_statut_mutation AS ENUM (
    'mute',
    'non_mute'
);


--
-- Name: t_type_imagerie; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_type_imagerie AS ENUM (
    'TDM',
    'IRM'
);


--
-- Name: t_type_test; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.t_type_test AS ENUM (
    'panel',
    'germinal',
    'biopsie_liquide',
    'ihc',
    'ngs_arn'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: analyse_moleculaire; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.analyse_moleculaire (
    id_analyse integer NOT NULL,
    id_evaluation integer NOT NULL,
    type_test public.t_type_test,
    gene character varying(50),
    alteration character varying(120),
    classe_escat public.t_classe_escat,
    date_test date,
    reference_rapport character varying(120)
);


--
-- Name: analyse_moleculaire_id_analyse_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.analyse_moleculaire_id_analyse_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: analyse_moleculaire_id_analyse_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.analyse_moleculaire_id_analyse_seq OWNED BY public.analyse_moleculaire.id_analyse;


--
-- Name: antecedent_familial; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.antecedent_familial (
    id_antecedent integer NOT NULL,
    id_dossier integer NOT NULL,
    degre_parente public.t_degre_parente,
    nombre_apparentes smallint,
    type_cancer character varying(80)
);


--
-- Name: antecedent_familial_id_antecedent_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.antecedent_familial_id_antecedent_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: antecedent_familial_id_antecedent_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.antecedent_familial_id_antecedent_seq OWNED BY public.antecedent_familial.id_antecedent;


--
-- Name: biologie; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.biologie (
    id_biologie integer NOT NULL,
    id_evaluation integer NOT NULL,
    ca19_9 numeric(10,2),
    ca19_9_multiple_lsn numeric(8,2),
    cholestase boolean,
    bilirubine numeric(8,2),
    bilirubine_ratio_lsn numeric(6,2),
    statut_lewis public.t_statut_lewis,
    statut_dpd public.t_statut_dpd,
    albuminemie numeric(5,2),
    date_analyse date
);


--
-- Name: biologie_id_biologie_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.biologie_id_biologie_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: biologie_id_biologie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.biologie_id_biologie_seq OWNED BY public.biologie.id_biologie;


--
-- Name: comorbidite; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comorbidite (
    id_comorbidite integer NOT NULL,
    code character varying(30) NOT NULL,
    libelle_fr character varying(120),
    libelle_en character varying(120)
);


--
-- Name: comorbidite_id_comorbidite_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comorbidite_id_comorbidite_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comorbidite_id_comorbidite_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comorbidite_id_comorbidite_seq OWNED BY public.comorbidite.id_comorbidite;


--
-- Name: compte; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compte (
    id_compte integer NOT NULL,
    email character varying(255) NOT NULL,
    mot_de_passe_hash text NOT NULL,
    role public.t_role_compte NOT NULL,
    statut public.t_statut_compte NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    telephone character varying(30),
    hopital character varying(150),
    id_medecin integer,
    doit_changer_mdp boolean NOT NULL,
    motif_blocage text,
    tentatives_echouees integer NOT NULL,
    verrouille_jusqu_a timestamp with time zone,
    date_activation timestamp with time zone,
    active_par integer,
    date_derniere_connexion timestamp with time zone,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: compte_id_compte_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.compte_id_compte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: compte_id_compte_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.compte_id_compte_seq OWNED BY public.compte.id_compte;


--
-- Name: decision; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.decision (
    id_decision integer NOT NULL,
    id_evaluation integer NOT NULL,
    date_decision timestamp with time zone DEFAULT now() NOT NULL,
    decide_par integer,
    source_code character varying(20),
    source_version character varying(30),
    snapshot_patient json,
    resume text,
    decision_medecin text,
    necessite_rcp boolean
);


--
-- Name: decision_id_decision_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.decision_id_decision_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: decision_id_decision_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.decision_id_decision_seq OWNED BY public.decision.id_decision;


--
-- Name: demande_reinitialisation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.demande_reinitialisation (
    id_demande integer NOT NULL,
    id_compte integer NOT NULL,
    statut public.t_statut_demande_reinit NOT NULL,
    jeton_hash text,
    expire_le timestamp with time zone,
    motif text,
    traite_par integer,
    date_demande timestamp with time zone DEFAULT now() NOT NULL,
    date_traitement timestamp with time zone
);


--
-- Name: demande_reinitialisation_id_demande_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.demande_reinitialisation_id_demande_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: demande_reinitialisation_id_demande_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.demande_reinitialisation_id_demande_seq OWNED BY public.demande_reinitialisation.id_demande;


--
-- Name: donnees_derivees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.donnees_derivees (
    id_derive integer NOT NULL,
    id_evaluation integer NOT NULL,
    version_moteur character varying(20) NOT NULL,
    source_code character varying(20) NOT NULL,
    source_version character varying(30) NOT NULL,
    date_calcul timestamp with time zone DEFAULT now() NOT NULL,
    resecabilite public.t_resecabilite,
    categorie_t public.t_categorie_t,
    categorie_n public.t_categorie_n,
    categorie_m public.t_categorie_m,
    stade_global public.t_stade_global,
    critere_abc_a character varying(30),
    critere_abc_b boolean,
    critere_abc_c boolean,
    sous_categorie_abc character varying(30),
    justification_calcul text
);


--
-- Name: donnees_derivees_id_derive_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.donnees_derivees_id_derive_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: donnees_derivees_id_derive_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.donnees_derivees_id_derive_seq OWNED BY public.donnees_derivees.id_derive;


--
-- Name: dossier_patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dossier_patient (
    id_dossier integer NOT NULL,
    id_patient integer NOT NULL,
    id_medecin_referent integer,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    statut public.t_statut_dossier NOT NULL
);


--
-- Name: dossier_patient_id_dossier_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dossier_patient_id_dossier_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dossier_patient_id_dossier_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dossier_patient_id_dossier_seq OWNED BY public.dossier_patient.id_dossier;


--
-- Name: evaluation_clinique; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_clinique (
    id_evaluation integer NOT NULL,
    id_dossier integer NOT NULL,
    id_medecin_evaluateur integer,
    date_evaluation date NOT NULL,
    contexte public.t_contexte_evaluation,
    ecog smallint,
    etat_nutritionnel public.t_etat_nutritionnel,
    douleur_presente boolean,
    intensite_douleur smallint,
    ictere boolean,
    diabete public.t_diabete,
    date_creation timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: evaluation_clinique_id_evaluation_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.evaluation_clinique_id_evaluation_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: evaluation_clinique_id_evaluation_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.evaluation_clinique_id_evaluation_seq OWNED BY public.evaluation_clinique.id_evaluation;


--
-- Name: evaluation_comorbidite; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_comorbidite (
    id_evaluation integer NOT NULL,
    id_comorbidite integer NOT NULL,
    severite public.t_severite,
    note text
);


--
-- Name: evaluation_parcours_therapeutique; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.evaluation_parcours_therapeutique (
    id_parcours bigint NOT NULL,
    id_evaluation integer NOT NULL,
    angiocholite boolean,
    comorbidites_lourdes boolean,
    tumeur_controlee boolean,
    nouvelles_metastases boolean,
    chirurgie_d_emblee boolean,
    traitement_medical_prevu boolean,
    pas_de_progression_apres_16_semaines_platine boolean,
    date_reevaluation date,
    commentaire text,
    date_creation timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: evaluation_parcours_therapeutique_id_parcours_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.evaluation_parcours_therapeutique_id_parcours_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: evaluation_parcours_therapeutique_id_parcours_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.evaluation_parcours_therapeutique_id_parcours_seq OWNED BY public.evaluation_parcours_therapeutique.id_parcours;


--
-- Name: gene; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.gene (
    id_gene integer NOT NULL,
    code character varying(30) NOT NULL,
    libelle character varying(120),
    syndrome character varying(150),
    cancers_associes text
);


--
-- Name: gene_id_gene_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.gene_id_gene_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: gene_id_gene_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.gene_id_gene_seq OWNED BY public.gene.id_gene;


--
-- Name: histologie_biologie; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.histologie_biologie (
    id_histo integer NOT NULL,
    id_evaluation integer NOT NULL,
    preuve_histologique boolean,
    statut_brca_germinal public.t_statut_brca,
    statut_kras public.t_statut_kras,
    statut_msi_dmmr public.t_statut_msi,
    fusion_ntrk public.t_fusion,
    fusion_nrg1 public.t_fusion
);


--
-- Name: histologie_biologie_id_histo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.histologie_biologie_id_histo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: histologie_biologie_id_histo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.histologie_biologie_id_histo_seq OWNED BY public.histologie_biologie.id_histo;


--
-- Name: imagerie; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.imagerie (
    id_imagerie integer NOT NULL,
    id_evaluation integer NOT NULL,
    type_imagerie public.t_type_imagerie NOT NULL,
    date_imagerie date NOT NULL,
    localisation_tumorale public.t_localisation_tumorale,
    taille_tumorale_cm numeric(5,2),
    contact_ams public.t_contact_vaisseau,
    contact_tronc_coeliaque public.t_contact_vaisseau,
    contact_art_hepatique public.t_contact_art_hepatique,
    contact_vms_vp public.t_contact_vms_vp,
    extension_ganglionnaire_regionale boolean,
    extension_ganglionnaire_distance boolean,
    metastases_presentes boolean
);


--
-- Name: imagerie_id_imagerie_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.imagerie_id_imagerie_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: imagerie_id_imagerie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.imagerie_id_imagerie_seq OWNED BY public.imagerie.id_imagerie;


--
-- Name: journal_audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.journal_audit (
    id_journal integer NOT NULL,
    id_medecin integer,
    action character varying(40),
    type_entite character varying(40),
    id_entite integer,
    detail json,
    date_action timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: journal_audit_id_journal_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.journal_audit_id_journal_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: journal_audit_id_journal_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.journal_audit_id_journal_seq OWNED BY public.journal_audit.id_journal;


--
-- Name: medecin; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medecin (
    id_medecin integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    telephone character varying(30),
    hopital character varying(150),
    date_creation timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: medecin_id_medecin_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.medecin_id_medecin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: medecin_id_medecin_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.medecin_id_medecin_seq OWNED BY public.medecin.id_medecin;


--
-- Name: metastase_localisation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.metastase_localisation (
    id_metastase integer NOT NULL,
    id_imagerie integer NOT NULL,
    site public.t_site_metastase NOT NULL,
    detail text
);


--
-- Name: metastase_localisation_id_metastase_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.metastase_localisation_id_metastase_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: metastase_localisation_id_metastase_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.metastase_localisation_id_metastase_seq OWNED BY public.metastase_localisation.id_metastase;


--
-- Name: mutation_germinale; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mutation_germinale (
    id_mutation integer NOT NULL,
    id_dossier integer NOT NULL,
    id_gene integer NOT NULL,
    statut public.t_statut_mutation NOT NULL,
    date_test date
);


--
-- Name: mutation_germinale_id_mutation_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mutation_germinale_id_mutation_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mutation_germinale_id_mutation_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mutation_germinale_id_mutation_seq OWNED BY public.mutation_germinale.id_mutation;


--
-- Name: patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patient (
    id_patient integer NOT NULL,
    nom character varying(100) NOT NULL,
    prenom character varying(100) NOT NULL,
    date_naissance date,
    sexe public.t_sexe NOT NULL,
    telephone character varying(30),
    email character varying(255),
    adresse character varying(255),
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: patient_id_patient_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patient_id_patient_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: patient_id_patient_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patient_id_patient_seq OWNED BY public.patient.id_patient;


--
-- Name: protocole_traitement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.protocole_traitement (
    id_protocole integer NOT NULL,
    code character varying(30) NOT NULL,
    libelle_fr character varying(120),
    libelle_en character varying(120),
    description text
);


--
-- Name: protocole_traitement_id_protocole_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.protocole_traitement_id_protocole_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: protocole_traitement_id_protocole_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.protocole_traitement_id_protocole_seq OWNED BY public.protocole_traitement.id_protocole;


--
-- Name: traitement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traitement (
    id_traitement integer NOT NULL,
    id_dossier integer NOT NULL,
    id_protocole integer,
    numero_ligne smallint,
    date_debut date,
    date_fin date,
    reponse public.t_reponse,
    toxicite_residuelle boolean,
    type_toxicite character varying(120),
    termine_comme_prevu boolean,
    notes text
);


--
-- Name: traitement_id_traitement_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traitement_id_traitement_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traitement_id_traitement_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traitement_id_traitement_seq OWNED BY public.traitement.id_traitement;


--
-- Name: analyse_moleculaire id_analyse; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analyse_moleculaire ALTER COLUMN id_analyse SET DEFAULT nextval('public.analyse_moleculaire_id_analyse_seq'::regclass);


--
-- Name: antecedent_familial id_antecedent; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.antecedent_familial ALTER COLUMN id_antecedent SET DEFAULT nextval('public.antecedent_familial_id_antecedent_seq'::regclass);


--
-- Name: biologie id_biologie; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biologie ALTER COLUMN id_biologie SET DEFAULT nextval('public.biologie_id_biologie_seq'::regclass);


--
-- Name: comorbidite id_comorbidite; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comorbidite ALTER COLUMN id_comorbidite SET DEFAULT nextval('public.comorbidite_id_comorbidite_seq'::regclass);


--
-- Name: compte id_compte; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compte ALTER COLUMN id_compte SET DEFAULT nextval('public.compte_id_compte_seq'::regclass);


--
-- Name: decision id_decision; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.decision ALTER COLUMN id_decision SET DEFAULT nextval('public.decision_id_decision_seq'::regclass);


--
-- Name: demande_reinitialisation id_demande; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.demande_reinitialisation ALTER COLUMN id_demande SET DEFAULT nextval('public.demande_reinitialisation_id_demande_seq'::regclass);


--
-- Name: donnees_derivees id_derive; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donnees_derivees ALTER COLUMN id_derive SET DEFAULT nextval('public.donnees_derivees_id_derive_seq'::regclass);


--
-- Name: dossier_patient id_dossier; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dossier_patient ALTER COLUMN id_dossier SET DEFAULT nextval('public.dossier_patient_id_dossier_seq'::regclass);


--
-- Name: evaluation_clinique id_evaluation; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_clinique ALTER COLUMN id_evaluation SET DEFAULT nextval('public.evaluation_clinique_id_evaluation_seq'::regclass);


--
-- Name: evaluation_parcours_therapeutique id_parcours; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_parcours_therapeutique ALTER COLUMN id_parcours SET DEFAULT nextval('public.evaluation_parcours_therapeutique_id_parcours_seq'::regclass);


--
-- Name: gene id_gene; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gene ALTER COLUMN id_gene SET DEFAULT nextval('public.gene_id_gene_seq'::regclass);


--
-- Name: histologie_biologie id_histo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.histologie_biologie ALTER COLUMN id_histo SET DEFAULT nextval('public.histologie_biologie_id_histo_seq'::regclass);


--
-- Name: imagerie id_imagerie; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imagerie ALTER COLUMN id_imagerie SET DEFAULT nextval('public.imagerie_id_imagerie_seq'::regclass);


--
-- Name: journal_audit id_journal; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journal_audit ALTER COLUMN id_journal SET DEFAULT nextval('public.journal_audit_id_journal_seq'::regclass);


--
-- Name: medecin id_medecin; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medecin ALTER COLUMN id_medecin SET DEFAULT nextval('public.medecin_id_medecin_seq'::regclass);


--
-- Name: metastase_localisation id_metastase; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metastase_localisation ALTER COLUMN id_metastase SET DEFAULT nextval('public.metastase_localisation_id_metastase_seq'::regclass);


--
-- Name: mutation_germinale id_mutation; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mutation_germinale ALTER COLUMN id_mutation SET DEFAULT nextval('public.mutation_germinale_id_mutation_seq'::regclass);


--
-- Name: patient id_patient; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient ALTER COLUMN id_patient SET DEFAULT nextval('public.patient_id_patient_seq'::regclass);


--
-- Name: protocole_traitement id_protocole; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.protocole_traitement ALTER COLUMN id_protocole SET DEFAULT nextval('public.protocole_traitement_id_protocole_seq'::regclass);


--
-- Name: traitement id_traitement; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traitement ALTER COLUMN id_traitement SET DEFAULT nextval('public.traitement_id_traitement_seq'::regclass);


--
-- Name: analyse_moleculaire analyse_moleculaire_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analyse_moleculaire
    ADD CONSTRAINT analyse_moleculaire_pkey PRIMARY KEY (id_analyse);


--
-- Name: antecedent_familial antecedent_familial_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.antecedent_familial
    ADD CONSTRAINT antecedent_familial_pkey PRIMARY KEY (id_antecedent);


--
-- Name: biologie biologie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biologie
    ADD CONSTRAINT biologie_pkey PRIMARY KEY (id_biologie);


--
-- Name: comorbidite comorbidite_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comorbidite
    ADD CONSTRAINT comorbidite_code_key UNIQUE (code);


--
-- Name: comorbidite comorbidite_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comorbidite
    ADD CONSTRAINT comorbidite_pkey PRIMARY KEY (id_comorbidite);


--
-- Name: compte compte_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compte
    ADD CONSTRAINT compte_pkey PRIMARY KEY (id_compte);


--
-- Name: decision decision_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.decision
    ADD CONSTRAINT decision_pkey PRIMARY KEY (id_decision);


--
-- Name: demande_reinitialisation demande_reinitialisation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.demande_reinitialisation
    ADD CONSTRAINT demande_reinitialisation_pkey PRIMARY KEY (id_demande);


--
-- Name: donnees_derivees donnees_derivees_id_evaluation_version_moteur_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donnees_derivees
    ADD CONSTRAINT donnees_derivees_id_evaluation_version_moteur_key UNIQUE (id_evaluation, version_moteur);


--
-- Name: donnees_derivees donnees_derivees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donnees_derivees
    ADD CONSTRAINT donnees_derivees_pkey PRIMARY KEY (id_derive);


--
-- Name: dossier_patient dossier_patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dossier_patient
    ADD CONSTRAINT dossier_patient_pkey PRIMARY KEY (id_dossier);


--
-- Name: evaluation_clinique evaluation_clinique_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_clinique
    ADD CONSTRAINT evaluation_clinique_pkey PRIMARY KEY (id_evaluation);


--
-- Name: evaluation_comorbidite evaluation_comorbidite_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_comorbidite
    ADD CONSTRAINT evaluation_comorbidite_pkey PRIMARY KEY (id_evaluation, id_comorbidite);


--
-- Name: evaluation_parcours_therapeutique evaluation_parcours_therapeutique_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_parcours_therapeutique
    ADD CONSTRAINT evaluation_parcours_therapeutique_pkey PRIMARY KEY (id_parcours);


--
-- Name: gene gene_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gene
    ADD CONSTRAINT gene_code_key UNIQUE (code);


--
-- Name: gene gene_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gene
    ADD CONSTRAINT gene_pkey PRIMARY KEY (id_gene);


--
-- Name: histologie_biologie histologie_biologie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.histologie_biologie
    ADD CONSTRAINT histologie_biologie_pkey PRIMARY KEY (id_histo);


--
-- Name: imagerie imagerie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imagerie
    ADD CONSTRAINT imagerie_pkey PRIMARY KEY (id_imagerie);


--
-- Name: journal_audit journal_audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journal_audit
    ADD CONSTRAINT journal_audit_pkey PRIMARY KEY (id_journal);


--
-- Name: medecin medecin_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medecin
    ADD CONSTRAINT medecin_pkey PRIMARY KEY (id_medecin);


--
-- Name: metastase_localisation metastase_localisation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metastase_localisation
    ADD CONSTRAINT metastase_localisation_pkey PRIMARY KEY (id_metastase);


--
-- Name: mutation_germinale mutation_germinale_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mutation_germinale
    ADD CONSTRAINT mutation_germinale_pkey PRIMARY KEY (id_mutation);


--
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (id_patient);


--
-- Name: protocole_traitement protocole_traitement_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.protocole_traitement
    ADD CONSTRAINT protocole_traitement_code_key UNIQUE (code);


--
-- Name: protocole_traitement protocole_traitement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.protocole_traitement
    ADD CONSTRAINT protocole_traitement_pkey PRIMARY KEY (id_protocole);


--
-- Name: traitement traitement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traitement
    ADD CONSTRAINT traitement_pkey PRIMARY KEY (id_traitement);


--
-- Name: ix_analyse_moleculaire_id_analyse; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_analyse_moleculaire_id_analyse ON public.analyse_moleculaire USING btree (id_analyse);


--
-- Name: ix_antecedent_familial_id_antecedent; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_antecedent_familial_id_antecedent ON public.antecedent_familial USING btree (id_antecedent);


--
-- Name: ix_biologie_id_biologie; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_biologie_id_biologie ON public.biologie USING btree (id_biologie);


--
-- Name: ix_comorbidite_id_comorbidite; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_comorbidite_id_comorbidite ON public.comorbidite USING btree (id_comorbidite);


--
-- Name: ix_compte_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_compte_email ON public.compte USING btree (email);


--
-- Name: ix_compte_id_compte; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_compte_id_compte ON public.compte USING btree (id_compte);


--
-- Name: ix_decision_id_decision; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_decision_id_decision ON public.decision USING btree (id_decision);


--
-- Name: ix_demande_reinitialisation_id_demande; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_demande_reinitialisation_id_demande ON public.demande_reinitialisation USING btree (id_demande);


--
-- Name: ix_donnees_derivees_id_derive; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_donnees_derivees_id_derive ON public.donnees_derivees USING btree (id_derive);


--
-- Name: ix_dossier_patient_id_dossier; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_dossier_patient_id_dossier ON public.dossier_patient USING btree (id_dossier);


--
-- Name: ix_evaluation_clinique_id_evaluation; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_evaluation_clinique_id_evaluation ON public.evaluation_clinique USING btree (id_evaluation);


--
-- Name: ix_evaluation_parcours_therapeutique_id_evaluation; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_evaluation_parcours_therapeutique_id_evaluation ON public.evaluation_parcours_therapeutique USING btree (id_evaluation);


--
-- Name: ix_gene_id_gene; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_gene_id_gene ON public.gene USING btree (id_gene);


--
-- Name: ix_histologie_biologie_id_histo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_histologie_biologie_id_histo ON public.histologie_biologie USING btree (id_histo);


--
-- Name: ix_imagerie_id_imagerie; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_imagerie_id_imagerie ON public.imagerie USING btree (id_imagerie);


--
-- Name: ix_journal_audit_id_journal; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_journal_audit_id_journal ON public.journal_audit USING btree (id_journal);


--
-- Name: ix_medecin_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_medecin_email ON public.medecin USING btree (email);


--
-- Name: ix_medecin_id_medecin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_medecin_id_medecin ON public.medecin USING btree (id_medecin);


--
-- Name: ix_metastase_localisation_id_metastase; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_metastase_localisation_id_metastase ON public.metastase_localisation USING btree (id_metastase);


--
-- Name: ix_mutation_germinale_id_mutation; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_mutation_germinale_id_mutation ON public.mutation_germinale USING btree (id_mutation);


--
-- Name: ix_patient_id_patient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_patient_id_patient ON public.patient USING btree (id_patient);


--
-- Name: ix_protocole_traitement_id_protocole; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_protocole_traitement_id_protocole ON public.protocole_traitement USING btree (id_protocole);


--
-- Name: ix_traitement_id_traitement; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_traitement_id_traitement ON public.traitement USING btree (id_traitement);


--
-- Name: analyse_moleculaire analyse_moleculaire_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analyse_moleculaire
    ADD CONSTRAINT analyse_moleculaire_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: antecedent_familial antecedent_familial_id_dossier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.antecedent_familial
    ADD CONSTRAINT antecedent_familial_id_dossier_fkey FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE;


--
-- Name: biologie biologie_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.biologie
    ADD CONSTRAINT biologie_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: compte compte_active_par_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compte
    ADD CONSTRAINT compte_active_par_fkey FOREIGN KEY (active_par) REFERENCES public.compte(id_compte) ON DELETE SET NULL;


--
-- Name: compte compte_id_medecin_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compte
    ADD CONSTRAINT compte_id_medecin_fkey FOREIGN KEY (id_medecin) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL;


--
-- Name: decision decision_decide_par_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.decision
    ADD CONSTRAINT decision_decide_par_fkey FOREIGN KEY (decide_par) REFERENCES public.medecin(id_medecin);


--
-- Name: decision decision_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.decision
    ADD CONSTRAINT decision_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE RESTRICT;


--
-- Name: demande_reinitialisation demande_reinitialisation_id_compte_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.demande_reinitialisation
    ADD CONSTRAINT demande_reinitialisation_id_compte_fkey FOREIGN KEY (id_compte) REFERENCES public.compte(id_compte) ON DELETE CASCADE;


--
-- Name: demande_reinitialisation demande_reinitialisation_traite_par_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.demande_reinitialisation
    ADD CONSTRAINT demande_reinitialisation_traite_par_fkey FOREIGN KEY (traite_par) REFERENCES public.compte(id_compte) ON DELETE SET NULL;


--
-- Name: donnees_derivees donnees_derivees_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donnees_derivees
    ADD CONSTRAINT donnees_derivees_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: dossier_patient dossier_patient_id_medecin_referent_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dossier_patient
    ADD CONSTRAINT dossier_patient_id_medecin_referent_fkey FOREIGN KEY (id_medecin_referent) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL;


--
-- Name: dossier_patient dossier_patient_id_patient_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dossier_patient
    ADD CONSTRAINT dossier_patient_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES public.patient(id_patient) ON DELETE RESTRICT;


--
-- Name: evaluation_clinique evaluation_clinique_id_dossier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_clinique
    ADD CONSTRAINT evaluation_clinique_id_dossier_fkey FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE RESTRICT;


--
-- Name: evaluation_clinique evaluation_clinique_id_medecin_evaluateur_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_clinique
    ADD CONSTRAINT evaluation_clinique_id_medecin_evaluateur_fkey FOREIGN KEY (id_medecin_evaluateur) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL;


--
-- Name: evaluation_comorbidite evaluation_comorbidite_id_comorbidite_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_comorbidite
    ADD CONSTRAINT evaluation_comorbidite_id_comorbidite_fkey FOREIGN KEY (id_comorbidite) REFERENCES public.comorbidite(id_comorbidite);


--
-- Name: evaluation_comorbidite evaluation_comorbidite_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_comorbidite
    ADD CONSTRAINT evaluation_comorbidite_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: evaluation_parcours_therapeutique evaluation_parcours_therapeutique_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.evaluation_parcours_therapeutique
    ADD CONSTRAINT evaluation_parcours_therapeutique_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: histologie_biologie histologie_biologie_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.histologie_biologie
    ADD CONSTRAINT histologie_biologie_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: imagerie imagerie_id_evaluation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imagerie
    ADD CONSTRAINT imagerie_id_evaluation_fkey FOREIGN KEY (id_evaluation) REFERENCES public.evaluation_clinique(id_evaluation) ON DELETE CASCADE;


--
-- Name: journal_audit journal_audit_id_medecin_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journal_audit
    ADD CONSTRAINT journal_audit_id_medecin_fkey FOREIGN KEY (id_medecin) REFERENCES public.medecin(id_medecin) ON DELETE SET NULL;


--
-- Name: metastase_localisation metastase_localisation_id_imagerie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.metastase_localisation
    ADD CONSTRAINT metastase_localisation_id_imagerie_fkey FOREIGN KEY (id_imagerie) REFERENCES public.imagerie(id_imagerie) ON DELETE CASCADE;


--
-- Name: mutation_germinale mutation_germinale_id_dossier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mutation_germinale
    ADD CONSTRAINT mutation_germinale_id_dossier_fkey FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE;


--
-- Name: mutation_germinale mutation_germinale_id_gene_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mutation_germinale
    ADD CONSTRAINT mutation_germinale_id_gene_fkey FOREIGN KEY (id_gene) REFERENCES public.gene(id_gene);


--
-- Name: traitement traitement_id_dossier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traitement
    ADD CONSTRAINT traitement_id_dossier_fkey FOREIGN KEY (id_dossier) REFERENCES public.dossier_patient(id_dossier) ON DELETE CASCADE;


--
-- Name: traitement traitement_id_protocole_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traitement
    ADD CONSTRAINT traitement_id_protocole_fkey FOREIGN KEY (id_protocole) REFERENCES public.protocole_traitement(id_protocole);


--
-- PostgreSQL database dump complete
--


