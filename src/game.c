#include <stdlib.h>
#include "game.h"
#include "matrice.h"

int placeable_square(int x, int y) {
	return (x + y) % 2 == 1;
}

matrice start_game(int s) {
	matrice board;
	if ((board = create_matrice(s)) == NULL) return NULL;

	int i = 0;
	while (i < s) {
		int j = 0;
		while (j < s) {
			if (placeable_square(i, j)) {
				if (i < 3) set_pos(board, i, j, Black);
				if (i >= 5) set_pos(board, i, j, White);
			}
			j++;	
		}
		i++;
	}

	set_char(board, White);

	return board;
}

int valid_board(matrice m) {
	int i = 0;
	int s = get_size(m);
	while (i < s) {
		int j = 0;
		while (j < s) {
			char pos = get_pos(m, i, j);
			if (!placeable_square(i, j) && pos != 0) return 0;
			if (pos != 0 && pos != White && pos != Black) return 0;

			j++;	
		}
		i++;
	}
	return 1;	
}

int find_pawns_moves(matrice board, TurnEnum for_player, int ** xs, int ** ys) {
	int size = get_size(board);
	int coeff = for_player == White ? -1 : 1;

	int count = 0;
	int i = 0;
	while (i < size) {
		int j = 0;
		while (j < size) {
			char pawn = get_pos(board, i, j);
			
			if (pawn == (char)for_player) {
				char left = get_pos(board, i + coeff, j + 1);
				char right = get_pos(board, i + coeff, j - 1);

				if (left == 0 || right == 0) count++;
			}
			j++;
		}
		i++;
	}

	if ((*xs = malloc(sizeof(int) * count)) == NULL) return -1;
	if ((*ys = malloc(sizeof(int) * count)) == NULL) {
		free(*xs);
		return -1;
	}

	int index = 0;
	i = 0;
	while (i < size) {
		int j = 0;
		while (j < size) {
			char pawn = get_pos(board, i, j);

			if (pawn == (char)for_player && (get_pos(board, i + coeff, j + 1) == 0 || get_pos(board, i + coeff, j - 1) == 0)) {
				(*xs)[index] = i;
				(*ys)[index++] = j;
			}
			
			j++;
		}
		i++;
	}

	return count;
}
int find_squares_move(matrice board, TurnEnum player, int x, int y, int ** xs, int **ys) {
	char coeff = player == White ? -1 : 1;
	char pawn = get_pos(board, x, y);

	if (pawn != (char)player) return -1;

	char left = get_pos(board, x + coeff, y + 1);
	char right = get_pos(board, x + coeff, y - 1);
	int count = (left == 0) + (right == 0);

	if (count == 0) return 0;

	if ((*xs = malloc(sizeof(int) * count)) == NULL) return -1;
	if ((*ys = malloc(sizeof(int) * count)) == NULL) {
		free(*xs);
		return 0;
	}

	int i = 0;
	if (left == 0) {
		(*xs)[i] = x + coeff;
		(*ys)[i++] = y + 1;
	}
	if (right == 0) {
		(*xs)[i] = x + coeff;
		(*ys)[i++] = y - 1;
	}

	return i;
}
int move_pawn(matrice board, TurnEnum player, int x, int y, int tx, int ty) {
	char pawn = get_pos(board, x, y);
	if (pawn != (char)player) return 0;

	char dest = get_pos(board, tx, ty);
	if (dest != 0) return 0;

	set_pos(board, tx, ty, player);
	set_pos(board, x, y, 0);

	return 1;
}
