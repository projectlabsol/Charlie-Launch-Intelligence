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

(token.meta*0.30)+
(token.volumen*0.25)+
(token.comunidad*0.20)+
(token.viralidad*0.15)+
(token.seguridad*0.10);


return {

...token,

score:Math.round(score)

};

}



let resultados = tokens.map(analizarToken);



resultados.sort((a,b)=>b.score-a.score);



document.getElementById("resultado").innerHTML =

resultados.map(token=>`

<div class="card">

<h3>${token.nombre}</h3>

<p class="badge">${token.ticker}</p>


<p class="score">
Score: ${token.score}/100
</p>


<p>Meta: ${token.meta}</p>

<p>Volumen: ${token.volumen}</p>

<p>Comunidad: ${token.comunidad}</p>

<p>Viralidad: ${token.viralidad}</p>

<p>Seguridad: ${token.seguridad}</p>


</div>


`).join("");
