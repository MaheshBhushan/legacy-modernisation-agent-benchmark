# Legacy modernisation benchmark execution plan

## Objective

Ship a reproducible C-to-TypeScript modernization benchmark with real Claude Code and Codex candidates, an Angular report and playground, and a public GitHub repository.

## Architecture decisions

- Simulate the legacy sensor tool in a deterministic C executable.
- Use a Python standard-library adapter for bounded JSON and subprocess execution.
- Freeze the exact eight-field `sensor-config-v1` contract before agent generation.
- Recover examples by querying the actual C oracle.
- Keep public examples separate from seeded heldout evaluations.
- Evaluate a pure TypeScript function through Node and import the same function into Angular.
- Label the deterministic reference as agent-authored.
- Leave unmeasured human effort and unavailable costs null.
- Record real CLI attempts, source hashes, timings, and exposure limitations.
- Use pressure-profile parity as a limited cross-profile measure.

## Work assignments

| Responsibility | Model | Deliverable |
| --- | --- | --- |
| Detailed implementation handoff | GPT-6 Astra | `docs/IMPLEMENTATION_HANDOFF.md` |
| Core implementation and UI | GPT-6.1 Sol, medium | Executable benchmark and Angular application |
| External candidate generation | Actual Claude Code and Codex CLIs | Candidate source and provenance manifests |
| Integration, verification, publication | Supervising implementation session | Measured report and public repository |

## Gates

1. Freeze contract, methodology, and provenance requirements.
2. Build and test the C executable with strict compiler checks.
3. Run oracle recovery and freeze public/heldout identities.
4. Compile and evaluate the TypeScript reference.
5. Verify evaluator behavior with an incorrect candidate.
6. Run both actual agent CLIs in fresh generation workdirs.
7. Evaluate generated candidates without heldout-driven source repairs.
8. Build and inspect the Angular report and playground.
9. Check artifact provenance, unknown metrics, and publication hygiene.
10. Push at least eight substantive commits to a public repository.

## Required evidence

- Compiler, Python, Node, npm, and agent CLI versions.
- Strict C compilation and sanitizer outcome.
- Recovery observations and oracle identity hashes.
- Frozen contract and public-example hashes.
- Heldout seed, corpus hash, count, and nonoverlap check.
- Generation prompts, attempt outcomes, timings, and candidate source hashes.
- Public and heldout parity with category and profile denominators.
- Quality signals with explicit collection methods.
- Unavailable human baseline and cost values preserved as null.
- Production Angular build and browser screenshots.
- Exported report JSON and reproducible command sequence.
- Verified public repository URL and pushed revision.

## Completion tracking

This file records the implementation plan.
The release report records executed checks and measured outcomes.
The implementation handoff supplies the detailed contract, failure semantics, UI requirements, and acceptance checklist.
