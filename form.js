(function(){
  var CFG = window.NORA_CONFIG;
  var $ = function(s){return document.querySelector(s)};
  var form = $('#appForm');

  /* ---- il listesi ---- */
  var iller = ['Adana','Adıyaman','Afyonkarahisar','Ağrı','Aksaray','Amasya','Ankara','Antalya','Ardahan','Artvin','Aydın','Balıkesir','Bartın','Batman','Bayburt','Bilecik','Bingöl','Bitlis','Bolu','Burdur','Bursa','Çanakkale','Çankırı','Çorum','Denizli','Diyarbakır','Düzce','Edirne','Elazığ','Erzincan','Erzurum','Eskişehir','Gaziantep','Giresun','Gümüşhane','Hakkâri','Hatay','Iğdır','Isparta','İstanbul','İzmir','Kahramanmaraş','Karabük','Karaman','Kars','Kastamonu','Kayseri','Kilis','Kırıkkale','Kırklareli','Kırşehir','Kocaeli','Konya','Kütahya','Malatya','Manisa','Mardin','Mersin','Muğla','Muş','Nevşehir','Niğde','Ordu','Osmaniye','Rize','Sakarya','Samsun','Şanlıurfa','Siirt','Sinop','Sivas','Şırnak','Tekirdağ','Tokat','Trabzon','Tunceli','Uşak','Van','Yalova','Yozgat','Zonguldak'];
  var sel = $('#il');
  iller.forEach(function(il){var o=document.createElement('option');o.value=il;o.textContent=il;if(il==='İstanbul')o.selected=true;sel.appendChild(o)});

  /* ---- başvuru türü ---- */
  var hafiza = $('#hafizaBox');
  function mode(){return (form.querySelector('input[name=tur]:checked')||{}).value}
  function syncMode(){hafiza.classList.toggle('hidden', mode()!=='hafiza')}
  form.querySelectorAll('input[name=tur]').forEach(function(r){r.addEventListener('change',syncMode)});
  var pre = new URLSearchParams(location.search).get('tur');
  if(pre){var r=form.querySelector('input[name=tur][value='+pre+']');if(r)r.checked=true}
  syncMode();

  /* ---- doğrulama ---- */
  function val(id){return (document.getElementById(id).value||'').trim()}
  function mark(id,bad){var el=document.getElementById(id).closest('.f');if(el)el.classList.toggle('bad',bad);return bad}
  var LABEL={hafizaAd:'Kitapların içine yazılacak ad',ad:'Ad',soyad:'Soyad',tel:'Telefon',email:'E-posta (geçersiz)',ilce:'İlçe',kvkk:'KVKK onayı'};
  function validate(){
    var bad=[];
    ['ad','soyad','ilce'].forEach(function(id){if(mark(id,!val(id)))bad.push(id)});
    var digits=val('tel').replace(/\D/g,'');
    if(mark('tel',digits.length<10||digits.length>13))bad.push('tel');
    var em=val('email');
    if(mark('email',em&&!/^\S+@\S+\.\S+$/.test(em)))bad.push('email');
    if(mode()==='hafiza'&&mark('hafizaAd',!val('hafizaAd')))bad.push('hafizaAd');
    var k=$('#kvkk').closest('.chk');var kb=!$('#kvkk').checked;k.style.color=kb?'#b3201f':'';if(kb)bad.push('kvkk');
    // ekranda yukarıdan aşağıya sırala
    var order=['hafizaAd','ad','soyad','tel','email','ilce','kvkk'];
    bad.sort(function(a,b){return order.indexOf(a)-order.indexOf(b)});
    return bad;
  }
  function summary(bad){
    var box=$('#errSum');
    if(!bad.length){box.classList.remove('show');box.innerHTML='';return}
    box.innerHTML='Başvuru gönderilemedi. Şu alanları doldurmanız gerekiyor:<ul>'+bad.map(function(id){return '<li>'+LABEL[id]+'</li>'}).join('')+'</ul>';
    box.classList.add('show');
  }

  /* ---- mesaj ---- */
  var NEDEN={tasinma:'Taşınma',kentsel:'Kentsel dönüşüm',vefat:'Aileden birinin vefatı',diger:'Diğer'};
  function code(){
    var d=new Date(),p=function(n){return String(n).padStart(2,'0')};
    var n=String(Math.floor(Math.random()*900)+100);
    return 'NORA-'+String(d.getFullYear()).slice(2)+p(d.getMonth()+1)+p(d.getDate())+'-'+n;
  }
  function message(c){
    var t=mode(),L=[];
    L.push('*Nora Kitap Evi · Kitap Başvurusu*');
    L.push('Başvuru no: '+c);
    L.push('');
    L.push('Merhaba, kitaplarımı '+(t==='sat'?'satmak':t==='bagis'?'karşılıksız bağışlamak':'Nora Hafıza kapsamında bağışlamak')+' istiyorum.');
    L.push('');
    L.push('Ad Soyad: '+val('ad')+' '+val('soyad'));
    L.push('Telefon: '+val('tel'));
    if(val('email'))L.push('E-posta: '+val('email'));
    L.push('Konum: '+val('ilce')+' / '+val('il'));
    if(val('sayi'))L.push('Tahmini kitap sayısı: '+val('sayi'));
    if(val('notlar'))L.push('Kitaplar hakkında: '+val('notlar'));
    if(t==='hafiza'){
      L.push('');
      L.push('*Hafıza bilgileri*');
      L.push('Kitapların içine yazılacak ad: '+val('hafizaAd'));
      var n=val('hafizaNeden');if(n)L.push('Neden: '+NEDEN[n]);
      if(val('hafizaNot'))L.push('Eklenecek not: '+val('hafizaNot'));
    }
    L.push('');
    L.push('Kitap fotoğraflarını bu sohbete ekliyorum.');
    return L.join('\n');
  }

  /* ---- gönder ---- */
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=validate();
    summary(bad);
    if(bad.length){$('#errSum').scrollIntoView({behavior:'smooth',block:'center'});return}
    var c=code(),msg=message(c);
    var wa='https://wa.me/'+CFG.phone+'?text='+encodeURIComponent(msg);
    $('#doneCode').textContent=c;
    $('#waBtn').href=wa;
    var mail=$('#mailBtn');
    if(CFG.email){mail.href='mailto:'+CFG.email+'?subject='+encodeURIComponent('Kitap başvurusu '+c)+'&body='+encodeURIComponent(msg.replace(/\*/g,''));mail.classList.remove('hidden')}
    $('#copyBtn').onclick=function(){
      var t=msg.replace(/\*/g,'');
      (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){$('#copyBtn').textContent='Kopyalandı ✓'}).catch(function(){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');$('#copyBtn').textContent='Kopyalandı ✓'}catch(_){}document.body.removeChild(ta)});
    };
    form.classList.add('hidden');
    $('#done').classList.add('show');
    $('#done').scrollIntoView({behavior:'smooth',block:'start'});
    window.open(wa,'_blank','noopener');
  });
  $('#backBtn').onclick=function(){$('#done').classList.remove('show');form.classList.remove('hidden');window.scrollTo({top:0,behavior:'smooth'})};
})();
