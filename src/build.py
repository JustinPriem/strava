import json,sys,statistics as st,collections
race=json.load(open(sys.argv[1])); tpl=open(sys.argv[2]).read()
pts=race['pts']
F=json.load(open(sys.argv[4]))
ak=[r['t'] for r in F if r['ak']=='Männer']
bins=collections.Counter(int(r['t']//120)*2 for r in F)
FIELD={'n':len(F),'median':st.median(r['t'] for r in F),'akMedian':st.median(ak),'winner':F[0]['t'],'bins':sorted(bins.items())}
data={
 'pts':pts,
 'splits':race['splits'],
 'zones':race['zones'],
 'gpsKm':11.33,'elevGain':68,
 'halves':[1854,1699],
 'field':FIELD,
 'firstZ5':1137,
 'segments':[
  {'name':'Weimarer Stadtlauf 5-km-Runde','len':5622,'a':1806,'ha':178,'b':1680,'hb':187},
  {'name':'Ilmpark 1K Sprint','len':1063,'a':355,'ha':176,'b':321,'hb':186},
  {'name':'Falkenburg Sprint','len':309,'a':105,'ha':183,'b':90,'hb':191},
  {'name':'Zwiebelsprint','len':693,'a':182,'ha':178,'b':210,'hb':191},
  {'name':'Goethe Gartenhaus Sprint','len':209,'a':51,'ha':186,'b':0,'hb':0},
  {'name':'Start/Ziel-Gerade Weimar Stadtlauf','len':367,'a':110,'ha':190,'b':0,'hb':0},
 ],
 'efforts':[['400 m',106],['½ Meile',222],['1 km',278],['1 Meile',448],['2 Meilen',935],['5 km',1492],['10 km',3123]],
 'effDist':{'400 m':400,'½ Meile':804.67,'1 km':1000,'1 Meile':1609.34,'2 Meilen':3218.69,'5 km':5000,'10 km':10000},
 'facts':[
  ['10.735','Herzschläge zwischen Start und Ziel, im Schnitt 181 pro Minute.'],
  ['≈ 22 Zwiebeln','So viel Energie stecken in 970 kcal, bei rund 44 kcal pro mittelgroßer Zwiebel. Passend zum Markt.'],
  ['20,4 km/h','Spitzentempo im Zielsprint auf den letzten 100 Metern, also 2:57 pro Kilometer.'],
  ['−1:12 /km','So viel schneller als dein Schnitt im Training seit Juli (6:19 /km über 24 Läufe).'],
  ['2.','Höchster Relative Effort deines Läuferlebens. Nur der erste Halbmarathon im April lag mit 262 höher.'],
  ['5:49','So lange lief die Uhr nach dem Ziel noch weiter. Deshalb zeigt Strava 1:05:04 statt 58:49.'],
  ['0,1 s','Fehlten dir zu Platz 414. Vier Läufer kamen innerhalb von 1,1 Sekunden ins Ziel.'],
  ['123','Läufer hast du in der zweiten Runde überholt. Nur 2 sind an dir vorbeigezogen.'],
  ['2. von 4','Starter aus Bad Berka. Einer aus deinem Ort war 45 Sekunden schneller.'],
  ['170 m','Die Strecke war laut Ergebnisliste 11,5 km lang. Das GPS hat nur 11,33 km erfasst, in der Altstadt nichts Ungewöhnliches.'],
  ['24:52','Deine neue 5-km-Bestzeit, mitten im Rennen gelaufen. Bisher lag dein schnellster 5er im Training bei gut 25 Minuten.'],
  ['1653','Seit diesem Jahr gibt es den Weimarer Zwiebelmarkt. Goethe soll ein Fan der Zwiebelzöpfe gewesen sein.'],
 ]}
open(sys.argv[3],'w').write(tpl.replace('/*DATA*/null',json.dumps(data,ensure_ascii=False,separators=(',',':'))))
