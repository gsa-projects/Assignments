#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include <time.h>
#include <stdbool.h>
#include <Windows.h>

#define DOL_YOU "⬤ "
#define DOL_BOT "◯ "
#define AROUND 2

typedef enum key {
    ENTER = 13,
    ARROW = -32,
    ARROW_UP = 72,
    ARROW_LEFT = 75,
    ARROW_RIGHT = 77,
    ARROW_DOWN = 80
} key;

typedef enum stat {
    EMPTY, YOU, BOT, WALL
} stat;

typedef enum color {
    BLACK, BLUE, GREEN, TEAL, RED, PURPLE, YELLOW, WHITE, GRAY,
    BRIGHT_BLUE, BRIGHT_GREEN, BRIGHT_TEAL, BRIGHT_RED, BRIGHT_PURPLE, BRIGHT_YELLOW,
    DEEP_WHITE
} color;

typedef struct coord {
    int row;
    int col;
} coord;

typedef struct grid {
    coord pos;
    stat stat;
    int weight;
} grid;

coord get_bot(coord cursor);
coord best_choice(coord pos1, coord pos2);
coord best_choiceof(coord* choices, int len);
stat get_stat(int row, int col);
int is_around(coord pos);
int is_around_s(coord pos, stat s);
int random(int a, int b); int dist(coord c1, coord c2);
bool is_none(coord pos);
bool is_equal(coord pos1, coord pos2);
bool is_in(coord pos, coord* crds, int len);
void game_status_reload();
void set_pos(coord* pos, int r, int c);
void print_board(coord cursor);
void cursor_move(coord* cursor, char key);
void go(int x, int y);
void set_color(int color);