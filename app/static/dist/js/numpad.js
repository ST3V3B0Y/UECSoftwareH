var numpad = {
    selector : null, // MANTENDRÁ TODO EL TECLADO NÚMERICO EN PANTALLA
    display : null, // MANTENDRÁ LA PANTALLA DEL TECLADO NÚMERICO
    zero : null, // MANTENDRÁ PRESIONADO EL BOTON DE CERO
    dot : null, // MANTENDRÁ PRESIONADO EL BOTON DE PUNTO
    init : function () {
      // CREACIÓN DE NUMPAD
      numpad.selector = document.createElement("div");
      numpad.selector.id = "numpad-back";
      var wrap = document.createElement("div");
      wrap.id = "numpad-wrap";
      numpad.selector.appendChild(wrap);
  
      // ADJUNTAR LA PANTALLA DE NÚMEROS
      numpad.display = document.createElement("input");
      numpad.display.id = "numpad-display";
      numpad.display.type = "text";
      numpad.display.readOnly = true;
      wrap.appendChild(numpad.display);
  
      // ADJUNTAR BOTONES
      var buttons = document.createElement("div"),
          button = null,
          append = function (txt, fn, css) {
            button = document.createElement("div");
            button.innerHTML = txt;
            button.classList.add("numpad-btn");
            if (css) {
              button.classList.add(css);
            }
            button.addEventListener("click", fn);
            buttons.appendChild(button);
          };
      buttons.id = "numpad-btns";
      // Primera fila - 7 a 9, eliminar.
      for (var i=7; i<=9; i++) {
        append(i, numpad.digit);
      }
      append("&#10502;", numpad.delete, "ng");
      // Segunda fila - 4 a 6, limpiar.
      for (var i=4; i<=6; i++) {
        append(i, numpad.digit);
      }
      append("C", numpad.reset, "ng");
      // Tercera fila - 1 a 3, cancelar.
      for (var i=1; i<=3; i++) {
        append(i, numpad.digit);
      }
      append("&#10006;", numpad.hide, "cx");
      // Última fila - 0, punto, ok
      append(0, numpad.digit, "zero");
      numpad.zero = button;
      numpad.dot = button;
      append("&#10004;", numpad.select, "ok");
      // Agregar todos los botones al envoltorio
      wrap.appendChild(buttons);
      document.body.appendChild(numpad.selector);
    },
  
    /* [ADJUNTAR A LA ENTRADA] */
    attach : function (opt) {
    // ADJUNTAR (): ADJUNTAR EL TECLADO NÚMERICO AL CAMPO DE ENTRADA DE DESTINO
  
      var target = document.getElementById(opt.id);
      if (target!=null) {
        // AÑADIR OPCIONES PREDETERMINADAS
        if (opt.readonly==undefined || typeof opt.readonly!="boolean") { opt.readonly = true; }
        if (opt.decimal==undefined || typeof opt.decimal!="boolean") { opt.decimal = true; }
        if (opt.max==undefined || typeof opt.max!="number") { opt.max = 10; }
  
        // ESTABLECER EL ATRIBUTO DE SÓLO LECTURA EN EL CAMPO DE DESTINO
        if (opt.readonly) { target.readOnly = true; }
  
        // ¿PERMITIR DECIMALES?
        target.dataset.decimal = opt.decimal ? 1 : 0;
  
        // CARACTERES MÁXIMOS PERMITIDOS
        target.dataset.max = opt.max;
  
        // MOSTRAR TECL NUMÉRICO AL HACER CLIC
        target.addEventListener("click", numpad.show);
      } else {
        console.log(opt.id + " NOT FOUND!");
      }
    },
  
    target : null, // CONTIENE EL CAMPO SELECCIONADO ACTUAL
    dec : true, // ¿PERMITE DECIMALES?
    max : 10, // CARACTERES MÁXIMOS PERMITIDOS
    show : function (evt) {
    // show() : MUESTRA EL TECLADO NÚMERICO
  
      // ESTABLECER EL CAMPO DE DESTINO ACTUAL
      numpad.target = evt.target;
  
      // MOSTRAR U OCULTAR EL BOTON DECIMAL
      numpad.dec = numpad.target.dataset.decimal==1;
      if (numpad.dec) {
        numpad.zero.classList.remove("zeroN");
        numpad.dot.classList.remove("ninja");
      } else {
        numpad.zero.classList.add("zeroN");
        numpad.dot.classList.add("ninja");
      }
  
      // MÁXIMO DE CARACTERES PERMITIDOS
      numpad.max = parseInt(numpad.target.dataset.max);
  
      // ESTABLECER VALOR DE VISUALIZACIÓN
      var dv = evt.target.value;
      if (!isNaN(parseFloat(dv)) && isFinite(dv)) {
        numpad.display.value = dv;
      } else {
        numpad.display.value = "";
      }
  
      // MOSTRAR TECLADO NÚMERICO
      numpad.selector.classList.add("show");
    },
  
    hide : function () {
    // hide() : OCULTAR EL TECLADO NÚMERICO
  
      numpad.selector.classList.remove("show");
    },
  
    /* [ACCIONES DE BOTÓN ONCLICK] */
    delete : function () {
    // delete () : ELIMINA EL ÚLTIMO DÍGITO EN EL TECLADO NÚMERICO
  
      var length = numpad.display.value.length;
      if (length > 0) {
        numpad.display.value = numpad.display.value.substring(0, length-1);
      }
    },
  
    reset : function () {
    // reset() : REINICIA EL TECLADO NÚMERICO
  
      numpad.display.value = "";
    },
  
    digit : function (evt) {
    // digit() : AGREGA UN DÍGITO
  
      var current = numpad.display.value,
          append = evt.target.innerHTML;
  
      if (current.length < numpad.max) {
        if (current=="0") {
          numpad.display.value = append;
        } else {
          numpad.display.value += append;
        }
      }
    },
  
    dot : function () {
    // dot() : AGREGA EL PUNTO DECIMAL (SOLO SI AÚN NO SE HA AGREGADO)
  
      if (numpad.display.value.indexOf(".") == -1) {
        if (numpad.display.value=="") {
          numpad.display.value = "0.";
        } else {
          numpad.display.value += ".";
        }
      }
    },
  
    select : function () {
    // select() : SELECCIONA EL NÚMERO ACTUAL
  
      var value = numpad.display.value;
  
      // NO SE PERMITEN DECIMALES - FRANJA DECIMAL
      if (!numpad.dec && value%1!=0) {
        value = parseInt(value);
      }
  
      // PONER EL VALOR SELECCIONADO EN EL CAMPO DE DESTINO + CERRAR EL TECLADO NÚMERICO
      numpad.target.value = value;
      numpad.hide();
    }
  };
  
  /* [INICIANDO] */
  window.addEventListener("load", numpad.init);