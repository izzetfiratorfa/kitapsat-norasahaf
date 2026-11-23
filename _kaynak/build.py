#!/usr/bin/env python3
import os, shutil, html, json

OUT = '/home/claude/nora-kitap'
SRC = '/home/claude/build'

PHONE_RAW = '905539358912'
PHONE_TXT = '0553 935 89 12'
PHONE_TEL = '+905539358912'
EMAIL = ''  # varsa buraya yaz: 'nora@ornek.com' -> formda ve iletişimde görünür
ADDR = 'Ahmet Vefikpaşa Cd. No:26A, Şehremini, Fatih / İstanbul'
WA = f'https://wa.me/{PHONE_RAW}'
WA_HI = WA + '?text=' + 'Merhaba%2C%20kitaplar%C4%B1m%20hakk%C4%B1nda%20yazmak%20istiyorum.'
CTA = 'kitap-sat.html'

SERVICES = [
    ('kutuphane-alimi.html', 'Kütüphane ve toplu kitap', 'Yüzlerce kitabı tek tek ayıklamayın. Raf raf fotoğraflayın, gerisini biz yapalım.'),
    ('tasinma-kentsel-donusum.html', 'Taşınma ve kentsel dönüşüm', 'Tarih belli, koliler yetmiyor, kitaplar hâlâ rafta. Süre darken yapılacaklar.'),
    ('vefat-sonrasi-kutuphane.html', 'Vefat sonrası kütüphane', 'Birinin kütüphanesi, onun hafızasıdır. Sahipsiz kalmasın.'),
    ('eski-nadir-kitap.html', 'Eski, nadir ve eski harfli kitap', 'İlk baskı, imzalı, eski harfli (Osmanlıca), numaralı baskılar.'),
    ('ansiklopedi-dergi.html', 'Ansiklopedi, dergi ve seriler', 'Takım halindeki setler, dergi koleksiyonları, cilt cilt seriler.'),
]

def e(s): return html.escape(s, quote=True)

def head(title, desc, extra=''):
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
{extra}
</head>
<body>
'''

def header():
    return f'''<header class="hdr"><div class="wrap">
<a class="logo" href="index.html" aria-label="Nora Kitap Evi ana sayfa">NORA<i>.</i><small>kitap evi</small></a>
<button class="burger" aria-label="Menü" aria-expanded="false">Menü</button>
<nav class="nav" aria-label="Ana menü">
<a href="index.html#nasil">Nasıl çalışır?</a>
<a href="nora-hafiza.html">Nora Hafıza</a>
<a href="index.html#rehber">Fotoğraf rehberi</a>
<a href="index.html#sss">Sık sorulanlar</a>
<a href="index.html#iletisim">İletişim</a>
<a class="btn" href="{CTA}">Kitaplarımı vermek istiyorum</a>
</nav></div></header>
'''

def footer():
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL else ''
    return f'''<footer class="ftr"><div class="wrap">
<div class="cols">
<div><h4>Nora Kitap Evi</h4>
<p>Fatih Şehremini'nde kitapçı-kafe. Kitapları satın alırız, bağış olarak devralırız, Nora Hafıza ile adını yazıp raflarımıza koyarız.</p>
<p>{e(ADDR)}</p></div>
<div><h4>Sayfalar</h4>
<a href="{CTA}">Başvuru formu</a>
<a href="nora-hafiza.html">Nora Hafıza</a>
<a href="kutuphane-alimi.html">Kütüphane alımı</a>
<a href="tasinma-kentsel-donusum.html">Taşınma ve kentsel dönüşüm</a>
<a href="vefat-sonrasi-kutuphane.html">Vefat sonrası kütüphane</a>
<a href="eski-nadir-kitap.html">Eski ve nadir kitap</a>
<a href="ansiklopedi-dergi.html">Ansiklopedi ve dergi</a></div>
<div><h4>İletişim</h4>
<a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>
<a href="{WA_HI}">WhatsApp ile yaz</a>
{mail}
<a href="kvkk.html">KVKK aydınlatma metni</a></div>
</div>
<div class="fine">© <span id="yil"></span> Nora Kitap Evi. Bu site bir ilan ya da pazar yeri değildir; kitapları doğrudan Nora satın alır ya da bağış olarak devralır.</div>
</div></footer>
<div class="wa"><a href="{WA_HI}">WhatsApp</a><a href="{CTA}">Başvuru formu</a></div>
<script src="main.js"></script>
<script>document.getElementById('yil').textContent=new Date().getFullYear()</script>
</body></html>
'''

def faq(items):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)

def steps3(a, b, c):
    return f'''<div class="steps">
