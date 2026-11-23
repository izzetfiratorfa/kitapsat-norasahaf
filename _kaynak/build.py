#!/usr/bin/env python3
"""Nora Kitap Evi — kitap alım/bağış sitesi üreticisi.
Çalıştır: python3 build.py [çıktı_klasörü]   (statik siteyi yazar)
"""
import os, shutil, html, json, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/nora-kitap'
SRC = HERE if os.path.exists(os.path.join(HERE, 'style.css')) else '/home/claude/build'
os.makedirs(OUT, exist_ok=True)

PHONE_RAW = '905529358912'
PHONE_TXT = '0552 935 89 12'
PHONE_TEL = '+905529358912'
EMAIL = ''  # varsa buraya yaz: 'nora@ornek.com' -> formda ve iletişimde görünür
ADDR = 'Ahmet Vefikpaşa Cd. No:26A, Şehremini, Fatih / İstanbul'
WA = f'https://wa.me/{PHONE_RAW}'
def wa(text): return WA + '?text=' + quote(text)
WA_HI = wa('Merhaba, kitaplarım hakkında yazmak istiyorum.')
WA_PHOTO = wa('Merhaba, kitaplığımın fotoğraflarını göndermek istiyorum. Yardımcı olur musunuz?')
WA_KURUM = wa('Merhaba, kurum olarak toplu kitap devretmek istiyoruz.\n\nKurum adı:\nTahmini kitap sayısı:\nİstenen teslim tarihi:\nKitapların bulunduğu adres (ilçe):\nKat / asansör var mı:\nTaşıma koşulları (araç girişi, mesafe vb.):\n\nFotoğrafları bu sohbete ekliyorum.')
WA_ACIL = wa('Merhaba, boşaltma tarihim yakın, kitaplarım için yardım istiyorum.\n\nBoşaltma tarihi:\nTahmini kitap sayısı:\nİlçe:\nKat / asansör var mı:\nNedeni (taşınma / kentsel dönüşüm):\n\nFotoğrafları bu sohbete ekliyorum.')
CTA = 'kitap-sat.html'
GBP = 'https://share.google/qawsznqt1ohQSFSN0'
IG = 'https://www.instagram.com/nora.cafekitap/'
XTW = 'https://x.com/NoraBiKitapEvi'
FB = 'https://www.facebook.com/norakitapcafe'
HOURS = 'Pazartesi–Cumartesi 08.00–20.00 · Pazar 13.00–19.00'
GOATCOUNTER = ''  # goatcounter.com'da kayıt olup seçtiğin kodu yaz, ör. 'norakitap' -> https://norakitap.goatcounter.com
SURE = 'Başvuruları genellikle 3 iş günü içinde yanıtlıyoruz. Yoğun dönemlerde süre uzayabilir.'
FREE = 'Teklif almak ücretsizdir. Kabul etmek zorunda değilsiniz.'

SERVICES = [
    ('kutuphane-alimi.html', 'Kütüphane ve toplu kitap', 'Çok sayıda kitabı nasıl değerlendiriyoruz? Kurumlar için de.'),
    ('tasinma-kentsel-donusum.html', 'Taşınma ve kentsel dönüşüm', 'Süre daralırken yapılacaklar ve teslim.'),
    ('vefat-sonrasi-kutuphane.html', 'Vefat sonrası kütüphane', 'Bir yakınımızın kütüphanesini nasıl devredeceğiz?'),
    ('eski-nadir-kitap.html', 'Eski, nadir ve eski harfli kitap', 'Kitabın gerçek değerini nasıl anlayacağız?'),
    ('ansiklopedi-dergi.html', 'Ansiklopedi, dergi ve seriler', 'Ağır ve eksik setleri nasıl değerlendiriyoruz?'),
]

def e(s): return html.escape(s, quote=True)

