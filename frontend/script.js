let ws;
let gameId;
let playerSymbol;
let currentTurn = "X";

function createGame() {
    const name = document.getElementById("playerName").value;
    fetch("http://localhost:8000/create_game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({player_name: name})
    })
    .then(res => res.json())
    .then(data => {
        gameId = data.game_id;
        playerSymbol = "X";
        document.getElementById("gameIdText").innerText = "Game ID: " + gameId;
        connectWebSocket();
    });
}

function joinGame() {
    const name = document.getElementById("playerName").value;
    const id = document.getElementById("joinId").value;
    fetch(`http://localhost:8000/join_game/${id}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({player_name: name})
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) alert(data.error);
        else {
            gameId = id;
            playerSymbol = "O";
            connectWebSocket();
        }
    });
}

function connectWebSocket() {
    ws = new WebSocket(`ws://localhost:8000/ws/${gameId}`);
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.action === "start") {
            document.getElementById("menu").classList.add("hidden");
            document.getElementById("gameBoard").classList.remove("hidden");
            renderBoard(data.board);
            currentTurn = data.turn;
            updateInfoPanel(currentTurn, playerSymbol, "Game started!");
        } else if (data.action === "update") {
            renderBoard(data.board);
            currentTurn = data.turn;
            if (data.winner) {
                updateInfoPanel(currentTurn, playerSymbol, `Player ${data.winner} won!`);
            } else {
                updateInfoPanel(currentTurn, playerSymbol, "Your move or wait for opponent...");
            }
        }
    };
}

function renderBoard(board) {
    const boardDiv = document.getElementById("board");
    boardDiv.innerHTML = "";
    board.forEach((cell, i) => {
        const div = document.createElement("div");
        div.classList.add("cell");
        div.innerText = cell;
        div.onclick = () => makeMove(i);
        boardDiv.appendChild(div);
    });
}

function makeMove(position) {
    ws.send(JSON.stringify({
        action: "move",
        position: position,
        symbol: playerSymbol
    }));
}

function updateInfoPanel(currentPlayer, youPlayBy, info) {
    document.getElementById("currentPlayer").innerText = `Current Player: ${currentPlayer}`;
    document.getElementById("youPlayBy").innerText = `You play by: ${youPlayBy}`;
    document.getElementById("infoText").innerText = `Info: ${info}`;
}