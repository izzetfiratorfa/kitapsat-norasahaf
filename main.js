(function(){
  var b=document.querySelector('.burger'),n=document.querySelector('.nav');
  if(b&&n){
    b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
    n.addEventListener('click',function(e){if(e.target.tagName==='A')n.classList.remove('open')});
  }
})();
