import random as rd

class Bot:
    def find_winning_move(self, board, player):
        lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in lines:
            pieces = [board[i] for i in line]
            count_player = sum(1 for p in pieces if p.startswith(player))
            count_empty = sum(1 for p in pieces if p[1] == ' ')
            if count_player == 2 and count_empty == 1:
                for i in line:
                    if board[i][1] == ' ':
                        return i
        return -1

    def get_move(self, board, pieces, player):
        s = pieces.split(",")
        x_pieces = s[0][1:]
        o_pieces = s[1][1:]
        my_pieces = x_pieces if player == 'X' else o_pieces
        opponent = 'O' if player == 'X' else 'X'

        corners = [0, 2, 6, 8]
        opposite_corner = {0:8, 2:6, 6:2, 8:0}
        center = 4

        # 1) 우리 이기는 수 우선 둠
        win_pos = self.find_winning_move(board, player)
        if win_pos != -1:
            for size in [3, 2, 1]:
                if str(size) in my_pieces:
                    pick = str(size)
                    return pick + " " + str(win_pos)

        # 2) 상대 이기는 수 막기
        block_pos = self.find_winning_move(board, opponent)
        if block_pos != -1:
            for size in [3, 2, 1]:
                if str(size) in my_pieces:
                    pick = str(size)
                    return pick + " " + str(block_pos)

        # 3) 기본 전략 시작
        size_order = [3, 1, 2]

        for size in size_order:
            if str(size) not in my_pieces:
                continue

            pick_index = []
            move_index = []

            for i in range(9):
                cup = board[i][:2]
                if cup == player + str(size):
                    pick_index.append(i)
                if cup[1] == ' ':
                    move_index.append(i)
                else:
                    try:
                        if int(cup[1]) < size:
                            move_index.append(i)
                    except:
                        pass

            if str(size) in my_pieces:
                if rd.randrange(2) == 0:
                    pick_index.append(9)
                else:
                    pick_index = [9]

            if len(pick_index) == 0 or len(move_index) == 0:
                continue

            # 모서리 전략
            my_corners = [c for c in corners if board[c].startswith(player)]
            if not my_corners:
                empty_corners = [c for c in corners if (board[c][1] == ' ' or (board[c][1] != ' ' and int(board[c][1]) < size))]
                if empty_corners:
                    move_pos = empty_corners[0]
                    pick_pos = 9 if 9 in pick_index else pick_index[0]
                    pick = str(size) if pick_pos == 9 else "9" + str(pick_pos)
                    return pick + " " + str(move_pos)
            elif len(my_corners) == 1:
                opp = opposite_corner[my_corners[0]]
                if board[opp][1] == ' ' or (board[opp][1] != ' ' and int(board[opp][1]) < size):
                    pick_pos = 9 if 9 in pick_index else pick_index[0]
                    pick = str(size) if pick_pos == 9 else "9" + str(pick_pos)
                    return pick + " " + str(opp)

            if board[center][1] == ' ' or (board[center][1] != ' ' and int(board[center][1]) < size):
                pick_pos = 9 if 9 in pick_index else pick_index[0]
                pick = str(size) if pick_pos == 9 else "9" + str(pick_pos)
                return pick + " " + str(center)

            # 상대 컵 위 덮어씌우기 (특히 낚시용 작은 컵도 활용)
            threat_positions = []
            for pos in move_index:
                if board[pos].startswith(opponent):
                    try:
                        if int(board[pos][1]) < size:
                            threat_positions.append(pos)
                    except:
                        pass

            if threat_positions:
                move_pos = threat_positions[0]
                pick_pos = 9 if 9 in pick_index else pick_index[0]
                pick = str(size) if pick_pos == 9 else "9" + str(pick_pos)
                return pick + " " + str(move_pos)

            # 마지막 fallback
            pick_pos = 9 if 9 in pick_index else pick_index[0]
            move_pos = move_index[0]
            pick = str(size) if pick_pos == 9 else "9" + str(pick_pos)
            return pick + " " + str(move_pos)

        return "random_bot_error"
