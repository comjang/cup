class Bot:
    def get_move(self, board, pieces, player):
        opponent = 'O' if player == 'X' else 'X'
        p = pieces.split(",")
        x_pieces = p[0][1:]
        o_pieces = p[1][1:]
        my_pieces = x_pieces if player == 'X' else o_pieces
        op_pieces = o_pieces if player == 'X' else x_pieces

        def get_top(i):
            return board[i][:2] if board[i][1] != ' ' else "  "

        def can_place(size, pos):
            top = get_top(pos)
            if top[0] == player:
                return False
            return top[1] == ' ' or int(top[1]) < size


        def get_lines():
            return [
                [0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]
            ]

        def safe_block(size, pos):
            if not can_place(size, pos):
                return False
            temp_board = board[:]
            temp_board[pos] = player + str(size)
            for line in get_lines():
                line_vals = [temp_board[i] for i in line]
                owners = [v[0] if v[1] != ' ' else None for v in line_vals]
                if owners.count(opponent) == 2:
                    for i in line:
                        if temp_board[i][1] == ' ' or temp_board[i][0] == player:
                            continue
                        top_piece = temp_board[i]
                        if top_piece[0] == player:
                            continue
                        op_available = [int(s) for s in op_pieces if int(s) > int(top_piece[1])]
                        if op_available:
                            return False
            return True


        def movable_positions():
            return [i for i in range(9) if get_top(i)[0] == player]

        def exposes_opponent_win(from_pos):
            if len(board[from_pos]) < 4:
                return False
            below = board[from_pos][2:]
            if not below or below[0] != opponent:
                return False

            temp_board = board[:]
            temp_board[from_pos] = below if len(below) >= 2 else "  "

            # 상대가 이길 수 있는 라인이 실제로 생기는지 확인
            for line in get_lines():
                top_owners = [get_top(i)[0] for i in line]
                if top_owners.count(opponent) == 2 and top_owners.count(None) == 1:
                    return True
            return False

        def move_strategy_block():
            for from_pos in movable_positions():
                size = int(get_top(from_pos)[1])
                simulated_board = board[:]
                # 이동 시뮬레이션
                simulated_board[from_pos] = simulated_board[from_pos][2:] if len(simulated_board[from_pos]) > 2 else "  "

                for line in get_lines():
                    count_op = 0
                    empty_pos = -1
                    for i in line:
                        top = get_top(i)
                        if top[0] == opponent:
                            count_op += 1
                        elif top[0] is None:
                            empty_pos = i
                    if count_op == 2 and empty_pos != -1 and can_place(size, empty_pos):
                        # 상대가 이기기 직전인 줄을 막을 수 있으면
                        test_board = simulated_board[:]
                        test_board[empty_pos] = test_board[empty_pos] + player + str(size)
                        if not check_winner(test_board, opponent):  # 덮은 후 상대 승리 방지됨
                            return f"{size} {empty_pos} {from_pos}"
            return None
        
        def check_winner(sim_board, player_check):
            for line in get_lines():
                owners = [sim_board[i][0] if sim_board[i][1] != ' ' else None for i in line]
                if owners.count(player_check) == 3:
                    return True
            return False

    
        def try_move():
            # 2. 방어 시도 (정의된 함수 사용)
            block_move = move_strategy_block()
            if block_move:
                return block_move

            # 3. 줄 만들기 시도
            for from_pos in movable_positions():
                piece = get_top(from_pos)
                size = int(piece[1])
                original_stack = board[from_pos]

                board[from_pos] = board[from_pos][2:] if len(board[from_pos]) > 2 else "  "

                for line in get_lines():
                    if from_pos in line:
                        continue
                    owners = [get_top(i)[0] for i in line]
                    if owners.count(player) == 1 and owners.count(None) == 2:
                        for i in line:
                            if get_top(i)[0] is None and can_place(size, i) and not exposes_opponent_win(from_pos):
                                board[from_pos] = original_stack
                                return f"{size} {i} {from_pos}"

                # 4. 안전한 임의 이동
                for i in range(9):
                    if can_place(size, i) and not exposes_opponent_win(from_pos):
                        board[from_pos] = original_stack
                        return f"{size} {i} {from_pos}"

                board[from_pos] = original_stack  # 복구

            return None


        def strategy_win(size, _):
            for line in get_lines():
                count_me = 0
                count_none = 0
                target_idx = -1
                for i in line:
                    top = get_top(i)
                    if top[0] == player:
                        count_me += 1
                    elif top[0] == opponent:
                        continue
                    else:
                        count_none += 1
                        target_idx = i
                if count_me == 2 and count_none == 1 and can_place(size, target_idx):
                    return str(target_idx)
            for i in range(9):
                top = get_top(i)
                if top[0] == opponent:
                    top_size = int(top[1])
                    if size > top_size and can_place(size, i):
                        return str(i)
            return None

        def strategy_block(size, _):
            my_sizes = sorted([int(x) for x in my_pieces], reverse=True)
            op_sizes = sorted([int(x) for x in op_pieces], reverse=True)
            for line in get_lines():
                count_op = 0
                empty_pos = -1
                opponent_sizes_on_line = []
                for i in line:
                    top = get_top(i)
                    if top[0] == opponent:
                        count_op += 1
                        opponent_sizes_on_line.append(int(top[1]))
                    elif top[0] == player:
                        continue
                    else:
                        empty_pos = i
                if count_op == 2 and empty_pos != -1:
                    max_op = max(opponent_sizes_on_line)
                    bigger = [s for s in my_sizes if s > max_op]
                    if bigger and size == min(bigger) and can_place(size, empty_pos) and safe_block(size, empty_pos):
                        return str(empty_pos)
                    if 2 - op_pieces.count(str(max_op)) >= 2 and not any(s > max_op for s in op_sizes):
                        smaller = max_op - 1
                        if smaller in my_sizes and size == smaller and can_place(size, empty_pos) and safe_block(size, empty_pos):
                            return str(empty_pos)
                    poss = [s for s in my_sizes if s >= max_op]
                    if poss and size == max(poss) and can_place(size, empty_pos) and safe_block(size, empty_pos):
                        return str(empty_pos)
            return None

        def strategy_cover(size, _):
            if size != 3:
                return None
            for i in range(9):
                if get_top(i) == opponent + '2' and can_place(3, i):
                    return str(i)
            return None

        def strategy_build(size, _):
            for line in get_lines():
                owners = [board[i][0] if board[i][1] != ' ' else None for i in line]
                if owners.count(player) == 1 and owners.count(None) == 2:
                    for i in line:
                        if board[i][1] == ' ' and can_place(size, i):
                            return str(i)
            return None

        def strategy_any(size, _):
            for i in range(9):
                if can_place(size, i):
                    return str(i)
            return None

        place_strategies = [strategy_win, strategy_block, strategy_cover, strategy_build, strategy_any]
        if my_pieces:
            if len(my_pieces) == 6 and board[4][1] == ' ':
                return "1 4"

            for strategy in place_strategies:
                for s in sorted([int(x) for x in my_pieces]):
                    pos = strategy(s, -1)
                    if pos:
                        return f"{s} {pos}"
        else:
            result = try_move()
            if result:
                return result
