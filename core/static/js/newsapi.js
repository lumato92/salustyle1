const requestOptions = {
  method: "GET",
};

const params = {
  apiKey: "t4-SGMjXCHKcNeaVTcwq1aGQxnUXtDubSyw8FwXSjhGPz5d2",
  language: "es",
  category: "health",
  limit: "6",
  page_size: "6",
};

const esc = encodeURIComponent;
let query = Object.keys(params)
  .map(function (k) {
    return esc(k) + "=" + esc(params[k]);
  })
  .join("&");

fetch("https://api.currentsapi.services/v1/search?" + query, requestOptions)
  .then((response) => response.json())
  .then((result) => {
    let { news } = result;
    console.log(news);
    const content_div = document.getElementById("noticias");
    news.forEach((noticia) => {
      let div = document.createElement("div");
      div.className = "col";
      div.innerHTML=`<div class="card h-100">
      <img src="${noticia.image}" class="card-img-top"
        alt="Imagen de noticia" />
      <div class="card-body">
        <h5 class="card-title title-noticia fw-bold">${noticia.title}</h5>
        <p class="card-text body-noticia">
          ${noticia.description}
        </p>
        <a class="btn btn-primary text-white" href="${noticia.url}" target="_blank">Ver más</a>
      </div>
    </div>`
      content_div.appendChild(div);
    });
  })
  .catch((error) => console.log("error", error));

//   <div class="col">
      
//     </div>
