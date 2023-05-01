#include "omok.h"
#define ROW 19
#define COL 19
// #define DEBUG

int dols = 0;
stat game = EMPTY;
grid board[ROW][COL];
coord mok5_position[5] = {{-1,-1}, {-1,-1}, {-1,-1}, {-1,-1}, {-1,-1}};
coord last = { -1, -1 };

int main() {
    coord cursor = { ROW / 2, COL / 2 };  // 커서의 위치를 오목판 가운데로 초기화
    char input; // 키 입력 받을 변수

    // 오목판 초기화
    for (int i = 0; i < ROW; i++) {
        for (int j = 0; j < COL; j++) {
            board[i][j].pos.row = i;
            board[i][j].pos.col = j;
            board[i][j].stat = EMPTY;
            board[i][j].weight = 0;
        }
    }

    print_board(cursor);
    while (true) {
        if (!_kbhit()) continue;    // 키보드 입력을 받을 수 있을 때까지 반복

        input = _getch();
        switch (input) {
        case ARROW:
            input = _getch();

            system("cls");
            cursor_move(&cursor, input);
            print_board(cursor);

            break;
        case ENTER:
            switch (get_stat(cursor.row, cursor.col)) {
            case EMPTY:
                board[cursor.row][cursor.col].stat = YOU;
                dols++;
                system("cls");
                print_board(cursor);

                set_color(BRIGHT_BLUE);
                printf("\n\n[YOU]");
                set_color(WHITE);
                printf(" installed at (%d, %d)", cursor.row, cursor.col);

                coord bot = get_bot(cursor);
                last = bot;

#ifdef DEBUG
                char ip; printf("\nkeep going? "); ip = getchar();
                getchar();
#endif              
                Sleep(500);

                game_status_reload();

                if (game == YOU || game == BOT) {
                    system("cls");
                    print_board(cursor);

                    set_color(BRIGHT_YELLOW);
                    printf("\n\n[CMD] ");

                    set_color(game == YOU ? BRIGHT_BLUE : BRIGHT_RED);
                    printf("%s", game == YOU ? "You" : "Bot");

                    set_color(WHITE);
                    printf(" Win\n");
                    
                    set_color(BLACK);
                    return 0;
                }

                board[bot.row][bot.col].stat = BOT;

                game_status_reload();

                system("cls");
                print_board(cursor);

                if (game == YOU || game == BOT) {

                    set_color(BRIGHT_YELLOW);
                    printf("\n\n[CMD] ");

                    set_color(game == YOU ? BRIGHT_BLUE : BRIGHT_RED);
                    printf("%s", game == YOU ? "You" : "Bot");

                    set_color(WHITE);
                    printf(" Win\n");

                    set_color(BLACK);
                    return 0;
                }

                set_color(BRIGHT_RED);
                printf("\n\n[BOT]");
                set_color(WHITE);
                printf(" installed at (%d, %d)", bot.row, bot.col);
                break;

            default:
                system("cls");
                print_board(cursor);

                set_color(BRIGHT_YELLOW);
                printf("\n\n[CMD]");
                set_color(WHITE);
                printf(" Already installed");
                break;
            }
            break;
        }
    }
}

