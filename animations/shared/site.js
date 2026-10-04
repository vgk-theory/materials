// Общая шапка и подвал сайта. Подключается на каждой странице:
//   <script src="<путь до>/animations/shared/site.js"></script>
// Корень сайта вычисляется от адреса самого скрипта, поэтому ссылки верны на любой глубине.
(function () {
  var root = new URL('../../', document.currentScript.src);
  var REPO = 'https://github.com/vgk-theory/materials';
  var NAV = [
    ['Анимации', 'animations/index.html'],
    ['Презентации', 'view.html?file=presentations/README.md'],
    ['Монография', 'view.html?file=sources/monograph/README.md'],
    ['Об авторе', 'view.html?file=author.md'],
    ['Как участвовать', 'view.html?file=CONTRIBUTING.md']
  ];
  var FOOTER = [
    ['Репозиторий на GitHub', REPO]
  ];
  // Адрес репозитория нужен просмотрщику: рабочие файлы он открывает на GitHub.
  window.siteRepo = REPO;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function link(item) {
    var a = el('a', null, item[0]);
    a.href = new URL(item[1], root).href;
    return a;
  }

  function isCurrent(a) {
    var target = new URL(a.href);
    if (target.pathname !== location.pathname) {
      // Любая страница внутри animations/ относится к разделу «Анимации».
      var folder = target.pathname.replace(/index\.html$/, '');
      return /\/animations\/$/.test(folder) && location.pathname.indexOf(folder) === 0;
    }
    return target.search === location.search;
  }

  var header = el('header', 'site-header');
  var bar = el('div', 'site-bar');
  var brand = link(['Теория В. Г. Катющика', 'index.html']);
  brand.className = 'site-brand';
  bar.appendChild(brand);
  var nav = el('nav', 'site-nav');
  nav.setAttribute('aria-label', 'Разделы сайта');
  NAV.forEach(function (item) {
    var a = link(item);
    if (isCurrent(a)) a.setAttribute('aria-current', 'page');
    nav.appendChild(a);
  });
  bar.appendChild(nav);
  header.appendChild(bar);
  document.body.insertBefore(header, document.body.firstChild);

  var footer = el('footer', 'site-footer');
  var inner = el('div', 'site-bar');
  FOOTER.forEach(function (item) { inner.appendChild(link(item)); });
  footer.appendChild(inner);
  document.body.appendChild(footer);
})();
