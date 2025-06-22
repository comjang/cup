import random as rd

class Bot:
    
    def get_move(self, board, peices, player):
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        size = rd.randrange(1, 4)

        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로
            [0, 4, 8], [2, 4, 6]  # 대각선
        ]

        b = [' '] * 9
        
        if player == 'X':
            my_peices = x_peices
            opponent = 'O'
            opponent_peices = o_peices  
        else:
            my_peices = o_peices
            opponent = 'X'
            opponent_peices = x_peices  

        center_cup = board[4][:2]

        for size in ['3','2','1']:
            if size not in my_peices:
                continue
            
            if center_cup[1] == ' ' or (center_cup != player and int(center_cup[1]) < 3):
                return "3 " + " " + str(4)

            for i in range(9):
                b[i] = board[i][0]



            for pattern in win_patterns:

                if b[pattern[0]] == b[pattern[1]] and b[pattern[1]] == player and (b[pattern[2]] == ' ' or b[pattern[0]] == opponent):
                    return str(size) + " " + str(pattern[2])
                
                elif b[pattern[1]] == b[pattern[2]] and b[pattern[1]] == player and (b[pattern[0]] == ' ' or b[pattern[0]] == opponent):
                    return str(size) + " " + str(pattern[0])
                
                elif b[pattern[0]] == b[pattern[2]] and b[pattern[0]] == player and (b[pattern[1]] == ' ' or b[pattern[0]] == opponent):
                    return str(size) + " " + str(pattern[1])
                



            for pattern in win_patterns:

                if b[pattern[0]] == b[pattern[1]] and b[pattern[1]] == opponent and (b[pattern[2]] == ' ' or b[pattern[0]] == player):
                    return str(size) + " " + str(pattern[2])
                
                elif b[pattern[1]] == b[pattern[2]] and b[pattern[1]] == opponent and (b[pattern[0]] == ' ' or b[pattern[0]] == player):
                    return str(size) + " " + str(pattern[0])
                
                elif b[pattern[0]] == b[pattern[2]] and b[pattern[0]] == opponent and (b[pattern[1]] == ' ' or b[pattern[0]] == player):
                    return str(size) + " " + str(pattern[1])


            
            top_players = [board[i][0] for i in range(9)]
            top_sizes = []
            for i in range(9):
                if board[i][1] == ' ':
                    top_sizes.append(0)
                else:
                    top_sizes.append(int(board[i][1]))

            # 인접 칸 찾기 함수
            def neighbors(idx):
                neigh = []
                row, col = divmod(idx, 3)
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row+dr, col+dc
                        if 0 <= nr < 3 and 0 <= nc < 3:
                            neigh.append(nr*3 + nc)
                return neigh

            # 상대 컵 위치 찾기
            opponent_positions = [i for i, p in enumerate(top_players) if p == opponent]

            # 내 컵 사이즈 정렬 (내가 가진 컵 크기)
            my_sizes = sorted([int(c) for c in set(my_peices)], reverse=True)

            for opp_pos in opponent_positions:
                opp_size = top_sizes[opp_pos]
                for adj in neighbors(opp_pos):
                    adj_player = top_players[adj]
                    adj_size = top_sizes[adj]
                   
                    if adj_player == ' ' or (adj_player != player and adj_size < int(size)) or (adj_player == player and adj_size < int(size)):
                        if opp_size == 1:
                            if 2 in my_sizes and int(size) == 2 and adj_size < 2:
                                return "2 " + str(adj)
                        elif opp_size > 1:
                            target_size = opp_size - 1
                            if target_size in my_sizes and int(size) == target_size and adj_size < target_size:
                                return str(target_size) + " " + str(adj)

            pick_index = []
            move_index = []

            for i in range(9):
                cup = board[i][:2]
                if cup == player + str(size):
                    pick_index.append(i)
                if cup[1] == ' ':
                    move_index.append(i)
                else:
                    if int(cup[1]) < int(size):
                        move_index.append(i)
            i = -1
            if player == 'X':
                i = x_peices.find(str(size))
            else:
                i = o_peices.find(str(size))

            

            if len(pick_index) == 0 or len(move_index) == 0:
                pass
            else:
                pick = rd.randrange(len(pick_index))
                if pick_index[pick] == 9: # 남은 컵 중 선택
                    pick = str(size)
                else: # 보드에 놓인 컵 중 선택
                    pick = "9" + str(pick_index[pick]) 
                move = rd.randrange(len(move_index))
                move = move_index[move]
                return pick + " " + str(move)
            
        return "random_bot_error"