coord get_bot(coord cursor) {
    // todo: 막아야 하는 경우가 생겨도 자기가 이길 수 있는 경우 무시하고 공격
    // todo: 가중치가 빈틈 연속목에서 가장 높은 수를 가지게 하기
    // todo: 오목을 만들 수 없는 거리의 벽에서는 연속목을 하지 않게 하기

    coord choices[4] = {
        {-1, -1},
        {-1, -1},
        {-1, -1},
        {-1, -1}
    };
    coord final_choice = { -1, -1 };
    coord voids[4] = {
                    {-1, -1},
                    {-1, -1},
                    {-1, -1},
                    {-1, -1}
    };
    int changes[4][2] = {
        {0, 1}, {1, 0}, {1, -1}, {1, 1}
    };
    int cur_dols = 0;
#ifdef DEBUG
    char* letters[4] = { "-", "|", "/", "\\" };
#endif

    // 가중치 초기화
    for (int i = 0; i < ROW; i++)
        for (int j = 0; j < COL; j++)
            board[i][j].weight = 0;

    // 방어 및 가중치 부여
    for (int i = 0; i < ROW; ++i) {
        for (int j = 0; j < COL; ++j) {
            if (get_stat(i, j) == YOU) {
                cur_dols++;
                int counts[4] = { 0, 0, 0, 0 };

                // 연속목 체크
                for (int kind = 0; kind < 4; ++kind) {
                    for (int idx = 0; idx < 5; ++idx) {
                        coord crd = { i + changes[kind][0] * idx, j + changes[kind][1] * idx };
                        stat this = get_stat(crd.row, crd.col);
#ifdef DEBUG
                        //if (counts[kind] >= 3) printf("\n%s: (%d, %d) --%d-> (%d, %d)", letters[kind], i, j, counts[kind], i + changes[kind][0] * idx, j + changes[kind][1] * idx);
#endif // DEBUG
                        if (this == BOT) break;
                        else {
                            if (this == YOU)
                                counts[kind]++;
                            else if (this == EMPTY && is_none(voids[kind]) && get_stat(crd.row + changes[kind][0], crd.col + changes[kind][1]) == YOU)
                                voids[kind] = board[crd.row][crd.col].pos;
                            else break;
                        }
                    }
                    //if (counts[kind] < 3) set_pos(&voids[kind], -1, -1);
                }

#ifdef DEBUG
                if (counts[0] >= 3 || counts[1] >= 3 || counts[2] >= 3 || counts[3] >= 3) {
                    printf("\n(%d, %d) report: ", i, j);
                    printf("\n\t└ (-, |, /, \\) = (%d, %d, %d, %d)", counts[0], counts[1], counts[2], counts[3]);
                }
#endif

#ifdef DEBUG
                printf("\nvoid and count [%d(%d, %d), %d(%d, %d), %d(%d, %d), %d(%d, %d)]", counts[0], voids[0].row, voids[0].col, counts[1], voids[1].row, voids[1].col, counts[2], voids[2].row, voids[2].col, counts[3], voids[3].row, voids[3].col);
#endif // DEBUG

                // 연속목 방어
                for (int kind = 0; kind < 4; ++kind) {
                    if (counts[kind] == 5) {
                        game = YOU;
                        for (int t = 0; t < 5; ++t) {
                            set_pos(&mok5_position[t], i + t * changes[kind][0], j + t * changes[kind][1]);
                        }
                    }
                    else if (counts[kind] >= 3) {
                        if (!is_none(voids[kind]) && counts[kind] == 4) {
                            set_pos(&choices[kind], voids[kind].row, voids[kind].col);
                            continue;
                        }

                        coord next1 = { i - changes[kind][0], j - changes[kind][1] };
                        coord next2 = { i + (is_none(voids[kind]) ? 0 : 1) + counts[kind] * changes[kind][0], j + (is_none(voids[kind]) ? 0 : 1) + counts[kind] * changes[kind][1] };

                        bool isblock1 = get_stat(next1.row, next1.col) != EMPTY;
                        bool isblock2 = get_stat(next2.row, next2.col) != EMPTY;

                        if (!is_none(voids[kind]) && counts[kind] == 3 && !isblock1 && !isblock2) {
                            set_pos(&choices[kind], voids[kind].row, voids[kind].col);
                            continue;
                        }

                        if (!isblock1 && !isblock2)
                            choices[kind] = best_choice(next1, next2);
                        else if (!isblock1 && isblock2 && counts[kind] >= 4)
                            choices[kind] = next1;
                        else if (isblock1 && !isblock2 && counts[kind] >= 4)
                            choices[kind] = next2;
                    }
                }
            }
            else if (get_stat(i, j) == BOT) {
                int weightp = 0;

                for (int kind = 0; kind < 4; ++kind) {
                    weightp = 0;
                    for (int ip = i, jp = j; get_stat(ip, jp) != WALL; ip += changes[kind][0], jp += changes[kind][1]) {
                        if (i == ip && j == jp) continue;

                        if (get_stat(ip, jp) == YOU)
                            weightp = (weightp > 0) ? 0 : weightp - 1;
                        else if (get_stat(ip, jp) == BOT)
                            weightp++;

                        //weightp += max(AROUND + 1 - dist(board[i][j].pos, board[ip][jp].pos), 0);

                        board[ip][jp].weight += weightp;
                    }

                    weightp = 0;
                    for (int ip = i, jp = j; get_stat(ip, jp) != WALL; ip -= changes[kind][0], jp -= changes[kind][1]) {
                        if (i == ip && j == jp) continue;

                        if (get_stat(ip, jp) == YOU)
                            weightp = (weightp > 0) ? 0 : weightp - 1;
                        else if (get_stat(ip, jp) == BOT)
                            weightp++;

                        //weightp += max(AROUND + 1 - dist(board[i][j].pos, board[ip][jp].pos), 0);

                        board[ip][jp].weight += weightp;
                    }
                }
            }

            if (cur_dols >= dols) break;
        }
        if (cur_dols >= dols) break;
    }

    // 방어 착수 지점 선택
    final_choice = best_choice(choices[0], best_choice(choices[1], best_choice(choices[2], choices[3])));
#ifdef DEBUG
    printf("\nchoices = [(%d, %d), (%d, %d), (%d, %d), (%d, %d)] so choose (%d, %d)", choices[0].row, choices[0].col, choices[1].row, choices[1].col, choices[2].row, choices[2].col, choices[3].row, choices[3].col, final_choice.row, final_choice.col);
#endif // DEBUG

    // 착수
    if (!is_none(final_choice)) return final_choice;
    else {
        if (dols == 1) {
            coord ret = { -1, -1 };
            do {
                srand(time(NULL));
                set_pos(&ret, cursor.row + (rand() % 3) - 1, cursor.col + (rand() % 3) - 1);
            } while (get_stat(ret.row, ret.col) == WALL || (cursor.row == ret.row && cursor.col == ret.col));

            return ret;
        }
        else {
            grid max_pos = board[0][0];
            for (int i = 0; i < ROW; ++i)
                for (int j = 0; j < COL; ++j)
                    if (board[i][j].weight > max_pos.weight && get_stat(i, j) == EMPTY)
                        max_pos = board[i][j];

            int distance = is_around_s(board[0][0].pos, BOT);
            for (int i = 0; i < ROW; i++) {
                for (int j = 0; j < COL; j++) {
                    if (board[i][j].weight == max_pos.weight && is_around_s(board[i][j].pos, BOT) > distance && get_stat(i, j) == EMPTY) {
                        distance = is_around_s(board[i][j].pos, BOT);
                        max_pos = board[i][j];
                    }
                }
            }

            return max_pos.pos;
        }
    }
}