<div class="step"><h3>{a[0]}</h3><p>{a[1]}</p></div>
<div class="step"><h3>{b[0]}</h3><p>{b[1]}</p></div>
<div class="step"><h3>{c[0]}</h3><p>{c[1]}</p></div>
</div>'''

def other_services(skip):
    cards = ''.join(f'<a class="card" href="{u}"><h3>{t}</h3><p>{d}</p><span class="more">Sayfaya git →</span></a>' for u, t, d in SERVICES if u != skip)
    return f'<div class="grid g2">{cards}</div>'

def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)

# ---------------------------------------------------------------- ANA SAYFA
STEPS_HOME = steps3(
    ('Fotoğraf ve form', 'Kitaplarınızın fotoğraflarını çekin, formu doldurun. Form hazır bir WhatsApp mesajı üretir, fotoğrafları o sohbete eklersiniz.'),
    ('Yanıtımız', 'Fotoğraflara bir insan bakar. Satmak istediyseniz teklif, bağış istediyseniz teslim planı gelir. Teklif ücretsizdir, kabul zorunluluğu yoktur.'),
    ('Teslim', 'Uygun olduğunuz gün kitaplar teslim alınır. Satışta ödeme, kitaplar kontrol edildikten sonra yapılır. Hafıza bağışında kitaplara adınız yazılır.'),
)

jsonld = json.dumps({
    "@context": "https://schema.org", "@type": "BookStore", "name": "Nora Kitap Evi",
    "telephone": PHONE_TEL,
    "address": {"@type": "PostalAddress", "streetAddress": "Ahmet Vefikpaşa Cd. No:26A", "addressNeighborhood": "Şehremini",
                "addressLocality": "Fatih", "addressRegion": "İstanbul", "addressCountry": "TR"},
}, ensure_ascii=False)

home = head('Kitaplarınızı Nora Kitap Evi satın alsın ya da bağış olarak devralsın',
            'Taşınma, kentsel dönüşüm veya vefat sonrası kitaplarınızı satın alırız ya da bağış olarak devralırız. Nora Hafıza ile içine adınızı yazıp raflarımıza koyarız. Fatih Şehremini, İstanbul.',
            f'<script type="application/ld+json">{jsonld}</script>')
home += header()
home += f'''<main>
<section class="hero"><div class="wrap">
<span class="kicker" style="color:#e0584f">Nora Kitap Evi · Şehremini, İstanbul</span>
<h1>Kitaplarınızın bir sonraki <em>durağı.</em></h1>
<p class="lead">Taşınıyorsunuz, bina yıkılıyor ya da bir kütüphane sahipsiz kaldı. Kitaplarınızı satın alırız ya da bağış olarak devralırız. Bağışta içine adınızı yazar, rafımıza koyarız. Çöpe gitmesinler diye.</p>
<div class="btns"><a class="btn" href="{CTA}">Fotoğraf gönder, yanıt al</a><a class="btn ghost" href="{WA_HI}">WhatsApp'tan yaz</a></div>
</div></section>

<section><div class="wrap">
<div class="head"><span class="kicker">Üç yol</span><h2>Ne yapmak istiyorsunuz?</h2></div>
<div class="grid g3">
<a class="card" href="{CTA}?tur=sat"><div class="tag">Seçenek 1</div><h3>Satmak</h3><p>Fotoğrafları gönderin, teklifimizi verelim. Beğenmezseniz hiçbir yükümlülük yok. Kabul ederseniz kitaplar kontrol edilir, ödeme yapılır.</p><span class="more">Satış başvurusu →</span></a>
<a class="card" href="{CTA}?tur=bagis"><div class="tag">Seçenek 2</div><h3>Bağışlamak</h3><p>Satmak istemiyor, sadece iyi bir yere gitsinler istiyorsanız kitapları devralırız. Okurlarla buluşmaları için raflara koyarız.</p><span class="more">Bağış başvurusu →</span></a>
<a class="card red" href="nora-hafiza.html"><div class="tag">Seçenek 3 · Nora Hafıza</div><h3>Adınızla bağışlamak</h3><p>Kitapların içine sahibinin adını ve istediğiniz notu yazıp öyle raflara koyarız. Kitap hafızasını kaybetmeden yoluna devam eder.</p><span class="more">Nasıl işliyor →</span></a>
</div></div></section>

<section class="alt" id="nasil"><div class="wrap">
<div class="head"><span class="kicker">Nasıl çalışır</span><h2>Üç adım. Kitapları ayıklamanıza gerek yok.</h2></div>
{STEPS_HOME}
<div class="btns"><a class="btn dark" href="{CTA}">Başvuru formuna git</a></div>
</div></section>

<section class="red"><div class="wrap narrow">
<span class="kicker">Nora Hafıza</span>
<h2>Kitaplar adınızla kalır.</h2>
<p class="lead" style="color:#fff">Kentsel dönüşüm, taşınma ya da bir yakınınızın vefatı yüzünden kitaplarınızdan ayrılmak zorunda kalanlar için. Kitapları bize bağışlarsınız. İçine sahibinin adını, isterseniz bir not da yazarız. Sonra raflarımıza koyarız; okurlara ve öğrencilere ulaşmaya devam ederler.</p>
<div class="btns"><a class="btn" href="nora-hafiza.html">Nora Hafıza nedir?</a><a class="btn ghost" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a></div>
</div></section>

<section><div class="wrap">
<div class="head"><span class="kicker">Hangi kitaplar</span><h2>Duruma göre sayfalar</h2><p class="lead">Durumunuz neyse oradan başlayın. Hepsinin akışı aynı: fotoğraf, yanıt, teslim.</p></div>
<div class="grid g2">
''' + ''.join(f'<a class="card" href="{u}"><h3>{t}</h3><p>{d}</p><span class="more">Sayfaya git →</span></a>' for u, t, d in SERVICES) + f'''
</div></div></section>

<section class="alt" id="rehber"><div class="wrap">
<div class="head"><span class="kicker">Fotoğraf rehberi</span><h2>Nasıl fotoğraflayın?</h2><p class="lead">Fotoğraf ne kadar okunaklıysa teklif o kadar doğru gelir. Tek tek çekmenize gerek yok; raf raf çekin.</p></div>
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
<li>10 fotoğraf yetmiyorsa durun: kalanını WhatsApp'ta göndeririz.</li>
</ul></div>
</div></div></section>

