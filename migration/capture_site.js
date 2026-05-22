const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const pages = [
  ['https://sabertechlogistics.com/', 'home-full.png'],
  ['https://sabertechlogistics.com/leadership/', 'leadership-full.png'],
  ['https://sabertechlogistics.com/atmp-courier/', 'atmp-courier-full.png'],
  ['https://sabertechlogistics.com/atmp-core/', 'atmp-core-full.png'],
  ['https://sabertechlogistics.com/customer-order/', 'customer-order-full.png'],
  ['https://sabertechlogistics.com/driver-access/', 'driver-access-full.png'],
  ['https://sabertechlogistics.com/press/', 'press-full.png'],
  ['https://sabertechlogistics.com/contact-us/', 'contact-full.png'],
  ['https://sabertechlogistics.com/about/', 'about-full.png'],
  ['https://sabertechlogistics.com/privacy-policy/', 'privacy-policy-full.png'],
  ['https://sabertechlogistics.com/term-and-conditions/', 'terms-full.png'],
];

async function settle(page) {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(3000);
  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y <= height + 900; y += 650) {
    await page.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
    await page.waitForTimeout(500);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(1800);
}

(async () => {
  fs.mkdirSync(path.join('migration', 'screenshots'), { recursive: true });
  const browser = await chromium.launch();
  const desktop = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  for (const [url, name] of pages) {
    console.log(`Capturing ${url}`);
    await desktop.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await settle(desktop);
    await desktop.screenshot({ path: path.join('migration', 'screenshots', name), fullPage: true });
  }

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
  for (const [url, name] of [
    ['https://sabertechlogistics.com/', 'home-mobile-full.png'],
    ['https://sabertechlogistics.com/leadership/', 'leadership-mobile-full.png'],
  ]) {
    console.log(`Capturing mobile ${url}`);
    await mobile.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await settle(mobile);
    await mobile.screenshot({ path: path.join('migration', 'screenshots', name), fullPage: true });
  }

  await browser.close();
})();
