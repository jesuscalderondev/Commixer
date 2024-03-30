function filter(form) {
    var formData = new FormData(form);
    var jsonData = {};

    for (var [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    return jsonData;
}

function requestPost(url, headers, body, action){

    headers['Content-Type'] = 'application/json';
    fetch(url, {
        method: 'POST',

        headers : headers,
    
        body: JSON.stringify(body)
    })
        .then(response => response.json())
        .then(data => {
            action(data);
        })
        .catch(error => {
            console.error("Error en la comunicación con el servidor", error);
        });
}
