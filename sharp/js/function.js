static {{ name }} (
    {%- for parameter in parameters -%}
        {{ parameter }},
    {%- endfor -%}
) {

    return Core.makeRequest("{{route}}", {
        {% for parameter in parameters -%}
        {{ parameter }}: {{ parameter }},
        {% endfor -%}
    });
}