<section id="sss"><div class="wrap narrow">
<div class="head"><span class="kicker">Sık sorulanlar</span><h2>Aklınızdakiler</h2></div>
''' + faq([
    ('Nora ilan sitesi mi, pazar yeri mi?', 'Hayır. Burada ilan verilmez, kimse kimseye bağlanmaz. Kitapları doğrudan Nora Kitap Evi satın alır ya da bağış olarak devralır.'),
    ('Ne kadar ödeyeceğinizi nasıl belirliyorsunuz?', 'Kitabın türüne, durumuna, adedine ve bizim için talebine bakarız. Otomatik bir fiyat listesi yok; fotoğraflara bir insan bakar ve rakamı açıkça yazar.'),
    ('Teklifi kabul etmek zorunda mıyım?', 'Hayır. Teklif ücretsizdir, reddederseniz hiçbir şey olmaz.'),
    ('Her kitabı alıyor musunuz?', 'Her kitabı almak zorunda değiliz. Almayacaklarımızı teklifte açıkça yazarız. Onları bağış olarak bırakabilir ya da geri alabilirsiniz.'),
    ('Kitapları kim, nasıl teslim alıyor?', 'Teslim şeklini teklifte konuşuruz: adresinizden alım ya da dükkâna getirme. Sayıya ve mesafeye göre ikisinden biri seçilir.'),
    ('Ödeme ne zaman, nasıl yapılıyor?', 'Satışta ödeme, kitaplar teslim alınıp fotoğraflarla karşılaştırıldıktan sonra, sizinle kararlaştırdığımız yöntemle yapılır. Online ödeme ya da ön ödeme istemiyoruz.'),
    ('Sadece kitap mı alıyorsunuz?', 'Evet, kitap alıyoruz. Dergi ve ansiklopedi dahil. Kitap dışı eşyaları alamıyoruz.'),
    ('Bilgilerim nereye gidiyor?', 'Bu site hiçbir şey saklamaz. Form, bilgilerinizi WhatsApp mesajına çevirir ve doğrudan bize gider. Ayrıntı için <a href="kvkk.html">KVKK metnine</a> bakın.'),
]) + f'''
</div></section>

<section class="alt"><div class="wrap narrow">
<span class="kicker">Hakkımızda</span>
<h2>Kitapçı-kafe, hepsi bu.</h2>
<p>Nora Kitap Evi, Şehremini'nde kitap satan ve çay-kahve servis eden bir yer. Pazarlama diliyle aramız iyi değil: ya alırız ya almayız, ikisini de açıkça söyleriz. Kitaplar bize hep bağışla da geliyor; o yüzden iyi bir yere gitmeleri meselesine ciddiyetle bakarız.</p>
</div></section>

<section class="dark" id="iletisim"><div class="wrap">
<div class="contact">
<div><span class="kicker" style="color:#e0584f">İletişim</span><h2>Önce yazın, sonra konuşalım.</h2>
<p class="lead">Fotoğrafları göndermek için formu kullanın. Soru sormak için WhatsApp'tan yazın ya da arayın.</p>
<div class="btns"><a class="btn" href="{WA_HI}">WhatsApp</a><a class="btn ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div>
<dl>
<dt>Telefon / WhatsApp</dt><dd><a style="color:#fff" href="tel:{PHONE_TEL}">{PHONE_TXT}</a></dd>
<dt>Adres</dt><dd>{e(ADDR)}</dd>
<dt>Saatler</dt><dd>Her gün açığız. Pazarları geç açıp erken kapatıyoruz; gelmeden önce yazın.</dd>
</dl></div></div></section>
</main>
''' + footer()
write('index.html', home)

# ---------------------------------------------------------------- FORM
form_page = head('Kitap başvurusu · Nora Kitap Evi', 'Kitaplarınızı satmak ya da bağışlamak için fotoğraf ve bilgilerinizi gönderin. Teklif ücretsiz, kabul zorunlu değil.',
                 f'<script>window.NORA_CONFIG={{phone:"{PHONE_RAW}",email:"{EMAIL}"}}</script>')
form_page += header()
form_page += f'''<main>
<section class="hero sub"><div class="wrap">
<div class="crumb"><a href="index.html">Ana sayfa</a> / Başvuru</div>
<h1>Kitap başvurusu</h1>
<p class="lead">Başvuru ücretsiz, teklifi kabul etmek zorunda değilsiniz. Formu doldurun, hazır mesaj WhatsApp'ta açılır; fotoğrafları o sohbete eklersiniz.</p>
</div></section>
<section style="padding-top:40px"><div class="wrap narrow">
<p class="note">Bu bir ilan sitesi değil. Kitaplar listelenmez, kimseye gösterilmez. Kabul ederseniz Nora doğrudan satın alır ya da bağış olarak devralır. Form bilgilerinizi bir sunucuda saklamaz; yalnızca WhatsApp mesajına çevirir.</p>

<form id="appForm" class="" novalidate autocomplete="on">
<div class="form">
<h2><span>01</span> Ne yapmak istiyorsunuz?</h2>
<div class="modes">
<label class="mode"><input type="radio" name="tur" value="sat" checked><span><b>Satmak istiyorum</b>Teklif verin, uygunsa kitaplar teslim alınsın, ödeme yapılsın.</span></label>
<label class="mode"><input type="radio" name="tur" value="bagis"><span><b>Bağışlamak istiyorum</b>Para istemiyorum, kitaplar iyi bir yere gitsin.</span></label>
<label class="mode"><input type="radio" name="tur" value="hafiza"><span><b>Nora Hafıza olarak bağışlamak istiyorum</b>Kitapların içine adı ve istediğim not yazılsın, öyle raflara konsun.</span></label>
</div>
<div id="hafizaBox" class="hidden" style="margin-top:20px;border-top:1px solid var(--line);padding-top:20px">
<label class="f">Kitapların içine yazılacak ad *<small> (örn. "Ahmet Yılmaz'ın kitaplığından")</small>
<input type="text" id="hafizaAd" maxlength="120"><div class="err">Hafıza için bir ad yazın.</div></label>
<label class="f">Neden ayrılıyorsunuz? <small>(isteğe bağlı)</small>
<select id="hafizaNeden"><option value="">Seçin</option><option value="tasinma">Taşınma</option><option value="kentsel">Kentsel dönüşüm</option><option value="vefat">Aileden birinin vefatı</option><option value="diger">Diğer</option></select></label>
<label class="f">Eklenmesini istediğiniz not <small>(isteğe bağlı)</small>
<textarea id="hafizaNot" maxlength="400" placeholder="Kitaba yazılmasını istediğiniz birkaç cümle"></textarea></label>
</div>
</div>

