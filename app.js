let tokens = [

{
nombre:"Future AI Meme",
ticker:"$FAIM",
score:90,
meta:95,
volumen:90,
comunidad:85,
viralidad:92,
seguridad:80
},

{
nombre:"Animal Viral",
ticker:"$ANV",
score:86,
meta:88,
volumen:82,
comunidad:90,
viralidad:85,
seguridad:84
}

];



function mostrarTokens(){

let html="";


tokens.forEach(t=>{

let estado="";

if(t.score>=85){
estado="🟢 Alta oportunidad";
}
else if(t.score>=70){
estado="🟡 Analizar más";
}
else{
estado="🔴 Riesgo alto";
}


html+=`

<div class="card">

<h3>${t.nombre}</h3>

<p>${t.ticker}</p>

<h3>Score: ${t.score}/100</h3>

<h4>${estado}</h4>

<hr>

<p>Meta: ${t.meta}</p>

<p>Volumen: ${t.volumen}</p>

<p>Comunidad: ${t.comunidad}</p>

<p>Viralidad: ${t.viralidad}</p>

<p>Seguridad: ${t.seguridad}</p>


</div>

`;

});


document.getElementById("resultado").innerHTML=html;


}



function analizarToken(){

let ticker=document.getElementById("ticker").value;


if(ticker===""){
alert("Ingrese un ticker");
return;
}


let nuevo={

nombre:"Nuevo Token "+ticker,

ticker:"$"+ticker.toUpperCase(),

score:88,

meta:90,

volumen:85,

comunidad:86,

viralidad:89,

seguridad:82

};


tokens.unshift(nuevo);


mostrarTokens();


}



function actualizarRanking(){

tokens.sort((a,b)=>b.score-a.score);

mostrarTokens();

}



function recomendarLanzamiento(){


let ganador=tokens[0];


let estado="";

let color="";


if(ganador.score>=85){

estado="🚀 LANZAMIENTO RECOMENDADO";

color="verde";

}

else if(ganador.score>=70){

estado="⚠️ ANALIZAR ANTES DE LANZAR";

color="amarillo";

}

else{

estado="❌ NO RECOMENDADO";

color="rojo";

}



document.getElementById("recomendacion").innerHTML=

`

<div class="recomendacion ${color}">


<h2>${estado}</h2>


<h3>${ganador.nombre}</h3>


<p>Token: ${ganador.ticker}</p>


<p>Score Inteligencia: ${ganador.score}/100</p>


<hr>


<p>
Potencial: ${ganador.meta}/100
</p>


<p>
Comunidad: ${ganador.comunidad}/100
</p>


<p>
Viralidad: ${ganador.viralidad}/100
</p>


<p>
Riesgo Seguridad: ${ganador.seguridad}/100
</p>


</div>

`;


}



window.onload=mostrarTokens;
