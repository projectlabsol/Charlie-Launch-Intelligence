const API_URL = "https://charlie-launch-intelligence.onrender.com";


function analizarToken(){

    const ticker = document.getElementById("ticker").value;

    if(!ticker){
        alert("Ingrese un ticker");
        return;
    }

    fetch(`${API_URL}/analizar/${ticker.toUpperCase()}`)
    .then(response => response.json())
    .then(data => {

        mostrarResultado(data);

    })
    .catch(error => {

        console.log(error);
        alert("No se pudo conectar con el motor de análisis");

    });

}



function mostrarResultado(data){

    const resultado = document.getElementById("resultado");

    resultado.innerHTML = `

    <div class="card">

        <h3>${data.nombre || "Token analizado"}</h3>

        <p><b>Ticker:</b> ${data.ticker}</p>

        <h2>Score: ${data.score}/100</h2>

        <h3>${estadoScore(data.score)}</h3>

        <hr>

        <p>Volumen: ${data.volumen}</p>

        <p>Comunidad: ${data.comunidad}</p>

        <p>Viralidad: ${data.viralidad}</p>

        <p>Seguridad: ${data.seguridad}</p>

    </div>

    `;

}



function estadoScore(score){

    if(score >= 85){

        return "🟢 Alta oportunidad";

    }


    if(score >= 70){

        return "🟡 Analizar más";

    }


    return "🔴 No recomendado";

}




function actualizarRanking(){

    fetch(`${API_URL}/ranking`)
    .then(response => response.json())
    .then(data => {


        const ranking = document.getElementById("ranking");


        ranking.innerHTML = `

        <div class="card">

            <h2>Ranking de oportunidades</h2>

            ${data.map(token => `

                <div>

                    <h3>${token.nombre}</h3>

                    <p>
                    ${token.ticker}
                    </p>

                    <p>
                    Score: ${token.score}/100
                    </p>

                    <hr>

                </div>

            `).join("")}

        </div>

        `;


    })
    .catch(error=>{

        console.log(error);

        alert("Error cargando ranking");

    });

}




function recomendarLanzamiento(){

    fetch(`${API_URL}/recomendar`)
    .then(response => response.json())
    .then(data => {


        const recomendacion = document.getElementById("recomendacion");


        if(data.recomendaciones.length === 0){

            recomendacion.innerHTML = `

            <div class="card">

            <h2>❌ No hay lanzamientos recomendados</h2>

            </div>

            `;

            return;

        }



        let html = "";


        data.recomendaciones.forEach(token=>{


            html += `

            <div class="card">

                <h2>🚀 ${token.token}</h2>

                <p>
                Ticker: ${token.ticker}
                </p>

                <h3>
                ${token.decision}
                </h3>

                <p>
                Score: ${token.score}/100
                </p>

            </div>

            `;


        });



        recomendacion.innerHTML = html;



    })
    .catch(error=>{

        console.log(error);

        alert("Error conectando con el servidor");

    });


}
