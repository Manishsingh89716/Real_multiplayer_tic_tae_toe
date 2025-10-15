from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

#fastAPI app initialization
app = FastAPI(title="Multiplayer Tic-Tac-Toe API")

#enable CORS for frontend (Netlify) connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#eoot route (important for Render health check)
@app.get("/")
def read_root():
    """Render uses this route to confirm the service is alive."""
    return {"message": "Tic Tac Toe Backend is running successfully!"}


#player model for request validation
class Player(BaseModel):
    player_name: str


#core Game class to handle board, turns, and game state
class TicTacToeGame:
    def __init__(self):
        self.board = [""] * 9  # Represents 3x3 game board
        self.turn = "X"        # X always starts
        self.winner = None
        self.players = {}      # Maps X and O to player names
        self.connections = []  # Active WebSocket connections

    def make_move(self, position: int, symbol: str):
        """Handles a player's move"""
        if self.winner or self.board[position] != "":
            return False  # Invalid move
        self.board[position] = symbol
        self.check_winner()
        self.turn = "O" if self.turn == "X" else "X"
        return True

    def check_winner(self):
        """Check all possible winning combinations"""
        winning_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in winning_positions:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                break


#in-memory storage for active games
games = {}


#create new game endpoint
@app.post("/create_game")
async def create_game(player: Player):
    """Create a new game and assign player as 'X'"""
    game_id = str(uuid.uuid4())[:6]  # short unique id
    game = TicTacToeGame()
    game.players["X"] = player.player_name
    games[game_id] = game
    return {
        "game_id": game_id,
        "message": "Game created. Share Game ID with another player."
    }


#join existing game endpoint
@app.post("/join_game/{game_id}")
async def join_game(game_id: str, player: Player):
    """Join an existing game and assign player as 'O'"""
    if game_id not in games:
        return {"error": "Game not found."}
    game = games[game_id]
    if "O" in game.players:
        return {"error": "Game already full."}
    game.players["O"] = player.player_name
    return {"message": "Joined game successfully.", "game_id": game_id}


#webSocket Manager class to handle connections and real-time communication
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        """Remove WebSocket when player disconnects"""
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)

    async def broadcast(self, message: dict, game_id: str):
        """Send message to all players in same game"""
        for connection in self.active_connections.get(game_id, []):
            await connection.send_json(message)


#manager instance (single for all connections)
manager = ConnectionManager()


#webSocket endpoint for real-time gameplay
@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """Main real-time WebSocket communication endpoint"""
    await manager.connect(websocket, game_id)
    game = games.get(game_id)

    #when both players connected, start the game
    if len(manager.active_connections.get(game_id, [])) == 2:
        await manager.broadcast({
            "action": "start",
            "board": game.board,
            "turn": game.turn
        }, game_id)

    try:
        while True:
            data = await websocket.receive_json()
            if data["action"] == "move":
                position = data["position"]
                symbol = data["symbol"]
                if game.make_move(position, symbol):
                    await manager.broadcast({
                        "action": "update",
                        "board": game.board,
                        "turn": game.turn,
                        "winner": game.winner
                    }, game_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
        print(f"Player disconnected from game {game_id}")