<div class="form">
<h2><span>02</span> Kitap fotoğrafları</h2>
<div id="drop" class="drop" tabindex="0" role="button" aria-label="Fotoğraf seç">
<b>Fotoğraf seçin ya da buraya bırakın</b>
<span>En fazla 10 fotoğraf · JPEG, PNG, WebP, HEIC · her biri en fazla 10 MB</span>
</div>
<input id="photos" type="file" accept="image/*,.heic,.heif" multiple class="hidden">
<div class="count" id="count">0 / 10</div>
<div class="err" id="fileErr" style="display:none"></div>
<div class="thumbs" id="thumbs"></div>
<p class="hint" style="margin-top:12px">Sırt yazıları okunsun, gün ışığında çekin, flaş kullanmayın. Fotoğraflar buradan gönderilmez: formu bitirince açılan WhatsApp sohbetine eklersiniz. Burada seçmek, kaç tane ekleyeceğinizi hatırlamanız ve mesaja yazmamız içindir. Daha fazlası varsa orada ekleyebilirsiniz.</p>
<div class="row">
<label class="f">Tahmini kitap sayısı <small>(isteğe bağlı)</small><input type="number" id="sayi" min="1" inputmode="numeric"></label>
<span></span></div>
<label class="f">Kitaplar hakkında not <small>(isteğe bağlı)</small>
<textarea id="notlar" maxlength="600" placeholder="Hangi tür kitaplar, durumu, boşaltma tarihi vb."></textarea></label>
</div>

<div class="form">
<h2><span>03</span> Sizin bilgileriniz</h2>
<div class="row">
<label class="f">Ad *<input type="text" id="ad" autocomplete="given-name"><div class="err">Adınızı yazın.</div></label>
<label class="f">Soyad *<input type="text" id="soyad" autocomplete="family-name"><div class="err">Soyadınızı yazın.</div></label>
</div>
<div class="row">
<label class="f">Telefon *<input type="tel" id="tel" autocomplete="tel" inputmode="tel" placeholder="05xx xxx xx xx"><div class="err">Geçerli bir telefon yazın.</div></label>
<label class="f">E-posta <small>(isteğe bağlı)</small><input type="email" id="email" autocomplete="email"><div class="err">E-posta geçersiz görünüyor.</div></label>
</div></div>

<div class="form">
<h2><span>04</span> Kitapların bulunduğu adres</h2>
<div class="row">
<label class="f">İl *<select id="il" autocomplete="address-level1"></select></label>
<label class="f">İlçe *<input type="text" id="ilce" autocomplete="address-level2"><div class="err">İlçeyi yazın.</div></label>
</div>
<label class="f">Mahalle *<input type="text" id="mahalle"><div class="err">Mahalleyi yazın.</div></label>
<label class="f">Açık adres *<textarea id="adres" autocomplete="street-address" style="min-height:80px"></textarea><div class="err">Açık adresi yazın.</div></label>
<p class="hint">Adres, teklifi kabul ederseniz kitapları teslim almak için kullanılır. İstanbul dışındaysanız yine de yazın; nasıl yapacağımızı sizinle konuşuruz.</p>
</div>

<div class="form">
<label class="chk"><input type="checkbox" id="kvkk"><span><a href="kvkk.html" target="_blank" rel="noopener">KVKK Aydınlatma Metni</a>'ni okudum; bilgilerimin, başvurumu değerlendirmek ve benimle iletişime geçmek amacıyla Nora Kitap Evi ile WhatsApp üzerinden paylaşılmasına onay veriyorum. *</span></label>
<button class="btn submit" type="submit">Başvurumu WhatsApp'ta Gönder</button>
<p class="hint" style="margin:14px 0 0">Gönder'e basınca WhatsApp'ta hazır mesaj açılır. Mesajı göndermeden başvuru bize ulaşmaz.</p>
</div>
</form>

<div id="done" class="done" role="status" aria-live="polite">
<h2>Mesaj hazır. Son adım sizde.</h2>
<p>Başvuru kodunuz:<br><span class="code" id="doneCode"></span></p>
<ol>
<li>Açılan WhatsApp sohbetinde mesajı <b>gönderin</b>. Açılmadıysa aşağıdaki yeşil düğmeye basın.</li>
<li id="doneSome">Aynı sohbete <b id="doneN">0</b> fotoğrafı (ve varsa fazlasını) ekleyin: sohbette ataç simgesi → Galeri.</li>
<li id="doneNone" class="hidden">Aynı sohbete kitap fotoğraflarını ekleyin: ataç simgesi → Galeri.</li>
<li>Fotoğraflara bakıp size yazarız. Teklif ücretsiz, kabul zorunlu değil.</li>
</ol>
<div class="btns">
<a class="btn" id="waBtn" href="#" target="_blank" rel="noopener" style="background:#1c8c4e;border-color:#1c8c4e">WhatsApp'ı aç</a>
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

# ---------------------------------------------------------------- HİZMET SAYFALARI
def service_page(slug, title, desc, h1, lead, sections, steps, faqs, pull=None, hafiza_cta=True):
    body = ''
    for i, (h2, paras) in enumerate(sections):
        body += f'<h2>{h2}</h2>'
        for p in paras:
            if p.startswith('- '):
                pass
            body += p if p.startswith('<') else f'<p>{p}</p>'
        if pull and i == 0:
            body += f'<div class="pull">{pull}</div>'
    pg = head(title + ' · Nora Kitap Evi', desc)
    pg += header()
    pg += f'''<main>
<section class="hero sub"><div class="wrap">
<div class="crumb"><a href="index.html">Ana sayfa</a> / {e(h1)}</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="btns"><a class="btn" href="{CTA}">Fotoğraf gönder, yanıt al</a><a class="btn ghost" href="{WA_HI}">WhatsApp'tan yaz</a></div>
</div></section>
<section><div class="wrap narrow prose">{body}</div></section>
<section class="alt"><div class="wrap"><div class="head"><span class="kicker">Süreç</span><h2>Nasıl ilerliyor?</h2></div>{steps}</div></section>
<section><div class="wrap narrow"><div class="head"><span class="kicker">Sık sorulanlar</span><h2>Bu durumda en çok sorulanlar</h2></div>{faq(faqs)}</div></section>
'''
    if hafiza_cta:
        pg += f'''<section class="red"><div class="wrap narrow"><span class="kicker">Nora Hafıza</span><h2>Satmak istemiyorsanız, adınızla bırakın.</h2>
<p class="lead" style="color:#fff">Kitapları bağışlarsanız içine sahibinin adını ve istediğiniz notu yazıp raflarımıza koyarız.</p>
<div class="btns"><a class="btn" href="nora-hafiza.html">Nora Hafıza nedir?</a></div></div></section>'''
    pg += f'''<section class="alt"><div class="wrap"><div class="head"><span class="kicker">Diğer durumlar</span><h2>Başka bir şey mi var?</h2></div>{other_services(slug)}</div></section>
<section class="dark"><div class="wrap narrow"><h2>Fotoğraf göndermek yeterli.</h2><p class="lead">Gerisini konuşuruz. Teklif ücretsiz, kabul zorunlu değil.</p><div class="btns"><a class="btn" href="{CTA}">Başvuru formuna git</a><a class="btn ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div></section>
</main>
''' + footer()
    write(slug, pg)

