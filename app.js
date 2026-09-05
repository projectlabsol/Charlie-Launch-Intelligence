const API_URL = "https://charlie-launch-intelligence.onrender.com";


let tokensMostrados = [];



// =============================
// ANALIZAR TOKEN
// =============================

function analizarToken(){

    const ticker =
    document.getElementById("ticker").value;


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

        alert("No se pudo conectar con el motor");

    });


}





function mostrarResultado(data){


    document.getElementById("resultado").innerHTML = crearCardToken(data);


}






// =============================
// RECOMENDACION EN TIEMPO REAL
// =============================


function recomendarLanzamiento(){


    fetch(`${API_URL}/recomendar?t=${Date.now()}`)


    .then(response=>response.json())


    .then(data=>{


        let token = data.recomendacion;



        if(!token){

            mostrarSinResultado();

            return;

        }



        // evitar repetidos

        if(tokensMostrados.includes(token.mint)){


            buscarOtra();


            return;

        }



        tokensMostrados.push(token.mint);



        mostrarRecomendacion(token);



    })


    .catch(error=>{


        console.log(error);


        alert(
            "Error buscando oportunidad"
        );


    });


}






// =============================
// BUSCAR OTRA MONEDA
// =============================


function buscarOtra(){


    recomendarLanzamiento();


}






// =============================
// MOSTRAR RECOMENDACION
// =============================


function mostrarRecomendacion(token){


    const zona =
    document.getElementById(
        "recomendacion"
    );



    zona.innerHTML = crearCardToken(token,true);


}






function crearCardToken(token, recomendado=false){


    if(!token || !token.mint){

        return `

        <div class="card">

            <h2>❌ Sin oportunidad encontrada</h2>

            <p>
            El scanner no encontró una moneda válida en este escaneo.
            </p>


            <button onclick="buscarOtra()">
            🔄 Buscar Otra
            </button>


        </div>

        `;

    }



    return `

    <div class="card token-card">


        ${
        recomendado
        ?
        `<h2>🚀 Recomendación de Lanzamiento</h2>`
        :
        ""
        }



        <img

        src="${token.imagen || 'https://placehold.co/200'}"

        class="token-image"

        >



        <h1>

        ${token.nombre || "Token"}

        $${token.ticker || ""}

        </h1>




        <h2>

        Score ${token.score || 0}/100

        </h2>




        <p>

        CA:

        ${token.mint}

        </p>




        <p>

        Volumen 24H:

        $${token.volumen || 0}

        </p>




        <p>

        Liquidez:

        $${token.liquidez || 0}

        </p>




        <div class="buttons">


            <button onclick="copiarCA('${token.mint}')">

            📋 Copiar CA

            </button>



            <button onclick="abrirLink('${token.original}')">

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



    </div>


    `;

}





${
token.web ?

`

<button onclick="abrirLink('${token.web}')">

🌐 Ver Web

</button>

`

:''

}



</div>



</div>


`;

}







// =============================
// RANKING
// =============================


function actualizarRanking(){


fetch(`${API_URL}/ranking?t=${Date.now()}`)


.then(response=>response.json())


.then(data=>{


let html="";


data.forEach(token=>{


html += crearCardToken(token);


});



document.getElementById("ranking").innerHTML = html;



})

.catch(error=>{


console.log(error);


});

}






// =============================
// UTILIDADES
// =============================


function copiarCA(ca){


navigator.clipboard.writeText(ca);


alert("CA copiado");


}





function abrirLink(url){


if(url){

window.open(url,"_blank");

}


}




function mostrarSinResultado(){


document.getElementById("recomendacion").innerHTML=

`

<div class="card">

<h2>
❌ No se encontraron oportunidades
</h2>

<button onclick="buscarOtra()">

🔄 Intentar nuevamente

</button>

</div>

`;

}
