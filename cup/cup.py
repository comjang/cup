import multiprocessing
import time
import importlib
import os
import random as rd

class CupTacToe:
    def __init__(self):
        self.board = ['  '] * 9
        self.current_player = 'X'
        self.x_peices = '332211'
        self.o_peices = '332211'
        self.move_cnt = 0
        self.second_player = 'O'
    
    def display_board(self):
        b = ['  '] * 9
        for i in range(9):
            b[i] = self.board[i][0:2]
        print("\n".join([
            f" {b[0]} | {b[1]} | {b[2]} ",
            "----+----+----",
            f" {b[3]} | {b[4]} | {b[5]} ",
            "----+----+----",
            f" {b[6]} | {b[7]} | {b[8]}  [X{self.x_peices},O{self.o_peices}]"
        ]))
        # print(self.board)
    
    def pick_up(self, pick, size):
        if pick == 9:
            i = -1
            if self.current_player == 'X':
                i = self.x_peices.find(str(size))
            else:
                i = self.o_peices.find(str(size))
            if i < 0:
                return "pickup error: no peices: " + self.current_player
            else:
                if self.current_player == 'X':
                    self.x_peices = self.x_peices[:i] + self.x_peices[i+1:]
                else:
                    self.o_peices = self.o_peices[:i] + self.o_peices[i+1:]
                return self.current_player + str(size)
        elif 0 <= pick <= 8:
            cup = self.board[pick][:2]
            if cup[0] != self.current_player:
                return "pickup error: its not your cup! " + self.current_player
            else:
                self.board[pick] = self.board[pick][2:]
                return cup
        else:
            return "error: 0<=pick<=9 pick:" + str(pick)
    
    def make_move(self, move, cup):
        if 0 <= move < 9:
            top_cup = self.board[move][:2]
            if top_cup[1] != ' ':
                top_cup = int(top_cup[1])
            else:
                top_cup = 0
            if int(cup[1]) <= top_cup:
                return "move error: " + self.current_player
            else:
                self.board[move] = cup + self.board[move]
        else:    
            return "move error: 0<=pick<=9 move:" + str(move)
    
    def switch_palyer(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.move_cnt += 1
    
    def is_game_over(self):
        return self.get_winner() is not None
    
    def get_winner(self):
        if self.move_cnt > 30:
            return game.second_player
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로
            [0, 4, 8], [2, 4, 6]  # 대각선
        ]
        b = [' '] * 9
        for i in range(9):
            b[i] = self.board[i][0]
        for pattern in win_patterns:
            if b[pattern[0]] == b[pattern[1]] == b[pattern[2]] and b[pattern[0]] != ' ':
                return b[pattern[0]]
        return None

    def get_peices(self):
        return f"X{self.x_peices},O{self.o_peices}"

def load_bot(bot_name):
    try:
        module = importlib.import_module(f"bots.{bot_name}")
        return module.Bot()
    except ModuleNotFoundError:
        print(f"봇 {bot_name}을(를) 찾을 수 없습니다.")
        return None

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_log(play_mode, s):
    if play_mode != 4:
        print(s)


def long_running_task(q, bot, game):
    """실행 시간이 긴 작업"""
    result = bot.get_move(game.board, game.get_peices(), game.current_player)
    q.put(result)  # 결과를 큐에 저장

def run_with_timeout(timeout_sec, *args):
    q = multiprocessing.Queue()  # 결과를 저장할 큐
    process = multiprocessing.Process(target=long_running_task, args=(q, *args))
    process.start()

    process.join(timeout_sec)  # 지정한 시간 동안 대기
    if process.is_alive():
        process.terminate()  # 프로세스 강제 종료
        process.join()  # 안전한 종료
        print("타임아웃 발생! 프로세스를 강제 종료했습니다.")
        return None  # 타임아웃 발생 시 None 반환

    return q.get() if not q.empty() else None  # 결과 반환

def get_bot_name():
    script_file_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_file_path)
    # folder_path = os.getcwd()
    file_list = os.listdir(script_dir + "\\\\bots")
    file_list = [os.path.splitext(file)[0] for file in file_list if file.endswith(".py")]
    return file_list

