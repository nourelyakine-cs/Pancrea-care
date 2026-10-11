-- ============================================================================
-- MIGRATION : suppression des tables inutilisées
--
-- Aucune de ces tables n'est lue ni écrite par le code (modèles SQLAlchemy,
-- services, routes). Le moteur de règles vit entièrement en Python
-- (app/services/clinical_rules/recommendation_rules.py) et ne consulte pas la
-- base ; les tables `regle*` / `decision_*` associées sont donc mortes.
--
--   1. regle, regle_condition, regle_conclusion, regle_historique
--   2. decision_regle_declenchee, decision_explication
--   3. rcp, rcp_participant
--   4. protocole_contexte, source_referentiel (modèles présents mais jamais
--      interrogés ; `source_referentiel` n'existait que pour `regle`)
--
-- Ordre de suppression : les tables enfants avant leurs parents (aucune table
-- conservée ne référence ces tables).
--
-- Exécuter localement : psql -f ... ou
--   python -m app.utils.appliquer_migration database/migrations/<ce fichier>
-- ============================================================================

BEGIN;

DROP TABLE IF EXISTS public.decision_regle_declenchee;
DROP TABLE IF EXISTS public.decision_explication;

DROP TABLE IF EXISTS public.regle_condition;
DROP TABLE IF EXISTS public.regle_conclusion;
DROP TABLE IF EXISTS public.regle_historique;
DROP TABLE IF EXISTS public.regle;

DROP TABLE IF EXISTS public.rcp_participant;
DROP TABLE IF EXISTS public.rcp;

DROP TABLE IF EXISTS public.protocole_contexte;
DROP TABLE IF EXISTS public.source_referentiel;

-- Types énumérés devenus orphelins (utilisés uniquement par les tables
-- ci-dessus) : t_operateur et t_operateur_liaison (regle_condition),
-- t_grade_preuve (regle), t_type_conclusion (regle_conclusion).
DROP TYPE IF EXISTS public.t_operateur;
DROP TYPE IF EXISTS public.t_operateur_liaison;
DROP TYPE IF EXISTS public.t_grade_preuve;
DROP TYPE IF EXISTS public.t_type_conclusion;

COMMIT;
