-- ============================================================================
-- MIGRATION : identité déclarée sur `compte` (colonnes manquantes)
--
-- POURQUOI CE FICHIER EST NÉCESSAIRE
-- -------------------------------
-- `2026_10_05_auth_compte_admin.sql` a été exécuté dans sa version initiale,
-- avant l'ajout des colonnes d'identité. Il utilise `CREATE TABLE IF NOT
-- EXISTS` : le relancer ne fait donc RIEN, la table existe déjà et Postgres
-- ignore l'instruction. D'où ce fichier de correction, à exécuter une fois.
--
-- Les requêtes de l'API échouaient alors avec :
--   column compte.nom does not exist
--
-- L'API lit `compte.nom` / `compte.prenom` dès la page de connexion (elle
-- affiche qui a validé le compte), l'écran d'administration affiche l'identité
-- déclarée, et la validation recopie ces colonnes dans `medecin`.
--
-- Exécuter dans : Supabase Dashboard -> SQL Editor
-- Idempotent : peut être relancé sans effet de bord.
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Ajout des colonnes, nullable dans un premier temps
--
-- On ne pose pas NOT NULL ici : si des comptes existent déjà, la contrainte
-- échouerait sur les lignes existantes. Le NOT NULL est posé plus bas, une
-- fois le remplissage fait.
-- ---------------------------------------------------------------------------
ALTER TABLE public.compte ADD COLUMN IF NOT EXISTS nom       VARCHAR(100);
ALTER TABLE public.compte ADD COLUMN IF NOT EXISTS prenom    VARCHAR(100);
ALTER TABLE public.compte ADD COLUMN IF NOT EXISTS telephone VARCHAR(30);
ALTER TABLE public.compte ADD COLUMN IF NOT EXISTS hopital   VARCHAR(150);

-- ---------------------------------------------------------------------------
-- 2. Remplissage depuis le profil médecin rattaché
--
-- Défensif : si aucun compte n'existe encore, cette requête ne fait rien.
-- Sinon elle évite de laisser des identités vides, que l'admin ne pourrait
-- pas vérifier avant d'accorder un accès.
-- ---------------------------------------------------------------------------
UPDATE public.compte c
SET nom       = coalesce(c.nom,       m.nom),
    prenom    = coalesce(c.prenom,    m.prenom),
    telephone = coalesce(c.telephone, m.telephone),
    hopital   = coalesce(c.hopital,   m.hopital)
FROM public.medecin m
WHERE m.id_medecin = c.id_medecin
  AND (
       c.nom       IS NULL OR c.prenom IS NULL
    OR c.telephone IS NULL OR c.hopital IS NULL
  );

-- ---------------------------------------------------------------------------
-- 3. Lignes sans profil médecin
--
-- Elles correspondent à des comptes en attente : leur identité vient de
-- l'inscription et n'a pas encore été recopiée. Sans valeur de repli, le
-- NOT NULL ci-dessous échouerait et laisserait la migration enrolled.
-- Ces comptes sont inactifs de toute façon : le texte est un marqueur
-- visible qui rappelle qu'aucun profil ne leur est encore rattaché.
-- ---------------------------------------------------------------------------
UPDATE public.compte
SET nom    = coalesce(nom,    'À COMPLÉTER'),
    prenom = coalesce(prenom, 'À COMPLÉTER')
WHERE nom IS NULL OR prenom IS NULL;

-- ---------------------------------------------------------------------------
-- 4. Contraintes finales, en correspondance avec le modèle SQLAlchemy
-- ---------------------------------------------------------------------------
ALTER TABLE public.compte ALTER COLUMN nom     SET NOT NULL;
ALTER TABLE public.compte ALTER COLUMN prenom  SET NOT NULL;

-- Un compte d'administration est toujours actif : l'inverse le laisserait
-- sans aucun moyen de déverrouiller qui que ce soit. Postgres n'acceptant pas
-- `ADD CONSTRAINT IF NOT EXISTS`, on teste l'existence au préalable.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'ck_compte_role_admin'
    ) THEN
        ALTER TABLE public.compte
            ADD CONSTRAINT ck_compte_role_admin CHECK (
                role <> 'super_admin' OR statut = 'actif'
            );
    END IF;
END
$$;

COMMIT;

-- ---------------------------------------------------------------------------
-- Vérification (doit renvoyer 4) :
--   SELECT column_name FROM information_schema.columns
--   WHERE table_schema='public' AND table_name='compte'
--     AND column_name IN ('nom','prenom','telephone','hopital');
-- ---------------------------------------------------------------------------
