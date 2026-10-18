# Method and evidence

This project implements a synthetic legacy-modernisation experiment. The C program simulates a sensor configuration tool. It does not control physical hardware or represent a recovered industrial system.

## Specification and recovery

The implementation handoff defined the intended rules before the C oracle existed. The oracle then exercised those rules. `artifacts/recovery-probes.json` records 64 actual requests and observed responses from the compiled C program through its Python JSON boundary. These observations verify boundary behavior and support reconstruction exercises. They do not establish independent historical discovery of an unknown program. `spec/contract.json` records the selected contract; `spec/public-cases.json` contains nine observed examples supplied to the generators.

The Python boundary validates exact keys, native JSON types, canonical error ordering, and bounded numeric inputs. The C executable independently validates argv ranges and owns rounding, calibration, clamping, status priority, and warning ordering. Both components constitute the oracle for JSON requests. TypeScript implementations independently reproduce the boundary and calculations.

## Frozen first generation

`benchmark.experiment` supplied the same three files and identical prompt to both tools in separate temporary directories. The directories contained no reference implementation, heldout cases, or C source. The experiment imposed an instruction boundary. It did not provide a security sandbox or establish that the agents lacked access to other machine files. The tools used different runtime configurations. CLI logs record those differences.

Codex used `gpt-6.1-sol` with medium reasoning. Its original source remains unmodified. Claude Code requested `sonnet`, which resolved to `claude-sonnet-5-5` in the recorded runtime. Attempt 1 used bare mode and could not authenticate. Attempt 2 used normal authenticated configuration and received an API usage-limit error. The provider reported access would resume on 2026-11-01 at 00:00 UTC. No Claude implementation was produced. The report marks this outcome unavailable. The attempt-1 directory preserves its transcript and metadata. No heldout feedback was supplied to either generator.

The raw records include CLI framework details and commands. Source and input SHA-256 values make artifacts checkable. Cost remains null because this experiment did not establish comparable billing measurements. Elapsed generation time includes startup and remote service latency.

## Evaluation

The deterministic suite uses seed 241019 and 432 heldout requests:

| Category | Cases |
|---|---:|
| Root and keyset failures | 4 |
| Per-field type and range boundaries | 60 |
| Missing keys | 8 |
| Other invalid and multi-error ordering requests | 4 |
| Seeded random valid requests | 300 |
| Profile, alarm, clamp and disabled boundaries | 56 |

The harness compiles each artifact with TypeScript strict mode, executes a shared JSON adapter, and compares whole JSON responses against the oracle. A missing artifact has no behavioral result. Matching responses demonstrate parity on this finite suite. They do not prove equivalence on all inputs. The inputs are JSON; non-JSON JavaScript values such as undefined, NaN and cyclic objects fall outside the harness domain.

`python -m benchmark.mutation` injects five deliberate faults into the reference and checks whether the suite detects each fault. This measures sensitivity to these specific faults. It does not measure general mutation coverage. Strict compilation and source line counts provide descriptive quality proxies. No expert maintainability score or transferable task performance was measured. Pressure cases measure cross-profile parity because both profiles appear in the supplied specification.

## Independent manual baseline

No independently written human port or timed human trial was supplied. The deterministic reference is agent-authored. It cannot establish a human-effort advantage.

To add a manual participant, place their unmodified TypeScript implementation at `ports/manual/src/port.ts`. Export `evaluate(input: unknown)` with the same contract. Place participant-supplied metadata at `ports/manual/src/provenance.json`; include `authorship`, `elapsedSeconds`, `humanMinutes`, `costUsd`, and an explanation of assistance used. Use null for unavailable measurements. Record whether the participant saw heldout tests. Run `npm run benchmark` to add the manual result to the machine-readable report. Keep source and timing evidence in the repository or a linked immutable artifact. Self-reported timing does not become controlled study evidence automatically.

## Reproduction and retry

Run `make oracle`, `npm ci`, `make verify`, `npm run benchmark`, then `python -m benchmark.mutation`. No authenticated agent service is required for evaluation. Run `python -m benchmark.experiment` only to perform new paid/authenticated generation attempts. Preserve existing variants before a new attempt. A retry after publication is exposed to public heldout tests; label it as a new, potentially contaminated attempt. The included original artifacts remain the basis for the recorded results.