service_page('kutuphane-alimi.html', 'Kütüphane ve toplu kitap alımı',
    'Yüzlerce kitaplık kütüphaneleri raf raf fotoğraflayın, Nora teklif versin. Ayıklamaya gerek yok. Fatih Şehremini, İstanbul.',
    'Kütüphane ve toplu kitap alımı',
    'Kitapları tek tek ayıklamanız, listelemeniz ya da fotoğraflamanız gerekmez. Rafları gösterin, kütüphaneye bütün olarak bakalım.',
    [('Ayıklamanıza gerek yok', ['Çoğu insan kitaplarını satmadan önce "değerli olanları" ayırmaya çalışır ve yorulur. Değerli olan çoğu zaman beklediğiniz kitap değildir; sıradan görünen bir baskı ya da bir seri, rafın en iyi parçası çıkabilir. Bu yüzden önceden elemeyin.', 'Bir kütüphane parçaların toplamından fazlasıdır. Aynı yazarın, aynı dönemin, aynı konunun bir arada durması da değer taşır. Bütün olarak bakınca bunu görürüz.']),
     ('Büyük kütüphanede fotoğraf nasıl çekilir?', ['<ul><li>Önce rafın tamamını, sonra sırtlar okunacak kadar yakından çekin.</li><li>Gün ışığını kullanın, flaştan kaçının.</li><li>Raf sırasıyla ilerleyin ki neyin nerede olduğunu biz de takip edelim.</li><li>Kitapların arkasındaki ikinci sıra varsa belirtin.</li><li>Eski ya da nadir görünenleri ayrıca, kapak ve künye sayfasıyla çekin.</li><li>10 fotoğrafa sığmıyorsa formdan sonra kalanını WhatsApp sohbetinde ekleyin.</li></ul>']),
     ('Teklif nasıl hazırlanıyor?', ['Otomatik fiyatlandırma kullanmıyoruz. Fotoğraflara bir insan bakar; türü, durumu, adedi ve bizim için talebi tartar. Teklifte neyi neden aldığımızı, neyi alamayacağımızı açıkça yazarız.']),
     ('Taşınma, ev küçültme, dükkân ya da ofis kapanışı', ['Bu durumlarda süre genellikle dardır. Boşaltma tarihini formdaki nota yazın, planı ona göre yaparız. Acele varsa WhatsApp\'tan da yazabilirsiniz.']),
     ('Teslim alma ve ödeme', ['Teklifi kabul ederseniz kitapların nasıl teslim alınacağını (adresten ya da dükkâna getirerek) birlikte kararlaştırırız. Kitaplar teslim alınıp fotoğraflarla karşılaştırıldıktan sonra, sizinle anlaştığımız yöntemle ödeme yapılır.'])],
    steps3(('Fotoğrafları gönderin', 'Raf raf, sırtlar okunur biçimde. Form size hazır bir mesaj verir.'), ('Teklifi alın', 'Bakıp WhatsApp ya da telefonla yazarız. Kabul zorunluluğu yok.'), ('Teslim edin', 'Kitaplar teslim alınır, kontrol edilir, ödeme yapılır.')),
    [('Önceden ayıklamam gerekir mi?', 'Hayır. Olduğu gibi gösterin. Ayıklama, işi zorlaştırır ve sizi yorar.'), ('Çok fazla fotoğraf olursa sorun olur mu?', 'Olmaz. Formdan sonra WhatsApp sohbetinde dilediğiniz kadar ekleyebilirsiniz.'), ('Fiyat düşük gelirse?', 'Reddedebilirsiniz. Almadığımız kitapları bağış olarak bırakmak da, geri almak da size kalmış.')])

