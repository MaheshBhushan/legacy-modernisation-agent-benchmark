# Legacy modernisation agent benchmark: implementation handoff

Document status: implementation specification, version 1.
Contract identifier: `sensor-config-v1`.
Design date: 2026-10-18.
Design model: GPT-6 Astra.
Implementation model assignment: GPT-6.1 Sol, medium reasoning.

## 1. Product and research objective

Build a runnable benchmark that ports a small simulated legacy C sensor-configuration tool to TypeScript.
Expose the resulting implementation through a real Angular application.
Recover observable behavior through executable oracle queries.
Generate independent implementations through actual Claude Code and Codex command-line sessions.
Compare those implementations with a separately authored deterministic reference port.
Measure parity, available quality signals, test sensitivity, observed effort, and cross-profile behavior.
Preserve enough provenance for another developer to rerun the experiment.

The project implements a hypothetical project proposal as a new demonstrator.
The starting material supplies an idea and technology choices.
The project does not claim access to an existing industrial legacy codebase.
The C fixture simulates legacy behavior for controlled experimentation.
The fixture does not control physical sensors.
The benchmark results apply to the fixture and evaluated cases.

The reference port has the label **agent-authored reference**.
Its implementation must never receive the label “manual baseline.”
A human baseline remains unavailable until a human participant performs a separately recorded task.
Human development time, cost, and productivity comparisons remain `null` until measured.
The final report must preserve these distinctions beside its headline metrics.

The project demonstrates these concrete activities:

- Reverse engineering through controlled black-box oracle queries.
- A specification-driven development workflow through frozen machine-readable artifacts.
- Porting through independent TypeScript implementations of the same contract.
- Proof of concept delivery through a working Angular sensor playground.
- Experimental comparison through repeatable scripts and recorded source identities.

## 2. Completion criteria

The repository is complete when all required checks below pass or record an explicit unavailable state.

1. A strict C build produces a deterministic executable.
2. The C executable computes the specified sensor behavior.
3. A Python adapter accepts bounded JSON inputs and invokes that executable safely.
4. An extraction command queries the oracle and writes executable examples with provenance.
5. A frozen public specification describes the input and output boundary.
6. An independently generated heldout corpus exercises broader combinations.
7. The reference TypeScript implementation passes the parity evaluation.
8. Claude Code and Codex generation runners invoke the installed CLIs.
9. Each generation attempt records its outcome, including authentication or execution failures.
10. Each successfully produced candidate is compiled and evaluated as its own variant.
11. Generated sources remain separate from the reference source.
12. An Angular application loads measured report data and runs a sensor playground.
13. The UI exports the displayed benchmark report as JSON.
14. The report distinguishes measured, unavailable, and inapplicable metrics.
15. Tests verify the evaluator itself with deliberately incorrect variants or mutations.
16. A fresh checkout can run the documented installation and verification commands.
17. A public GitHub repository contains meaningful implementation history.
18. The release includes at least eight substantive commits with coherent changes.

An unavailable external agent does not justify a fabricated candidate.
A failed external run remains a failed run in the evidence.
The delivery can contain a usable reference demonstration and an explicitly incomplete comparison.
The delivery summary must name every missing required comparison.
Authentication success does not guarantee available provider usage.
A provider quota or usage-limit rejection produces an unavailable candidate with a recorded reason.
The generation runner remains available for a later authenticated rerun.
The report must never substitute the reference implementation for that missing candidate.

## 3. Deliberate scope boundaries

Use a Python standard-library core for orchestration and measurement.
Use the system C compiler for the simulated legacy tool.
Use Angular and TypeScript for the web experience.
Use a committed npm lockfile for reproducible frontend dependencies.
Use static report files instead of an application server.
Use subprocess execution instead of a plugin registry.
Use a small fixed contract instead of a general schema framework.
Use a few transparent metrics instead of an invented aggregate quality score.

The first version does not require accounts, a database, scheduling, hardware, or cloud deployment.
The first version does not install an agent framework.
The first version does not infer developer productivity from source length.
The first version does not rank models across programming tasks in general.
The first version does not claim statistical significance from one generation attempt.
The first version does not execute uploaded browser code.

## 4. Architecture and ownership boundaries

The C process owns successful sensor calculations.
The Python JSON adapter owns transport validation and process execution.
The frozen specification owns the public boundary contract.
The TypeScript port owns the equivalent browser and Node behavior.
The evaluation harness owns case execution, comparison, and measurements.
The generation runner owns CLI invocation and generation provenance.
The Angular application owns presentation and interactive exploration.

```text
                       C source
                          |
                     strict compiler
                          |
                       C oracle
                          |
                bounded Python adapter
                    /             \
          public recovery       heldout evaluation
                |                     |
       frozen spec + examples         |
            /          \              |
    Claude Code       Codex           |
            \          /              |
          candidate TypeScript -------+
                     |
            generated report JSON
                     |
             Angular report UI

    agent-authored reference TypeScript
                 /            \
       same evaluator       Angular playground
```

