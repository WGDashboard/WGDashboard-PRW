import { describe, expect, it } from "vitest";

import config from "./vite.config.js";
import { proxy } from "./proxy.js";

describe("Vite configuration", () => {
  it("loads the client development proxy configuration", () => {
    expect(proxy).toBe("http://wg.local:10086/");
    expect(config.server.proxy["/client"]).toBe(proxy);
  });
});
