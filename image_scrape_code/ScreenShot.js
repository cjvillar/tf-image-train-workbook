/*
  YouTube Video Screenshot Capture
  ---------------------------------
  Captures screenshots at regular intervals from a YouTube video.
  Uses puppeteer v24+ APIs.

  Assumptions:
  - A ~60sec ad may play at the beginning (script waits it out)
  - Screenshots are used for image training data

  Setup:
    npm install puppeteer
    node ScreenShot.js
*/

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const path = require('path');
const fs = require('fs');

// ─── Config ──────────────────────────────────────────────────────────────────
const VIDEO_URL         = 'https://youtu.be/WK4tNpULpd8?feature=shared&t=975';
const SCREENSHOT_FOLDER = path.join(__dirname, 'screenshots');
const INTERVAL_SECONDS  = 10;   // capture one frame every N seconds of real time
const MAX_SCREENSHOTS   = 20;   // stop after this many frames (0 = run until video ends)
const AD_WAIT_MS        = 10_000; // wait 65s  for pre-roll ad to finish before capturing
// ─────────────────────────────────────────────────────────────────────────────

/** Simple async delay — replaces the removed page.waitForTimeout() */
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function ensureFolder(folderPath) {
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
    console.log(`Created folder: ${folderPath}`);
  }
}

async function captureVideoScreenshots() {
  await ensureFolder(SCREENSHOT_FOLDER);

  const browser = await puppeteer.launch({
    headless: "new",          // set false or "new" for youtube
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--autoplay-policy=no-user-gesture-required',
      '--disable-blink-features=AutomationControlled', // hides webdriver flag
      '--start-maximized',
    ],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  await page.setUserAgent(
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
);

  // Suppress YouTube UI overlays so screenshots show only the video
  await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });

  console.log('Navigating to video…');
  await page.goto(VIDEO_URL, { waitUntil: 'networkidle2', timeout: 60_000 });

  // Wait for the <video> element to appear
  await page.waitForSelector('video', { timeout: 30_000 });

  // Start playback
  await page.evaluate(() => {
    const video = document.querySelector('video');
    if (video) {
      video.muted = false;
      video.play();
    }
  });

  // Hide YouTube chrome (title bar, controls, end-cards) for cleaner frames
  await page.addStyleTag({
    content: `
      .ytp-chrome-top,
      .ytp-chrome-bottom,
      .ytp-endscreen-content,
      .iv-branding,
      .ytp-ce-element { display: none !important; }
    `,
  });

  // Wait for any pre-roll ad to finish
  console.log(`Waiting ${AD_WAIT_MS / 1000}s for ad to finish…`);
  await delay(AD_WAIT_MS);

  // ── Screenshot loop ──────────────────────────────────────────────────────
  let count = 0;

  while (true) {
    // Check whether the video has ended
    const videoEnded = await page.evaluate(() => {
      const v = document.querySelector('video');
      return !v || v.ended || v.paused;
    });

    if (videoEnded) {
      console.log('Video has ended. Stopping.');
      break;
    }

    if (MAX_SCREENSHOTS > 0 && count >= MAX_SCREENSHOTS) {
      console.log(`Reached max screenshots (${MAX_SCREENSHOTS}). Stopping.`);
      break;
    }

    // Build a timestamp-based filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filePath  = path.join(SCREENSHOT_FOLDER, `screenshot-${timestamp}.png`);

    try {
      await page.screenshot({
        path: filePath,
        clip: { x: 0, y: 0, width: 1280, height: 720 },
      });
      count++;
      console.log(`[${count}] Screenshot saved: ${filePath}`);
    } catch (err) {
      console.error('Screenshot failed:', err.message);
    }

    // Wait for the next interval
    await delay(INTERVAL_SECONDS * 1000);
  }

  await browser.close();
  console.log(`Done. ${count} screenshot(s) saved to ${SCREENSHOT_FOLDER}`);
}

captureVideoScreenshots().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