service_page('tasinma-kentsel-donusum.html', 'Taşınma ve kentsel dönüşümde kitaplar',
    'Kentsel dönüşüm ya da taşınma yüzünden kitaplarınızdan ayrılmak zorundaysanız Nora satın alır ya da Hafıza ile bağış olarak devralır.',
    'Taşınma ve kentsel dönüşümde kitaplar',
    'Bina boşaltılıyor ya da yeni ev küçük. Kitaplar çoğu zaman en son düşünülen ama en çok yer kaplayan eşya olur. Birlikte çözelim.',
    [('Süre dar, kitaplar çok', ['Kentsel dönüşümde ya da taşınmada kitapların sorunu hep aynıdır: tarih bellidir, koliler yetmez, yeni evde raf yoktur. Çoğu zaman kitaplar son güne kalır ve bir yerlerde çürür.', 'Boşaltma tarihinizi başvuru formundaki nota yazın. Plan o tarihe göre yapılır.']),
     ('Satmak, bağışlamak ya da Hafıza', ['<ul><li><b>Satmak:</b> Fotoğraflara bakarız, teklif veririz. Kabul edilirse kitaplar teslim alınır, ödeme yapılır.</li><li><b>Bağışlamak:</b> Kitapları devralırız, raflarımıza koyarız.</li><li><b><a href="nora-hafiza.html">Nora Hafıza:</a></b> Bağışlıyorsunuz, kitapların içine adınızı (ve istediğiniz notu) yazıyoruz. Yaşadığınız evin, mahallenin kitapları adıyla kalır.</li></ul>']),
     ('Kolilemeden önce yazın', ['Kitapları kutulayıp bantlamadan önce bize fotoğraf gönderin. Teklif sonrası kitapları nasıl teslim alacağımızı ve neyin kolilenmesi gerektiğini birlikte netleştiririz; gereksiz iş yapmazsınız.'])],
    steps3(('Tarihi ve fotoğrafı yazın', 'Boşaltma tarihi, adres, birkaç fotoğraf. Yeter.'), ('Plan', 'Tarihe göre teslim yöntemini ve zamanını konuşuruz.'), ('Teslim', 'Kitaplar alınır; satış ise ödeme, Hafıza ise adınızla raf.')),
    [('Binamız 2 hafta içinde boşalıyor, yetişir mi?', 'Yazın. Süre kısaysa WhatsApp\'tan ya da telefonla doğrudan konuşmak en hızlısı.'), ('Hepsini sığdıramayacağım, bir kısmını bağışlayabilir miyim?', 'Evet. Bir kısmı satış, bir kısmı bağış olabilir; formda notta belirtmeniz yeter.'), ('Evde zarar görmüş (nemli, küflü) kitaplar var.', 'Fotoğrafta gösterin. Almadıklarımızı teklifte açıkça yazarız.')])

service_page('vefat-sonrasi-kutuphane.html', 'Vefat sonrası kütüphane',
    'Aileden birinin vefatından sonra kütüphanesini sahipsiz bırakmayın. Nora satın alır ya da adıyla Hafıza raflarına koyar.',
    'Vefat sonrası kütüphane',
    'Birinin kütüphanesi, onun hafızasıdır. Başvurmak için acele etmeyin ama kitaplar sahipsiz de kalmasın.',
    [('Bir kütüphane bir insandır', ['Kitaplara bakmak çoğu zaman zordur. Bazılarının kenarına not düşülmüştür, bazılarının arasında bir fotoğraf ya da mektup unutulmuştur. Bu yüzden böyle bir kütüphaneyi "eski kitaplar" diye bir kenara atmamak gerekir.', 'Biz de öyle bakarız. Sorumuz yalnızca "kaç para eder" değil, "nereye gitsin"dir.'],),
     ('Üç seçeneğiniz var', ['<ul><li><b>Satmak:</b> Fotoğraflara bakıp teklif veririz. Kabul etmek zorunda değilsiniz.</li><li><b>Bağışlamak:</b> Kitaplar bize gelir, raflarımıza konur.</li><li><b><a href="nora-hafiza.html">Nora Hafıza:</a></b> Kitapların içine kütüphane sahibinin adını yazarız. İsterseniz kısa bir not da ekleriz. Kitaplar adıyla yoluna devam eder.</li></ul>']),
     ('Kitap aralarından çıkanlar', ['Kitapların arasından kişisel kâğıtlar çıkabilir: mektup, fotoğraf, not, ayraç. Bunları görürsek ayırır, size veririz. Önceden bakmak isterseniz de buna zaman tanırız.']),
     ('Aile ortak karar verir', ['Böyle bir kütüphane genellikle birden fazla kişiyi ilgilendirir. Başvuruyu bir kişi yapabilir, ama teslimden önce ailenin hemfikir olması iyi olur. Acelemiz yok; hazır olduğunuzda yazın.'])],
    steps3(('Fotoğraf ve birkaç cümle', 'Kütüphaneyi gösterin, kimin olduğunu isterseniz yazın.'), ('Konuşma', 'Satış mı, bağış mı, Hafıza mı; yöntemi birlikte seçeriz.'), ('Teslim', 'Kitaplar alınır. Aralarından çıkan kişisel kâğıtlar size verilir.')),
    [('Kitaplardan bazılarını ailede tutmak istiyoruz.', 'Elbette. Önce istediklerinizi ayırın, kalanı bize gösterin. Kısmi başvuru sorun değil.'), ('Hafıza için ne yazıyorsunuz?', 'Kitabın içine kütüphane sahibinin adını, isterseniz sizin belirlediğiniz kısa bir notu yazarız. Not isteğe bağlıdır.'), ('Hafıza bağışında kitaplara ne oluyor?', 'Kitaplar raflarımıza konur ve okurlarla buluşur. Dükkâna gelip bakabilirsiniz.')],
    pull='"Kitaplar yalnızca kâğıt değil; bir insanın merakının, yarım bıraktığı sayfaların kaydıdır."')

