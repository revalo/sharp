export class Core {
    static makeRequest(route, body) {
        return new Promise((resolve, reject) => {
            fetch(route, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body),
            }).then((r) => {
                r.json().then((data) => {
                    if (data.result != null && "error" in data.result) {
                        reject(data.result.error);
                        return;
                    }
                    resolve(data.result);
                });
            }).catch((e) => {
                reject(e);
            })
        });
    }
}

export class API {
    {{ functions }}
}