void game_status_reload() {
    if (game != EMPTY) return;

    int changes[4][2] = {
        {0, 1}, {1, 0}, {1, -1}, {1, 1}
    };

    for (int i = 0; i < ROW; ++i) {
        for (int j = 0; j < COL; j++) {
            if (get_stat(i, j) == BOT) {
                int counts[4] = { 0, 0, 0, 0 };

                for (int kind = 0; kind < 4; ++kind) {
                    for (int idx = 0; idx < 5; ++idx) {
                        coord crd = { i + changes[kind][0] * idx, j + changes[kind][1] * idx };
                        stat this = get_stat(crd.row, crd.col);

                        if (this != BOT) break;
                        else counts[kind]++;
                    }
                    
                    if (counts[kind] == 5) {
                        game = BOT;
                        for (int t = 0; t < 5; ++t) {
                            set_pos(&mok5_position[t], i + t * changes[kind][0], j + t * changes[kind][1]);
                        }
                        return;
                    }
                }
            }
        }
    }
}

coord best_choice(coord pos1, coord pos2) {
    int a = is_around_s(pos1, BOT), b = is_around_s(pos2, BOT);

    if (is_none(pos1)) return pos2;
    else if (is_none(pos2)) return pos1;
    else if (a == b) return random(a, b) == a ? pos1 : pos2;
    else return (a > b) ? pos1 : pos2;
}

coord best_choiceof(coord* choices, int len) {
    coord ret = choices[0];
    for (int i = 1; i < len; i++) {
        ret = best_choice(ret, choices[i]);
    }
    return ret;
}

int is_around(coord pos) {
    return is_around_s(pos, YOU) + is_around_s(pos, BOT);
}

int is_around_s(coord pos, stat s) {
    int cnt = 0;

    // todo: 범위 휴리스틱
    for (int i = pos.row - 1; i <= pos.row + 1; ++i)
        for (int j = pos.col - 1; j <= pos.col + 1; ++j)
            cnt += (get_stat(i, j) == s);

    return cnt - (get_stat(pos.row, pos.col) == s);
}

