import { afterEach, describe, expect, it, vi } from "vitest";

import { requestURl } from "./request.js";

describe("requestURl", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("uses the client proxy in development", () => {
    vi.stubEnv("MODE", "development");

    expect(requestURl("/api/configurations")).toBe(
      "/client/api/configurations",
    );
  });
});
