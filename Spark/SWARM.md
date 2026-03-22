# Spark Swarm Recipe — aoa-memo

Рекомендуемый путь назначения: `Spark/SWARM.md`

## Для чего этот рой
Используй Spark здесь для одного memory seam: memory object, registry, recall contract, provenance thread, lifecycle audit example или generated memory surfaces. Этот рой должен укреплять explicit and reviewable memory, не давая памяти тихо подменить proof.

## Читать перед стартом
- `README.md`
- `CHARTER.md`
- `docs/MEMORY_MODEL.md`
- `docs/NARRATIVE_CORE_CONTRACT.md`
- `docs/BOUNDARIES.md`
- `ROADMAP.md`

## Форма роя
- **Coordinator**: выбирает один memory-layer surface
- **Scout**: картографирует object/registry/surfaces/examples
- **Builder**: делает минимальный diff
- **Verifier**: запускает три memory validators
- **Boundary Keeper**: следит за provenance, salience boundaries и anti-proof-replacement

## Параллельные дорожки
- Lane A: memory object / registry / schema
- Lane B: generated memory surfaces
- Lane C: lifecycle / provenance-thread / audit examples
- Не запускай больше одного пишущего агента на одну и ту же семью файлов.

## Allowed
- чинить memory object or registry contract
- усиливать recall or provenance surfaces
- чинить lifecycle audit examples
- прояснять authored/core vs derived memory boundaries

## Forbidden
- превращать memory в proof or execution meaning
- тащить сюда techniques/skills/evals as primary meaning
- размывать provenance или temporal relevance
- вводить generic notes without memory contract

## Launch packet для координатора
```text
We are working in aoa-memo with a one-repo one-swarm setup.
Pick exactly one memory-layer surface:
- memory object
- registry
- recall contract
- provenance thread
- lifecycle audit example
- generated memory surface

Return:
1. chosen surface
2. exact files to touch
3. which validator(s) should catch regressions
4. whether this change affects router-facing surfaces
```

## Промпт для Scout
```text
Map only. Do not edit.
Return:
- exact files involved
- generated surfaces likely affected
- provenance or audit assumptions
- whether this risks replacing proof with memory
- whether the change belongs here or in a neighboring source-owned layer
```

## Промпт для Builder
```text
Make the smallest reviewable change.
Rules:
- keep memory explicit and reviewable
- preserve provenance
- keep temporal/salience assumptions bounded
- do not let memory silently replace proof
```

## Промпт для Verifier
```text
Run all three memory validators and report actual results:
- python scripts/validate_memo.py
- python scripts/validate_memory_surfaces.py
- python scripts/validate_lifecycle_audit_examples.py
```

## Промпт для Boundary Keeper
```text
Review only for anti-scope.
Check:
- memory did not become proof
- provenance is still visible
- salience and recall temperature stayed bounded
- no neighboring layer meaning got absorbed
```

## Verify
```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

## Done when
- один memory-layer surface strengthened
- provenance / audit / recall assumptions названы явно
- все три validators реально прогнаны
- память не подменила proof meaning

## Handoff
Если изменение на самом деле меняет source-owned truth, follow-up должен идти в `aoa-techniques`, `aoa-skills`, `aoa-evals` или `Tree-of-Sophia`, а не оставаться здесь.
