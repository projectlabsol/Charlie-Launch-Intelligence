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

        alert("No se pudo conectar con el motor");

    });

}





function mostrarResultado(data){


    const resultado = document.getElementById("resultado");


    resultado.innerHTML = `


    <div class="card token-card">


        ${data.imagen ? 

        `<img src="${data.imagen}" class="token-image">`

        :

        ""

        }



        <h2>

        ${data.nombre || "Token"}

        <span>

        $${data.ticker || ""}

        </span>

        </h2>



        <h1>

        Score: ${data.score}/100

        </h1>



        <p>

        CA:

        ${data.mint || ""}

        </p>



        <p>

        Volumen 24H:

        $${data.volumen || 0}

        </p>



        <p>

        Liquidez:

        $${data.liquidez || 0}

        </p>




        <div class="buttons">


        <button onclick="copiarCA('${data.mint}')">

        📋 Copiar CA

        </button>



        <button onclick="window.open('${data.original}')">

        🚀 Abrir Original

        </button>




        ${data.x ?

        `<button onclick="window.open('${data.x}')">

        𝕏 Ver X

        </button>`

        :

        ""

        }



        ${data.web && data.web.length ?

        `<button onclick="window.open('${data.web[0]}')">

        🌐 Ver Web

        </button>`

        :

        ""

        }



        </div>


    </div>


    `;

}





function recomendarLanzamiento(){


    fetch(`${API_URL}/recomendar`)


    .then(response => response.json())


    .then(data => {


        mostrarRecomendacion(
            data.recomendacion
        );


    })


    .catch(error=>{


        console.log(error);


        alert(
            "Error buscando oportunidad"
        );


    });


}





function buscarOtra(){


    recomendarLanzamiento();


}





function mostrarRecomendacion(token){


    const recomendacion =
    document.getElementById(
        "recomendacion"
    );



    if(!token){


        recomendacion.innerHTML = `

        <div class="card">

        ❌ Sin oportunidades

        </div>

        `;


        return;

    }




    recomendacion.innerHTML = `


    <div class="card token-card">


        <h2>

        🚀 Recomendación de Lanzamiento

        </h2>



        <img 

        src="${token.imagen || ''}"

        class="token-image"

        >



        <h1>

        ${token.nombre}

        $${token.ticker}

        </h1>




        <h2>

        Score ${token.score}/100

        </h2>




        <p>

        Volumen 24H:

        $${token.volumen}

        </p>



        <p>

        Liquidez:

        $${token.liquidez}

        </p>



        <p>

        CA:

        ${token.mint}

        </p>



        <button onclick="copiarCA('${token.mint}')">

        📋 Copiar CA

        </button>



        <button onclick="window.open('${token.original}')">

        🚀 Abrir Original

        </button>




        <button onclick="buscarOtra()">

        🔄 Buscar Otra

        </button>




        ${
        token.x ?

        `<button onclick="window.open('${token.x}')">

        𝕏 Ver X

        </button>`

        :

        ""

        }




        ${
        token.web && token.web.length ?

        `<button onclick="window.open('${token.web[0]}')">

        🌐 Ver Web

        </button>`

        :

        ""

        }



    </div>


    `;


}





function copiarCA(ca){


    navigator.clipboard.writeText(ca);


    alert(
        "CA copiado"
    );

}
