# Spark Swarm Recipe - aoa-memo

Рекомендуемый путь назначения: `.agents/spark/SWARM.md`

## Для чего этот рой
Используй Spark здесь для одного memory seam: memory object, registry, recall
contract, provenance thread, lifecycle audit example, mechanic seam, or
generated memory surface. Этот рой должен укреплять explicit and reviewable
memory, не давая памяти тихо подменить proof.

Ordinary Spark work starts from one scenario in `.agents/spark/registry.json`.
Use this file only when the user explicitly asks for a swarm.

## Читать перед стартом
- `README.md`
- `CHARTER.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `docs/MEMORY_MODEL.md`
- `docs/NARRATIVE_CORE_CONTRACT.md`
- `docs/BOUNDARIES.md`
- `ROADMAP.md`

## Форма роя
- **Coordinator**: выбирает один memory-layer surface
- **Scout**: картографирует object/registry/surfaces/examples and chooses one
  registered scenario
- **Builder**: делает минимальный diff
- **Verifier**: запускает named scenario validation, then broader gates only
  when requested
- **Boundary Keeper**: следит за provenance, salience boundaries и anti-proof-replacement

## Параллельные дорожки
- Lane A: memory object / registry / schema
- Lane B: generated memory surfaces
- Lane C: lifecycle / provenance-thread / audit examples
- Lane D: mechanic seam / recall contract / release-prep
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
Pick exactly one registered scenario from .agents/spark/registry.json and one
memory-layer surface:
- memory object or doctrine surface
- recall contract
- provenance thread
- lifecycle audit example
- generated memory surface
- mechanic seam
- concrete diff or release-prep pass

Return:
1. scenario id
2. chosen surface
3. exact files to touch
4. which validator(s) should catch regressions
5. whether this change affects router-facing surfaces
6. handoff condition
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
Run the Spark validation route from .agents/spark/AGENTS.md and report actual
results.
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
Executable validation lives in [AGENTS](AGENTS.md#validation), and scenario
shape is checked by:

```bash
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
```

## Done when
- один memory-layer surface strengthened
- provenance / audit / recall assumptions названы явно
- named validators реально прогнаны or skipped checks are explicitly reported
- память не подменила proof meaning

## Handoff
Если изменение на самом деле меняет source-owned truth, follow-up должен идти в `aoa-techniques`, `aoa-skills`, `aoa-evals` или `Tree-of-Sophia`, а не оставаться здесь.
