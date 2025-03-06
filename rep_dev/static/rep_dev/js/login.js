$(document).ready(function () {
    const numPuntos = 200;
    const maxDistPuntos = 100;
    const velocidad = 0.5;
    const puntos = [];
    const canvas = $("#canvas-lineas")[0];
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function generarPosicion() {
        return {
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            vx: (Math.random() - 0.5) * velocidad,
            vy: (Math.random() - 0.5) * velocidad
        };
    }

    function crearPuntos() {
        for (let i = 0; i < numPuntos; i++) {
            puntos.push(generarPosicion());
        }
    }

    function actualizarPuntos() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < numPuntos; i++) {
            let p = puntos[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        }

        dibujarLineas();
        dibujarPuntos();
        requestAnimationFrame(actualizarPuntos);
    }

    function dibujarPuntos() {
        ctx.fillStyle = "white";
        for (let p of puntos) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function dibujarLineas() {
        ctx.strokeStyle = "white";
        ctx.lineWidth = 0.5;
        for (let i = 0; i < numPuntos; i++) {
            for (let j = i + 1; j < numPuntos; j++) {
                let dx = puntos[i].x - puntos[j].x;
                let dy = puntos[i].y - puntos[j].y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < maxDistPuntos) {
                    ctx.globalAlpha = 1 - dist / maxDistPuntos;
                    ctx.beginPath();
                    ctx.moveTo(puntos[i].x, puntos[i].y);
                    ctx.lineTo(puntos[j].x, puntos[j].y);
                    ctx.stroke();
                }
            }
        }
        ctx.globalAlpha = 1;
    }

    $(window).resize(() => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    crearPuntos();
    actualizarPuntos();
});
