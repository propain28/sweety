APARTMAN FOGLALÁSOK - önálló Android app (APK) készítése
=========================================================

Ez az app semmilyen weboldaltól nem függ: a fájljai az APK-ban vannak,
a foglalások a telefonon tárolódnak. Az APK-t egyszer le kell fordítani
egy számítógépen (Windows vagy Mac). Ez nagyjából 20-30 perc, nagy
részét a letöltések teszik ki.

A. EGYSZERI ELŐKÉSZÍTÉS A SZÁMÍTÓGÉPEN
   1. Telepítsd a Node.js LTS verzióját: nodejs.org
   2. Telepítsd az Android Studiót: developer.android.com/studio
      (a telepítő a szükséges Java-t is hozza). Indítsd el egyszer, és
      fogadd el az alapértelmezett beállításokat, hogy letöltse az
      Android SDK-t.

B. AZ APK ELKÉSZÍTÉSE
   1. Csomagold ki ezt a mappát (apartman-capacitor), és nyiss benne
      egy terminált (Windows: a mappában írd be a címsorba, hogy cmd,
      majd Enter. Mac: Terminal, cd a mappába).
   2. Futtasd sorban ezeket a parancsokat:
        npm install
        npx cap add android
        npx @capacitor/assets generate --android
        npx cap sync
        npx cap open android
      (Az utolsó megnyitja az Android Studiót.)
   3. Az Android Studióban várd meg, amíg lefut az alsó sávban a
      "Gradle sync" (első alkalommal akár 10 perc is).
   4. Menü: Build > Build Bundle(s) / APK(s) > Build APK(s).
      Ha kész, a jobb alsó sarokban megjelenik a "locate" link, az
      a mappát nyitja meg, ahol az app-debug.apk található.

C. TELEPÍTÉS A TELEFONRA
   Másold át az app-debug.apk fájlt a telefonra (USB, e-mail vagy Drive),
   nyisd meg a Fájlok alkalmazásban, és engedélyezd az ismeretlen
   forrásból való telepítést, amikor a telefon rákérdez.

D. A RÉGI (NETLIFY-S) APP ADATAINAK ÁTVITELE
   Az új app külön tárolót használ, ezért a foglalások nem kerülnek át
   automatikusan.
   1. A régi appban: Mentés (Google Drive), a fájlt tedd fel a Drive-ra.
   2. Az új appban: "Visszaállítás fájlból", válaszd ki a mentést.

E. MENTÉS GOOGLE DRIVE-RA
   Az új appban a "Mentés (Google Drive)" gomb megnyitja az Android
   megosztási menüjét. Válaszd a Drive-ot. Utána az app megkérdezi,
   hogy sikerült-e a mentés, és csak akkor jelöli mentettnek.

F. FRISSÍTÉS KÉSŐBB
   Ha új verziót kapsz: cseréld le a www/index.html fájlt, majd futtasd:
        npx cap sync
   és építsd újra az APK-t (B/4). Telepítsd a régi fölé.
   Fontos: ha másik számítógépen készíted az APK-t, a telefon nem
   engedi a régi fölé telepíteni, mert más a digitális aláírás. Ilyenkor
   előbb mentsd el az adatokat, töröld a régi appot, telepítsd az újat,
   és állítsd vissza az adatokat.

G. ELŐFORDULHATÓ HIBÁK
   - "npm" nem található: indítsd újra a terminált a Node.js
     telepítése után.
   - Az Android Studio hibát ír a Java vagy az SDK miatt: a
     Tools > SDK Manager menüben telepítsd a javasolt csomagokat.
   - Ha egy parancs hibával áll le, másold be a hibaüzenetet, és
     segítek megoldani.
