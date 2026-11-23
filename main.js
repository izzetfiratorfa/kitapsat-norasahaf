(function(){
  var b=document.querySelector('.burger'),n=document.querySelector('.nav');
  if(b&&n){
    b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
    n.addEventListener('click',function(e){if(e.target.tagName==='A')n.classList.remove('open')});
  }
  var g=document.querySelector('.grp');
  if(g){
    var gb=g.querySelector('.gbtn');
    gb.addEventListener('click',function(e){e.stopPropagation();var o=g.classList.toggle('open');gb.setAttribute('aria-expanded',o)});
    document.addEventListener('click',function(e){if(!g.contains(e.target)){g.classList.remove('open');gb.setAttribute('aria-expanded','false')}});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'){g.classList.remove('open');gb.setAttribute('aria-expanded','false')}});
  }
  function openHash(){var h=location.hash&&document.querySelector(location.hash);if(h&&h.tagName==='DETAILS'){h.open=true;h.scrollIntoView()}}
  window.addEventListener('hashchange',openHash);openHash();
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(a){setTimeout(openHash,0)}});
})();
