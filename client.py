import xmlrpc.client

def main():
    # Conexão com o servidor
    server = xmlrpc.client.ServerProxy('http://localhost:8000')

    
    # Jogadores escolhem entre o símbolo 'X' e 'O'.
    while True:
        player = input('Escolha o seu simbolo (X ou O): ').upper()

        if player in 'XO':
            if (server.register_player(player)):
                break
            else:
                print('Escolha o outro Simbolo.')
        else:
            print('Escolha um simbolo valido.')

    print(server.print_board())
    
    # Loop do jogo
    while True:

        if not server.in_game():
            print('Você perdeu, o adversário completou 4 em linha.')
            break

        try:
            col = int(input('Digite o numero da coluna que deseja jogar [1-9]: ')) - 1
            if col < 0 or col > 8:
                print('Valor fora do intervalo.')
                continue
            
        except ValueError:
            print('Caractere invalido.')
            continue
        
        # Verifica se é o turno do jogador.
        if server.verify_turn(player):

            # Verifica se a posição é válida.
            while True:
                if server.make_move(col,player):
                    break
                
                print('Coluna cheia, escolha outra posição para jogar.')

            print(server.print_board())

            # Ao realizar movimento, verifica se o jogador completou quatro em linha.
            if server.check_win(player):
                print('Parabéns, você ganhou!')
                break

        else:
            print('Vez do adversário.')

        print('Aguardando jogada do adversário.')
        
        # Após realizar a jogada, fica em loop aguardando adversário jogar
        while True:
            if server.verify_turn(player):
                break
        print(server.print_board())

if __name__ == '__main__':
    main()