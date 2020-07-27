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
            const data = r.json();
            resolve(data);
        }).catch((e) => {
            reject(e);
        })
    });
}