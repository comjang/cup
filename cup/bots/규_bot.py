import random as rd

class Bot:
    def get_move(self, board, peices, player):
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        opponent = 'O' if player == 'X' else 'X'
        my_peices = x_peices if player == 'X' else o_peices
        available_sizes = list(my_peices)

        
        for i in range(9):
            cup = board[i][:2]
            if cup[0] == opponent:
                opp_size = int(cup[1])
                bigger_cups = [int(size) for size in available_sizes if int(size) > opp_size]
                if bigger_cups:
                    best_size = min(bigger_cups)
                    return f"{best_size} {i}"  

        
        size = rd.randrange(1, 4)
        while size < 4:
            pick_index = []
            move_index = []

            for i in range(9):
                cup = board[i][:2]

                
                if cup == player + str(size):
                    under_cup = board[i][2:4]  
                    if under_cup[0] != opponent:
                        pick_index.append(i)

                
                if cup[1] == ' ' or (cup[0] != player and int(cup[1]) < size):
                    move_index.append(i)

            
            if str(size) in my_peices:
                if rd.randrange(100) < 80:
                    pick_index.append(9)
                else:
                    pick_index = [9]

            
            if 4 in move_index and len(pick_index) > 0:
                pick = pick_index[0]
                if pick == 9:
                    pick_str = "3"
                else:
                    pick_str = "9" + "3"
                return pick_str + " 4"

            
            if len(pick_index) == 0 or len(move_index) == 0:
                pass
            else:
                pick = rd.randrange(len(pick_index))
                if pick_index[pick] == 9: # 남은 컵 중 선택
                    pick = str(size)
                else: # 보드에 놓인 컵 중 선택
                    pick = "9" + str(pick_index[pick]) 
                    if pick == "934":
                        continue
                move = rd.randrange(len(move_index))
                move = move_index[move]
                

            size += 1

        return "random_bot_error"
