class Bot:

    def __init__(self):
        self.win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로
        [0, 4, 8], [2, 4, 6]  # 대각선
        ]

    # 삼목 완성 판정
    def is_win(self, board):
        for pattern in self.win_patterns:
            if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] == 1:
                return True
        return False
    
    # 이목 완성 판정
    def is_two(self, board):
        for pattern in self.win_patterns:
            if board[pattern[0]] + board[pattern[1]] + board[pattern[2]] >= 2:
                return True
        return False

    def get_move(self, board, peices, player):
        

        # 집을 수 있는 컵들, 움직일 수 있는 칸들 모두 구하기
        s = peices.split(",")
        if player == 'X':
            player_peices = s[0][1:]
            opp_peices = s[1][1:]
            opp = 'O'
        else:
            player_peices = s[1][1:]
            opp_peices = s[0][1:]
            opp = 'X'

        pick_index = [[],[],[]]
        move_index = [[],[],[]]
        for size in range(1,4):
            for i in range(9):
                cup = board[i][:2]
                if cup == player + str(size):
                    pick_index[size-1].append((i+1)*10+size)
                if cup[1] == ' ':
                    move_index[size-1].append(i)
                else:
                    if int(cup[1]) < size:
                        move_index[size-1].append(i)
            if player_peices.find(str(size)) > -1:
                pick_index[size-1].append(size)
        
        # 자신, 상대방 컵 위치
        player_board = [board[i][:1]==player for i in range(9)]
        opp_board = [board[i][:1]==opp for i in range(9)]

        # 상대 공격 막는 위치
        defense_point = []
        for pattern in self.win_patterns:
            if opp_board[pattern[0]] + opp_board[pattern[1]] + opp_board[pattern[2]] >= 2:
                defense_point.extend(pattern)


        # 움질일 수 있는 모든 경우 스코어 계산
        best_score = -10000
        global best_move
        for s in range(2,-1,-1):
            for pick in pick_index[s]:
                for move in move_index[s]:
                    score = 0

                    # 중앙, 모서리 점령
                    if move == 4:
                        score += 10
                        if pick%10 == 3:
                            score += 10
                    if move in [0,2,6,8]:
                        score += 5
                        if pick%10 == 3:
                            score +=5
                    if pick//10-1 == 4:
                        score -= 10
                        if pick%10 == 3:
                            score -= 10
                    if pick//10-1 in [0,2,6,8]:
                        score -= 5
                        if pick%10 == 3:
                            score -=5

                    # 상대방 컵 덮기
                    if board[move][0] == opp:
                        score += 10
                    if len(board[pick//10-1]) >= 3 and board[pick//10-1][2] == opp:
                        score -= 10

                    # 내 컵 풀어주기
                    if len(board[pick//10-1]) >= 3 and board[pick//10-1][2] == player:
                        score += 30
                    if board[move][0] == player:
                        score -= 30

                    # 상대 공격 방어
                    score += 1000*defense_point.count(move)
                    
                    # 승리
                    player_board[move] = 1
                    board[move] = player+str(s)+board[move]
                    if pick>9:
                        player_board[pick//10-1] = 0
                        board[pick//10-1] = board[pick//10-1][2:]
                    if self.is_win(player_board):
                        score += 10000
                    
                    # 공격하기
                    if player == 'X':
                        for pattern in self.win_patterns:
                            if move in pattern and player_board[pattern[0]] + player_board[pattern[1]] + player_board[pattern[2]] >= 2:
                                for i in range(3):
                                    if player_board[pattern[i]] == 0:
                                        if opp_board[pattern[i]] == 0:
                                            score+=100
                                        elif int(board[pattern[i]][1]) < 3 and int(board[pattern[(i+1)%3]][1])+int(board[pattern[(i+2)%3]][1]) < 6:
                                            score+=100
                                        break

                    # 컵 이동하면 상대가 연속 두개 완성
                    for pattern in self.win_patterns:
                        if pick//10-1 in pattern and player_board[pattern[0]] + player_board[pattern[1]] + player_board[pattern[2]] == 0 and opp_board[pattern[0]] + opp_board[pattern[1]] + opp_board[pattern[2]] >= 2:
                            score -= 1000
                    player_board[move] = 0
                    board[move] = board[move][2:]
                    if pick>9:
                        player_board[pick//10-1] = 1
                        board[pick//10-1] = player+str(s)+board[pick//10-1]
                    
                    # 컵 들면 상대가 승리
                    if len(board[pick//10-1]) >= 3 and board[pick//10-1][2] == opp:
                        opp_board[pick//10-1] = 1
                        if self.is_win(opp_board):
                            score -= 20000
                        opp_board[pick//10-1] = 0

                    
                
                    if score > best_score:
                        best_score = score
                        if pick > 9:
                            best_move = f"9{pick//10-1} {move}"
                        else:
                            best_move = f"{pick} {move}"

        # 디버깅
        # print(best_score)
        # print(pick_index)
        # print(move_index)
        return best_move


