-- ============================================================================
-- MIGRATION : decision — ajout de decision_medecin (décision finale du médecin)
-- Exécuter dans : Supabase Dashboard -> SQL Editor
-- ============================================================================

BEGIN;

ALTER TABLE public.decision
    ADD COLUMN IF NOT EXISTS decision_medecin TEXT;

COMMIT;