service_page('eski-nadir-kitap.html', 'Eski, nadir ve eski harfli kitap',
    'İlk baskı, imzalı, numaralı, eski harfli (Osmanlıca) ve eski basım kitapları Nora değerlendirir. Fotoğraf gönderin, teklif alın.',
    'Eski, nadir ve eski harfli kitap',
    'İlk baskılar, imzalı nüshalar, numaralı baskılar, Osmanlıca ve eski harfli basımlar. Nadir kitabın değeri çoğu zaman ayrıntıda gizlidir.',
    [('Ne tür kitaplara bakıyoruz?', ['<ul><li>İlk baskılar, imzalı ya da ithaflı nüshalar</li><li>Numaralı, sınırlı sayıda basılmış kitaplar</li><li>Eski harfli (Osmanlıca) basımlar, matbu ve el yazması</li><li>Eski ve yıpranmış ama içeriği önemli basımlar</li><li>Dönemin yayınevlerinin eski serileri</li></ul>']),
     ('Ayrıntı fotoğrafları işe yarar', ['Nadir kitapta kapak yetmez. Kapak, iç kapak (başlık sayfası), künye (basım yılı, baskı sayısı, matbaa) ve varsa imza ya da mühür sayfasını ayrı ayrı çekin. Hasarı da gösterin; yırtık, leke, koparılmış sayfa değeri etkiler ve bunu baştan bilmek herkesin işini kolaylaştırır.']),
     ('Dürüst değerlendirme', ['Her eski kitap nadir değildir, her nadir kitap da pahalı değildir. Bunu fotoğraflara bakarak açıkça söyleriz. Değerli çıkarsa ona göre teklif veririz; değeri düşükse bunu da saklamayız.']),
     ('Eski harfli kitaplar', ['Osmanlıca ve eski harfli basımlarda içeriğin okunması da önemlidir. Başlık sayfasını ve birkaç iç sayfayı çekin; ayrıca kitabı kimden aldığınızı ya da ailede nasıl bulunduğunu da yazarsanız (biliyorsanız) işimizi kolaylaştırır.'])],
    steps3(('Ayrıntıyı çekin', 'Kapak, iç kapak, künye ve hasarlı yerler.'), ('Değerlendirme', 'Baktıktan sonra durumu ve teklifi açıkça yazarız.'), ('Teslim', 'Kitap elden ya da güvenli bir yolla teslim alınır, kontrol edilir, ödeme yapılır.')),
    [('Kitabımın değerini bilmiyorum, ne yapmalıyım?', 'Fotoğraf gönderin. Değerli çıkmasa bile bunu açıkça söyleriz.'), ('Birkaç kitap için de başvurabilir miyim?', 'Evet, adedin alt sınırı yok.'), ('Nadir kitabı kargoyla göndermek zorunda mıyım?', 'Hayır. Önce fotoğraflara bakarız, sonra nasıl teslim edileceğini birlikte seçeriz.')])

service_page('ansiklopedi-dergi.html', 'Ansiklopedi, dergi ve seriler',
    'Ansiklopedi setleri, dergi koleksiyonları ve cilt cilt serileri Nora değerlendirir. Eksik ciltler de sorun değil. Fotoğraf gönderin.',
    'Ansiklopedi, dergi ve seriler',
    'Takım halindeki setler, dergi koleksiyonları ve cilt cilt seriler. Eksik cilt de olabilir, yine de yazın.',
    [('Neleri alıyoruz?', ['<ul><li>Ansiklopediler ve sözlük setleri</li><li>Dergi koleksiyonları (yıllık ciltler, tek sayılar)</li><li>Cilt cilt biriken seri kitaplar</li><li>Dönemsel yayınlar ve eski gazete kolajları</li></ul>']),
     ('Takım olarak ya da tek tek', ['Setin eksiksiz olması değerini ciddi biçimde artırır. Eksik cilt varsa söyleyin; bu durumda da değerlendirme yaparız. Dergilerde sayıları ve yılları okunur çekmeniz yeter.']),
     ('Fotoğraf nasıl çekilir?', ['<ul><li>Seti bütün olarak, sırtlar okunur biçimde çekin.</li><li>Dergilerde sayı ve yılın görüldüğü kapakları gösterin.</li><li>Ciltlerde hasar varsa (kopuk cilt, leke, nem) ayrıca çekin.</li><li>Kaç cilt/sayı olduğunu mesaja yazın.</li></ul>']),
     ('Ağır ve hacimli', ['Ansiklopedi setleri çok ağırdır. Bu yüzden teslimi önceden konuşmak gerekir. Teklif sonrası yöntemi birlikte kararlaştırırız.'])],
    steps3(('Seti gösterin', 'Bütün set ve sırtlar, eksik varsa belirtin.'), ('Teklif', 'Fotoğraflara bakıp yazarız.'), ('Teslim', 'Ağırlık nedeniyle yöntemi birlikte seçeriz, kontrolden sonra ödeme.')),
    [('Setim eksik, yine de alır mısınız?', 'Bazen. Fotoğraflara bakarız, almıyorsak bunu açıkça yazarız.'), ('Dergileri tek sayı olarak da alır mısınız?', 'Evet, değeri taşıyorsa. Sayıları ve yılları yazarsanız hızlanırız.'), ('Çok ağır, nasıl getiririm?', 'Getirmenize gerek olmayabilir. Teslim şeklini teklifte konuşuruz.')])

