export function evaluate(input: unknown) {
  const invalid = (field: string) => ({
    ok: false as const,
    error: { code: "INVALID_REQUEST" as const, field },
  });
  const fields = [
    "profile", "sampleMs", "gain", "offsetMilli", "rawMilli",
    "alarmLowMilli", "alarmHighMilli", "enabled",
  ];
  if (typeof input !== "object" || input === null || Array.isArray(input)) {
    return invalid("$");
  }
  const request = input as Record<string, unknown>;
  const keys = Object.keys(request);
  if (keys.length !== fields.length ||
      fields.some(field => !Object.prototype.hasOwnProperty.call(request, field)) ||
      keys.some(key => !fields.includes(key))) {
    return invalid("$");
  }
  if (request.profile !== "temperature" && request.profile !== "pressure") {
    return invalid("profile");
  }
  const ranges: [string, number, number][] = [
    ["sampleMs", 10, 60000],
    ["gain", 1, 16],
    ["offsetMilli", -100000, 100000],
    ["rawMilli", -1000000, 1000000],
    ["alarmLowMilli", -20000000, 20000000],
    ["alarmHighMilli", -20000000, 20000000],
  ];
  for (const [field, min, max] of ranges) {
    const value = request[field];
    if (typeof value !== "number" || !Number.isSafeInteger(value) || value < min || value > max) {
      return invalid(field);
    }
  }
  if (typeof request.enabled !== "boolean") return invalid("enabled");
  const sampleMs = request.sampleMs as number;
  const gain = request.gain as number;
  const offsetMilli = request.offsetMilli as number;
  const rawMilli = request.rawMilli as number;
  const low = request.alarmLowMilli as number;
  const high = request.alarmHighMilli as number;
  if (low >= high) return invalid("alarmHighMilli");

  const effectiveSampleMs = Math.ceil(sampleMs / 10) * 10;
  const rawReading = rawMilli * gain + offsetMilli;
  const minReading = request.profile === "temperature" ? -40000 : 0;
  const maxReading = request.profile === "temperature" ? 125000 : 1000000;
  const readingMilli = Math.max(minReading, Math.min(maxReading, rawReading));
  const warnings: string[] = [];
  if (effectiveSampleMs !== sampleMs) warnings.push("sample-rounded");
  if (readingMilli !== rawReading) warnings.push("reading-clamped");
  const status = !request.enabled ? "disabled"
    : readingMilli < low ? "low"
    : readingMilli > high ? "high" : "ok";
  return {
    ok: true as const,
    profile: request.profile,
    effectiveSampleMs,
    readingMilli,
    status,
    warnings,
  };
}
