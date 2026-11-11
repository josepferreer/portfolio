// Movimiento: las cosas aparecen al entrar en pantalla (al bajar por la página).
// Solo funciona si <html> tiene la clase «mov», que se pone en el <head> cuando el sistema
// NO pide reducir el movimiento. Sin JavaScript todo se ve normal, sin animar.
(() => {
  if (!document.documentElement.classList.contains('mov')) return;

  // qué aparece al bajar (el título grande del proyecto y los nombres de las tarjetas no:
  // son los que viajan de una página a otra)
  const QUE = [
    '.cab', '.tarjeta .cubierta', '.tarjeta .etiquetas',
    '.p-ficha dl > div', '.p-ficha .texto p', '.p-cab .lema',
    '.logos figure', '.sub', '.piezas figure', '.secciones figure',
    '.ir-web', '.p-pantallas', '.p-siguiente',
    '.archivo figure', '.sobre .texto p', '.cv', '.hablemos', '.contacto .pie'
  ].join(',');

  const elementos = [...document.querySelectorAll(QUE)];
  // en una rejilla, cada uno sale un poco después que el anterior
  const porPadre = new Map();
  for (const el of elementos) {
    const n = porPadre.get(el.parentElement) || 0;
    porPadre.set(el.parentElement, n + 1);
    el.style.setProperty('--d', Math.min(n, 6) * 70 + 'ms');
    el.classList.add('rv');
  }

  const io = new IntersectionObserver(entradas => {
    for (const e of entradas) {
      if (!e.isIntersecting) continue;
      e.target.classList.add('visto');
      io.unobserve(e.target);
    }
  }, { rootMargin: '0px', threshold: 0 });
  elementos.forEach(el => io.observe(el));
})();