# ---------------------------------------------------------------- NORA HAFIZA
hf = head('Nora Hafıza · Kitaplar adınızla kalır', 'Kentsel dönüşüm, taşınma ya da vefat nedeniyle ayrıldığınız kitapları Nora\'ya bağışlayın; içine adınızı ve notunuzu yazıp raflarımıza koyalım.')
hf += header()
hf += f'''<main>
<section class="hero"><div class="wrap">
<span class="kicker" style="color:#e0584f">Nora Hafıza</span>
<h1>Kitaplar <em>hafızasını</em> yitirmeden yoluna devam etsin.</h1>
<p class="lead">Kentsel dönüşüm, taşınma ya da bir yakınınızın vefatı yüzünden kitaplarınızdan ayrılmak zorundaysanız: kitapları bize bağışlayın. İçine sahibinin adını, isterseniz bir not yazarız. Sonra raflarımıza koyarız. Okurlarla ve öğrencilerle buluşmaya devam ederler.</p>
<div class="btns"><a class="btn" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a><a class="btn ghost" href="{WA_HI}">Önce soru soracağım</a></div>
</div></section>

<section><div class="wrap narrow prose">
<h2>Neden böyle bir şey?</h2>
<p>Bir evden çıkarken kitaplar en çok zorlanılan eşyadır. Taşıyamazsınız, sığdıramazsınız, çöpe de atamazsınız. Yeni yere gidince de çoğu kitap yalnızca "bir yerlere gitmiş" olur.</p>
<p>Hafıza bu boşluk için. Kitabın bir geçmişi vardır: kimin okuduğu, kimin kütüphanesinden geldiği. Biz bunu silmek yerine kitabın içine yazıyoruz.</p>

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
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
<div class="step"><h3>Başvurun</h3><p>Formda "Nora Hafıza" seçeneğini işaretleyin. Kitapların içine yazılacak adı ve isterseniz notu yazın. Fotoğrafları ekleyin.</p></div>
<div class="step"><h3>Teslim</h3><p>Kitapların nasıl teslim edileceğini birlikte seçeriz: adresten alım ya da dükkâna getirme.</p></div>
<div class="step"><h3>Adı yazarız</h3><p>Her kitabın içine sahibinin adını, istediğiniz notu yazarız. Aralarından çıkan kişisel kâğıtları size veririz.</p></div>
<div class="step"><h3>Raflara</h3><p>Kitaplar raflarımıza konur. Okurlarla ve öğrencilerle buluşmaya devam eder.</p></div>
</div></div></section>

<section><div class="wrap narrow prose">
<h2>Ne yazıyoruz?</h2>
<p>Siz belirlersiniz. Kısa ve sade olur:</p>
<div class="pull">"Ahmet Yılmaz'ın kitaplığından."</div>
<p>İsterseniz yanına birkaç cümle ekleriz. Örneğin kitabı kimin, hangi yıllarda okuduğunu ya da yeni okura bir dilek. Not isteğe bağlıdır; yalnızca ad da yeterlidir.</p>

<h2>Satış değil, bağış</h2>
<p>Hafıza bir bağış biçimidir. Kitapları satın almıyoruz, bir bedel ödemiyoruz. Para almak isterseniz normal <a href="{CTA}?tur=sat">satış başvurusu</a> yapabilirsiniz; kitaplar adınızla yazılmaz.</p>

<h2>Yalnızca kitap</h2>
<p>Kitapları alıyoruz; dergi ve ansiklopedi dahil. Kitap dışındaki eşyaları (mobilya, koleksiyon objeleri, plak vb.) alamıyoruz.</p>
</div></section>

<section class="alt"><div class="wrap narrow">
<div class="head"><span class="kicker">Sık sorulanlar</span><h2>Hafıza hakkında</h2></div>
''' + faq([
    ('Her kitabı raflara koyuyor musunuz?', 'Çoğunu. Çok yıpranmış, kullanılamayacak durumdakileri ayırırız; bunu size de söyleriz.'),
    ('Kitapların içine yazı yazmanız kitaba zarar vermez mi?', 'Zarar vermeyecek biçimde, kısa ve okunaklı yazarız. İsterseniz önce nasıl yazılacağını sorabilirsiniz.'),
    ('Bağış sonrası kitaplara ne olduğunu görebilir miyim?', 'Evet. Dükkânımıza gelip raflara bakabilirsiniz.'),
    ('Kaç kitap getirebilirim?', 'Adedin alt ve üst sınırı yok. Çok sayıda ise önce fotoğraf gönderin; teslim yöntemini konuşuruz.'),
]) + f'''
</div></section>

<section class="red"><div class="wrap narrow"><h2>Kitaplarınız adınızla kalsın.</h2>
<p class="lead" style="color:#fff">Başvuru ücretsiz. Fotoğraf yeter.</p>
<div class="btns"><a class="btn" href="{CTA}?tur=hafiza">Hafıza bağışı yap</a><a class="btn ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_TXT}</a></div></div></section>
</main>
''' + footer()
write('nora-hafiza.html', hf)

# ---------------------------------------------------------------- KVKK
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
<li><b>Adres bilgileri:</b> Teklifi kabul ederseniz kitapları teslim almak için.</li>
<li><b>Kitap fotoğrafları ve notlar:</b> Teklifi hazırlamak için.</li>
<li><b>Hafıza bilgileri (ad, neden, not):</b> Kitapların içine yazılacak bilgileri belirlemek için.</li>
</ul>

<h2>Hukuki sebep</h2>
<p>Verileriniz, başvurunuzu değerlendirmek ve sözleşme (satış ya da bağış) kurmak amacıyla, açık rızanıza dayanılarak işlenir.</p>

<h2>Aktarım</h2>
<p>Verileriniz üçüncü kişilerle paylaşılmaz. Mesajı WhatsApp üzerinden ilettiğiniz için WhatsApp'ın kendi gizlilik koşulları geçerlidir.</p>

<h2>Saklama</h2>
<p>Başvuru süreci bittikten sonra, siz talep ettiğinizde, ilettiğiniz bilgiler silinir. Satış ya da bağış gerçekleşmişse, yasal olarak tutulması gereken kayıtlar mevzuatta öngörülen süre kadar saklanır.</p>

<h2>Haklarınız</h2>
<p>KVKK madde 11 uyarınca verilerinizin işlenip işlenmediğini öğrenme, düzeltilmesini, silinmesini ya da işlenmesine itiraz etmeyi isteme haklarına sahipsiniz. Talebinizi <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a> numarasından ya da WhatsApp üzerinden bize iletebilirsiniz.</p>
</div></section>
</main>
''' + footer()
write('kvkk.html', kv)

# ---------------------------------------------------------------- 404 + dosyalar
nf = head('Sayfa bulunamadı · Nora Kitap Evi', 'Aradığınız sayfa bulunamadı.')
nf += header()
nf += f'''<main><section class="hero sub"><div class="wrap"><h1>Bu sayfa kayıp.</h1><p class="lead">Kitaplar gibi, bazen sayfalar da raftan düşer.</p><div class="btns"><a class="btn" href="index.html">Ana sayfaya dön</a></div></div></section></main>
''' + footer()
write('404.html', nf)

for fn in ['style.css', 'main.js', 'form.js']:
    shutil.copy(os.path.join(SRC, fn), os.path.join(OUT, fn))
write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#0d0d0d"/><text x="32" y="44" font-family="Georgia,serif" font-size="38" font-weight="700" text-anchor="middle" fill="#f2ece0">N</text><circle cx="49" cy="44" r="5" fill="#b3201f"/></svg>')
write('.nojekyll', '')
print(sorted(os.listdir(OUT)))
