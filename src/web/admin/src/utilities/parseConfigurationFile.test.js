import { describe, expect, it } from "vitest";

import { parseInterface, parsePeers } from "./parseConfigurationFile.js";

describe("parseConfigurationFile", () => {
  it("parses interface settings before the first peer", () => {
    const configuration = parseInterface(
      "[Interface]\nAddress = 10.0.0.1/24\nListenPort = 51820\n[Peer]\nPublicKey = key",
    );

    expect(configuration).toEqual({
      Address: "10.0.0.1/24",
      ListenPort: 51820,
    });
  });

  it("parses peer settings", () => {
    const peers = parsePeers(
      "[Interface]\nAddress = 10.0.0.1/24\n[Peer]\nPublicKey = key\nAllowedIPs = 10.0.0.2/32",
    );

    expect(peers).toEqual([
      {
        name: "",
        PublicKey: "key",
        AllowedIPs: "10.0.0.2/32",
      },
    ]);
  });
});
