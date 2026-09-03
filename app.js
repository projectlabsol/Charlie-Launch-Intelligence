const API_URL = "http://127.0.0.1:8000";


function analizarToken(){

const ticker = document.getElementById("ticker").value;


if(!ticker){

alert("Ingrese un ticker");

return;

}


fetch(`${API_URL}/analizar/${ticker.toUpperCase()}`)

.then(response=>response.json())

.then(data=>{


mostrarResultado(data);


})

.catch(error=>{


console.log(error);

alert("No se pudo conectar con el motor de análisis");


});


}



function mostrarResultado(data){


let resultado = document.getElementById("resultado");


resultado.innerHTML = `


<div class="card">


<h3>${data.nombre || "Token analizado"}</h3>


<p>${data.ticker}</p>


<h2>
Score: ${data.score}/100
</h2>


<h3>
${estadoScore(data.score)}
</h3>


<hr>


<p>Volumen: ${data.volumen}</p>

<p>Comunidad: ${data.comunidad}</p>

<p>Viralidad: ${data.viralidad}</p>

<p>Seguridad: ${data.seguridad}</p>



</div>


`;



}



function estadoScore(score){


if(score>=85){

return "🟢 Alta oportunidad";

}


if(score>=70){

return "🟡 Analizar más";

}


return "🔴 No recomendado";


}





function recomendarLanzamiento(){

    fetch("https://charlie-launch-intelligence.onrender.com/recomendar")
    .then(res => res.json())
    .then(datos => {

        let mensaje = "";

        if(datos.recomendaciones.length === 0){

            mensaje = "❌ No hay lanzamientos recomendados";

        } else {

            datos.recomendaciones.forEach(token => {

                mensaje += `
🚀 ${token.token}

${token.ticker}

DECISIÓN:
${token.decision}

SCORE:
${token.score}/100

------------------
`;

            });

        }

        document.getElementById("recomendacion").innerHTML = `
        <div class="recomendacion verde">
            <h2>${mensaje}</h2>
            <p>Evaluación basada en inteligencia de mercado.</p>
        </div>
        `;

    })
    .catch(error => {

        alert("Error conectando con el servidor");
        console.log(error);

    });

}

}



function actualizarRanking(){

location.reload();

}
