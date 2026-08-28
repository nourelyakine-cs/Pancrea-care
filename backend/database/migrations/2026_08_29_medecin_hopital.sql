-- ============================================================================
-- MIGRATION : medecin — ajout de hopital, suppression de specialite
-- Exécuter dans : Supabase Dashboard -> SQL Editor
-- (spécialité déjà existante perdue : à backup avant si besoin)
-- ============================================================================

BEGIN;

ALTER TABLE public.medecin
    ADD COLUMN IF NOT EXISTS hopital VARCHAR(150),
    DROP COLUMN IF EXISTS specialite;

COMMIT;