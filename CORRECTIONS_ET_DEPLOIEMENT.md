# Corrections appliquées

## Corrections fonctionnelles

- Alignement du modèle SQLAlchemy `metastase_localisation.site` sur l’ENUM PostgreSQL `public.t_site_metastase`.
- Alignement de plusieurs autres colonnes ORM sur les ENUM PostgreSQL : sexe, statut du dossier, degré de parenté, statut mutation et réponse de traitement.
- Correction de la limite ECOG : `0..4`, conforme à la contrainte SQL.
- Persistance du parcours thérapeutique dans `evaluation_parcours_therapeutique`.
- Persistance des traitements saisis dans le wizard.
- Transmission des champs nécessaires aux règles R05, R09, R14, R15, R16, R17, T1 et T4.
- Prise en compte du signal « comorbidités lourdes » pour R03.
- Sélection réelle des sites de métastases dans l’étape Imagerie.
- Correction SSR de la page `reset-password` : `window` n’est plus lu pendant le rendu serveur.

## Migration Supabase à exécuter

Après déploiement du code, exécuter dans Supabase SQL Editor :

```sql
-- fichier backend/database/migrations/2026_09_07_parcours_comorbidites.sql
BEGIN;
ALTER TABLE public.evaluation_parcours_therapeutique
    ADD COLUMN IF NOT EXISTS comorbidites_lourdes BOOLEAN;
COMMIT;
```

Les migrations précédentes doivent être appliquées dans l’ordre si elles ne le sont pas encore :

1. `2026_08_29_medecin_hopital.sql`
2. `2026_09_02_decision_medecin.sql`
3. `2026_09_06_parcours_therapeutique_clinique.sql`
4. `2026_09_07_parcours_comorbidites.sql`

## Validation effectuée

- Backend : `104 passed` avec `pytest`.
- Backend : compilation Python réussie.
- Frontend : `npm run build` réussi.
- `npm run lint` conserve des erreurs déjà présentes dans le projet initial, principalement des règles ESLint sur `any`, les effets React et les apostrophes JSX. Ces erreurs ne bloquent pas le build Next.js.

## Important

Le code exige que les tables de référence des protocoles soient correctement alimentées si l’on souhaite rattacher les traitements à `id_protocole`. À défaut, le nom saisi est conservé dans `traitement.notes`, et le moteur peut l’utiliser comme solution de repli pour identifier le traitement précédent.
