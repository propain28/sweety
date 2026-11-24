KEZDŐKÉPERNYŐS WIDGET (Apartmanok ma)
=====================================

Mit mutat: négy sor, apartmanonként egy. Például:
    Apartman 1     2 fő távozik · 3 fő érkezik
Piros a sor, ha aznap érkezik valaki, vagy bent van egy vendég, aki aznap
nem távozik. Zöld, ha minden más (üres, vagy csak távozik valaki).
Ha nincs érkező és nincs távozó, a sorban egy "–" áll.
A widget a mai napot magától számolja, éjfélkor is átáll. Vendégnevet nem
tárol és nem mutat. Rákoppintva megnyílik az app.

Frissítés: a widget magától legfeljebb félóránként frissül. Ha az appban
mentesz egy foglalást, az új adat a widgeten a következő frissítéskor jelenik meg.

MIT KELL TENNI A GITHUB TÁROLÓBAN
1. Töltsd fel (írd felül) ezeket a fájlokat az apartman-capacitor mappában:
     package.json         (új: @capacitor/preferences bővítmény)
     www/index.html       (új: az app kiírja a widget adatait)
     widget/install_widget.py   (új mappa és fájl)
2. A fordító fájlban (.github/workflows/...) add hozzá ezt a lépést a
   "Capacitor szinkronizálás" és az "APK fordítása" lépés közé:

      - name: Widget beillesztése
        run: python3 widget/install_widget.py

3. Várd meg a fordítást, töltsd le az új APK-t, és telepítsd a régi fölé.
4. Nyisd meg az appot EGYSZER (ekkor írja ki az első adatot a widgetnek).
5. A kezdőképernyőn nyomd hosszan az üres részt > Widgetek > "Apartmanok ma".
   Húzd ki a kezdőképernyőre, és szükség esetén méretezd át.

HA A FORDÍTÁS HIBÁT ÍR
Másold be a hibaüzenet utolsó sorait, és segítek. A szkript a legvalószínűbb
hibákat szövegesen jelzi (például ha nem találja a MainActivity.java fájlt).
