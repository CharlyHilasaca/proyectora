$(document).ready(function () {
    const numEstrellas = 150;
    const minDist = 40;
    const maxDistCursor = 120;
    const estrellas = [];
    const fondoEstrellas = $("#fondo-estrellas");
    const canvas = $("#canvas-lineas")[0];
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function generarPosicion() {
        let x, y;
        let valido = false;
        
        while (!valido) {
            x = Math.random() * window.innerWidth;
            y = Math.random() * window.innerHeight;
            valido = estrellas.every(estrella => {
                let dx = estrella.x - x;
                let dy = estrella.y - y;
                return Math.sqrt(dx * dx + dy * dy) >= minDist;
            });
        }

        return { x, y };
    }

    function crearEstrellas() {
        for (let i = 0; i < numEstrellas; i++) {
            let pos = generarPosicion();
            estrellas.push(pos);
            fondoEstrellas.append(`<div class='estrella' style="left:${pos.x}px; top:${pos.y}px"></div>`);
        }
        animarEstrellas();
    }

    function animarEstrellas() {
        setInterval(() => {
            $(".estrella").each((index, el) => {
                let { x, y } = generarPosicion();
                estrellas[index] = { x, y };
                $(el).fadeOut(1000, function () {
                    $(this).css({ left: x, top: y }).fadeIn(1000);
                });
            });
        }, 2000);
    }

    $(window).resize(() => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    let mouseX = 0, mouseY = 0;
    $(document).mousemove(e => {
        mouseX = e.pageX;
        mouseY = e.pageY;
    });

    function dibujarLineaCursor() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        estrellas.forEach(({ x, y }) => {
            let dx = x - mouseX;
            let dy = y - mouseY;
            if (Math.sqrt(dx * dx + dy * dy) < maxDistCursor) {
                ctx.strokeStyle = "white";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(mouseX, mouseY);
                ctx.lineTo(x, y);
                ctx.stroke();
            }
        });

        requestAnimationFrame(dibujarLineaCursor);
    }

    requestAnimationFrame(dibujarLineaCursor);
    crearEstrellas();

    $("#register-container").hide();
    $("#t-lr").click(() => {
        $("#login-container").hide();
        $("#register-container").show();
    });

    $("#t-rl").click(() => {
        $("#register-container").hide();
        $("#login-container").show();
    });
});
