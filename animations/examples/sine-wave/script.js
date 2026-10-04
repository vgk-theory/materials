// Демонстрационный пример: бегущая синусоида на canvas. Не относится к теории.
(function () {
  var canvas = document.getElementById('stage');
  var ctx = canvas.getContext('2d');
  var inputs = {
    amplitude: document.getElementById('amplitude'),
    periods: document.getElementById('periods'),
    speed: document.getElementById('speed')
  };
  var phase = 0;
  var last = null;

  function color(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function draw(time) {
    var w = canvas.width;
    var h = canvas.height;
    var amplitude = Number(inputs.amplitude.value);
    var periods = Number(inputs.periods.value);
    var speed = Number(inputs.speed.value);

    Object.keys(inputs).forEach(function (key) {
      document.getElementById(key + '-value').textContent = inputs[key].value;
    });

    if (last !== null) phase += (time - last) / 1000 * speed * Math.PI;
    last = time;

    ctx.clearRect(0, 0, w, h);

    // Ось
    ctx.strokeStyle = color('--border');
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();

    // Синусоида
    ctx.strokeStyle = color('--accent');
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (var x = 0; x <= w; x++) {
      var y = h / 2 - amplitude * Math.sin(x / w * periods * 2 * Math.PI - phase);
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
})();
