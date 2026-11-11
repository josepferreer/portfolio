// Visor: al pulsar una pieza se abre en grande. Flechas para pasar, Esc o clic fuera para cerrar.
(() => {
  const visor = document.querySelector('.visor');
  if (!visor) return;
  const img = visor.querySelector('img');
  let grupo = [], actual = 0;

  function mostrar(i) {
    actual = (i + grupo.length) % grupo.length;
    const f = grupo[actual], o = f.querySelector('img');
    img.src = o.src;
    img.alt = o.alt;
    visor.querySelector('.nombre-pieza').textContent = f.querySelector('figcaption')?.textContent || '';
    visor.querySelector('.cuenta').textContent = grupo.length > 1 ? (actual + 1) + ' / ' + grupo.length : '';
    visor.classList.toggle('uno', grupo.length < 2);
  }

  document.querySelectorAll('.piezas, .secciones, .archivo').forEach(g => {
    const figs = [...g.querySelectorAll('figure')];
    figs.forEach((f, i) => f.querySelector('img').addEventListener('click', () => {
      grupo = figs;
      mostrar(i);
      visor.showModal();
    }));
  });

  visor.querySelector('.cerrar').addEventListener('click', () => visor.close());
  visor.querySelector('.ant').addEventListener('click', () => mostrar(actual - 1));
  visor.querySelector('.sig').addEventListener('click', () => mostrar(actual + 1));
  visor.addEventListener('click', e => {
    if (e.target === visor || e.target.tagName === 'FIGURE') visor.close();
  });
  document.addEventListener('keydown', e => {
    if (!visor.open) return;
    if (e.key === 'ArrowLeft') mostrar(actual - 1);
    if (e.key === 'ArrowRight') mostrar(actual + 1);
  });
})();
