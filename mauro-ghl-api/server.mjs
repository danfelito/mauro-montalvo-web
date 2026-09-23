import http from "node:http";

const PORT = Number(process.env.PORT || 3000);
const ALLOWED_ORIGIN = "https://mauro-montalvo-web.onrender.com";
const GHL_BASE = "https://services.leadconnectorhq.com";
const API_VERSION = "2021-07-28";
const MAX_BODY_BYTES = 16 * 1024;
const rateWindows = new Map();

function send(res, status, payload, origin) {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Vary": "Origin"
  };
  if (origin === ALLOWED_ORIGIN) {
    headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN;
    headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS";
    headers["Access-Control-Allow-Headers"] = "Content-Type";
    headers["Access-Control-Max-Age"] = "600";
  }
  res.writeHead(status, headers);
  res.end(JSON.stringify(payload));
}

function allowedOrigin(req) {
  const origin = req.headers.origin || "";
  return origin === ALLOWED_ORIGIN ? origin : null;
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(Object.assign(new Error("too_large"), { status: 413 }));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
      } catch {
        reject(Object.assign(new Error("invalid_json"), { status: 400 }));
      }
    });
    req.on("error", () => reject(Object.assign(new Error("request_error"), { status: 400 })));
  });
}

function clean(value, limit) {
  return typeof value === "string" ? value.trim().replace(/[\u0000-\u001f\u007f]/g, "").slice(0, limit) : "";
}

function checkRateLimit(req) {
  const forwarded = req.headers["x-forwarded-for"];
  const ip = (typeof forwarded === "string" ? forwarded.split(",")[0].trim() : req.socket.remoteAddress) || "unknown";
  const now = Date.now();
  const current = rateWindows.get(ip);
  if (!current || now - current.start >= 60_000) {
    rateWindows.set(ip, { start: now, count: 1 });
    return true;
  }
  current.count += 1;
  if (rateWindows.size > 2000) {
    for (const [key, value] of rateWindows) {
      if (now - value.start >= 60_000) rateWindows.delete(key);
    }
  }
  return current.count <= 20;
}

async function ghlRequest(path, init = {}) {
  const token = process.env.GHL_MAURO_PRIVATE_TOKEN;
  if (!token || !process.env.GHL_MAURO_LOCATION_ID) {
    const error = new Error("not_configured");
    error.status = 503;
    throw error;
  }
  const response = await fetch(GHL_BASE + path, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      Version: API_VERSION,
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(init.headers || {})
    },
    signal: AbortSignal.timeout(10_000)
  });
  if (!response.ok) {
    const error = new Error("upstream_error");
    error.status = response.status;
    throw error;
  }
  return response.json();
}

const server = http.createServer(async (req, res) => {
  const origin = req.headers.origin || "";
  const corsOrigin = allowedOrigin(req);

  if (req.method === "OPTIONS") {
    if (!corsOrigin) return send(res, 403, { error: "origin_not_allowed" }, null);
    return send(res, 204, {}, corsOrigin);
  }
  if (!corsOrigin) return send(res, 403, { error: "origin_not_allowed" }, null);

  const url = new URL(req.url || "/", "http://localhost");
  if (req.method === "GET" && url.pathname === "/health") {
    const configured = Boolean(process.env.GHL_MAURO_PRIVATE_TOKEN && process.env.GHL_MAURO_LOCATION_ID);
    return send(res, 200, { ok: true, configured }, corsOrigin);
  }

  if (req.method === "GET" && url.pathname === "/api/integrations/gohighlevel/status") {
    try {
      const result = await ghlRequest(`/locations/${encodeURIComponent(process.env.GHL_MAURO_LOCATION_ID)}`);
      return send(res, 200, {
        connected: true,
        status: 200,
        locationId: result.location?.id || process.env.GHL_MAURO_LOCATION_ID,
        locationName: result.location?.name || null,
        error: null
      }, corsOrigin);
    } catch (error) {
      const status = error.status || 502;
      return send(res, status === 503 ? 503 : 502, {
        connected: false,
        status,
        locationId: process.env.GHL_MAURO_LOCATION_ID || null,
        locationName: null,
        error: status === 401 || status === 403 ? "credential_or_permission_error" :
          status === 404 ? "location_not_found" :
          status === 503 ? "integration_not_configured" : "upstream_unavailable"
      }, corsOrigin);
    }
  }

  if (req.method === "POST" && url.pathname === "/api/leads") {
    if (!checkRateLimit(req)) return send(res, 429, { error: "rate_limited" }, corsOrigin);
    if (!String(req.headers["content-type"] || "").toLowerCase().includes("application/json")) {
      return send(res, 415, { error: "json_required" }, corsOrigin);
    }

    let body;
    try {
      body = await readJson(req);
    } catch (error) {
      return send(res, error.status || 400, { error: error.message || "invalid_request" }, corsOrigin);
    }

    if (clean(body.website, 200)) return send(res, 202, { ok: true }, corsOrigin);

    const fullName = clean(body.name, 120);
    const parts = fullName.split(/\s+/).filter(Boolean);
    const firstName = clean(parts.shift() || "", 80);
    const lastName = clean(parts.join(" "), 80);
    const email = clean(body.email, 254).toLowerCase();
    const phone = clean(body.phone, 40);
    const companyName = clean(body.company, 160);

    if (!firstName && !email && !phone) return send(res, 400, { error: "contact_required" }, corsOrigin);
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return send(res, 400, { error: "invalid_email" }, corsOrigin);
    }

    try {
      const result = await ghlRequest("/contacts/upsert", {
        method: "POST",
        body: JSON.stringify({
          locationId: process.env.GHL_MAURO_LOCATION_ID,
          firstName: firstName || undefined,
          lastName: lastName || undefined,
          email: email || undefined,
          phone: phone || undefined,
          companyName: companyName || undefined,
          source: "Sitio web Mauro Montalvo"
        })
      });
      return send(res, 200, { ok: true, created: Boolean(result.new) }, corsOrigin);
    } catch (error) {
      const status = error.status || 502;
      return send(res, status === 503 ? 503 : 502, {
        error: status === 503 ? "integration_not_configured" : "crm_unavailable"
      }, corsOrigin);
    }
  }

  return send(res, 404, { error: "not_found" }, corsOrigin);
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Mauro GHL API listening on port ${PORT}`);
});