Use direct function imports for the browser playground.
Use a Node JSON runner for command-line comparisons.
Both paths must call the same TypeScript function for a selected implementation.
The browser must never reimplement sensor arithmetic in a component.

Recommended repository layout:

```text
legacy-modernisation-agent-benchmark/
  README.md
  LICENSE
  package.json
  package-lock.json
  pyproject.toml
  legacy/
    sensor_config.c
  benchmark/
    __init__.py
    cli.py
    protocol.py
    cases.py
    runner.py
    report.py
  spec/
    contract.json
    public-cases.json
    recovered-spec.json
  ports/
    reference/
      port.ts
  variants/
    claude-code/
    codex/
  web/
    src/
    public/
  tests/
  docs/
    IMPLEMENTATION_HANDOFF.md
    METHODOLOGY.md
  reports/
    latest.json
  .scratch/
    legacy-benchmark/
      plan.md
```

The builder may consolidate Python modules or select conventional Angular paths.
Consolidation must preserve the architecture boundaries and executable entrypoints.
The README must document the actual paths.
Build directories, npm dependencies, authentication files, and raw private CLI transcripts stay ignored.

## 5. Frozen input contract

The request contains exactly eight fields.
Every field is required.
No field has a default.
Unknown fields make the entire request invalid.
The root must be a JSON object.
Arrays, strings, booleans, numbers, and `null` are invalid roots.

| Field | JSON type | Accepted values |
| --- | --- | --- |
| `profile` | string | `temperature` or `pressure` |
| `sampleMs` | number | integer from 10 through 60000 |
| `gain` | number | integer from 1 through 16 |
| `offsetMilli` | number | integer from -100000 through 100000 |
| `rawMilli` | number | integer from -1000000 through 1000000 |
| `alarmLowMilli` | number | integer from -20000000 through 20000000 |
| `alarmHighMilli` | number | integer from -20000000 through 20000000 |
| `enabled` | boolean | `true` or `false` |

The alarm interval also requires `alarmLowMilli < alarmHighMilli`.
Equality between alarm thresholds is invalid.
Alarm thresholds may lie outside the profile's physical reading range.
The tool must preserve those thresholds through evaluation semantics.

Use mathematical integer semantics for JSON numeric values.
A finite value such as `10.0` represents the integer 10.
A fractional value such as `10.5` is invalid for an integer field.
JavaScript must require `Number.isSafeInteger` before range validation.
Python must reject booleans before numeric validation.
Python must accept integral finite floating-point values if JSON decoding produces them.
Python's unbounded integer type must not broaden the accepted contract.
The accepted field ranges already fit JavaScript safe integers.
NaN and infinities are invalid JSON transport values.
Python's decoder must reject its permissive non-finite extensions.

Use this valid baseline input throughout examples:

```json
{
  "profile": "temperature",
  "sampleMs": 100,
  "gain": 1,
  "offsetMilli": 0,
  "rawMilli": 25000,
  "alarmLowMilli": 0,
  "alarmHighMilli": 100000,
  "enabled": true
}
```

## 6. Validation and error precedence

Validation precedence forms part of behavioral parity.
Perform the root-object and exact-keyset checks first.
An invalid root, a missing key, or an unknown key produces field `$`.
Then visit required fields in the table order from section 5.
At each field, validate type and its own value constraints.
Return immediately after the first failure.
After all fields validate, check the alarm interval relationship.
A failed relationship produces field `alarmHighMilli`.

