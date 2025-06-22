import random as rd

class Bot:
    def get_move(self, board, peices, player):
        s = peices.split(",")
        x_peices = s[0][1:]
        o_peices = s[1][1:]
        opponent = 'O' if player == 'X' else 'X'
        own_peices = x_peices if player == 'X' else o_peices

        def top_cup(cell):
            return cell[:2] if len(cell) >= 2 else '  '

        def can_place(size, cell):
            top = top_cup(board[cell])
            if top.strip() == '':
                return True
            return int(top[1]) < size

        def all_positions():
            return list(range(9))

        def available_new_sizes():
            return [int(x) for x in own_peices]

        def available_board_cups():
            cups = []
            for i in range(9):
                top = top_cup(board[i])
                if top[0] == player:
                    cups.append((int(top[1]), i))
            return cups

        def prefer_positions():
            return [4, 0, 2, 6, 8, 1, 3, 5, 7]

        def get_line(pos1, pos2):
            win_lines = [
                [0,1,2], [3,4,5], [6,7,8],
                [0,3,6], [1,4,7], [2,5,8],
                [0,4,8], [2,4,6]
            ]
            for line in win_lines:
                if pos1 in line and pos2 in line:
                    return line
            return []

        if '3' in own_peices and board[4] == '  ':
            return "3 4"

        for line in [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]:
            owner = [top_cup(board[i])[0] for i in line]
            if owner.count(opponent) == 2 and owner.count(' ') == 1:
                idx = line[owner.index(' ')]
                for sz in sorted(available_new_sizes(), reverse=True):
                    if can_place(sz, idx):
                        return f"{sz} {idx}"

        for (sz, from_pos) in available_board_cups():
            for to_pos in prefer_positions():
                if to_pos == from_pos:
                    continue
                if can_place(sz, to_pos):
                    return f"9{from_pos} {to_pos}"

        for sz in sorted(available_new_sizes(), reverse=True):
            for pos in prefer_positions():
                if can_place(sz, pos):
                    return f"{sz} {pos}"

        for (sz, from_pos) in available_board_cups():
            for to_pos in all_positions():
                if to_pos == from_pos:
                    continue
                if can_place(sz, to_pos):
                    return f"9{from_pos} {to_pos}"

        return "1 0"
