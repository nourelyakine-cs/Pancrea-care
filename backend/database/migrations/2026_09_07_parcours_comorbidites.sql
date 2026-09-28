BEGIN;
ALTER TABLE public.evaluation_parcours_therapeutique
    ADD COLUMN IF NOT EXISTS comorbidites_lourdes BOOLEAN;
COMMIT;