(function(){
  var f=document.getElementById('calcForm');
  if(!f)return;
  var T=[{n:'Grupo 1 · Flexible',hora:6500,modulo:24000},{n:'Grupo 2 · Frecuente',hora:6000,modulo:22000},{n:'Grupo 3 · Estable',hora:5500,modulo:20000}];
  var $=function(id){return document.getElementById(id)};
  var money=function(n){return '$ '+Math.round(n).toLocaleString('es-AR')};
  var clamp=function(v,a,b){return Math.min(b,Math.max(a,v))};
  function calc(){
    var d=clamp(Math.round(Number($('dias').value)||1),1,5);
    var h=clamp(Math.round((Number($('horas').value)||0.5)*2)/2,0.5,13);
    var H=d*h*4;
    var g=H>30?T[2]:(H>=15?T[1]:T[0]);
    var mods=Math.floor(h/4+1e-9),su=h-mods*4;
    var porDia=mods*g.modulo+Math.min(su*g.hora,g.modulo);
    var total=porDia*d*4;
    $('rGrp').textContent=g.n;
    $('rTotal').textContent=money(total);
    $('rHs').textContent=H.toLocaleString('es-AR',{maximumFractionDigits:1})+' h';
    $('rDia').textContent=money(porDia);
    $('rHora').textContent=money(total/H);
  }
  f.querySelectorAll('.stepper button').forEach(function(b){
    b.addEventListener('click',function(){
      var i=$(b.getAttribute('data-t'));
      i.value=clamp((Number(i.value)||0)+Number(b.getAttribute('data-d')),Number(i.min),Number(i.max));
      calc();
    });
  });
  $('dias').addEventListener('input',calc);
  $('horas').addEventListener('input',calc);
  f.addEventListener('submit',function(e){e.preventDefault()});
  calc();
})();