def head(title, desc, extra=''):
    GC = f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>' if GOATCOUNTER else ''
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>{e(title)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0d0d0d">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
{GC}
{extra}
</head>
<body>
'''

def header():
    subs = ''.join(f'<a href="{u}">{t}</a>' for u, t, _ in SERVICES)
    return f'''<header class="hdr"><div class="wrap">
<a class="logo" href="index.html" aria-label="Nora Kitap Evi ana sayfa">NORA<i>.</i><small>kitap evi</small></a>
<button class="burger" aria-label="Menü" aria-expanded="false">Menü</button>
<nav class="nav" aria-label="Ana menü">
<a href="index.html">Ana sayfa</a>
<a href="nora-hafiza.html">Nora Hafıza</a>
<div class="grp"><button class="gbtn" type="button" aria-expanded="false">Kitap türleri ve özel durumlar</button><div class="gsub">{subs}</div></div>
<a href="index.html#iletisim">İletişim</a>
<a class="btn" href="{CTA}">Satış / bağış başvurusu</a>
</nav></div></header>
'''

def footer():
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL else ''
    return f'''<footer class="ftr"><div class="wrap">
<div class="cols">
<div><h4>Nora Kitap Evi</h4>
<p>Fatih, Şehremini’nde bir kitapçı-kafe. Kitapları satın alırız, bağış olarak kabul ederiz. Hafıza bağışı olarak devraldığımız kitaplara Nora Hafıza kaydı açarız.</p>
<p>{e(ADDR)}</p></div>
<div><h4>Sayfalar</h4>
<a href="{CTA}">Başvuru formu</a>
<a href="nora-hafiza.html">Nora Hafıza</a>
<a href="kutuphane-alimi.html">Kütüphane ve toplu alım</a>
<a href="tasinma-kentsel-donusum.html">Taşınma ve kentsel dönüşüm</a>
<a href="vefat-sonrasi-kutuphane.html">Vefat sonrası kütüphane</a>
<a href="eski-nadir-kitap.html">Eski ve nadir kitap</a>
<a href="ansiklopedi-dergi.html">Ansiklopedi ve dergi</a></div>
<div><h4>İletişim</h4>
<a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>
<a href="{WA_HI}">WhatsApp ile yaz</a>
{mail}
<a href="kvkk.html">KVKK aydınlatma metni</a>
<p style="margin:.8rem 0 0">{HOURS}</p></div>
</div>
<div class="social"><a href="{GBP}" rel="noopener">Google’da yol tarifi ve yorumlar</a><a href="{IG}" rel="noopener">Instagram</a><a href="{XTW}" rel="noopener">X</a><a href="{FB}" rel="noopener">Facebook</a></div>
<div class="fine">© <span id="yil"></span> Nora Kitap Evi. Bu site bir ilan ya da pazar yeri değildir; kitapları doğrudan Nora satın alır ya da bağış olarak kabul eder.</div>
</div></footer>
<div class="wa"><a class="main" data-goatcounter-click="mobil-form" href="{CTA}">Başvuru formu</a><a data-goatcounter-click="mobil-whatsapp" href="{WA_HI}">WhatsApp</a></div>
<script src="main.js"></script>
<script>document.getElementById('yil').textContent=new Date().getFullYear()</script>
</body></html>
'''

def faq(items):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)

def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)

def quick_box():
    return f'''<div class="quick"><div><b>Formla uğraşmak istemiyor musunuz?</b><span>Kitaplığınızın fotoğraflarını WhatsApp’tan gönderin. Size yardımcı olalım.</span></div><a class="btn" data-goatcounter-click="whatsapp-fotograf" href="{WA_PHOTO}">WhatsApp’tan gönder</a></div>'''

def visit_box():
    return f'''<div class="quick visit"><div><b>Fotoğraf çekemiyor musunuz ya da çok kitabınız mı var?</b><span>Evinize gelip bakabiliriz. Yerinde bakış kapasitemize göre planlanır; sizi arayıp uygun günü birlikte belirleriz.</span></div><a class="btn dark" data-goatcounter-click="yerinde-bakis" href="{CTA}?yerinde=1">Evde bakılmasını isteyin</a></div>'''

# ================================================================ ANA SAYFA
jsonld = json.dumps({
    "@context": "https://schema.org", "@type": "BookStore", "name": "Nora Kitap Evi",
    "telephone": PHONE_TEL, "hasMap": GBP, "sameAs": [IG, XTW, FB],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "08:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "13:00", "closes": "19:00"}],
    "address": {"@type": "PostalAddress", "streetAddress": "Ahmet Vefikpaşa Cd. No:26A", "addressNeighborhood": "Şehremini",
                "addressLocality": "Fatih", "addressRegion": "İstanbul", "addressCountry": "TR"},
}, ensure_ascii=False)

home = head('Kitaplarınızı satın alıyor veya bağış olarak devralıyoruz · Nora Kitap Evi',
            'Taşınma, kentsel dönüşüm veya vefat sonrası kitaplarınızı satın alır ya da bağış olarak kabul ederiz. Nora Hafıza ile kitaplığınızı adınızla yaşatın. Fatih Şehremini, İstanbul.',
            f'<script type="application/ld+json">{jsonld}</script>')
home += header()
home += f'''<main>
<section class="hero"><div class="wrap">
<span class="kicker" style="color:#e0584f">Nora Kitap Evi · Şehremini, İstanbul</span>
<h1>Kitaplarınızı satın alıyor veya bağış olarak devralıyoruz.</h1>
<p class="tagline">Kitaplarınızın bir sonraki <em>durağı.</em></p>
<p class="lead">Taşınıyorsunuz, bina yıkılıyor ya da bir kütüphane sahipsiz kaldı. Kitaplarınızı satın alır veya bağış olarak kabul ederiz. İsterseniz Nora Hafıza ile her kitabın içine sahibinin adını yazarız.</p>
<div class="btns"><a class="btn" href="{CTA}">Fotoğrafları gönderin, teklifinizi alın</a><a class="btn ghost" href="{WA_HI}">WhatsApp’tan yazın</a></div>
</div></section>

<section><div class="wrap">
<div class="head"><span class="kicker">Üç yol</span><h2>Ne yapmak istiyorsunuz?</h2></div>
<div class="grid g3">
<a class="card" href="{CTA}?tur=sat"><div class="tag">Satış</div><h3>Kitaplarımı satmak istiyorum</h3><p>Fotoğrafları gönderin, teklifimizi alın.</p><span class="more">Satış başvurusu →</span></a>
<a class="card" href="{CTA}?tur=bagis"><div class="tag">Karşılıksız bağış</div><h3>Kitaplarımı bağışlamak istiyorum</h3><p>Kitaplarınızı karşılıksız devredin.</p><span class="more">Bağış başvurusu →</span></a>
<a class="card red" href="nora-hafiza.html"><div class="tag">Nora Hafıza</div><h3>Nora Hafıza</h3><p>Kitaplarınızı adınızla ve notunuzla yaşatın.</p><span class="more">Nasıl işliyor →</span></a>
</div>
{quick_box()}
{visit_box()}
</div></section>

<section class="alt" id="nasil"><div class="wrap">
<div class="head"><span class="kicker">Nasıl çalışır</span><h2>Üç adım. Kitapları ayıklamanıza gerek yok.</h2></div>
<div class="steps">
<div class="step"><h3>Fotoğraf ve form</h3><p>Formu doldurun. Form hazır bir WhatsApp mesajı üretir; kitap fotoğraflarını o sohbete eklersiniz.</p></div>
<div class="step"><h3>Yanıtımız</h3><p>Fotoğraflara bir insan bakar. Satışta teklif, bağışta teslim planı gelir. {FREE}</p></div>
<div class="step"><h3>Teslim</h3><p>Uygun olduğunuz gün kitaplar teslim alınır. Satışta ödeme, kitaplar kontrol edildikten sonra yapılır.</p></div>
</div>
<p style="margin-top:1.6rem"><b>{SURE}</b></p>
<div class="btns"><a class="btn dark" href="{CTA}">Başvuru formuna git</a></div>
</div></section>

<section class="red"><div class="wrap narrow">
<span class="kicker">Nora Hafıza</span>
<h2>Kitaplar adınızla kalır.</h2>
<p class="lead" style="color:#fff">Kentsel dönüşüm, taşınma ya da bir yakınınızın vefatı yüzünden kitaplarınızdan ayrılmak zorunda kalanlar için. Her kitabın içine sahibinin adını, isterseniz belirlediğiniz bir notu yazarız. Kitaplar, geçmişlerini kaybetmeden yoluna devam eder.</p>
<p style="font-size:1.1rem"><b>Nora Hafıza’da bağışlanan kitaplar asla satılmaz; daima yerleşik kütüphanemizde kalır.</b></p>
<div class="btns"><a class="btn" href="nora-hafiza.html">Nora Hafıza nedir?</a><a class="btn ghost" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a></div>
</div></section>

<section><div class="wrap">
<div class="head"><span class="kicker">Kitap türleri ve özel durumlar</span><h2>Durumunuz neyse oradan başlayın</h2><p class="lead">Akış hepsinde aynı: fotoğraf, teklif, teslim. Sayfalar, her durumun kendi sorusuna cevap verir.</p></div>
<div class="grid g2">
''' + ''.join(f'<a class="card" href="{u}"><h3>{t}</h3><p>{d}</p><span class="more">Sayfaya git →</span></a>' for u, t, d in SERVICES) + f'''
</div></div></section>

<section class="alt" id="rehber"><div class="wrap">
<div class="head"><span class="kicker">Fotoğraf rehberi</span><h2>Nasıl fotoğraflamalısınız?</h2><p class="lead">Fotoğraf ne kadar okunaklıysa teklif o kadar doğru gelir. Tek tek çekmenize gerek yok; raf raf çekin.</p></div>
<div class="dd">
<div class="yes"><h3>Yapın</h3><ul>
<li>Gün ışığında çekin.</li>
<li>Kitapların sırtındaki yazılar okunsun.</li>
<li>Rafı bütün olarak, sonra yakından çekin.</li>
<li>Nadir ya da eski kitapların kapağını ve künye sayfasını ayrıca çekin.</li>
<li>Yırtık, leke, kopuk cilt gibi hasarı saklamayın, gösterin.</li>
</ul></div>
<div class="no"><h3>Yapmayın</h3><ul>
<li>Flaş kullanmayın, sırtlarda parlama yapar.</li>
<li>Kitapları üst üste yığıp uzaktan çekmeyin.</li>
<li>Bulanık ve karanlık fotoğraf göndermeyin.</li>
<li>Önceden ayıklamayın. Hangisinin değerli olduğuna biz bakarız.</li>
<li>Fotoğraf sayısına takılmayın: WhatsApp sohbetinde dilediğiniz kadar ekleyebilirsiniz.</li>
</ul></div>
</div></div></section>

<section id="almiyoruz"><div class="wrap narrow">
<div class="head"><span class="kicker">Alım koşulları</span><h2>Hangi kitapları almıyoruz?</h2><p class="lead">Her kitabı kabul ettiğimiz izlenimi vermek istemiyoruz. Genellikle şunları alamıyoruz:</p></div>
<ul class="plain-list">
<li>Yoğun nem ve küf hasarı olanlar.</li>
<li>Sayfaları eksik ya da kullanılamayacak durumda olanlar.</li>
<li>Çok ağır yıpranmış, okunamayacak durumdaki kitaplar.</li>
<li>Güncelliğini yitirmiş yayınlar, test kitapları.</li>
</ul>
<p style="margin-top:1.2rem">Emin değilseniz yine de fotoğraf gönderin. Neyi neden almadığımızı teklifte açıkça yazarız.</p>
</div></section>

<section class="alt" id="sss"><div class="wrap narrow">
<div class="head"><span class="kicker">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>
''' + faq([
    ('Ne kadar sürede yanıt alırım?', SURE),
    ('Nora ilan sitesi mi, pazar yeri mi?', 'Hayır. Burada ilan verilmez, kimse kimseye bağlanmaz. Kitapları doğrudan Nora Kitap Evi satın alır ya da bağış olarak kabul eder.'),
    ('Ne kadar ödeyeceğinizi nasıl belirliyorsunuz?', 'Kitabın türüne, durumuna, adedine ve bizim için talebine bakarız. Otomatik bir fiyat listesi yok; fotoğraflara bir insan bakar ve rakamı açıkça yazar.'),
    ('Teklifi kabul etmek zorunda mıyım?', 'Hayır. ' + FREE),
    ('Her kitabı alıyor musunuz?', 'Hayır. <a href="#almiyoruz">Hangi kitapları alamadığımızı</a> yukarıda yazdık. Almadıklarımızı teklifte de açıkça belirtiriz; bağış olarak bırakabilir ya da geri alabilirsiniz.'),
    ('Fotoğraf çekemiyorum ya da çok kitabım var, ne yapmalıyım?', 'Evinize gelip bakabiliriz. Yerinde bakış kapasitemize göre planlanır; <a href="kitap-sat.html?yerinde=1">formda bu seçeneği işaretleyin</a> ya da arayın, uygun günü birlikte belirleyelim.'),
    ('İstanbul dışından başvurabilir miyim?', 'Evet, başvurabilirsiniz. İstanbul dışı başvurular durumuna göre değerlendirilir: kitap sayısı, türü ve bulunduğu yer. Fotoğrafları gönderin, yapılıp yapılamayacağını yazarız.'),
    ('Kitapları kim, nasıl teslim alıyor?', 'Teslim şeklini teklifte konuşuruz: adresinizden alım ya da dükkâna getirme. Açık adresinizi bu aşamada istemiyoruz; teklifi kabul ederseniz sorarız.'),
    ('Ödeme ne zaman, nasıl yapılıyor?', 'Satışta ödeme, kitaplar teslim alınıp fotoğraflarla karşılaştırıldıktan sonra, sizinle kararlaştırdığımız yöntemle yapılır. Online ödeme ya da ön ödeme istemiyoruz.'),
    ('Sadece kitap mı alıyorsunuz?', 'Evet, kitap alıyoruz. Dergi ve ansiklopedi dahil. Kitap dışı eşyaları alamıyoruz.'),
    ('Nora Hafıza’da bağışlanan kitaplar satılır mı?', 'Hayır. Nora Hafıza kapsamında bağışlanan kitaplar asla satılmaz; daima yerleşik kütüphanemizde kalır.'),
    ('Bilgilerim nereye gidiyor?', 'Bu site hiçbir şey saklamaz. Form, bilgilerinizi WhatsApp mesajına çevirir ve doğrudan bize gider. Ayrıntı için <a href="kvkk.html">KVKK metnine</a> bakın.'),
]) + f'''
</div></section>

<section><div class="wrap narrow">
<span class="kicker">Hakkımızda</span>
<h2>Kitapçı-kafe, hepsi bu.</h2>
<p>Nora Kitap Evi, Şehremini’nde kitap satan, çay ve kahve servis eden bir yer. Pazarlama diliyle pek aramız yok. Bir şeyi ya alırız ya almayız; her ikisini de açıkça söyleriz.</p>
<p>Kitaplarımızın bir kısmı bağış yoluyla geliyor. Bu yüzden onların doğru okurlara ulaşmasını, iyi bir yere gitmesini önemsiyoruz. Meseleyi bundan ibaret görüyoruz.</p>
</div></section>

<section class="dark" id="iletisim"><div class="wrap">
<div class="contact">
<div><span class="kicker" style="color:#e0584f">İletişim</span><h2>Önce yazın, sonra konuşalım.</h2>
<p class="lead">Fotoğraf göndermek için formu ya da WhatsApp’ı kullanın. Soru sormak için arayın.</p>
<div class="btns"><a class="btn" href="{CTA}">Başvuru formu</a><a class="btn ghost" href="{WA_HI}">WhatsApp</a><a class="btn ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div>
<dl>
<dt>Telefon / WhatsApp</dt><dd><a style="color:#fff" href="tel:{PHONE_TEL}">{PHONE_TXT}</a></dd>
<dt>Adres</dt><dd>{e(ADDR)}</dd>
<dt>Saatler</dt><dd>{HOURS}</dd>
<dt>Bizi bulun</dt><dd><a style="color:#fff" href="{GBP}" rel="noopener">Google’da yol tarifi ve yorumlar</a><br><a style="color:#fff" href="{IG}" rel="noopener">Instagram</a> · <a style="color:#fff" href="{XTW}" rel="noopener">X</a> · <a style="color:#fff" href="{FB}" rel="noopener">Facebook</a></dd>
</dl></div></div></section>
</main>
''' + footer()
write('index.html', home)

# ================================================================ FORM
form_page = head('Kitap başvurusu · Nora Kitap Evi', 'Kitaplarınızı satmak ya da bağışlamak için formu doldurun; hazır mesaj WhatsApp’ta açılır. Teklif almak ücretsiz.',
                 f'<script>window.NORA_CONFIG={{phone:"{PHONE_RAW}",email:"{EMAIL}"}}</script>')
form_page += header()
form_page += f'''<main>
<section class="hero sub"><div class="wrap">
<div class="crumb"><a href="index.html">Ana sayfa</a> / Başvuru</div>
<h1>Kitap başvurusu</h1>
<p class="lead">Formu doldurun, hazır mesaj WhatsApp’ta açılır. Kitap fotoğraflarını o sohbete eklersiniz. {FREE}</p>
</div></section>
<section style="padding-top:40px"><div class="wrap narrow">
{quick_box()}
<p class="note" style="margin-top:24px">Bu bir ilan sitesi değil. Kitaplar listelenmez, kimseye gösterilmez. Form bilgilerinizi bir sunucuda saklamaz; yalnızca WhatsApp mesajına çevirir. {SURE}</p>

<div id="errSum" class="errsum" role="alert"></div>
<form id="appForm" novalidate autocomplete="on">
<div class="form">
<h2><span>01</span> Ne yapmak istiyorsunuz?</h2>
<div class="modes">
<label class="mode"><input type="radio" name="tur" value="sat" checked><span><b>Satış</b>Kitaplarınızı Nora’ya satın.</span></label>
<label class="mode"><input type="radio" name="tur" value="bagis"><span><b>Karşılıksız bağış</b>Kitaplarınızı bedelsiz devredin.</span></label>
<label class="mode"><input type="radio" name="tur" value="hafiza"><span><b>Nora Hafıza</b>Kitaplarınızı sahibinin adı ve kişisel notuyla yaşatın. Bu kitaplar asla satılmaz; yerleşik kütüphanemizde kalır.</span></label>
</div>
<div id="hafizaBox" class="hidden" style="margin-top:22px;border-top:1px solid var(--line);padding-top:22px">
<label class="f">Kitapların içine yazılacak ad *<small> (örn. "Ahmet Yılmaz’ın kitaplığından")</small>
<input type="text" id="hafizaAd" maxlength="120"><div class="err">Hafıza için bir ad yazın.</div></label>
<label class="f">Neden ayrılıyorsunuz? <small>(isteğe bağlı)</small>
<select id="hafizaNeden"><option value="">Seçin</option><option value="tasinma">Taşınma</option><option value="kentsel">Kentsel dönüşüm</option><option value="vefat">Aileden birinin vefatı</option><option value="diger">Diğer</option></select></label>
<label class="f">Eklenmesini istediğiniz not <small>(isteğe bağlı)</small>
<textarea id="hafizaNot" maxlength="400" placeholder="Kitaba yazılmasını istediğiniz birkaç cümle"></textarea></label>
</div>
</div>

<div class="form">
<h2><span>02</span> Kitaplarınız</h2>
<label class="chk" style="font-size:1.05rem"><input type="checkbox" id="yerinde"><span><b>Fotoğraf çekemiyorum ya da çok kitabım var; evde bakılmasını istiyorum.</b> Yerinde bakış kapasitemize göre planlanır; sizi arayıp uygun günü birlikte belirleriz.</span></label>
<label class="f">Tahmini kitap sayısı <small>(bilmiyorsanız tahmin edin)</small>
<select id="sayi"><option value="">Seçin</option><option>1–20</option><option>20–50</option><option>50–100</option><option>100–300</option><option>300–500</option><option>500+</option></select></label>
<label class="f">Kitaplar hakkında not <small>(isteğe bağlı)</small>
<textarea id="notlar" maxlength="600" placeholder="Hangi tür kitaplar, durumu, boşaltma tarihi vb."></textarea></label>
<p class="note" style="margin:0"><b>Fotoğraflar bu formdan gönderilmez.</b> Formu bitirince WhatsApp sohbeti açılır; kitap fotoğraflarını orada eklersiniz. Gün ışığında çekin, sırt yazıları okunsun, flaş kullanmayın. Kaç fotoğraf olduğu fark etmez.</p>
</div>

<div class="form">
<h2><span>03</span> Bilgileriniz</h2>
<div class="row">
<label class="f">Ad *<input type="text" id="ad" autocomplete="given-name"><div class="err">Adınızı yazın.</div></label>
<label class="f">Soyad *<input type="text" id="soyad" autocomplete="family-name"><div class="err">Soyadınızı yazın.</div></label>
</div>
<div class="row">
<label class="f">Telefon *<input type="tel" id="tel" autocomplete="tel" inputmode="tel" placeholder="05xx xxx xx xx"><div class="err">Geçerli bir telefon numarası yazın.</div></label>
<label class="f">E-posta <small>(isteğe bağlı)</small><input type="email" id="email" autocomplete="email"><div class="err">E-posta adresi geçersiz görünüyor.</div></label>
</div></div>

<div class="form">
<h2><span>04</span> Kitaplar nerede?</h2>
<div class="row">
<label class="f">İl *<select id="il" autocomplete="address-level1"></select></label>
<label class="f">İlçe *<input type="text" id="ilce" autocomplete="address-level2"><div class="err">İlçeyi yazın.</div></label>
</div>
<p class="hint">Açık adresinizi şimdi istemiyoruz. Teklifi kabul ederseniz, kitapları teslim almak için o zaman sorarız. İstanbul dışındaysanız yine de başvurun; durumu değerlendiririz.</p>
</div>

<div class="form">
<label class="chk" style="font-size:1rem"><input type="checkbox" id="kvkk"><span><a href="kvkk.html" target="_blank" rel="noopener">KVKK Aydınlatma Metni</a>’ni okudum; bilgilerimin, başvurumu değerlendirmek ve benimle iletişime geçmek amacıyla Nora Kitap Evi ile WhatsApp üzerinden paylaşılmasına onay veriyorum. *</span></label>
<button class="btn submit" type="submit">Başvurumu WhatsApp’ta Gönder</button>
<p class="hint" style="margin:14px 0 0">Gönder’e basınca WhatsApp’ta hazır mesaj açılır. Mesajı göndermeden başvuru bize ulaşmaz.</p>
</div>
</form>

<div id="done" class="done" role="status" aria-live="polite">
<h2>Mesajınız hazır.</h2>
<p>Başvuru numaranız<br><span class="code" id="doneCode"></span></p>
<ol class="ol-big">
<li>WhatsApp’ta hazır mesajı <b>gönderin</b>. Açılmadıysa aşağıdaki yeşil düğmeye basın.</li>
<li id="doneFoto">Kitap fotoğraflarını aynı sohbete ekleyin.</li>
<li id="doneYerinde" class="hidden">Fotoğraf göndermenize gerek yok. Size yazıp ya da arayıp evde bakmak için uygun günü belirleriz.</li>
</ol>
<p class="hint" style="margin-top:1.4rem"><b>Bundan sonra:</b> 1. Başvurunuz oluşturuldu · 2. Fotoğraflar incelenir (ya da yerinde bakış planlanır) · 3. Teklif iletilir · 4. Kitaplar teslim alınır. {SURE}</p>
<div class="btns">
<a class="btn" id="waBtn" href="#" target="_blank" rel="noopener" style="background:#1c8c4e;border-color:#1c8c4e">WhatsApp’ı aç</a>
<a class="btn dark hidden" id="mailBtn" href="#">E-posta ile gönder</a>
<button class="btn ghost" id="copyBtn" type="button" style="color:var(--ink)">Mesajı kopyala</button>
<button class="btn ghost" id="backBtn" type="button" style="color:var(--ink)">Formu düzenle</button>
</div>
</div>

</div></section>
</main>
<script src="form.js"></script>
''' + footer()
write('kitap-sat.html', form_page)

# ================================================================ HİZMET SAYFALARI
def service_page(slug, title, desc, h1, lead, body, faqs, hero_btns=None, hafiza_band=False):
    pg = head(title + ' · Nora Kitap Evi', desc)
    pg += header()
    btns = hero_btns or f'<a class="btn" href="{CTA}">Fotoğrafları gönderin, teklifinizi alın</a><a class="btn ghost" href="{WA_HI}">WhatsApp’tan yazın</a>'
    pg += f'''<main>
<section class="hero sub"><div class="wrap">
<div class="crumb"><a href="index.html">Ana sayfa</a> / {e(title)}</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="btns">{btns}</div>
</div></section>
<section><div class="wrap narrow prose">{body}
<p class="proc">Süreç her başvuruda aynı: fotoğraf, teklif, teslim. {FREE} <a href="index.html#nasil">Ayrıntı →</a></p>
</div></section>
<section class="alt"><div class="wrap narrow"><div class="head"><span class="kicker">Sık sorulanlar</span><h2>Bu durumda en çok sorulanlar</h2></div>{faq(faqs)}</div></section>
'''
    if hafiza_band:
        pg += f'''<section class="red"><div class="wrap narrow"><span class="kicker">Nora Hafıza</span><h2>Kitaplığınızı adınızla yaşatın.</h2>
<p class="lead" style="color:#fff">Her kitabın içine sahibinin adını yazarız. Bu kitaplar asla satılmaz.</p>
<div class="btns"><a class="btn" href="nora-hafiza.html">Nora Hafıza nedir?</a></div></div></section>'''
    others = ''.join(f'<a href="{u}">{t}</a>' for u, t, _ in SERVICES if u != slug)
    pg += f'''<section><div class="wrap narrow"><h3>Başka bir durum mu var?</h3><div class="links">{others}<a href="nora-hafiza.html">Nora Hafıza</a></div>
<div class="btns" style="margin-top:2rem"><a class="btn" href="{CTA}">Başvuru formuna git</a><a class="btn ghost" style="color:var(--ink)" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div></section>
</main>
''' + footer()
    write(slug, pg)

service_page('kutuphane-alimi.html', 'Kütüphane ve toplu kitap alımı',
    'Yüzlerce kitaplık kütüphaneleri raf raf fotoğraflayın, Nora teklif versin. Okul, dernek, vakıf, ofis ve kapanan işletmeler için ayrı başvuru. Fatih Şehremini, İstanbul.',
    'Kütüphane ve toplu kitap alımı',
    'Çok sayıda kitabı nasıl değerlendiriyoruz? Kısaca: raflara bütün olarak bakıyoruz, siz ayıklamıyorsunuz.',
    f'''<h2>Raflara bütün olarak bakıyoruz</h2>
<p>Fotoğrafları raf sırasıyla inceler, kitapları tür ve durumuna göre gruplarız. Hangi kitabın değerli olduğunu önceden bilmenize gerek yok; sıradan görünen bir baskı ya da bir seri, rafın en iyi parçası çıkabilir.</p>
<p>Aynı yazarın, aynı dönemin, aynı konunun bir arada durması da değer taşır. Kütüphane bütün olarak bakılınca daha iyi okunur.</p>

<h2>Teklif parça parça gelebilir</h2>
<p>Bütün kütüphaneyi almak zorunda değiliz, siz de bütününü vermek zorunda değilsiniz. Teklifte neyi aldığımızı, neyi alamadığımızı ve nedenini yazarız. Almadıklarımızı bağış olarak bırakabilir ya da geri alabilirsiniz.</p>

<h2>Üç yüz kitabı nasıl fotoğraflarsınız?</h2>
<ul>
<li>Önce rafın tamamını, sonra sırtlar okunacak kadar yakından çekin.</li>
<li>Raf sırasıyla ilerleyin, ikinci sıra varsa belirtin.</li>
<li>Eski ya da nadir görünenleri ayrıca, kapak ve künye sayfasıyla çekin.</li>
<li>Fotoğraf sayısı sınırı yok: WhatsApp sohbetine dilediğiniz kadar ekleyebilirsiniz.</li>
</ul>

<h2>Okul, dernek, vakıf, ofis ve kapanan işletmeler</h2>
<p>Kurumların toplu devri için farklı bilgiler gerekir: kitap sayısı, teslim tarihi, kitapların bulunduğu kat ve asansör durumu, taşıma koşulları. Aşağıdaki düğme, bu bilgileri soran hazır bir WhatsApp mesajı açar. Doldurup gönderin, fotoğrafları ekleyin.</p>
<div class="btns"><a class="btn dark" href="{WA_KURUM}">Kurum olarak WhatsApp’tan yaz</a></div>

<h2>Fotoğraf çekmek zorsa ya da çok kitap varsa</h2>
<p>Evinize gelip bakabiliriz. Yerinde bakış kapasitemize göre planlanır; formda seçeneği işaretleyin, sizi arayıp uygun günü birlikte belirleyelim.</p>
<div class="btns"><a class="btn dark" data-goatcounter-click="yerinde-bakis" href="{CTA}?yerinde=1">Evde bakılmasını isteyin</a></div>''',
    [('Önceden ayıklamam gerekir mi?', 'Hayır. Olduğu gibi gösterin. Ayıklama işi zorlaştırır ve sizi yorar.'),
     ('Fiyat düşük gelirse?', 'Reddedebilirsiniz. Almadığımız kitapları bağış olarak bırakmak da, geri almak da size kalmış.'),
     ('Kurum olarak da başvurabilir miyiz?', 'Evet. Yukarıdaki kurum mesajıyla yazın; sayı, tarih, kat ve taşıma koşullarını bilmemiz yeterli.')],
    hero_btns=f'<a class="btn" href="{CTA}">Fotoğrafları gönderin, teklifinizi alın</a><a class="btn ghost" href="{WA_KURUM}">Kurum başvurusu</a>')

service_page('tasinma-kentsel-donusum.html', 'Taşınma ve kentsel dönüşümde kitaplar',
    'Kentsel dönüşüm ya da taşınma yüzünden kitaplarınızdan ayrılmak zorundaysanız Nora satın alır ya da bağış olarak kabul eder. Süre daralırken yapılacaklar.',
    'Taşınma ve kentsel dönüşümde kitaplar',
    'Süre daralırken yapılacaklar. Zamanımız az, kitapları nasıl teslim edeceğiz?',
    f'''<h2>Önce boşaltma tarihini yazın</h2>
<p>Kentsel dönüşümde ya da taşınmada kitapların sorunu hep aynıdır: tarih bellidir, koliler yetmez, yeni evde raf yoktur. Kitaplar çoğu zaman son güne kalır. Başvurudaki nota boşaltma tarihini yazın; planı ona göre yaparız.</p>
<div class="btns"><a class="btn dark" href="{WA_ACIL}">Süre dar: WhatsApp’tan hızlıca yazın</a></div>

<h2>Teslim için bilmemiz gerekenler</h2>
<ul>
<li>Boşaltma ya da taşınma tarihi</li>
<li>Tahmini kitap sayısı</li>
<li>Kat ve asansör durumu</li>
<li>Araç girişi, park mesafesi gibi taşıma koşulları</li>
</ul>
<p>Buna göre teslim şeklini seçeriz: adresinizden alım ya da dükkâna getirme. Açık adresi, teklifi kabul ettikten sonra sorarız.</p>

<h2>Koliye koymadan önce fotoğraf gönderin</h2>
<p>Kitapları kutulayıp bantlamadan önce fotoğraf gönderin. Neyin alınacağını, neyin kolilenmesi gerektiğini birlikte netleştirirsek gereksiz iş yapmazsınız.</p>

<h2>Hepsini vermek zorunda değilsiniz</h2>
<p>Bir kısmı satış, bir kısmı bağış olabilir; bir kısmını da yeni evinize götürebilirsiniz. Formdaki nota yazmanız yeterli. Satmak istemiyor, ama kitaplar adınızla kalsın istiyorsanız <a href="nora-hafiza.html">Nora Hafıza</a>’ya bakın.</p>''',
    [('Binamız iki hafta içinde boşalıyor, yetişir mi?', 'Yazın. Süre kısaysa WhatsApp’tan ya da telefonla doğrudan konuşmak en hızlısı.'),
     ('Hepsini sığdıramayacağım, bir kısmını bağışlayabilir miyim?', 'Evet. Bir kısmı satış, bir kısmı bağış olabilir; formda notta belirtmeniz yeter.'),
     ('Nemli ya da küflü kitaplar var.', 'Fotoğrafta gösterin. Almadıklarımızı teklifte açıkça yazarız.')],
    hero_btns=f'<a class="btn" href="{CTA}">Fotoğrafları gönderin, teklifinizi alın</a><a class="btn ghost" href="{WA_ACIL}">Süre dar: WhatsApp</a>',
    hafiza_band=True)

service_page('vefat-sonrasi-kutuphane.html', 'Vefat sonrası kütüphane',
    'Aileden birinin vefatından sonra kütüphanesini sahipsiz bırakmayın. Nora satın alır, bağış olarak kabul eder ya da adıyla Nora Hafıza’ya alır.',
    'Vefat sonrası kütüphane',
    'Bir yakınımızın kütüphanesini nasıl devredeceğiz? Acele etmenize gerek yok; hazır olduğunuzda yazın.',
    f'''<h2>Bir kütüphane bir insandır</h2>
<p>Kitaplara bakmak çoğu zaman zordur. Bazılarının kenarına not düşülmüştür, bazılarının arasında bir fotoğraf ya da mektup unutulmuştur. Bu yüzden böyle bir kütüphaneyi “eski kitaplar” diye bir kenara atmamak gerekir. Sorumuz yalnızca “kaç para eder” değil, “nereye gitsin”dir.</p>

<h2>Üç yol</h2>
<ul>
<li><b>Satış:</b> Fotoğraflara bakıp teklif veririz. Kabul etmek zorunda değilsiniz.</li>
<li><b>Karşılıksız bağış:</b> Kitapları bedelsiz devralırız.</li>
<li><b><a href="nora-hafiza.html">Nora Hafıza:</a></b> Her kitabın içine kütüphane sahibinin adını, isterseniz belirlediğiniz bir notu yazarız. Bu kitaplar asla satılmaz; yerleşik kütüphanemizde kalır.</li>
</ul>

<h2>Kitap aralarından çıkanlar</h2>
<p>Kitapların arasından kişisel kâğıtlar çıkabilir: mektup, fotoğraf, not, ayraç. Bunları görürsek ayırır, size veririz. Önceden bakmak isterseniz buna zaman tanırız.</p>

<h2>Aile ortak karar versin</h2>
<p>Böyle bir kütüphane genellikle birden fazla kişiyi ilgilendirir. Başvuruyu bir kişi yapabilir, ama teslimden önce ailenin hemfikir olması iyi olur. Acelemiz yok.</p>

<h2>Fotoğraf çekmek zor geliyorsa</h2>
<p>Kütüphaneyi fotoğraflamak çoğu zaman yorucudur. Evinize gelip bakabiliriz; yerinde bakış kapasitemize göre planlanır. <a href="{CTA}?yerinde=1">Formda bu seçeneği işaretleyin</a> ya da arayın, sizin için uygun günü birlikte belirleyelim.</p>''',
    [('Kitaplardan bazılarını ailede tutmak istiyoruz.', 'Elbette. Önce istediklerinizi ayırın, kalanı bize gösterin. Kısmi başvuru sorun değil.'),
     ('Hafıza için ne yazıyorsunuz?', 'Kitabın içine kütüphane sahibinin adını, isterseniz sizin belirlediğiniz kısa bir notu yazarız. Not isteğe bağlıdır.'),
     ('Hafıza bağışında kitaplara ne oluyor?', 'Yerleşik kütüphanemizde kalır ve okurlarla buluşur. Satılmaz. Dükkâna gelip bakabilirsiniz.')],
    hero_btns=f'<a class="btn" href="{CTA}">Başvuru formu</a><a class="btn ghost" href="{WA_HI}">WhatsApp’tan yazın</a>')

service_page('eski-nadir-kitap.html', 'Eski, nadir ve eski harfli kitap',
    'İlk baskı, imzalı, numaralı, eski harfli (Osmanlıca) ve eski basım kitapları Nora değerlendirir. Fotoğraf gönderin, teklif alın.',
    'Eski, nadir ve eski harfli kitap',
    'Kitabın gerçek değerini nasıl anlayacağız? Çoğu zaman cevap, kapakta değil ayrıntıda.',
    '''<h2>Değeri ne belirler?</h2>
<ul>
<li>Baskı: ilk baskı mı, kaçıncı baskı?</li>
<li>Durum: cilt, sayfalar, leke, nem, eksik sayfa</li>
<li>İmza, ithaf ya da mühür var mı, kimin?</li>
<li>Numaralı ya da sınırlı sayıda basılmış mı?</li>
<li>Eksiksiz mi, takımın parçası mı?</li>
</ul>
<p>Her eski kitap nadir değildir, her nadir kitap da pahalı değildir. Bunu fotoğraflara bakarak açıkça söyleriz.</p>

<h2>Hangi fotoğraflar gerekli?</h2>
<ul>
<li>Kapak ve sırt</li>
<li>İç kapak (başlık sayfası)</li>
<li>Künye: basım yılı, baskı sayısı, matbaa</li>
<li>İmza, ithaf ya da mühür sayfası</li>
<li>Hasarlı yerler: yırtık, leke, koparılmış sayfa. Hasarı saklamayın, değeri baştan bilmek herkesin işini kolaylaştırır.</li>
</ul>

<h2>Osmanlıca ve eski harfli kitaplar</h2>
<p>Bu basımlarda başlık sayfasını ve birkaç iç sayfayı çekin. Kitabın ailede nasıl bulunduğunu biliyorsanız yazın; işimizi kolaylaştırır.</p>

<h2>Değer çıkmazsa</h2>
<p>Bunu da saklamayız. Değerli çıkarsa ona göre teklif veririz; değeri düşükse nedenini yazarız.</p>''',
    [('Kitabımın değerini bilmiyorum, ne yapmalıyım?', 'Fotoğraf gönderin. Değerli çıkmasa bile bunu açıkça söyleriz.'),
     ('Tek bir kitap için de başvurabilir miyim?', 'Evet, adedin alt sınırı yok.'),
     ('Nadir kitabı kargoyla göndermek zorunda mıyım?', 'Hayır. Önce fotoğraflara bakarız, sonra nasıl teslim edileceğini birlikte seçeriz.')])

service_page('ansiklopedi-dergi.html', 'Ansiklopedi, dergi ve seriler',
    'Ansiklopedi setleri, dergi koleksiyonları ve cilt cilt serileri Nora değerlendirir. Eksik ciltler de sorun değil. Fotoğraf gönderin.',
    'Ansiklopedi, dergi ve seriler',
    'Ağır ve eksik setleri nasıl değerlendiriyoruz? Önce setin tam olup olmadığına, sonra nasıl taşınacağına bakıyoruz.',
    '''<h2>Set tam mı, eksik mi?</h2>
<p>Setin eksiksiz olması değerini ciddi biçimde artırır. Eksik cilt varsa söyleyin; bu durumda da değerlendirme yaparız, ama her eksik seti alamayabiliriz. Almazsak nedenini yazarız.</p>

<h2>Dergilerde sayı ve yıl</h2>
<p>Dergi koleksiyonlarında kapakların sayı ve yıl görünecek biçimde çekilmesi yeter. Kaç sayı olduğunu, hangi yıllar arasında olduğunu mesaja yazın. Tek sayılar da değerlendirilir.</p>

<h2>Ağırlık ve teslim</h2>
<p>Ansiklopedi setleri çok ağırdır; getirmeniz gerekmeyebilir. Teklif sonrası teslim yöntemini birlikte seçeriz. Kat ve asansör durumunu yazarsanız planı kolaylaştırır.</p>

<h2>Fotoğraf nasıl çekilir?</h2>
<ul>
<li>Seti bütün olarak, sırtlar okunur biçimde çekin.</li>
<li>Ciltlerde hasar varsa (kopuk cilt, leke, nem) ayrıca çekin.</li>
<li>Kaç cilt ya da sayı olduğunu yazın.</li>
</ul>''',
    [('Setim eksik, yine de alır mısınız?', 'Bazen. Fotoğraflara bakarız, almıyorsak bunu açıkça yazarız.'),
     ('Dergileri tek sayı olarak da alır mısınız?', 'Evet, değeri taşıyorsa. Sayıları ve yılları yazarsanız hızlanırız.'),
     ('Çok ağır, nasıl getiririm?', 'Getirmenize gerek olmayabilir. Teslim şeklini teklifte konuşuruz.')])

# ================================================================ NORA HAFIZA
hf = head('Nora Hafıza · Kitaplarınızı adınızla yaşatın', 'Kentsel dönüşüm, taşınma ya da vefat nedeniyle ayrıldığınız kitapları Nora’ya bağışlayın; her kitabın içine adınızı ve notunuzu yazalım. Bu kitaplar asla satılmaz.')
hf += header()
hf += f'''<main>
<section class="hero"><div class="wrap">
<div class="crumb"><a href="index.html">Ana sayfa</a> / Nora Hafıza</div>
<h1>Kitaplar, geçmişlerini kaybetmeden <em>yoluna devam etsin.</em></h1>
<p class="lead">Kitapların geçmişini nasıl koruyoruz? Her kitabın içine sahibinin adını, isterseniz belirlediğiniz bir notu yazarız. Kitap, geçmişiyle birlikte kütüphanemizde yaşamaya devam eder.</p>
<div class="btns"><a class="btn" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a><a class="btn ghost" href="{WA_HI}">Önce soru soracağım</a></div>
</div></section>

<section><div class="wrap narrow prose">
<div class="callout"><b>Nora Hafıza’da bağışlanan kitaplar asla satılmaz.</b> Daima yerleşik kütüphanemizde kalır; okurlarla ve öğrencilerle buluşmaya orada devam eder.</div>

<h2>Neden böyle bir şey?</h2>
<p>Bir evden çıkarken kitaplar en çok zorlanılan eşyadır. Taşıyamazsınız, sığdıramazsınız, çöpe de atamazsınız. Kentsel dönüşümde, taşınmada, bir yakınımızı kaybettiğimizde de aynı şey olur: kitaplar “bir yerlere gider” ve geçmişleri silinir.</p>
<p>Hafıza bu boşluk için. Kitabın bir geçmişi vardır: kimin okuduğu, kimin kitaplığından geldiği. Biz bunu silmek yerine kitabın içine yazıyoruz.</p>

<h2>Kitaba ne yazılıyor?</h2>
<p>Her kitabın içine sahibinin adını, isterseniz belirlediğiniz bir notu yazarız. Kısa ve sade olur:</p>
<div class="pull">“Ahmet Yılmaz’ın kitaplığından.”</div>
<p>Yanına birkaç cümle eklemek isterseniz ekleriz; örneğin kitabı kimin, hangi yıllarda okuduğu ya da yeni okura bir dilek. Not isteğe bağlıdır; yalnızca ad da yeterlidir.</p>

<h2>Hafıza kaydı</h2>
<p>Hafıza bağışı olarak devraldığımız kitaplara Nora Hafıza kaydı açarız: kimin kitaplığından geldiği, neden devredildiği (söylemek isterseniz) ve notunuz. Kitaplık sahibinin adı kitapla birlikte kalır.</p>

<h2>Kimler için?</h2>
<ul>
<li>Binası yıkılan ya da kentsel dönüşüme giren evinden ayrılanlar</li>
<li>Taşınırken kitaplarını götüremeyenler</li>
<li>Bir yakınının kütüphanesini sahipsiz bırakmak istemeyen aileler</li>
<li>Kitaplarının iyi bir yere gitmesini isteyen herkes</li>
</ul>
</div></section>

<section class="alt"><div class="wrap">
<div class="head"><span class="kicker">Nasıl işliyor</span><h2>Dört adım</h2></div>
<div class="steps" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
<div class="step"><h3>Başvurun</h3><p>Formda “Nora Hafıza”yı seçin. Kitapların içine yazılacak adı ve isterseniz notu yazın. Fotoğrafları WhatsApp sohbetine ekleyin.</p></div>
<div class="step"><h3>Teslim</h3><p>Kitapların nasıl teslim edileceğini birlikte seçeriz: adresten alım ya da dükkâna getirme.</p></div>
<div class="step"><h3>Adı yazarız</h3><p>Her kitabın içine sahibinin adını, isterseniz belirlediğiniz notu yazarız. Aralarından çıkan kişisel kâğıtları size veririz.</p></div>
<div class="step"><h3>Kütüphanede kalır</h3><p>Kitaplar yerleşik kütüphanemizde yerini alır ve satılmaz.</p></div>
</div>
<p class="proc">Hafıza bir bağış biçimidir; kitapları satın almıyoruz. Para almak isterseniz normal <a href="{CTA}?tur=sat">satış başvurusu</a> yapabilirsiniz; bu kitaplar adınızla yazılmaz. Yalnızca kitap alıyoruz; dergi ve ansiklopedi dahil. Kitap dışı eşyaları alamıyoruz.</p>
</div></section>

<section><div class="wrap narrow">
<div class="head"><span class="kicker">Sık sorulanlar</span><h2>Hafıza hakkında</h2></div>
''' + faq([
    ('Hafıza kitapları satılır mı?', 'Hayır. Nora Hafıza kapsamında bağışlanan kitaplar asla satılmaz; daima yerleşik kütüphanemizde kalır.'),
    ('Her kitabı alıyor musunuz?', 'Çoğunu. Çok yıpranmış, kullanılamayacak durumdakileri ayırırız; bunu size de söyleriz. <a href="index.html#almiyoruz">Hangi kitapları alamadığımızı</a> ana sayfada yazdık.'),
    ('Kitabın içine yazı yazmanız kitaba zarar vermez mi?', 'Zarar vermeyecek biçimde, kısa ve okunaklı yazarız. İsterseniz önce nasıl yazılacağını sorabilirsiniz.'),
    ('Bağış sonrası kitaplara ne olduğunu görebilir miyim?', 'Evet. Dükkânımıza gelip bakabilirsiniz.'),
    ('Kaç kitap getirebilirim?', 'Adedin alt ve üst sınırı yok. Çok sayıda ise önce fotoğraf gönderin; teslim yöntemini konuşuruz.'),
]) + f'''
</div></section>

<section class="red"><div class="wrap narrow"><h2>Kitaplığınızı adınızla yaşatın.</h2>
<p class="lead" style="color:#fff">Başvuru ücretsiz. Fotoğraf yeter. {SURE}</p>
<div class="btns"><a class="btn" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a><a class="btn ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div></section>
</main>
''' + footer()
write('nora-hafiza.html', hf)

# ================================================================ KVKK
kv = head('KVKK Aydınlatma Metni · Nora Kitap Evi', 'Nora Kitap Evi kitap alım ve bağış başvurularında kişisel verilerin nasıl işlendiğine dair aydınlatma metni.')
kv += header()
kv += f'''<main>
<section class="hero sub"><div class="wrap"><div class="crumb"><a href="index.html">Ana sayfa</a> / KVKK</div>
<h1>KVKK Aydınlatma Metni</h1>
<p class="lead">6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında, kitap alım ve bağış başvurunuzda verilerinizin nasıl işlendiğini anlatır.</p></div></section>
<section><div class="wrap narrow prose">
<h2>Veri sorumlusu</h2>
<p>Nora Kitap Evi, {e(ADDR)}. Telefon: <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>.</p>

<h2>Bu site veri saklamaz</h2>
<p>Bu web sitesinde bir sunucu, veri tabanı ya da kullanıcı hesabı yoktur. Başvuru formuna yazdığınız bilgiler tarayıcınızda bir WhatsApp mesajına dönüştürülür. Mesajı siz gönderdiğinizde bize ulaşır. Göndermezseniz hiçbir yere gitmez. Fotoğraflar siteye yüklenmez; WhatsApp sohbetinde siz eklersiniz.</p>

<h2>Hangi veriler, ne amaçla?</h2>
<ul>
<li><b>Ad, soyad, telefon, e-posta (isteğe bağlı):</b> Sizinle iletişime geçmek ve teklifi iletmek için.</li>
<li><b>İl ve ilçe:</b> Kitapların bulunduğu bölgeyi bilmek için. Açık adres, başvuruda istenmez; teklifi kabul ederseniz teslim almak için ayrıca sorulur.</li>
<li><b>Kitap fotoğrafları ve notlar:</b> Teklifi hazırlamak için.</li>
<li><b>Hafıza bilgileri (ad, neden, not):</b> Kitapların içine yazılacak bilgileri belirlemek için.</li>
</ul>

{"<h2>Çerezsiz sayaç</h2><p>Bu sitede GoatCounter adlı, çerez kullanmayan, kişiyi tanımlamayan bir sayaç çalışır. Hangi sayfaların açıldığını anonim olarak sayar; ad, telefon gibi bilgileriniz buraya gönderilmez.</p>" if GOATCOUNTER else ""}
<h2>Hukuki sebep</h2>
<p>Verileriniz, başvurunuzu değerlendirmek ve sözleşme (satış ya da bağış) kurmak amacıyla, açık rızanıza dayanılarak işlenir.</p>

<h2>Aktarım</h2>
<p>Verileriniz üçüncü kişilerle paylaşılmaz. Mesajı WhatsApp üzerinden ilettiğiniz için WhatsApp’ın kendi gizlilik koşulları geçerlidir.</p>

<h2>Saklama</h2>
<p>Başvuru süreci bittikten sonra, siz talep ettiğinizde, ilettiğiniz bilgiler silinir. Satış ya da bağış gerçekleşmişse, yasal olarak tutulması gereken kayıtlar mevzuatta öngörülen süre kadar saklanır.</p>

<h2>Haklarınız</h2>
<p>KVKK madde 11 uyarınca verilerinizin işlenip işlenmediğini öğrenme, düzeltilmesini, silinmesini ya da işlenmesine itiraz etmeyi isteme haklarına sahipsiniz. Talebinizi <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a> numarasından ya da WhatsApp üzerinden bize iletebilirsiniz.</p>
</div></section>
</main>
''' + footer()
write('kvkk.html', kv)

# ================================================================ 404 + dosyalar
nf = head('Sayfa bulunamadı · Nora Kitap Evi', 'Aradığınız sayfa bulunamadı.')
nf += header()
nf += '''<main><section class="hero sub"><div class="wrap"><h1>Bu sayfa kayıp.</h1><p class="lead">Kitaplar gibi, bazen sayfalar da raftan düşer.</p><div class="btns"><a class="btn" href="index.html">Ana sayfaya dön</a></div></div></section></main>
''' + footer()
write('404.html', nf)

for fn in ['style.css', 'main.js', 'form.js']:
    shutil.copy(os.path.join(SRC, fn), os.path.join(OUT, fn))
write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#0d0d0d"/><text x="32" y="44" font-family="Georgia,serif" font-size="38" font-weight="700" text-anchor="middle" fill="#f2ece0">N</text><circle cx="49" cy="44" r="5" fill="#b3201f"/></svg>')
write('.nojekyll', '')
print(sorted(os.listdir(OUT)))
