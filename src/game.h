#ifndef __GAME_H__
#define __GAME_H__ 1
#include "matrice.h"

// Core
extern matrice start_game(int); // Sets the default board
extern int valid_board(matrice);

extern int placeable_square(int, int);

extern int find_pawns_moves(matrice, TurnEnum for_player, int ** xs, int ** ys);
extern int find_squares_move(matrice, TurnEnum, int, int, int **, int **);
extern int move_pawn(matrice, TurnEnum, int, int, int, int);

extern int find_pawn_takes(matrice, TurnEnum for_player, int ** xs, int ** ys);
extern int find_takes_pawn(matrice, TurnEnum, int, int, int **, int **);

extern int find_promotables(matrice, TurnEnum, int ** xs, int ** ys);

extern void end_game(matrice, TurnEnum);

// Utils
extern void clear_screen();

// Engine

extern void cycle(matrice);

#endif