The error response has exactly this shape:

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_REQUEST",
    "field": "sampleMs"
  }
}
```

Do not add a human-readable error message to the parity payload.
The UI can map a code and field to helpful presentation text.
The evaluator compares stable machine-readable output.

The Python adapter must not validate every type before validating any range.
That phase split would change the first error when two fields fail differently.
For example, an out-of-range `sampleMs` precedes a string-valued `gain`.
The expected error field for that example is `sampleMs`.
The Python boundary may duplicate these small input checks to preserve precedence.
The C executable must independently reject malformed argv inputs.

Malformed JSON, excessive input, process crashes, and timeouts belong to the transport result.
They must not become ordinary sensor responses.
The evaluator records those failures with an infrastructure or protocol classification.
Candidate failures still count as failed cases in the appropriate parity denominator.

## 7. Successful sensor behavior

Calculate the effective sample interval with integer arithmetic:

```text
effectiveSampleMs = ((sampleMs + 9) // 10) * 10
```

The sample interval rounds upward to the nearest multiple of 10 milliseconds.
An already aligned interval remains unchanged.
The upper bound of 60000 remains valid after rounding.

Calculate the unbounded calibrated reading:

```text
calibratedMilli = rawMilli * gain + offsetMilli
```

Select the profile bounds:

| Profile | Minimum reading | Maximum reading |
| --- | ---: | ---: |
| `temperature` | -40000 | 125000 |
| `pressure` | 0 | 1000000 |

Clamp the calibrated reading to the selected interval:

```text
readingMilli = min(max(calibratedMilli, minimum), maximum)
```

All validated intermediate values fit signed 32-bit arithmetic.
Use `int64_t` in C to make the intended overflow protection explicit.
The maximum absolute calibrated magnitude is 16100000.
The same arithmetic remains exact in JavaScript numbers.
The contract does not require floating-point calibration.

Select status in this order:

1. `disabled` when `enabled` is false.
2. `low` when `readingMilli < alarmLowMilli`.
3. `high` when `readingMilli > alarmHighMilli`.
4. `ok` for every remaining valid configuration.

Equality with either alarm boundary produces `ok`.
Compare alarm thresholds with the clamped reading.
Disabling the sensor changes status but retains calculations and warnings.

Populate warnings in the following fixed order:

1. Append `sample-rounded` when the effective interval differs from the input.
2. Append `reading-clamped` when the final reading differs from calibration.

The warnings array exists even when it is empty.
The success response contains exactly these fields:

```json
{
  "ok": true,
  "profile": "temperature",
  "effectiveSampleMs": 100,
  "readingMilli": 25000,
  "status": "ok",
  "warnings": []
}
```

Object key ordering does not affect parity.
Array ordering does affect parity.
Extra output fields fail exact contract comparison.
Numeric output values must remain integers.

## 8. C executable boundary

Keep the C tool focused on the simulated legacy behavior.
Pass eight positional arguments in the same order as the request fields.
Encode `enabled` as the ASCII token `0` or `1`.
Encode numeric fields as normalized base-10 integer strings.
Pass the profile token without shell interpolation.

Example invocation:

```sh
./build/sensor-config temperature 100 1 0 25000 0 100000 1
```

Write exactly one JSON response to stdout.
Write optional diagnostics to stderr.
End the response with a newline.
Use a zero exit status for a completed domain evaluation, including invalid requests.
Use a nonzero exit status for an internal execution failure.
Document any chosen difference in the actual CLI README.

Require the exact argument count.
Parse numeric tokens with `strtoll` and complete end-pointer checking.
Reset and inspect `errno` for range errors.
Reject trailing characters, empty values, and unsupported boolean tokens.
Reject invalid profile values before profile-dependent calculations.
Avoid unbounded copying and dynamically constructed JSON strings.
The fixed output vocabulary permits direct formatted output.

Build the release executable with a strict C standard and warnings:

```sh
cc -std=c11 -O2 -Wall -Wextra -Werror -Wpedantic \
  legacy/sensor_config.c -o build/sensor-config
```

Build a separate sanitizer executable when the host supports the flags:

```sh
cc -std=c11 -O1 -g -Wall -Wextra -Werror -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  legacy/sensor_config.c -o build/sensor-config-sanitized
```

Run successful and invalid-input boundaries against the sanitizer executable.
Treat sanitizer diagnostics as failed verification.
Record unsupported sanitizer execution as unavailable with its reason.
Do not describe an unavailable sanitizer check as a pass.

## 9. Bounded Python and Node transport

Use a JSON Lines wrapper around a pure evaluator where batch execution reduces overhead.
Each request and response occupies one line.
Reject input lines above a documented byte ceiling, such as 64 KiB.
Set a total request count ceiling for each subprocess batch.
Require exactly one response per submitted request.
Treat missing, extra, and malformed responses as protocol failures.

The initial implementation may use one process per case.
That choice simplifies cleanup and avoids cross-case state.
Report end-to-end timing as process-inclusive when using that design.
Do not call process-inclusive duration a pure function benchmark.

Invoke subprocesses with argument arrays and `shell=False`.
Set an explicit working directory.
Use a minimal environment for candidate evaluation.
Do not pass agent credentials into candidate processes.
Apply a deadline to each run.
Limit captured output before it can exhaust memory or disk.
Terminate process descendants when a deadline or output limit triggers.
Reap the process and close descriptors on every error path.

`subprocess.run(..., capture_output=True)` buffers captured output in memory.
Use it only where an independently enforced bound guarantees small output.
For untrusted candidates, use bounded pipe reads or a size-limited capture strategy.
Check limits while the process runs.
Checking file size only after process completion does not enforce a limit.
Python documents subprocess buffering and timeout behavior in its [subprocess reference](https://docs.python.org/3/library/subprocess.html).

Separate these concepts in the result model:

- A valid domain response.
- A domain response that differs from the oracle.
- Invalid candidate JSON or a contract-invalid response.
- An exceeded time or output limit.
- A failed executable launch or compile step.
- An unexpected C oracle failure.

An oracle failure invalidates affected comparisons.
The report must not count an oracle failure as a candidate success.

## 10. Executable specification recovery

Recovery must execute the compiled C fixture through the adapter.
The extracted artifact must contain actual observed outputs.
Do not substitute a hand-written expected-output table for oracle queries.
Keep the query recipe deterministic and versioned.
Record the C source hash and the executable hash.
Record the adapter source hash because the adapter defines JSON-boundary semantics.
Record the contract hash, compiler identity, extraction time, and case count.

The recovery script should query these behavioral families:

| Family | Required observations |
| --- | --- |
| Nominal behavior | Baseline request for each profile |
| Interval rounding | Aligned interval and both sides of a rounding boundary |
| Calibration | Positive gain, negative offset, and combined arithmetic |
| Temperature clamp | Below, on, and above each clamp boundary |
| Pressure clamp | Below, on, and above each clamp boundary |
| Alarm inclusion | Reading immediately below, equal to, and above each threshold |
| Disabled behavior | A disabled request that still rounds and clamps |
| Numeric validation | Lower minus one, lower, upper, upper plus one |
| Shape validation | Missing key, extra key, and invalid root |
| Type validation | String number, boolean number, fractional number, null |
| Error precedence | Two invalid fields with different failure kinds |

The recovered specification consists of rules plus their supporting observations.
Rules may be proposed from the experiment design.
Each reported observation must identify the query and actual oracle response.
Finite observations support the rule set but do not prove behavior over every possible input.
The document should state that limitation without weakening reproducibility.

Use stable case identifiers such as `interval.round-up.101`.
Store case category, request, observed response, and evidence metadata.
Preserve the raw request values that test JSON types.
Do not normalize away the difference between `true` and `1` before validation.

## 11. Public examples and heldout cases

Freeze the public contract and public cases before generation starts.
Write a SHA-256 manifest for both files.
Use the same frozen inputs for every candidate in a comparison group.
Give the agents the public contract and public cases.
Keep heldout expected results outside their working directories.

Generate the heldout corpus from a fixed, recorded seed.
Store the seed or a reproducible seed commitment in the run manifest.
Deduplicate heldout requests by canonical JSON encoding.
Assert that public and heldout request sets do not overlap.
Store the resulting case count and corpus hash.
Record random generator identity if reproduction depends on a library implementation.

Combine deliberate edge cases with seeded combinations.
Random cases alone rarely exercise exact threshold inclusion.
Include every validation family and both profiles.
Include multiple-invalid-field requests to test precedence.
Include integer-valued decimal tokens where the transport permits them.
Include large safe integers that fail range checks.
Include unsafe numeric values that fail integer validation.

A public repository cannot guarantee perpetual secrecy of heldout tests.
The initial run can withhold its corpus from the generation workspace.
Published reports may reveal failure cases and expected behavior.
Later runs against published artifacts have possible exposure.
Label those runs as exposed or generate a fresh heldout corpus.
Do not claim a security sandbox from a working-directory boundary alone.
If agents can access the broader filesystem, record that limitation.

A useful initial corpus contains tens of public observations and hundreds of heldout requests.
The exact counts must come from generated artifacts.
Never write a fixed count into the UI before the harness has produced that count.

## 12. Reference TypeScript implementation

Implement a single exported function:

```ts
export function evaluate(input: unknown): SensorResponse;
```

Use discriminated response types for `ok: true` and `ok: false`.
Validate `unknown` before accessing fields.
Use a fixed canonical field order.
Use `Object.keys` or an equivalent exact-key check.
Keep validation and calculation readable.
Avoid dependencies inside the port.
Avoid filesystem, process, and browser globals inside the function.
Avoid mutable module state.

The Node runner handles JSON parsing and serialization.
The Angular application handles forms and presentation.
The function performs domain evaluation only.
This separation makes the same port usable in both environments.

The reference must be independently authored from the frozen contract.
Record its authoring method as agent-authored.
Record its source hash during evaluation.
Do not use the reference output as the expected result when the C oracle is available.
The C fixture remains the independent behavior source.

## 13. External generation protocol

Provide a first-class command that generates a named candidate.
The command must support Claude Code and Codex through actual installed binaries.
Check the installed CLI version and relevant help before assembling flags.
Perform a narrow authentication preflight without printing credentials.
Record authentication availability as a boolean or status string.
Keep secret values out of logs and argv.

Create a fresh working directory for each attempt.
Copy only the frozen contract, public examples, a minimal build scaffold, and the task prompt.
Exclude C source, reference source, heldout corpus, reports, and other candidates.
Do not allow a candidate to overwrite benchmark infrastructure.
Preserve the initial scaffold hash.
Use the same scaffold for both agent families.

The generation task asks for a pure TypeScript `evaluate` function.
The task specifies the file path and export name.
The task permits public-case tests.
The task requires no network dependencies in the port.
The task asks the agent to preserve the response contract exactly.
The task states a fixed execution budget.

Use one initial attempt per agent for the first comparable run.
If repair attempts become necessary, record them separately.
Show initial-attempt and repaired-attempt results distinctly.
Do not silently replace a failed attempt with an improved implementation.
Do not feed heldout failures back to a candidate and call the result heldout performance.

Claude Code supports noninteractive print execution and structured output through its documented CLI.
Check exact installed flags against the [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference).
Codex supports noninteractive execution through its documented command-line workflow.
Check installed behavior against the [Codex noninteractive-mode documentation](https://learn.chatgpt.com/docs/non-interactive-mode).
Persist the actual selected model when the CLI reports one.
Record `null` when the model identity cannot be recovered reliably.

Do not mark a source file “Claude-generated” because a supervising agent wrote it.
Do not mark a source file “Codex-generated” without a matching completed CLI attempt.
Preserve original candidate source hashes before compilation or repairs.
If an evaluator modifies source for compatibility, record the patch and a new identity.

## 14. Generation manifest

Each attempt needs a machine-readable manifest with these fields or documented equivalents:

```json
{
  "schemaVersion": 1,
  "runId": "unique-attempt-id",
  "variant": "claude-code",
  "status": "completed",
  "cliVersion": "observed-version",
  "model": null,
  "startedAt": "ISO-8601 timestamp",
  "finishedAt": "ISO-8601 timestamp",
  "wallSeconds": 0,
  "exitCode": 0,
  "attempt": 1,
  "promptSha256": "sha256",
  "contractSha256": "sha256",
  "publicCasesSha256": "sha256",
  "scaffoldSha256": "sha256",
  "outputSourceSha256": "sha256",
  "heldoutVisible": false,
  "filesystemIsolation": "working-directory-only",
  "inputTokens": null,
  "outputTokens": null,
  "costUsd": null,
  "humanActiveSeconds": null
}
```

The numeric zero values above illustrate types.
The implementation must replace them with measurements.
Unknown values must be `null`.
The status field must distinguish skipped, running, completed, failed, and timed out states.
Incomplete attempts cannot acquire a completed status from a source-file existence check alone.

Keep raw logs local when they may contain private environment information.
Publish a sanitized summary and the generated source.
Sanitize by an explicit policy and manual review before publication.
Do not publish authentication output, private file paths, tokens, or account identifiers.
Hash public artifacts from their exact bytes.
Hash canonical JSON only where the manifest explicitly specifies canonicalization.

## 15. Behavioral parity evaluation

Run each frozen case through the C oracle and each compiled candidate.
Parse responses as JSON.
Validate the response shape before equality comparison.
Compare objects without depending on property order.
Compare arrays with order preserved.
Require exact integer and string values.
Reject booleans in numeric response fields.

Calculate parity as:

```text
passed_cases / evaluated_cases
```

Report numerator and denominator beside the percentage.
Keep public and heldout results separate.
Keep category slices and profile slices available.
Count candidate timeouts and malformed output as failures.
Report oracle failures separately and exclude invalid comparisons from completed totals.
If the oracle fails, mark the overall run incomplete.

For each failed case retain:

- Stable case identifier and category.
- Input request.
- Expected C response.
- Actual response or bounded failure diagnostic.
- Candidate source hash.
- Failure classification.

Cap displayed failure samples while retaining total failure counts.
Do not hide a failed variant from comparison tables.
Do not sort an unavailable variant as if it scored zero.
Use an explicit unavailable state in that row.

## 16. Quality and testability metrics

Prefer directly measured signals with plain definitions.
Every metric needs its denominator, scope, and collection method where applicable.

| Metric | Measurement | Interpretation limit |
| --- | --- | --- |
| Strict TypeScript compile | Actual compiler exit status | Compilation does not establish behavioral correctness |
| Source lines | Nonempty lines in the port source | Shorter code is not automatically better |
| Dependency count | Runtime imports outside the candidate | Import counting does not measure supply-chain risk |
| Public test pass rate | Passed public cases divided by cases | Public cases were available during generation |
| Heldout parity | Exact C matches divided by evaluated cases | Finite corpus only |
| Mutation sensitivity | Detected applicable mutations divided by tested mutations | Synthetic mutations approximate selected failure modes |
| Browser integration | Production Angular build and smoke test | A build alone does not establish usability |

Do not label regex-based branch counts “cyclomatic complexity.”
If no trustworthy complexity tool is present, omit complexity or report `null`.
Do not invent lint scores from warning counts.
Do not claim code coverage without instrumented execution.
Do not present a weighted score without a preregistered justification.
Separate implementation quality observations from automated measurements.

Use a small mutation set to test the suite's sensitivity:

1. Replace upward interval rounding with downward rounding.
2. Change inclusive alarm boundaries to exclusive boundaries.
3. Remove reading clamping.
4. Ignore the disabled flag.
5. Reverse warning order.

Apply mutations to a known correct fixture or a dedicated evaluator stub.
Use deterministic transformations with exact match assertions.
Record a mutation as inapplicable if its target cannot be matched.
Never count an inapplicable mutation as detected.
A detected mutation must cause at least one meaningful case failure.
The mutation run validates test sensitivity, not agent authorship quality.

## 17. Effort and timing metrics

Measure generation wall time with a monotonic clock.
Record total attempts and repair attempts.
Record actual CLI token and cost fields only when supplied reliably.
Record build duration separately from generation duration.
Record evaluation duration separately from both.
Keep environment versions beside timing measurements.

Human active effort remains `null` without an instrumented human session.
Agent wall time does not equal human work saved.
API cost does not equal overall engineering cost.
Reference authoring time is unavailable unless the implementation session measured it.
Do not reconstruct effort from commit timestamps.

### Human baseline registration and later import

Include a dedicated human-baseline entry with status `not-run` in the initial report.
Give that entry an explicit reason such as `No independent human implementation was measured`.
Keep parity, source identity, active effort, and cost null for that entry.
The agent-authored reference remains a separate entry.
An absent human baseline does not prevent evaluation of available agent candidates.
The report must state that the original manual-comparison objective remains incomplete.

Support a later human baseline through the same candidate interface.
The import workflow accepts a source file and a participant-provided provenance manifest.
Copy the source into a new variant directory before compilation.
Compute its SHA-256 from the imported bytes.
Record the supplied authoring declaration without presenting it as independently verified identity.
Record the public contract and example hashes that the participant received.
Record whether the participant saw prior reports, heldout cases, or other ports.
Record active minutes only when the participant measured them.
Preserve null values for unavailable effort information.

The human author should receive the same frozen task bundle and implementation interface.
If the participant saw the published heldout corpus, use a fresh corpus for a new comparison.
Evaluate the imported implementation through the same runner and metrics.
Include failed compilation or incomplete responses in its result.
An import changes status from `not-run` only after the runner records the actual attempt.
The initial repository may document this workflow through its general variant runner.
It does not need a dedicated identity system or participant portal.

If candidate latency is reported, define the measurement boundary.
A fresh Node process per request measures launch plus evaluation plus serialization.
A batched Node runner measures a different workload.
Compare variants under the same runner mode.
Repeat measurements only when performance conclusions require them.
Keep a one-run duration labeled as an observation.

## 18. Transferability experiment

Use `temperature` as the primary profile and `pressure` as the second profile.
Report parity for each profile independently.
The pressure slice tests reuse across a related sensor configuration.
The pressure slice does not establish generalization to an unseen specification when the public contract includes pressure.
Label that result **cross-profile parity**.

A stronger transfer experiment requires a separate second-stage task.
Freeze a new profile rule after the first generation attempt.
Give every agent the same additional specification and repair budget.
Record changed source, wall time, tests, and a fresh heldout corpus.
Keep that experiment separate from v1 parity.
Implement this extension only after the required end-to-end benchmark works.

A fresh contract version is required for a third profile or new conversion semantics.
Do not reuse `sensor-config-v1` for changed behavior.
Do not update frozen examples in place after candidate generation.

## 19. Report artifact

Use a versioned JSON report as the single data source for the web report.
Include a generated timestamp and run identifier.
Include contract, oracle, corpus, and candidate hashes.
Include environment versions and collection commands.
Include public and heldout parity summaries.
Include category and profile breakdowns.
Include measured quality and effort metrics.
Include explicit unavailable fields and reasons.
Include bounded failure examples.
Include methodological limitations as readable strings.

Use exact labels:

- `Agent-authored reference` for the deterministic reference implementation.
- `Claude Code` for a candidate produced by a verified Claude Code run.
- `Codex` for a candidate produced by a verified Codex run.
- `Human baseline unavailable` until an actual human baseline exists.

Render the human baseline as an explicit not-run row.
Render an unavailable external agent as an explicit row with its attempt outcome.
Keep missing-comparison rows visible in exported JSON as well as the browser table.

Do not display a placeholder report as a measured run.
A bundled development fixture must display a visible fixture label.
The release should bundle a real measured report whenever evaluation succeeds.
Generate Markdown or HTML summaries from the same JSON when useful.
Avoid maintaining multiple manually edited result tables.

## 20. Angular experience

Build a real Angular application with a production build command.
Use the installed Node version and a compatible Angular/TypeScript combination.
Angular 22.0.x currently documents Node 26 support and TypeScript 6.0 compatibility.
Verify package availability before pinning versions.
Use the official [Angular version compatibility table](https://angular.dev/reference/versions).
Commit resolved exact versions through `package-lock.json`.

The page should explain the benchmark immediately.
Use a concise title, an experiment-status badge, and a short objective statement.
Show the report run date and source identities through a compact details region.
Present measured parity before secondary code statistics.
Keep provenance and limitations accessible without obscuring the main comparison.

Recommended page sections:

1. Benchmark overview and completion state.
2. Variant comparison with public and heldout results.
3. Behavior categories and cross-profile parity.
4. Sensor configuration playground.
5. Executable specification examples and failed cases.
6. Methodology, provenance, and JSON export.

The comparison table should include every attempted variant.
Use text labels beside color-coded statuses.
Show unavailable values as an em dash with a reason.
Show parity as passed/total and percentage.
Keep human-baseline availability visible.

The playground needs all eight inputs with explicit units.
Use a select for profile.
Use numeric inputs for the six integer fields.
Use a checkbox or accessible switch for enabled.
Display the effective interval, reading, status, and ordered warnings.
Show validation errors near the relevant input.
Keep a raw JSON view available for reproducibility.
Provide presets for nominal, rounded, clamped, alarm-boundary, and disabled behavior.

Label which implementation powers the playground.
If variant selection is offered, call the corresponding compiled port directly.
Do not imply that changing the form executes C in the browser.
The C comparison belongs to the recorded benchmark unless a genuine backend exists.

Report export should download the exact loaded JSON artifact.
Use a Blob and a temporary object URL.
Revoke the object URL after use.
Include the run identifier in the filename.
Handle absent or malformed report files with a useful visible error state.

## 21. Visual and accessibility requirements

Use a restrained engineering-workbench visual style.
Choose clear typography and generous spacing.
Use a small palette with sufficient contrast.
Keep dense provenance data in disclosure panels or compact tables.
Avoid heavy decorative illustrations that compete with results.
Use semantic headings, labels, buttons, and tables.
Keep all controls keyboard accessible.
Give form errors a programmatic relationship to their inputs.
Provide a focus indicator on every interactive control.
Do not communicate a pass or failure through color alone.

Verify a narrow mobile viewport and a desktop viewport.
Allow comparison tables to scroll horizontally if needed.
Keep the primary form usable at narrow widths.
Avoid hardcoded fixed heights that clip error messages.
Check that the JSON view wraps or scrolls predictably.
Respect reduced-motion preferences if adding animation.

The visual proof must show a real rendered application.
A screenshot of source code does not demonstrate UI behavior.
Capture at least the report view and one non-default playground state.
Use native image inspection to check the screenshots.

## 22. Verification matrix

| Layer | Required verification |
| --- | --- |
| C arithmetic | Nominal, boundary, clamp, threshold, disabled cases |
| C parsing | Wrong argc, malformed integer, overflow token, invalid profile |
| JSON adapter | Invalid root, unknown keys, missing keys, bool-as-int, fractional values |
| Error precedence | Multiple failures across type and range checks |
| Recovery | Actual oracle calls, expected evidence families, stable hashes |
| Corpus | Deterministic generation, nonoverlap, unique IDs, both profiles |
| Reference port | Strict compile and complete corpus parity |
| Agent runner | Missing binary, auth failure, timeout, incomplete output, success manifest |
| Evaluator | Wrong answer, invalid JSON, missing output, excessive output, timeout |
| Metrics | Correct denominators and null handling |
| Report | Schema consistency and source hash correspondence |
| Angular | Production build, interactive smoke test, JSON export |

Keep tests focused on observable behavior and failure boundaries.
Avoid one test per implementation line.
Use Python `unittest` or existing test infrastructure for the harness.
Use a small Node assertion runner for port tests when sufficient.
Do not add a large test framework solely for a few pure-function checks.

Include at least one test that proves an incorrect candidate fails.
Include at least one test that proves an infrastructure failure remains visible.
Include at least one test that proves the report preserves unknown effort as `null`.
Run the actual candidate sources after their generation.
Do not substitute the reference port while keeping an agent variant label.

## 23. Execution sequence and commit plan

Each phase produces a runnable, reviewable change.
Use substantive commits instead of empty commits or cosmetic splits.

### Commit 1: establish contract and experimental method

Create the repository documentation and project metadata.
Freeze the eight-field contract and response schema.
Document attribution, heldout boundaries, and unavailable human metrics.
Add ignore rules for generated private artifacts and dependencies.
Gate: every example agrees with the frozen contract.

### Commit 2: implement the simulated C legacy tool

Add strict parsing and deterministic calculations.
Add a compiler command and focused boundary tests.
Gate: strict compilation and C behavior checks pass.

### Commit 3: recover executable specifications

Add the bounded Python adapter and actual oracle query workflow.
Write recovery evidence with hashes and observed outputs.
Add public and heldout corpus generation.
Gate: extraction is deterministic apart from timestamps and public/heldout requests do not overlap.

### Commit 4: add the TypeScript reference port

Implement the pure reference evaluator and JSON runner.
Compile under strict TypeScript settings.
Gate: reference parity passes the frozen corpus.

### Commit 5: implement measurement and reports

Add evaluator failure classification and report generation.
Add quality signals, timing fields, profile slices, and null effort handling.
Gate: deliberately incorrect and failing candidates are reported correctly.

### Commit 6: add real CLI generation and provenance

Add Claude Code and Codex runners with fresh workdirs.
Freeze prompts and manifests.
Run available CLIs and preserve actual generated sources.
Gate: each candidate label has a matching invocation manifest and source hash.

### Commit 7: build the Angular report and playground

Add the responsive report presentation and sensor form.
Import the actual reference port or selectable candidate ports.
Add report export and error states.
Gate: production build and browser smoke test pass.

### Commit 8: verify release evidence and publish

Add measured artifacts, methodology results, and final reproduction instructions.
Run strict checks and sanitizer checks where supported.
Review generated artifacts for credentials and private details.
Publish the public repository and verify its URL and default branch.
Gate: a fresh-checkout procedure matches the documented commands.

The builder may split a substantial phase into additional commits.
The final history should explain the work through coherent milestones.

## 24. Operational execution rules

Run long installs, builds, agent sessions, and test batches through tracked background execution.
Give every command an explicit working directory.
Print a progress line for each major evaluation or generation phase.
Check a launched process during its first minute.
Use the execution facility's native status mechanism.
Avoid polling loops and foreground log tails.

Keep files stable while active builds or agent runs consume them.
Freeze the public prompt bundle before launching both agents.
Do independent documentation or UI work while generation runs.
Wait only when the next step requires a job's result.
Do not modify heldout cases to improve observed parity.
Fix harness defects transparently and invalidate affected runs.

Use proper argument arrays for programmatic CLI execution.
Never construct shell commands by concatenating user or model text.
Keep credentials in their existing protected configuration.
Do not copy credentials into the repository or candidate workdir.
Review every tracked file before public publication.

## 25. Reproduction interface

The final README must provide a short working command sequence.
The precise entrypoint names can follow the chosen implementation.
The sequence must cover these operations:

```text
install locked frontend dependencies
build the C oracle
recover public executable specifications
compile TypeScript ports
run harness tests
generate Claude Code candidate
generate Codex candidate
evaluate all available variants
build Angular production assets
serve the report UI locally
```

Separate offline reproduction from paid external generation.
A user should be able to evaluate committed candidate sources without agent authentication.
Generation commands may require authenticated CLIs and incur provider usage.
Document those requirements beside the commands.
Keep the report generation command deterministic for fixed sources and cases.
Distinguish variable timestamps and wall times from deterministic behavioral results.

## 26. Risks, limitations, and truthful conclusions

The fixture is small and deliberately deterministic.
Real legacy systems contain state, undocumented persistence, timing, and hardware dependencies.
The benchmark does not cover those dimensions.
The C source and Python adapter jointly define the evaluated oracle boundary.
Record both identities to avoid attributing adapter behavior solely to C.

A passing finite corpus supports observed parity.
It does not prove universal equivalence.
An agent-authored reference offers a reproducible comparison point.
It does not measure a human developer baseline.
Single attempts expose useful failure modes.
They do not establish stable provider rankings.
Cross-profile parity tests a related configuration family.
It does not establish broad modernization transferability.

Generation provenance can establish that a particular CLI produced an artifact.
It cannot establish that a model had no prior knowledge of a public repository.
Working-directory isolation reduces accidental exposure.
It does not create an operating-system security boundary.
Reports should state the exposure model and the available evidence.

Use conclusions such as “all evaluated heldout cases matched the oracle.”
Avoid conclusions such as “the port is proven equivalent” or “the agent replaces developers.”
Keep observed results and proposed future studies separate.

## 27. Final acceptance checklist

- [ ] C fixture compiles with strict warnings.
- [ ] C parser rejects malformed numeric tokens safely.
- [ ] JSON adapter rejects booleans in integer fields.
- [ ] Numeric and error precedence semantics match across languages.
- [ ] Recovery artifact contains actual oracle observations.
- [ ] Public specification and examples have frozen hashes.
- [ ] Heldout corpus has no public request overlap.
- [ ] Reference port passes the evaluator.
- [ ] Both external agent runners have been attempted where authentication is available.
- [ ] Every generated candidate has a provenance manifest.
- [ ] Failed attempts remain visible.
- [ ] No metric uses invented human effort or cost.
- [ ] Mutation or incorrect-candidate checks exercise evaluator sensitivity.
- [ ] Angular production build succeeds.
- [ ] Playground uses the same port function as command-line evaluation.
- [ ] UI displays real report data and supports JSON export.
- [ ] Browser verification covers desktop and narrow layouts.
- [ ] Public artifacts contain no credentials or private transcripts.
- [ ] README commands match the actual implementation.
- [ ] Git history contains at least eight meaningful commits.
- [ ] Public GitHub URL and pushed commit are verified.

This checklist defines intended acceptance gates.
Checked completion belongs in the measured release evidence after execution.
