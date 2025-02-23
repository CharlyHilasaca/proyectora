$(document).ready(function () {
    let numEstrellas = 200;
    let minDist = 40;
    let maxDistConexion = 150;
    let estrellas = [];
    let canvas = document.getElementById("canvas-lineas");
    let ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function generarPosicion() {
        let x, y, valido;
        do {
            x = Math.floor(Math.random() * window.innerWidth);
            y = Math.floor(Math.random() * window.innerHeight);
            valido = true;

            for (let estrella of estrellas) {
                let dx = estrella.x - x;
                let dy = estrella.y - y;
                let distancia = Math.sqrt(dx * dx + dy * dy);
                if (distancia < minDist) {
                    valido = false;
                    break;
                }
            }
        } while (!valido);

        return { x, y };
    }

    function crearEstrellas() {
        let fondoEstrellas = $("#fondo-estrellas");

        for (let i = 0; i < numEstrellas; i++) {
            let { x, y } = generarPosicion();
            estrellas.push({ x, y });

            let estrella = $("<div class='estrella'></div>").css({
                left: x + "px",
                top: y + "px"
            });

            fondoEstrellas.append(estrella);
        }

        animarEstrellas();
    }

    function animarEstrellas() {
        setInterval(() => {
            let promesas = [];

            $(".estrella").each(function (index) {
                let { x, y } = generarPosicion();
                estrellas[index] = { x, y };

                let promesa = $(this).fadeOut(1000).promise().then(() => {
                    $(this).css({ left: x + "px", top: y + "px" }).fadeIn(1000);
                });

                promesas.push(promesa);
            });

            Promise.all(promesas).then(() => {
                dibujarLineas();
                detectarBrillo();
                dibujarLineaCursor(); // Ahora se ejecuta después de la animación
            });

        }, 2000);
    }

    function dibujarLineas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < estrellas.length; i++) {
            let estrella1 = estrellas[i];

            for (let j = i + 1; j < estrellas.length; j++) {
                let estrella2 = estrellas[j];

                let dx = estrella1.x - estrella2.x;
                let dy = estrella1.y - estrella2.y;
                let distancia = Math.sqrt(dx * dx + dy * dy);

                if (distancia < maxDistConexion) {
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
                    ctx.lineWidth = 0.8;
                    ctx.beginPath();
                    ctx.moveTo(estrella1.x, estrella1.y);
                    ctx.lineTo(estrella2.x, estrella2.y);
                    ctx.stroke();
                }
            }
        }
    }

    function detectarBrillo() {
        $(".estrella").each(function (index) {
            let estrella = estrellas[index];
            let bordeCercano = estrella.x < 50 || estrella.x > window.innerWidth - 50 ||
                               estrella.y < 50 || estrella.y > window.innerHeight - 50;

            if (bordeCercano) {
                $(this).addClass("estrella-brillo");
            } else {
                $(this).removeClass("estrella-brillo");
            }
        });
    }

    $(window).resize(function () {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    let mouseX = 0, mouseY = 0;

    $(document).mousemove(function (event) {
        mouseX = event.pageX;
        mouseY = event.pageY;
    });

    function dibujarLineaCursor() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let estrella of estrellas) {
            let dx = estrella.x - mouseX;
            let dy = estrella.y - mouseY;
            let distancia = Math.sqrt(dx * dx + dy * dy);

            if (distancia < 120) {
                ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(mouseX, mouseY);
                ctx.lineTo(estrella.x, estrella.y);
                ctx.stroke();
            }
        }
    }

    setInterval(dibujarLineaCursor, 50);

    crearEstrellas();

    $("#register-container").hide();
    $("#t-lr").click(function () {
        $("#login-container").hide();
        $("#register-container").show();
    });

    $("#t-rl").click(function () {
        $("#register-container").hide();
        $("#login-container").show();
    });
});
