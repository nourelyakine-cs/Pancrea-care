-- ============================================================================
-- MIGRATION : élargissement de donnees_derivees.sous_categorie_abc
--
-- Le moteur de règles construit cette valeur sous la forme
--   f"{statut_resecabilite}_{type_abc}"
-- ce qui produit des chaînes telles que 'metastatique_ABC' (17 caractères),
-- plus longues que la définition d'origine VARCHAR(15), d'où l'erreur
-- « valeur trop longue pour le type character varying(15) ».
--
-- La colonne passe à VARCHAR(30) pour couvrir toutes les combinaisons
-- (ex. 'non_resecable_borderline_ABC').
--
-- Exécuter localement :
--   python -m app.utils.appliquer_migration database/migrations/<ce fichier>
-- ============================================================================

BEGIN;

ALTER TABLE public.donnees_derivees
    ALTER COLUMN sous_categorie_abc TYPE VARCHAR(30);

COMMIT;
