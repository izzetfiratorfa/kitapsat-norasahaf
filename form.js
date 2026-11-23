(function(){
  var CFG = window.NORA_CONFIG;
  var MAX_FILES = 10, MAX_MB = 10;
  var OK_EXT = /\.(jpe?g|png|webp|heic|heif)$/i;
  var files = [];

  var $ = function(s){return document.querySelector(s)};
  var form = $('#appForm'), drop = $('#drop'), input = $('#photos'), thumbs = $('#thumbs'), count = $('#count'), fileErr = $('#fileErr');

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

  /* ---- fotoğraflar ---- */
  function addFiles(list){
    var msgs=[];
    Array.prototype.forEach.call(list,function(f){
      var okType=/^image\//.test(f.type)||OK_EXT.test(f.name);
      if(!okType){msgs.push(f.name+': fotoğraf değil');return}
      if(f.size>MAX_MB*1024*1024){msgs.push(f.name+': '+MAX_MB+' MB üstü');return}
      if(files.length>=MAX_FILES){msgs.push('En fazla '+MAX_FILES+' fotoğraf');return}
      if(files.some(function(x){return x.name===f.name&&x.size===f.size}))return;
      files.push(f);
    });
    fileErr.textContent=msgs.filter(function(v,i,a){return a.indexOf(v)===i}).join(' · ');
    fileErr.style.display=msgs.length?'block':'none';
    render();
  }
  function render(){
    thumbs.innerHTML='';
    files.forEach(function(f,i){
      var d=document.createElement('div');d.className='th';
      if(/^image\/(jpe?g|png|webp)/.test(f.type)){var im=document.createElement('img');im.alt='';im.src=URL.createObjectURL(f);im.onload=function(){URL.revokeObjectURL(im.src)};d.appendChild(im)}
      else d.appendChild(document.createTextNode(f.name));
      var x=document.createElement('button');x.type='button';x.textContent='×';x.setAttribute('aria-label','Fotoğrafı kaldır');
      x.onclick=function(){files.splice(i,1);render()};
      d.appendChild(x);thumbs.appendChild(d);
    });
    count.textContent=files.length+' / '+MAX_FILES;
  }
  input.addEventListener('change',function(){addFiles(input.files);input.value=''});
  drop.addEventListener('click',function(){input.click()});
  drop.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();input.click()}});
  ['dragenter','dragover'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add('over')})});
  ['dragleave','drop'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.remove('over')})});
  drop.addEventListener('drop',function(e){addFiles(e.dataTransfer.files)});
  render();

  /* ---- doğrulama ---- */
  function val(id){return (document.getElementById(id).value||'').trim()}
  function mark(id,bad){var el=document.getElementById(id).closest('.f');if(el)el.classList.toggle('bad',bad);return bad}
  function validate(){
    var bad=[];
    ['ad','soyad','ilce','mahalle','adres'].forEach(function(id){if(mark(id,!val(id)))bad.push(id)});
    var digits=val('tel').replace(/\D/g,'');
    if(mark('tel',digits.length<10||digits.length>13))bad.push('tel');
    var em=val('email');
    if(mark('email',em&&!/^\S+@\S+\.\S+$/.test(em)))bad.push('email');
    if(mode()==='hafiza'&&mark('hafizaAd',!val('hafizaAd')))bad.push('hafizaAd');
    var k=$('#kvkk').closest('.chk');var kb=!$('#kvkk').checked;k.style.color=kb?'#b3201f':'';if(kb)bad.push('kvkk');
    return bad;
  }

  /* ---- mesaj ---- */
  var TUR={sat:'SATMAK istiyor',bagis:'BAĞIŞLAMAK istiyor',hafiza:'NORA HAFIZA olarak BAĞIŞLAMAK istiyor'};
  var NEDEN={tasinma:'Taşınma',kentsel:'Kentsel dönüşüm',vefat:'Aileden birinin vefatı',diger:'Diğer'};
  function code(){
    var d=new Date(),p=function(n){return String(n).padStart(2,'0')};
    var r='';var a='ABCDEFGHJKLMNPRSTUVYZ23456789';for(var i=0;i<4;i++)r+=a[Math.floor(Math.random()*a.length)];
    return 'NORA-'+String(d.getFullYear()).slice(2)+p(d.getMonth()+1)+p(d.getDate())+'-'+r;
  }
  function message(c){
    var L=[];
    L.push('*Nora Kitap Evi · Kitap Başvurusu*');
    L.push('Başvuru no: '+c);
    L.push('');
    L.push('Merhaba, kitaplarımı '+(mode()==='sat'?'satmak':mode()==='bagis'?'bağışlamak':'Nora Hafıza kapsamında bağışlamak')+' istiyorum.');
    L.push('');
    L.push('Ad Soyad: '+val('ad')+' '+val('soyad'));
    L.push('Telefon: '+val('tel'));
    if(val('email'))L.push('E-posta: '+val('email'));
    L.push('Adres: '+val('adres')+', '+val('mahalle')+' Mah., '+val('ilce')+' / '+val('il'));
    if(val('sayi'))L.push('Tahmini kitap sayısı: '+val('sayi'));
    if(val('notlar'))L.push('Kitaplar hakkında: '+val('notlar'));
    if(mode()==='hafiza'){
      L.push('');
      L.push('*Hafıza bilgileri*');
      L.push('Kitapların içine yazılacak ad: '+val('hafizaAd'));
      var n=val('hafizaNeden');if(n)L.push('Neden: '+NEDEN[n]);
      if(val('hafizaNot'))L.push('Eklenecek not: '+val('hafizaNot'));
    }
    L.push('');
    L.push('Fotoğraf: '+files.length+' adet (bu sohbete ekliyorum)');
    return L.join('\n');
  }

  /* ---- gönder ---- */
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=validate();
    if(bad.length){var f=document.getElementById(bad[0])||$('#kvkk');f.scrollIntoView({behavior:'smooth',block:'center'});try{f.focus({preventScroll:true})}catch(_){}return}
    var c=code(),msg=message(c);
    var wa='https://wa.me/'+CFG.phone+'?text='+encodeURIComponent(msg);
    $('#doneCode').textContent=c;
    $('#doneN').textContent=files.length;
    $('#doneNone').classList.toggle('hidden',files.length>0);
    $('#doneSome').classList.toggle('hidden',files.length===0);
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
