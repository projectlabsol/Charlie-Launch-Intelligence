const API_URL = "https://charlie-launch-intelligence.onrender.com";


let ultimoToken = null;



function recomendarLanzamiento(){


    const boton = document.querySelector(
        "button"
    );


    fetch(
        `${API_URL}/recomendar?time=${Date.now()}`
    )
    .then(response => response.json())
    .then(data => {


        if(data.recomendacion){

            ultimoToken = data.recomendacion;

            mostrarRecomendacion(
                ultimoToken
            );

        }


    })
    .catch(error=>{

        console.log(error);

        alert(
            "Error conectando con scanner"
        );

    });

}




function buscarOtra(){


    ultimoToken = null;


    recomendarLanzamiento();


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
    Meta:
    ${token.meta || "Meme"}
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
    `
    <button onclick="abrirLink('${token.x}')">

    𝕏 Ver X

    </button>
    `
    :
    ""
    }



    ${
    token.web
    ?
    `
    <button onclick="abrirLink('${token.web}')">

    🌐 Ver Web

    </button>
    `
    :
    ""
    }



    </div>


    `;

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
