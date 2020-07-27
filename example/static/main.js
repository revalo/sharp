import { API } from  "./sharp.gen.js";

(function() {
    const name = document.getElementById("name");
    const button = document.getElementById("button");
    const result = document.getElementById("result");

    button.onclick = () => {
        // Calls the server.
        API.repeat(name.value, 5).then((c) => {
            result.innerText = c.repeated;
        });
    }
})();
