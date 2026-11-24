#!/usr/bin/env python3
"""
Az Apartman Foglalások kezdőképernyős widgetjének beillesztése a Capacitor által
generált Android-projektbe. A GitHub fordítás futtatja a `npx cap add android`
után. Többször is lefuttatható, nem duplikál semmit.

Használat (az apartman-capacitor mappából):   python3 widget/install_widget.py
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
MAIN = os.path.join(ROOT, "android", "app", "src", "main")

mains = glob.glob(os.path.join(MAIN, "java", "**", "MainActivity.java"), recursive=True)
if not mains:
    sys.exit("HIBA: nem találom a MainActivity.java fájlt. Előbb futtasd: npx cap add android")
main_java = mains[0]
pkg = re.search(r"^package\s+([\w.]+);", open(main_java, encoding="utf-8").read(), re.M).group(1)
java_dir = os.path.dirname(main_java)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("írva:", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------- Java: logika
LOGIC = """package PKG;

/** A widget szabályai, Android nélkül, hogy külön is tesztelhető legyen. */
final class WidgetLogic {

    static final class Row {
        String name;
        boolean red;
        String text;
    }

    /**
     * Piros: aznap érkezik valaki, vagy bent van egy vendég, aki aznap nem távozik.
     * Zöld: minden más. A dátumok "yyyy-MM-dd" alakúak, szövegként összehasonlíthatók.
     */
    static Row[] compute(String today, String[] names, int[] apt, String[] in, String[] out, int[] ppl) {
        Row[] rows = new Row[4];
        for (int a = 0; a < 4; a++) {
            int depN = 0, depP = 0, arrN = 0, arrP = 0;
            boolean stay = false;
            for (int k = 0; k < apt.length; k++) {
                if (apt[k] != a) continue;
                if (out[k].equals(today)) { depN++; depP += ppl[k]; }
                if (in[k].equals(today)) { arrN++; arrP += ppl[k]; }
                if (in[k].compareTo(today) < 0 && out[k].compareTo(today) > 0) stay = true;
            }
            Row r = new Row();
            r.name = (names != null && a < names.length && names[a] != null && !names[a].isEmpty())
                    ? names[a] : "Apartman " + (a + 1);
            r.red = arrN > 0 || stay;
            String d = depN > 0 ? (depP > 0 ? depP + " f\\u0151 t\\u00e1vozik" : "t\\u00e1vozik") : "";
            String e = arrN > 0 ? (arrP > 0 ? arrP + " f\\u0151 \\u00e9rkezik" : "\\u00e9rkezik") : "";
            if (d.isEmpty() && e.isEmpty()) r.text = "\\u2013";
            else if (d.isEmpty()) r.text = e;
            else if (e.isEmpty()) r.text = d;
            else r.text = d + " \\u00b7 " + e;
            rows[a] = r;
        }
        return rows;
    }
}
"""

# ------------------------------------------------------------- Java: widget
PROVIDER = """package PKG;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.widget.RemoteViews;

import org.json.JSONArray;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/** Mai nap, apartmanonként: ki távozik, ki érkezik. Az adatot az app írja a Capacitor Preferences-be. */
public class ApartmanWidget extends AppWidgetProvider {

    private static final int[] ROW = {R.id.aw_r1, R.id.aw_r2, R.id.aw_r3, R.id.aw_r4};
    private static final int[] NAME = {R.id.aw_n1, R.id.aw_n2, R.id.aw_n3, R.id.aw_n4};
    private static final int[] INFO = {R.id.aw_i1, R.id.aw_i2, R.id.aw_i3, R.id.aw_i4};

    @Override
    public void onUpdate(Context context, AppWidgetManager manager, int[] ids) {
        RemoteViews views = build(context);
        for (int id : ids) {
            manager.updateAppWidget(id, views);
        }
    }

    static RemoteViews build(Context context) {
        RemoteViews v = new RemoteViews(context.getPackageName(), R.layout.aw_widget);
        String today = new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date());

