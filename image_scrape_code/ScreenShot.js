/*
This is a screen capture script made specifically to capture screenshots of a YouTube video.
The script uses puppetter to caputre images at 60 sec intervals from a video.
Assumptions are: 
A 60sec ad plays at the begining of the video

the screenshots will be used for an image training model (or so I hope)

npm install puppeteer
node ScreenShot.js


*/ 

const puppeteer = require('puppeteer');
const path = require('path');

async function captureVideoScreenshots() {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  
  // set the viewport size
  await page.setViewport({ width: 1280, height: 720 });
  
  // YouTube video URL
  const videoUrl = 'https://youtu.be/yzo0lE-gk5I?feature=shared';
  
  // Nav to YouTube 
  await page.goto(videoUrl);


  // wait for the video to load
  await page.waitForSelector('video');

  // sim pressing the F key for full screen (does not currently work)
  await page.waitForTimeout(3000);
  await page.keyboard.press('F');

  // play vid
  await page.evaluate(() => {
    const video = document.querySelector('video');
    video.play();
  });


  // capture screenshots every minute
  setInterval(async () => {
    try {
      // generate timestamps for the screenshot filename
      const timestamp = new Date().toISOString().replace(/:/g, '-');

      // def folder to save the screenshots
      const folderPath = path.join(__dirname, 'screenshots'); // Change 'screenshots' to your desired folder name

      // capture and save screenshots
      await page.screenshot({ path: path.join(folderPath, `screenshot-${timestamp}.png`), clip: { x: 0, y: 0, width: 1280, height: 720 } });

      console.log(`Screenshot captured at ${timestamp}`);
    } catch (error) {
      console.error('An error occurred while capturing the screenshot:', error);
    }
  }, 60000); // 60000 milliseconds = 1 minute 
}

captureVideoScreenshots();