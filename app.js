const tokens = [

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


function analizarToken(token){

let score = 
(token.meta * 0.30) +
(token.volumen * 0.25) +
(token.comunidad * 0.20) +
(token.viralidad * 0.15) +
(token.seguridad * 0.10);


return {

...token,
score:Math.round(score)

};

}



function cargarDashboard(){

let resultados = tokens.map(analizarToken);


resultados.sort((a,b)=>b.score-a.score);



document.getElementById("resultado").innerHTML = resultados.map(token=>`

<div class="card">

<h3>${token.nombre}</h3>

<p>${token.ticker}</p>

<div class="score">
Score: ${token.score}/100
</div>


<p class="label">Meta ${token.meta}</p>
<div class="progress">
<div style="width:${token.meta}%"></div>
</div>


<p class="label">Volumen ${token.volumen}</p>
<div class="progress">
<div style="width:${token.volumen}%"></div>
</div>


<p class="label">Comunidad ${token.comunidad}</p>
<div class="progress">
<div style="width:${token.comunidad}%"></div>
</div>


<p class="label">Viralidad ${token.viralidad}</p>
<div class="progress">
<div style="width:${token.viralidad}%"></div>
</div>


<p class="label">Seguridad ${token.seguridad}</p>
<div class="progress">
<div style="width:${token.seguridad}%"></div>
</div>


</div>

`).join("");

}


window.onload = cargarDashboard;
