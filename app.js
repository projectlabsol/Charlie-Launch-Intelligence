const API_URL = "https://charlie-launch-intelligence.onrender.com";


let ultimoMint = "";



function recomendarLanzamiento(){

    buscarToken();

}




function buscarOtra(){

    buscarToken();

}




function buscarToken(){


    let url = `${API_URL}/recomendar?time=${Date.now()}`;


    if(ultimoMint){

        url += `&excluir=${ultimoMint}`;

    }



    fetch(url)

    .then(response => response.json())

    .then(data => {


        const token = data.recomendacion;



        if(!token || token.mensaje){

            document.getElementById(
                "recomendacion"
            ).innerHTML =
            "❌ Sin oportunidades";

            return;

        }



        ultimoMint = token.mint;



        mostrarRecomendacion(
            token
        );


    })

    .catch(error=>{

        console.log(error);

    });

}







function mostrarRecomendacion(token){


const zona = document.getElementById(
    "recomendacion"
);



zona.innerHTML = `


<div class="card token-card">


<h2>
🚀 Recomendación de Lanzamiento
</h2>



<img src="${token.imagen || ''}" class="token-image">



<h1>
${token.nombre}
<br>
$${token.ticker}
</h1>



<h2>
Score ${token.score}/100
</h2>



<p>
Meta: ${token.meta}
</p>


<p>
CA: ${token.mint}
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



</div>


`;

}





function copiarCA(ca){

navigator.clipboard.writeText(ca);

}



function abrirLink(url){

window.open(
url,
"_blank"
);

}
