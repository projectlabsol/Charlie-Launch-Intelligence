const API_URL = "https://charlie-launch-intelligence.onrender.com";


function recomendarLanzamiento(){

    fetch(`${API_URL}/recomendar`)
    .then(response => response.json())
    .then(data => {

        mostrarRecomendacion(
            data.recomendacion
        );

    })
    .catch(error => {

        console.log(error);
        alert("Error conectando con el motor");

    });

}



function mostrarRecomendacion(token){


    const zona = document.getElementById(
        "recomendacion"
    );


    if(!token || token.mensaje){

        zona.innerHTML = `
        <div class="card">
        ❌ Sin oportunidades
        </div>
        `;

        return;
    }



    zona.innerHTML = `

    <div class="card token-card">


        <h2>
        🚀 Recomendación de Lanzamiento
        </h2>


        ${
        token.imagen
        ?
        `<img src="${token.imagen}" class="token-image">`
        :
        ""
        }



        <h1>
        ${token.nombre}
        $${token.ticker}
        </h1>


        <h2>
        Score ${token.score}/100
        </h2>


        <p>
        Meta: ${token.meta}
        </p>


        <p>
        CA:
        ${token.mint}
        </p>


        <p>
        Volumen 24H:
        $${token.volumen24h}
        </p>


        <p>
        Liquidez:
        $${token.liquidez}
        </p>



        <button onclick="copiarCA('${token.mint}')">
        📋 Copiar CA
        </button>



        <button onclick="abrirLink('https://pump.fun/${token.mint}')">
        🚀 Abrir Original
        </button>



        <button onclick="buscarOtra()">
        🔄 Buscar Otra
        </button>



        ${
        token.x
        ?
        `<button onclick="abrirLink('${token.x}')">
        𝕏 Ver X
        </button>`
        :
        ""
        }



        ${
        token.web
        ?
        `<button onclick="abrirLink('${token.web}')">
        🌐 Ver Web
        </button>`
        :
        ""
        }



    </div>

    `;

}





function buscarOtra(){

    recomendarLanzamiento();

}



function abrirLink(url){

    window.open(
        url,
        "_blank"
    );

}



function copiarCA(ca){

    navigator.clipboard.writeText(
        ca
    );

    alert(
        "CA copiado"
    );

}
