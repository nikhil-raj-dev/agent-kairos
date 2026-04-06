document.getElementById("sendBtn").addEventListener("click", sendMessage);

let firstQuery = true;

async function showLogs(logs, stepsDiv) {
    stepsDiv.innerHTML = "";

    for (let log of logs) {
        const stepEl = document.createElement("p");
        stepEl.innerText = "→ " + log;
        stepsDiv.appendChild(stepEl);

        await delay(400);
    }
}

async function sendMessage() {

    const query = document.getElementById("query").value;
    if (!query) return;

    const chat = document.getElementById("chat");
    const sidebar = document.getElementById("sidebar");
    const stepsDiv = document.getElementById("steps");
    const inputArea = document.getElementById("inputArea");
    const title = document.getElementById("title");
    const titleContainer = document.getElementById("title");

    const API_URL = "https://agent-kairos.onrender.com"; // for deploying on render.com

    if (firstQuery) {
        chat.classList.remove("hidden");
        sidebar.classList.remove("hidden");

        document.getElementById("suggestions").style.display = "none";
        document.getElementById("suggestions-label").style.display = "none";
        document.getElementsByClassName("title-block")[0].style.display = "none";

        inputArea.classList.remove("centered-input");
        inputArea.classList.add("bottom-input");

        titleContainer.classList.add("compact");


        document.querySelector(".main").classList.add("chat-active");

        firstQuery = false;
    }

    const block = document.createElement("div");
    block.className = "message";

    const userMsg = document.createElement("p");
    userMsg.innerHTML = `<b>You:</b> ${query}`;
    block.appendChild(userMsg);

    const agentLabel = document.createElement("p");
    agentLabel.innerHTML = `<b><span class="agent-label">Agent</span>:</b>`;
    block.appendChild(agentLabel);

    chat.appendChild(block);

    stepsDiv.innerHTML = "";

    // const res = await fetch("http://127.0.0.1:8000/chat", {
    //     method: "POST",
    //     headers: {"Content-Type": "application/json"},
    //     body: JSON.stringify({ query })
    // });

    // for deploying on render.com
    const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query })
    });

    const data = await res.json();

    await showLogs(data.logs, stepsDiv);

    await streamText(block, data.response);

    if (data.chart) {

        const loading = document.createElement("div");
        loading.innerHTML = "Generating plot...";
        const spinner = document.createElement("div");
        spinner.className = "spinner";

        block.appendChild(loading);
        block.appendChild(spinner);

        await delay(1000);

        const chartDiv = document.createElement("div");
        block.appendChild(chartDiv);

        const chartData = JSON.parse(data.chart);

        Plotly.newPlot(chartDiv, chartData.data, chartData.layout);

        loading.remove();
        spinner.remove();
    }

    document.getElementById("query").value = "";
}

function delay(ms) {
    return new Promise(res => setTimeout(res, ms));
}

async function streamText(container, text) {

    let i = 0;
    let currentText = "";

    const div = document.createElement("div");
    div.style.marginTop = "5px";
    container.appendChild(div);

    while (i < text.length) {
        currentText += text[i];
        div.innerText = currentText;
        i++;
        await delay(10);
    }

    div.innerHTML = marked.parse(currentText);
}

function fillQuery(text) {
    document.getElementById("query").value = text;
}