        WidgetLogic.Row[] rows = null;
        try {
            SharedPreferences sp = context.getSharedPreferences("CapacitorStorage", Context.MODE_PRIVATE);
            String raw = sp.getString("apartmanWidget", null);
            if (raw != null) {
                JSONObject o = new JSONObject(raw);
                JSONArray n = o.optJSONArray("names");
                String[] names = new String[4];
                for (int i = 0; i < 4; i++) {
                    names[i] = n != null ? n.optString(i, "") : "";
                }
                JSONArray b = o.optJSONArray("b");
                int len = b == null ? 0 : b.length();
                int[] apt = new int[len];
                String[] in = new String[len];
                String[] out = new String[len];
                int[] ppl = new int[len];
                for (int k = 0; k < len; k++) {
                    JSONObject x = b.getJSONObject(k);
                    apt[k] = x.optInt("a", -1);
                    in[k] = x.optString("i", "");
                    out[k] = x.optString("o", "");
                    ppl[k] = x.optInt("p", 0);
                }
                rows = WidgetLogic.compute(today, names, apt, in, out, ppl);
            }
        } catch (Exception ignored) {
            rows = null;
        }

        for (int a = 0; a < 4; a++) {
            boolean red = rows != null && rows[a].red;
            String name = rows != null ? rows[a].name : "Apartman " + (a + 1);
            String text = rows != null ? rows[a].text : (a == 0 ? "Nyisd meg az appot" : "\\u2013");
            v.setTextViewText(NAME[a], name);
            v.setTextViewText(INFO[a], text);
            v.setInt(ROW[a], "setBackgroundResource", red ? R.drawable.aw_bg_red : R.drawable.aw_bg_green);
        }

        Intent launch = context.getPackageManager().getLaunchIntentForPackage(context.getPackageName());
        if (launch != null) {
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 23) {
                flags |= PendingIntent.FLAG_IMMUTABLE;
            }
            v.setOnClickPendingIntent(R.id.aw_root, PendingIntent.getActivity(context, 0, launch, flags));
        }
        return v;
    }
}
"""

# --------------------------------------------------------------- erőforrások
def layout():
    rows = ""
    for i in range(1, 5):
        rows += f"""
    <LinearLayout
        android:id="@+id/aw_r{i}"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_margin="2dp"
        android:paddingLeft="10dp"
        android:paddingRight="10dp"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:background="@drawable/aw_bg_green">

        <TextView
            android:id="@+id/aw_n{i}"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:maxLines="1"
            android:textColor="#FFFFFF"
            android:textSize="14sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/aw_i{i}"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:paddingLeft="8dp"
            android:gravity="end"
            android:maxLines="2"
            android:textColor="#FFFFFF"
            android:textSize="13sp" />
    </LinearLayout>
"""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/aw_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="4dp">
{rows}</LinearLayout>
"""


def shape(color):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="{color}" />
    <corners android:radius="10dp" />
</shape>
"""


INFO_XML = """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="250dp"
    android:minHeight="180dp"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/aw_widget"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"
    android:description="@string/aw_desc" />
"""

STRINGS = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="aw_label">Apartmanok ma</string>
    <string name="aw_desc">Mai érkezések és távozások apartmanonként. Piros: érkezik vagy bent van vendég.</string>
</resources>
"""

RECEIVER = """
        <receiver
            android:name="PKG.ApartmanWidget"
            android:exported="false"
            android:label="@string/aw_label">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/aw_widget_info" />
        </receiver>
"""

write(os.path.join(java_dir, "WidgetLogic.java"), LOGIC.replace("PKG", pkg))
write(os.path.join(java_dir, "ApartmanWidget.java"), PROVIDER.replace("PKG", pkg))
write(os.path.join(MAIN, "res", "layout", "aw_widget.xml"), layout())
write(os.path.join(MAIN, "res", "drawable", "aw_bg_red.xml"), shape("#B3261E"))
write(os.path.join(MAIN, "res", "drawable", "aw_bg_green.xml"), shape("#1B6B43"))
write(os.path.join(MAIN, "res", "xml", "aw_widget_info.xml"), INFO_XML)
write(os.path.join(MAIN, "res", "values", "aw_strings.xml"), STRINGS)

manifest_path = os.path.join(MAIN, "AndroidManifest.xml")
manifest = open(manifest_path, encoding="utf-8").read()
if "ApartmanWidget" in manifest:
    print("manifest: a widget már be van jegyezve")
else:
    if "</application>" not in manifest:
        sys.exit("HIBA: az AndroidManifest.xml-ben nincs </application>")
    manifest = manifest.replace("</application>", RECEIVER.replace("PKG", pkg) + "    </application>", 1)
    write(manifest_path, manifest)
print("A widget beillesztve, csomag:", pkg)
