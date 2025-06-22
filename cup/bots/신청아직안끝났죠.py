import random as rd

class Bot:
    def __init__(self):
        self.turn_count = 0

    def get_move(self, board, peices, player):
        self.turn_count += 1
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        my_peices = x_peices if player == 'X' else o_peices
        opponent = 'O' if player == 'X' else 'X'

        # ===  � ===
        if player == 'X':  #  �
            if self.turn_count == 1:
                if '3' in my_peices:
                    return "3 4"
            if self.turn_count == 2:
                last = self.find_opponent_last_move(board, opponent)
                if last in [0, 2, 6, 8]:  # ��
                    if board[last][1] in ['1', '2']:
                        if '3' in my_peices:
                            return f"3 {last}"
                    else:
                        mirror = 8 - last
                        if '2' in my_peices:
                            return f"2 {mirror}"
                elif last in [1, 3, 5, 7]:  # �
                    # 1� l1: �\ 0� 1� ��� 
                    if '3' in my_peices:
                        return "3 0"
            if self.turn_count == 3:
                moves = self.find_all_moves(board, opponent)
                if moves[0] in [0, 2, 6, 8] and moves[1] in [0, 2, 6, 8]:
                    if board[moves[1]][1] in ['1', '2']:
                        if '3' in my_peices:
                            return f"3 {moves[1]}"
                elif moves[0] in [0, 2, 6, 8] and moves[1] in [1, 3, 5, 7]:
                    if self.has_opponent_two_in_row(board, opponent):
                        pos = self.block_opponent_win(board, peices, player)
                        if pos:
                            return pos
                    else:
                        mirror = 8 - moves[1]
                        if '3' in my_peices:
                            return f"3 {mirror}"
                elif moves[0] in [1, 3, 5, 7] and board[moves[1]][0] == ' ':
                    if '3' in my_peices:
                        return f"3 0"
        else:  # ��
            if self.turn_count == 1:
                if '3' in my_peices:
                    return "3 1"
            if self.turn_count == 2:
                last = self.find_opponent_last_move(board, opponent)
                if board[last][1] in ['1', '2']:
                    if '3' in my_peices:
                        return f"3 {last}"

        # === � �:  0 �   � ===
        best_move = None
        best_score = -float('inf')
        for size in ['1', '2', '3']:
            if size not in my_peices:
                continue
            for pos in range(9):
                top = board[pos][:2]
                if top == '  ' or (top[0] != player and top[1] != ' ' and int(top[1]) < int(size)):
                    score = 0

                    for pattern in self.get_win_patterns():
                        if pos in pattern:
                            # � 0X
                            line = [board[i][:2] if i != pos else player + size for i in pattern]
                            players = [c[0] for c in line]
                            if players.count(player) == 3:
                                score += 1000
                            elif players.count(opponent) == 2 and players.count(' ') == 1:
                                score += 900
                            elif players.count(player) == 2 and players.count(opponent) == 0:
                                score += 100
                            elif players.count(player) == 1 and players.count(opponent) == 0:
                                score += 10

                    if top == '  ':
                        score += 1
                    if top[0] != ' ' and int(top[1]) < int(size):
                        score += 5

                    if score > best_score:
                        best_score = score
                        best_move = f"{size} {pos}"

        if best_move:
            return best_move

        return "random_bot_error"

    def get_win_patterns(self):
        return [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

    def find_smallest_available(self, peices, player):
        p = peices.split(",")
        my_peices = p[0][1:] if player == 'X' else p[1][1:]
        for size in ['1', '2', '3']:
            if size in my_peices:
                return size
        return '1'

    def find_largest_available(self, peices, player):
        p = peices.split(",")
        my_peices = p[0][1:] if player == 'X' else p[1][1:]
        for size in ['3', '2', '1']:
            if size in my_peices:
                return size
        return '3'

    def find_opponent_last_move(self, board, opponent):
        for i in range(8, -1, -1):
            if board[i][:1] == opponent:
                return i
        return -1

    def find_all_moves(self, board, opponent):
        return [i for i in range(9) if board[i][:1] == opponent]

    def has_opponent_two_in_row(self, board, opponent):
        for pattern in self.get_win_patterns():
            count = 0
            for idx in pattern:
                if board[idx][:1] == opponent:
                    count += 1
            if count == 2:
                return True
        return False

    def block_opponent_win(self, board, peices, player):
        opponent = 'O' if player == 'X' else 'X'
        for pattern in self.get_win_patterns():
            count = 0
            empty_idx = -1
            for idx in pattern:
                cup = board[idx][:2]
                if cup[0] == opponent:
                    count += 1
                elif cup[0] == ' ':
                    empty_idx = idx
            if count == 2 and empty_idx != -1:
                size = self.find_smallest_available(peices, player)
                return f"{size} {empty_idx}"
        return None
