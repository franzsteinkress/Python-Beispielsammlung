// Copyright (c) 2025 Franz Steinkress
// Licensed under the MIT License - see LICENSE file for details
//

const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const outputDir = path.join(__dirname, "insta-visuals/screenshots");
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

// Liste der Bilddateien
const images = [
    "bildverarbeitung.png", 
    "blockchain.png", 
    "finanzdatenanzeige.png", 
    "lizenzpruefer.png", 
    "verschluesselung.png", 
    "blog.png", 
    "blogcreate.png", 
    "chatbot.png", 
    "notizenverwaltung.png", 
    "notizenverwaltungnotizen.png", 
    "notizenverwaltungapi.png"
];

const titles = [
    "Bildverarbeitung", 
    "Blockchain", 
    "Finanzdatenanzeige", 
    "Lizenzpruefer", 
    "Verschluesselung", 
    "Blog", 
    "Blog", 
    "Chatbot", 
    "Notizenverwaltung", 
    "Notizenverwaltung", 
    "Notizenverwaltung"
];

const descriptions = [
    "Python-Anwendung mit OpenCV", 
    "Python-Blockchain-Demo mit Web3 und Ganache", 
    "Python-Anwendung mit Bankdaten im CSV-Format", 
    "Python-Anwendung mit RSA-Lizenzdateien", 
    "Python-AES-Verschlüsselung mit 'cryptography'", 
    "Webanwendung mit Flask und SQLite-Datenbank", 
    "Webanwendung zum Erstellen eines Blogbeitrags", 
    "Webanwendung mit Flask", 
    "Python-Anwendung mit Flask und SQLite", 
    "Webanwendung mit Flask und SQLite (REST-API)", 
    "Webanwendung mit Datenbankauszug der Notizen", 
];

const notes = [
    "Theme: 'plastik' - Layout-Manager: pack()", 
    "Theme: 'radiance' - Layout-Manager: grid()", 
    "Theme: 'alt' - Layout-Manager: grid()", 
    "Theme: 'classic' - Layout-Manager: grid()", 
    "Theme: tk-Widgets - Layout-Manager: grid()", 
    "Theme: Bootstrap 5.3 Standard mit Anpassungen", 
    "Theme: Bootstrap 5.3 Standard mit Anpassungen", 
    "Theme: Eigenes minimalistisches CSS", 
    "Theme: 'clam' - Layout-Manager: pack()", 
    "Theme: Bootstrap 5.3 Standard mit Anpassungen", 
    "Theme: Bootstrap 5.3 Standard mit Anpassungen"
];

const dominantColors = [
    "#ffde88", "#f56cb5", "#91d6ff", "#91d6ff", "#91d6ff",
    "#91d6ff", "#91d6ff", "#ffde88", "#ffde88", "#91d6ff",
    "#91d6ff"
];

const fontColors = [
    "#333", "#333", "#333", "#333", "#333", 
    "#333", "#333", "#333", "#333", "#333", 
    "#333"
];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.setViewport({
        width: 1080,
        height: 1920,
        deviceScaleFactor: 1,
    });

    await page.goto("file://" + __dirname + "/insta-visuals/index.html");

    for (let i = 0; i < images.length; i++) {
        const imageName = images[i];
        const titleName = titles[i];
        const descript = descriptions[i];
        const domColor = dominantColors[i];
        const fontColor = fontColors[i];
        console.log("Verarbeite Bild:", imageName, "Index:", i);

        // Dynamisches Setzen des Bildes und Textes
        await page.evaluate((imgSrc, idx, total, titleName, descript, domColor, fontColor) => {
            try {
                // Bildquelle aktualisieren
                const imgElement = document.querySelector("img");
                if (imgElement) {
                    imgElement.src = `./assets/${imgSrc}`;
                }

                // Text für den Button oder Rahmen aktualisieren
                const textElement = document.querySelector("#closeBtn") || document.querySelector(".frame > div:first-child");
                if (textElement) {
                    textElement.textContent = `Bild ${idx + 1} von ${total}`;
                }

                const textLine1 = document.querySelector("#title.line1")
                if (textLine1) {
                    textLine1.textContent = `${titleName}`;
                }

                const textLine2 = document.querySelector("#description.line2")
                if (textLine2) {
                    textLine2.textContent = `${descript}`;
                }

                const textLine3 = document.querySelector("#description.line3")
                if (textLine3) {
                    textLine3.textContent = `${descript}`;
                }

                const overlayBox = document.querySelector("#overlayBox");
                if (overlayBox) {
                    overlayBox.style.backgroundColor = `${domColor}`;
                    overlayBox.style.color = `${fontColor}`;
                    overlayBox.style.outline = `${domColor}`;
                }
            } catch (error) {
                console.error("Fehler in page.evaluate:", error);
            }
        }, imageName, i, images.length, titleName, descript, domColor, fontColor);

        // Warten, bis das Bild vollständig geladen ist
        await page.waitForFunction(() => {
            const img = document.querySelector("img");
            return img && img.complete && img.naturalHeight > 0;
        });

        // Kurze Verzögerung für Stabilität
        await new Promise(resolve => setTimeout(resolve, 300));

        const filename = `img${i + 1}-${imageName}`;
        const filepath = path.join(outputDir, `${filename}`);
        await page.screenshot({ path: filepath, omitBackground: false });
        console.log("Screenshot gespeichert:", filename);
    }

    await browser.close();
})();