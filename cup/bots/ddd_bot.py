import random as rd

class Bot:
    def get_move(self, board, peices, player):
        opponent = 'O' if player == 'X' else 'X'
        WINNING_LINES = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        # 남은 말 목록
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        my_peices = x_peices if player == 'X' else o_peices
        my_remain_sizes = [int(x) for x in my_peices]
        total_moves = sum(1 for b in board if b.strip())

        def center_empty():
            return board[4].strip() == ""

        # 특정 위치에 내 말 둘 수 있는 가장 큰 사이즈 선택
        def place_at_position(pos):
            for size in sorted(my_remain_sizes, reverse=True):
                top = board[pos].strip()
                if not top or int(top[1]) < size:
                    return f"{size} {pos}"
            return None

        # 즉시 승리 가능한 자리 찾기
        def find_winning_move(p):
            for line in WINNING_LINES:
                plays = [board[i] for i in line]
                owners = [x[0] if x.strip() else ' ' for x in plays]
                if owners.count(p) == 2 and owners.count(' ') == 1:
                    return line[owners.index(' ')]
            return None

        # 상대 말을 덮어서 승리 가능한 자리 찾기
        def find_dominating_win_move(board, player, my_remain_sizes):
            for line in WINNING_LINES:
                cells = [board[i].strip() for i in line]
                owners = [c[0] if c else " " for c in cells]
                if owners.count(player) == 2 and owners.count(opponent) == 1:
                    for idx, i in enumerate(line):
                        cell = board[i].strip()
                        if cell and cell[0] == opponent:
                            oppo_size = int(cell[1])
                            for size in sorted(my_remain_sizes, reverse=True):
                                if size > oppo_size:
                                    return f"{size} {i}"
            return None

        # 포크 중앙에 있는 상대 말을 L로 덮기 (패배하지 않을 때만)
        def detect_fork_center_to_eat(board, player, my_remain_sizes):
            center = 4
            cell = board[center].strip()
            if not cell or cell[0] != opponent:
                return None
            oppo_size = int(cell[1])
            if 3 not in my_remain_sizes:
                return None
            if oppo_size >= 3:
                return None

            # 시뮬레이션해서 상대가 이길 수 있는지 확인
            simulated = board[:]
            simulated[center] = player + '3'
            for line in WINNING_LINES:
                owners = [simulated[i][0] if simulated[i].strip() else ' ' for i in line]
                if owners.count(opponent) == 2 and owners.count(' ') == 1:
                    return None
            return f"3 {center}"

        # 귀에 포크 유도 전략
        def detect_corner_fork_opportunity(board, player):
            center = board[4].strip()
            if not center or center[0] != player or center[1] != '3':
                return None
            for corner in [0, 2, 6, 8]:
                cell = board[corner].strip()
                if cell and cell[0] == opponent and cell[1] == '3':
                    opposite = {0: 8, 2: 6, 6: 2, 8: 0}[corner]
                    if board[opposite].strip() == "":
                        return f"3 {opposite}"
            return None

        # 첫 수: 중앙이 비어있으면 L 놓기
        if total_moves == 0 and center_empty():
            return "3 4"

        # 포크 유도 전략 (2턴 차)
        if total_moves == 2:
            fork = detect_corner_fork_opportunity(board, player)
            if fork:
                return fork

        # 후공이고 중앙 비었으면 중앙에 L 놓기
        if total_moves == 1 and center_empty():
            if 3 in my_remain_sizes:
                return "3 4"

        # 즉시 승리 가능하면 실행
        win_idx = find_winning_move(player)
        if win_idx is not None:
            move = place_at_position(win_idx)
            if move:
                return move

        # 상대 말을 덮어서 승리 가능하면 실행
        dominating_win = find_dominating_win_move(board, player, my_remain_sizes)
        if dominating_win:
            return dominating_win

        # 포크 중앙 상대 말 L로 덮기 (안전한 경우만)
        fork_center_block = detect_fork_center_to_eat(board, player, my_remain_sizes)
        if fork_center_block:
            return fork_center_block

        # 상대 승리 막기
        block_move = self.smart_block(board, opponent, my_peices, board, player)
        if block_move:
            return block_move

        # 첫 수거나 두 번째 수면 귀 우선
        if total_moves <= 1:
            for pos in [0, 2, 6, 8]:
                move = place_at_position(pos)
                if move:
                    return move

        # 아무 전략 없을 경우 랜덤 수
        return self.random_move(board, my_peices, player)

    # 상대 승리 조건 차단
    def smart_block(self, board, opponent, my_remaining, board_state, my_player):
        WINNING_LINES = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        used = [int(b[1]) for b in board if b.strip() and b[0] == opponent]
        missing = [x for x in [3, 2, 1] if x not in used]
        oppo_max_possible = max(missing) if missing else 0
        my_remain_sizes = [int(s) for s in my_remaining]
        my_board_L_pos = None

        for i in range(9):
            if board[i].strip() == my_player + "3":
                my_board_L_pos = i

        for line in WINNING_LINES:
            owners = [board[i][0] if board[i].strip() else ' ' for i in line]
            if owners.count(opponent) == 2 and owners.count(' ') == 1:
                idx = line[owners.index(' ')]
                top = board[idx].strip()
                target_size = int(top[1]) if top else 0

                for size in sorted(my_remain_sizes, reverse=True):
                    if size >= oppo_max_possible and (not top or size > target_size):
                        return f"{size} {idx}"

                smallest = 4
                target_idx = -1
                for i in line:
                    if board[i].strip() and board[i][0] == opponent:
                        sz = int(board[i][1])
                        if sz < smallest:
                            smallest = sz
                            target_idx = i

                if 3 in my_remain_sizes:
                    return f"3 {target_idx}"
                elif my_board_L_pos is not None:
                    return f"93 {target_idx}"
        return None

    # 무작위 전략 (랜덤 봇)
    def random_move(self, board, pieces, player):
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
            if pieces.find(str(size)) > -1:
                if rd.randrange(2) == 0:
                    pick_index.append(9)
                else:
                    pick_index = [9]
            if len(pick_index) > 0 and len(move_index) > 0:
                pick = rd.choice(pick_index)
                pick_val = str(size) if pick == 9 else "9" + str(pick)
                move = rd.choice(move_index)
                return pick_val + " " + str(move)
            size += 1
        return "random_bot_error"
