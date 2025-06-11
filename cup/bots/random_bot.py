import random as rd

class Bot:
    def get_move(self, board, peices, player):
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        size = rd.randrange(1, 4)
        while size < 4:
            pick_index = []
            move_index = []
            for i in range(9):
                cup = board[i][:2]
                if cup == player + str(size):
                    pick_index.append(i)
                if cup[1] == ' ':
                    move_index.append(i)
                else:
                    if int(cup[1]) < size:
                        move_index.append(i)
            i = -1
            if player == 'X':
                i = x_peices.find(str(size))
            else:
                i = o_peices.find(str(size))
            if i > -1:
                if rd.randrange(2) == 0:
                    pick_index.append(9)
                else:
                    pick_index = [9] # 50% 확률로 새 컵 놓기
            
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

            size += 1
            
        return "random_bot_error"