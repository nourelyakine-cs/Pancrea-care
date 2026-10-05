-- ============================================================================
-- MIGRATION : index de cloisonnement par médecin référent
-- Exécuter dans : Supabase Dashboard -> SQL Editor
--
-- `GET /patients` filtre désormais sur dossier_patient.id_medecin_referent
-- (un médecin ne voit que ses patients). Sans index, chaque chargement de la
-- liste parcourt toute la table dossier_patient. Idem sur id_patient, utilisé
-- par la sous-requête « patients sans dossier » et par les contrôles d'accès.
-- ============================================================================

BEGIN;

CREATE INDEX IF NOT EXISTS idx_dossier_patient_medecin_referent
    ON public.dossier_patient (id_medecin_referent);

CREATE INDEX IF NOT EXISTS idx_dossier_patient_id_patient
    ON public.dossier_patient (id_patient);

COMMIT;