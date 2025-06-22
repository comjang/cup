import random as rd

class Bot:
    def get_move(self, board, peices, player):
        opponent = 'O' if player == 'X' else 'X'
        s = peices.split(',')
        x_left = s[0][1:]
        o_left = s[1][1:]
        my_left = x_left if player == 'X' else o_left

        win_patterns = [
            [0,1,2], [3,4,5], [6,7,8],  # 가로
            [0,3,6], [1,4,7], [2,5,8],  # 세로
            [0,4,8], [2,4,6]            # 대각선
        ]

        board_state = [b[:2] for b in board]
        my_top = [board[i][0] if board[i][0] == player else ' ' for i in range(9)]
        opponent_top = [board[i][0] if board[i][0] == opponent else ' ' for i in range(9)]

        def can_place(size, pos):
            top = board[pos][1]
            return top == ' ' or int(top) < size

        def place_new(size, pos):
            return f"{size} {pos}"

        def move_existing(from_pos, to_pos):
            return f"{90 + from_pos} {to_pos}"

        # 🥇 1. 이기기 가능한 자리 찾기
        for pattern in win_patterns:
            marks = [my_top[i] for i in pattern]
            if marks.count(player) == 2 and marks.count(' ') == 1:
                empty = pattern[marks.index(' ')]
                for sz in ['3', '2', '1']:
                    if sz in my_left and can_place(int(sz), empty):
                        return place_new(sz, empty)
                # 움직일 수 있는 기존 컵으로 만들기
                for i in pattern:
                    if board[i][:2].startswith(player):
                        top = int(board[i][1])
                        for j in [empty]:
                            if can_place(top, j):
                                return move_existing(i, j)

        # 🛡️ 2. 막아야 하는 상대 삼목
        for pattern in win_patterns:
            marks = [opponent_top[i] for i in pattern]
            if marks.count(opponent) == 2 and marks.count(' ') == 1:
                empty = pattern[marks.index(' ')]
                for sz in ['3', '2', '1']:
                    if sz in my_left and can_place(int(sz), empty):
                        return place_new(sz, empty)
                # 내 컵 중 이동 가능한 걸로 방어
                for i in range(9):
                    if board[i][:2].startswith(player):
                        top = int(board[i][1])
                        if board[i][2:] == '' and can_place(top, empty):
                            return move_existing(i, empty)

        # ⚙️ 3. 기존 컵 이동해서 삼목 유도
        for pattern in win_patterns:
            marks = [my_top[i] for i in pattern]
            if marks.count(player) == 1 and marks.count(' ') == 2:
                for sz in ['3', '2', '1']:
                    for idx in pattern:
                        if sz in my_left and can_place(int(sz), idx):
                            return place_new(sz, idx)

        # 🔄 4. 남은 컵 랜덤 배치 (우선순위: 중앙 > 대각선 > 나머지)
        prefer = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for sz in ['3', '2', '1']:
            if sz in my_left:
                for idx in prefer:
                    if can_place(int(sz), idx):
                        return place_new(sz, idx)

        # 🔁 5. 마지막 수단 - 이동 가능한 컵 무작위 이동
        movable = []
        for i in range(9):
            if board[i][:2].startswith(player) and board[i][2:] == '':
                sz = int(board[i][1])
                for j in range(9):
                    if i != j and can_place(sz, j):
                        return move_existing(i, j)

        return "1 0"  # fallback