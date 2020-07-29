static {{ name }} (
    {%- for parameter in parameters -%}
        {{ parameter }},
    {%- endfor -%}
) {
    return new Promise((resolve, reject) => {
        fetch("{{route}}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                {% for parameter in parameters -%}
                {{ parameter }}: {{ parameter }},
                {% endfor -%}
            }),
        }).then((r) => {
            r.json().then((data) => {
                if ("error" in data) {
                    reject(data.error);
                    return;
                }
                resolve(data.result);
            });
        }).catch((e) => {
            reject(e);
        })
    });
}