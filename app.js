let tokens=[

{
nombre:"Future AI Meme",
ticker:"$FAIM",
meta:95,
volumen:90,
comunidad:85,
viralidad:92,
seguridad:80
},


{
nombre:"Animal Viral",
ticker:"$ANV",
meta:88,
volumen:82,
comunidad:90,
viralidad:85,
seguridad:84
}

];



function calcularScore(token){

return Math.round(

(token.meta*0.30)+
(token.volumen*0.25)+
(token.comunidad*0.20)+
(token.viralidad*0.15)+
(token.seguridad*0.10)

);

}



function nivel(score){

if(score>=85){

return "high";

}

if(score>=70){

return "medium";

}

return "low";

}



function mostrar(){

let ranking=tokens.map(t=>{

return{

...t,

score:calcularScore(t)

}

});


ranking.sort((a,b)=>b.score-a.score);



document.getElementById("resultado").innerHTML=


ranking.map(token=>`

<div class="card">


<h3>${token.nombre}</h3>


<p>${token.ticker}</p>


<p class="score">
Score: ${token.score}/100
</p>


<p class="${nivel(token.score)}">

${token.score>=85?"🟢 Alta oportunidad":
token.score>=70?"🟡 Revisar":
"🔴 Riesgo"}

</p>


<hr>


<p>Meta: ${token.meta}</p>

<p>Volumen: ${token.volumen}</p>

<p>Comunidad: ${token.comunidad}</p>

<p>Viralidad: ${token.viralidad}</p>

<p>Seguridad: ${token.seguridad}</p>


</div>


`).join("");

}




function analizarNuevoToken(){

let ticker=document
.getElementById("tickerInput")
.value;


if(!ticker){

alert("Ingrese un ticker");

return;

}



tokens.push({

nombre:"Nuevo Meme Detectado",

ticker:"$"+ticker.toUpperCase(),

meta:Math.floor(Math.random()*30)+70,

volumen:Math.floor(Math.random()*30)+70,

comunidad:Math.floor(Math.random()*30)+70,

viralidad:Math.floor(Math.random()*30)+70,

seguridad:Math.floor(Math.random()*30)+70

});


mostrar();

}




function actualizarRanking(){

mostrar();

}



mostrar();
