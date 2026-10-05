-- ============================================================================
-- MIGRATION : l'administrateur est aussi un praticien
--
-- Les comptes `super_admin` créés avant l'évolution n'avaient pas de profil
-- `medecin` : `get_medecin_for_user` les refusait donc sur toutes les routes
-- cliniques, et l'interface médecin leur était inaccessible.
--
-- Ce script rattache un profil à ces comptes. `bootstrap_admin` le fait
-- désormais pour les nouveaux ; celui-ci rattrape l'existant.
--
-- Exécuter dans : Supabase Dashboard -> SQL Editor
-- Idempotent.
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- Un profil par compte d administration qui n'en a pas encore
--
-- `medecin.email` porte la même adresse que le compte : c'est cette colonne
-- qui permet à `bootstrap_admin` de réutiliser le profil au lieu d'en créer
-- un second pour la même personne.
-- ---------------------------------------------------------------------------
INSERT INTO public.medecin (nom, prenom, email, telephone, hopital)
SELECT c.nom, c.prenom, c.email, '', 'PANCRA'
FROM public.compte c
WHERE c.role = 'super_admin'
  AND c.id_medecin IS NULL
  AND NOT EXISTS (
      SELECT 1 FROM public.medecin m WHERE lower(m.email) = lower(c.email)
  )
ON CONFLICT (email) DO NOTHING;

-- Rattachement des comptes au profil portant leur adresse. C'est cette étape
-- qui débloque réellement l'espace médecin : sans elle, le profil créé juste
-- au-dessus resterait orphelin.
UPDATE public.compte c
SET id_medecin = m.id_medecin
FROM public.medecin m
WHERE c.role = 'super_admin'
  AND c.id_medecin IS NULL
  AND lower(m.email) = lower(c.email);

COMMIT;

-- Vérification (doit renvoyer 0) :
--   SELECT count(*) FROM public.compte
--   WHERE role = 'super_admin' AND id_medecin IS NULL;
