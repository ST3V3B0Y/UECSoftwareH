let navlist = document.querySelector('.navlist'); // ANIMACIÓN DE PANTALLA DE INICIO (INDEX)

const sr = ScrollReveal ({
    distance: '65px',
    duration: 2600,
    delay: 450,
    reset: true
});

sr.reveal('.hero-text',{delay:200, origin:'top'});
sr.reveal('.hero-img',{delay:450, origin:'top'});
sr.reveal('.scroll-down',{delay:500, origin:'right'}); 

