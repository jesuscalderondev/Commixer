# DOCUMENTATION

## Description
This server was created to manage the virtual food store, mainly

## Get started
1. Set your environment variables
    * Port
    * Secret Key
2. Install packages

2.1 Activate environment
    * Linux

    ```bash
    source env/lib/activate
    ```

    * Windows

    ```bash
    env/Scripts/activate
    ```

2.2 Install packages whit pip
```bash
pip install -r requirements.txt
```

3. Run server

```bash
python server.py
```

4. Define your host, with this you can communicate more easily with your server

5. Deploy


## ENDPOINTS
|Url|Method|Params|Headers|Response|
|---|---|---|---|---|
|/login|POST|username[text], password[text]||Authorization token|
|/getProducts|GET|||Json whit products|
|/createProduct|POST|price[double, float, int], name[text], size[text], weight[double, float, int], description[text], stock[int], quantity[int], color[text], cover[text]||Json with message|
### /login response

Correct

```json
{
    "token" : "generated token"
}

```
Incorrect

* If your credentials denied

```json
{
    "error" : "Incorrect credentials"
}
```

* Any fault

```json
{
    "error" : "generated error"
}
```

### /getProducts response

Example not empty
```json

{
    "products": [
        {
            "color": "amarillo",
            "cover": "No sé ni que va aquí",
            "id": "e5f02c5d-bba3-4663-b354-bd03b386ef8e",
            "name": "Platano",
            "price": 2000.0,
            "quantity": 300,
            "size": "20",
            "source": [
                "media/products/platano/platanoProfile.png"
            ],
            "stock": 10,
            "weight": 5.0
        }
    ],
    "productsReturn": "ready"
}
```

Example empty

```json
{
    "productsReturn": "empty"
}
```

### /createProduct
Correct register

```json
{
    "details": [],
    "register": "success"
}
```

Incorrect

```json
{
    "error": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand.",
    "register": "failed"
}
```