# 프로그램 시작 지점
if __name__ == "__main__":
    
    clear_console()
    print("게임 모드를 선택해주세요.")

    player_x_is_bot = False
    player_o_is_bot = False

    print("1. 플레이어 vs 플레이어\n2. 플레이어 vs 인공지능\n3. 인공지능 vs 인공지능")
    play_mode = int(input())
    bot_x_name = ""
    bot_o_name = ""
    play_time = 1
    if play_mode == 1:
        player_x_is_bot = False
        player_o_is_bot = False
    elif play_mode == 2:
        bot_list = get_bot_name()
        for i in range(0, len(bot_list)):
            print(i, bot_list[i])
        while True:
            n = int(input("사용할 AI 봇의 번호를 입력하세요: "))
            if 0 <= n <= len(bot_list)-1:
                bot_x_name = bot_list[n]
                bot_o_name = bot_list[n]
                break
        bot = None
        if rd.randrange(2) == 0:
            player_x_is_bot = True
            player_o_is_bot = False
            bot = bot_x = load_bot(bot_x_name)
        else:
            player_x_is_bot = False
            player_o_is_bot = True
            bot = bot_o = load_bot(bot_o_name)
        if not bot:
            print("봇을 찾을 수 없습니다.")
    elif play_mode == 3:
        player_x_is_bot = True
        player_o_is_bot = True
        bot_list = get_bot_name()
        for i in range(0, len(bot_list)):
            print(i, bot_list[i])
        while True:
            n = int(input("첫번째 AI 봇의 번호를 입력하세요 "))
            if 0 <= n <= len(bot_list)-1:
                bot_x_name = bot_list[n]
                break
        while True:
            n = int(input("두번째 AI 봇의 번호를 입력하세요 "))
            if 0 <= n <= len(bot_list)-1:
                bot_o_name = bot_list[n]
                break
        bot_x = load_bot(bot_x_name)
        bot_o = load_bot(bot_o_name)
        play_time = int(input("플레이 횟수? : "))
        if play_time > 3: 
            play_mode = 4 # 인공지능 vs 인공지능 다회 플레이

    x_win_cnt = 0
    o_win_cnt = 0
    round = 0
    tutorial = True
    last_game_first_player = 'O'
    while round < play_time:
        game = CupTacToe()
        if last_game_first_player == 'X':
            game.current_player = 'O'
            game.second_player = 'X'
            last_game_first_player = 'O'
        else:
            game.current_player = 'X'
            game.second_player = 'O'
            last_game_first_player = 'X'
        while not game.is_game_over():
            if play_mode < 4:
                clear_console()
                if play_mode <= 2 and tutorial:
                    b = ['  '] * 9
                    for i in range(9):
                        b[i] = ' ' + str(i)
                    print("\n".join([
                        f" {b[0]} | {b[1]} | {b[2]} ",
                        "----+----+----",
                        f" {b[3]} | {b[4]} | {b[5]} ",
                        "----+----+----",
                        f" {b[6]} | {b[7]} | {b[8]}",
                        "--------------"
                    ]))
                    tutorial = False
                else:
                    game.display_board()
            bot_turn = False
            bot = None
            bot_name = ''
            if game.current_player == 'X' and player_x_is_bot:
                bot = bot_x
                bot_name = bot_x_name
                bot_turn = True
            elif game.current_player == 'O' and player_o_is_bot:
                bot = bot_o
                bot_name = bot_o_name
                bot_turn = True
            
            if bot_turn:
                if play_mode < 4:
                    input("인공지능 " + bot_name + "(" + game.current_player + ")의 차례입니다. 진행: Enter")
                exception = False
                exception_limit = 3
                while exception_limit > 0:
                    try:
                        test = ''
                        move = ''
                        if not exception:
                            move = run_with_timeout(3, bot, game) # time out: 1 sec
                        else:
                            # random bot
                            random_bot = load_bot("random_bot")
                            move = random_bot.get_move(game.board, game.get_peices(), game.current_player)
                        if not move.replace(" ", "").isnumeric():
                            raise ValueError("오류:" + move)
                        
                        size, move_to = map(int, move.split())
                        pick = 0
                        if 1 <= size <= 3:
                            pick = 9
                        elif size >= 90:
                            pick = size % 10
                        
                        result = game.pick_up(pick, size)
                        if result == "error":
                            raise ValueError("pick up 오류")
                        cup = result
                        
                        # 승패 검사
                        winner = game.get_winner()
                        if winner != None:
                            break
                        
                        result = ""
                        try_cnt = 0
                        try_max = 10
                        while try_cnt < try_max:
                            result = game.make_move(move_to, cup)
                            if result == "error":
                                move_to = (move_to + rd.randrange(1, 3)) % 9
                                try_cnt += 1
                            else:
                                break
                        if try_cnt == try_max:
                            # pick한 이후 오류 발생 > piece 분실
                            pass
                        
                        # 승패 검사
                        winner = game.get_winner()
                        if winner != None:
                            break
                        
                        game.switch_palyer()
                        break
                            
                    except Exception as e:  # 모든 예외를 처리
                        print_log(play_mode, f"예외 발생: {e}")
                        exception = True
                        # s = input() # stop program / or make random move
                        exception_limit -= 1
                        continue
                
            else:
                print(game.current_player + "의 차례입니다.")
                size = int(input("어느 컵? [1~3]새 컵 [9]놓인 컵: "))
                result = ""
                if 1 <= size <= 3:
                    result = game.pick_up(9, size)
                elif size == 9:
                    pick = int(input("어떤 컵? [0~8]: "))
                    result = game.pick_up(pick, size)
                else:
                    print_log(play_mode, "오류! 다시 선택하세요.")
                    continue
                
                if result == "error":
                    print_log(play_mode, "오류! 다시 선택하세요.")
                    continue # error
                cup = result
                
                # 승패 검사
                winner = game.get_winner()
                if winner != None:
                    break
                
                while True:
                    s3 = int(input("어디에? [0~8]: "))
                    result = game.make_move(s3, cup)
                    if result == "error":
                        print_log(play_mode, "오류! 다시 선택하세요.")
                        continue # error
                    else:
                        break
                
                # 승패 검사
                winner = game.get_winner()
                if winner != None:
                    break
            
                game.switch_palyer()

        if game.get_winner() == 'X':
            x_win_cnt += 1
        else:
            o_win_cnt += 1
            
        if play_mode < 4:
            game.display_board()
            print(f"게임 종료! {game.get_winner()}의 승리")
            #print(f"X {x_win_cnt}:{o_win_cnt} O")
            #input()
        elif play_mode == 4:
            clear_console()
            name_len = max(len(bot_o_name), len(bot_x_name))
            num_len = len(str(play_time))
            print(str(bot_x_name).rjust(name_len), str(x_win_cnt).rjust(num_len), "|" * int((x_win_cnt/play_time)*100))
            print(str(bot_o_name).rjust(name_len), str(o_win_cnt).rjust(num_len), "|" * int((o_win_cnt/play_time)*100))
                
        round += 1