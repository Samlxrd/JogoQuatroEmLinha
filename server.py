from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restringe as chamadas para apenas um local
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    
    board = [['▢' for x in range(9)] for y in range(9)]
    players = []
    currentTurn = ''
    inGame = True
    
    # Adiciona um novo jogador à lista de jogadores.
    @server.register_function
    def register_player(player):
        if player not in players:
            players.append(player)
            print("Novo jogador.")
            return True
        return False
    
    # Verifica se o jogo está em progresso.
    @server.register_function
    def in_game():
        global inGame
        return inGame


    # Função que imprime o tabuleiro
    @server.register_function
    def print_board():
        return '\n'.join([' '.join(row) for row in board])
    

    # Verifica se é a vez do jogador que chamou a função.
    @server.register_function
    def verify_turn(player):

        global currentTurn

        if not currentTurn:
            currentTurn = player

        if player != currentTurn:
            return False
        
        return True


    # Função que registra o movimento do jogador no tabuleiro.
    @server.register_function
    def make_move(col, player):

        global currentTurn

        for row in range(8, -1, -1):
            if board[row][col] == '▢':
                board[row][col] = player

                if player == 'X':
                    currentTurn = 'O'
                
                else:
                    currentTurn = 'X'
                    
                return True
        return False
    

    # Função que verifica se o jogador fez um sequência de quatro em linha e ganhou jogo.
    @server.register_function
    def check_win(player):
        global inGame

        # Verifica sequência de 4 jogadas nas linhas e colunas
        for x in range(9):
            for y in range(6):
                if board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3] == player:
                    inGame = False
                    return True

                if board[y][x] == board[y+1][x] == board[y+2][x] == board[y+3][x] == player:
                    inGame = False
                    return True

        # Verifica sequência de 4 jogadas nas diagonais
        for lin in range(6):
            for col in range(6):
                if board[lin][col] == board[lin+1][col+1] == board[lin+2][col+2] == board[lin+3][col+3] == player:
                    inGame = False
                    return True

        for lin in range(6):
            for col in range(3, 9):
                if board[lin][col] == board[lin+1][col-1] == board[lin+2][col-2] == board[lin+3][col-3] == player:
                    inGame = False
                    return True
                
        return False
    
    print("Servidor iniciado na porta 8000...")
    server.serve_forever()