stat get_stat(int row, int col) {
    if (row >= ROW || row < 0) return WALL;
    else if (col >= COL || col < 0) return WALL;
    else return board[row][col].stat;
}

void print_board(coord cursor) {

    // todo: 방금 둔 돌 하이라이트
    // todo: 오목 하이라이트

    int idx;
    char* left[6] = { "└ ", "├ ", "┌ ", "┗ ", "┣ ", "┏ " };
    char* middle[6] = { "┴ ", "┼ ", "┬ ", "┻ ", "╋ ", "┳ " };
    char* right[6] = { "┘ ", "┤ ", "┐ ", "┛ ", "┫ ", "┓ " };

#ifdef DEBUG
    printf("dols: %d\n", dols);
#endif
    
#ifdef DEBUG
    printf(" ");
    set_color(GRAY);
    for (int i = 0; i < COL; i++)
        printf("%2d", i);

    printf("\n");
    for (int i = 0; i < ROW; ++i) {
        set_color(GRAY);
        printf("%2d", i);
        for (int j = 0; j < COL; ++j) {
            int iscursor = i == cursor.row && j == cursor.col;
            switch (get_stat(i, j)) {
            case YOU:
                set_color(BRIGHT_BLUE - 8 * iscursor);

                printf(DOL_YOU);
                break;
            case BOT:
                set_color(BRIGHT_RED - 8 * iscursor);

                printf(DOL_BOT);
                break;
            case EMPTY:
                if (iscursor) {
                    set_color(GREEN);
                    printf(DOL_YOU);
                }
                else {
                    set_color(board[i][j].weight > 0 ? YELLOW : board[i][j].weight == 0 ? WHITE : GRAY);
                    printf("%d ", abs(board[i][j].weight));
                }
                break;
            }
        }
        printf("\n");
    }
#endif
#ifndef DEBUG
        for (int i = 0; i < ROW; ++i) {
            for (int j = 0; j < COL; ++j) {
                int iscursor = i == cursor.row && j == cursor.col;
                int islast = i == last.row && j == last.col;

                switch (get_stat(i, j)) {
                case YOU:
                    set_color(iscursor ? WHITE : BRIGHT_BLUE);
                    if (is_in(board[i][j].pos, mok5_position, 5)) set_color(YELLOW);

                    printf(DOL_YOU);
                    break;  
                case BOT:
                    set_color(iscursor ? WHITE : (islast ? RED : BRIGHT_RED));
                    if (is_in(board[i][j].pos, mok5_position, 5)) set_color(YELLOW);

                    printf(DOL_BOT);
                    break;
                case EMPTY:
                    idx = (i == 0) ? 2 : (i == ROW - 1) ? 0 : 1;
                    if (iscursor) idx += 3;

                    set_color(iscursor ? WHITE : GRAY);

                    printf("%s", (j != 0 && j != COL - 1) ? middle[idx] : (j == 0) ? left[idx] : right[idx]);
                    break;
                }
            }
            printf("\n");
    }
#endif
}

void cursor_move(coord* cursor, char input) {
    switch (input) {
    case ARROW_UP:
        cursor->row = (cursor->row - 1 + ROW) % ROW;
        break;
    case ARROW_LEFT:
        cursor->col = (cursor->col - 1 + COL) % COL;
        break;
    case ARROW_RIGHT:
        cursor->col = (cursor->col + 1 + COL) % COL;
        break;
    case ARROW_DOWN:
        cursor->row = (cursor->row + 1 + ROW) % ROW;
        break;
    default:
        break;
    }
}

void set_pos(coord* pos, int r, int c) {
    pos->row = r;
    pos->col = c;
}

bool is_none(coord pos) {
    return pos.row == -1 && pos.col == -1;
}

bool is_equal(coord pos1, coord pos2) {
    return pos1.row == pos2.row && pos1.col == pos2.col;
}

bool is_in(coord pos, coord* crds, int len) {
    for (int i = 0; i < len; i++) {
        if (is_equal(pos, crds[i])) return true;
    }

    return false;
}

int dist(coord c1, coord c2) {
    return max(abs(c1.row - c2.row), abs(c1.col - c2.col));
}

int random(int a, int b) {
    srand(time(NULL));
    return (rand() % 2 == 0 ? a : b);
}

void go(int row, int col) {
    COORD Pos = { row - 1, col - 1 };
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), Pos);
}

void set_color(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}