const tokens = [
    {
        nombre: "Future AI Meme",
        ticker: "$FAIM",
        meta: 95,
        volumen: 90,
        comunidad: 85,
        viralidad: 92,
        seguridad: 80
    },
    {
        nombre: "Animal Viral",
        ticker: "$ANV",
        meta: 88,
        volumen: 82,
        comunidad: 90,
        viralidad: 85,
        seguridad: 84
    }
];


function analizarToken(token){

    let score =
        token.meta * 0.30 +
        token.volumen * 0.25 +
        token.comunidad * 0.20 +
        token.viralidad * 0.15 +
        token.seguridad * 0.10;


    return {
        ...token,
        score: Math.round(score)
    };

}


const resultados = tokens.map(analizarToken);


const ganador = resultados.sort(
    (a,b)=> b.score - a.score
)[0];


document.getElementById("token").innerHTML =
`
<h2>🚀 RECOMENDACIÓN CHARLIE</h2>

<h3>${ganador.nombre} ${ganador.ticker}</h3>

<p>META: ${ganador.meta}</p>
<p>VOLUMEN: ${ganador.volumen}</p>
<p>COMUNIDAD: ${ganador.comunidad}</p>
<p>VIRALIDAD: ${ganador.viralidad}</p>

<h2>Puntuación Charlie: ${ganador.score}/100</h2>

`;
