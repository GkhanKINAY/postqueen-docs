#!/usr/bin/env node
/**
 * Dark-theme, one screenshot per app page.
 * Exits 0 when credentials are missing so docs CI never depends on a login.
 */
import { mkdir, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = process.env.PQ_OUT || path.join(here, "out");
const appUrl = (process.env.PQ_APP_URL || "https://app.postqueen.ai").replace(/\/$/, "");
const email = process.env.PQ_EMAIL;
const password = process.env.PQ_PASSWORD;
const storageState = process.env.PQ_STORAGE_STATE;

const pages = [
  { slug: "calendar-week", path: "/launches?display=week" },
  { slug: "calendar-list", path: "/launches?display=list" },
  { slug: "channels", path: "/channels" },
  { slug: "composer", path: "/launches?display=week", openComposer: true },
  { slug: "media", path: "/media" },
  { slug: "analytics", path: "/analytics" },
  { slug: "settings", path: "/settings" },
  { slug: "integrations", path: "/settings?tab=integrations" },
  { slug: "social-sets", path: "/settings?tab=sets" },
  { slug: "plugs", path: "/plugs" },
  { slug: "billing", path: "/billing" },
  { slug: "agents", path: "/agents" },
];

async function main() {
  const hasSession = storageState && existsSync(storageState);
  const hasLogin = Boolean(email && password);
  if (!hasSession && !hasLogin) {
    console.log(
      "No PQ_STORAGE_STATE or PQ_EMAIL+PQ_PASSWORD. Skipping capture.\n" +
        "See scripts/screenshots/README.md. Existing Agents SVGs stay in place."
    );
    return;
  }

  let playwright;
  try {
    playwright = await import("playwright");
  } catch {
    console.log("playwright is not installed. Run: npx playwright install chromium");
    return;
  }

  await mkdir(outDir, { recursive: true });
  const browser = await playwright.chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    colorScheme: "dark",
    ...(hasSession ? { storageState } : {}),
  });
  const page = await context.newPage();

  if (!hasSession) {
    await page.goto(`${appUrl}/auth/login`, { waitUntil: "networkidle" });
    await page.locator("input[type=email], input[name=email]").first().fill(email);
    await page.locator("input[type=password], input[name=password]").first().fill(password);
    await page.getByRole("button", { name: /sign in|log in|continue/i }).first().click();
    await page.waitForURL((url) => !url.pathname.includes("/auth"), { timeout: 30000 }).catch(() => {});
  }

  await page.addInitScript(() => {
    document.documentElement.classList.add("dark");
    document.body?.classList.add("dark");
  });

  for (const item of pages) {
    await page.goto(`${appUrl}${item.path}`, { waitUntil: "networkidle" });
    await page.evaluate(() => {
      document.body?.classList.add("dark");
      document.documentElement.classList.add("dark");
    });
    if (item.openComposer) {
      const create = page.getByRole("button", { name: /create post|blank|new post/i }).first();
      if (await create.isVisible().catch(() => false)) {
        await create.click();
        await page.waitForTimeout(800);
      }
    }
    const dest = path.join(outDir, `${item.slug}.png`);
    await page.screenshot({ path: dest, fullPage: false });
    console.log("wrote", dest);
  }

  const manifest = pages.map((p) => `${p.slug}.png`).join("\n") + "\n";
  await writeFile(path.join(outDir, "manifest.txt"), manifest);
  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
