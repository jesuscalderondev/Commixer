function login(data) {
    let level = data.level;

    console.log(level);

    if (level == "admin") {
        window.location.href = "/admin/dashboard";
    }
    else{
        console.log("joaaa");
        var alerta = document.createElement("div");
        alerta.setAttribute("class", "alert alert-danger")
        alerta.style = "position: absolute; margin: 10px; transition: all ease .3s";
        alerta.innerHTML = data.message;

        document.body.appendChild(alerta);

        alerta.addEventListener("click", () => {
            alerta.style = "transition: all ease 1s"
            alerta.style = "margin-top: -200px;"
            alerta.remove();
        })
    }
}