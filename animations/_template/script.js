// Шаблон интерактивной анимации на canvas. Замените draw() своей отрисовкой.
(function () {
  var canvas = document.getElementById('stage');
  var ctx = canvas.getContext('2d');
  var param = document.getElementById('param');
  var paramValue = document.getElementById('param-value');

  function color(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function draw(time) {
    var w = canvas.width;
    var h = canvas.height;
    var value = Number(param.value);
    paramValue.textContent = value;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = color('--accent');
    var x = w / 2 + Math.cos(time / 1000) * value * 20;
    ctx.beginPath();
    ctx.arc(x, h / 2, 12, 0, Math.PI * 2);
    ctx.fill();

    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
})();
