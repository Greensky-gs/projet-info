#include <stdlib.h>
#include <stdio.h>
#include "game.h"
#include "prompt.h"
#include "matrice.h"
#include "preview.h"

static char * player_name(TurnEnum p) {
	if (p == White) return "\x1b[33mBlanc\x1b[0m";
	return "\x1b[33mNoir\x1b[0m";
}

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

	set_turn(board, White);

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

	if (count == 0) return 0;

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

int find_pawn_takes(matrice board, TurnEnum player, int ** xs, int ** ys) {
	int size = get_size(board);
	int count = 0;
	char opp = player == White ? Black : White;

	int i = 0;
	while (i < size) {
		int j = 0;
		while (j < size) {
			if (get_pos(board, i, j) != (char)player) {
				j++;
				continue;
			}
			char tl = get_pos(board, i - 1, j - 1);
			char tr = get_pos(board, i - 1, j + 1);
			char bl = get_pos(board, i + 1, j - 1);
			char br = get_pos(board, i + 1, j + 1);

			int a = tl == opp && get_pos(board, i - 2, j - 2) == 0;
			int b = tr == opp && get_pos(board, i - 2, j + 2) == 0;
			int c = bl == opp && get_pos(board, i + 2, j - 2) == 0;
			int d = br == opp && get_pos(board, i + 2, j + 2) == 0;

			if (a || b || c || d) count++;
			j++;
		}
		i++;
	}

	if (count == 0) return 0;

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
			if (get_pos(board, i, j) != (char)player) {
				j++;
				continue;
			}
			char tl = get_pos(board, i - 1, j - 1);
			char tr = get_pos(board, i - 1, j + 1);
			char bl = get_pos(board, i + 1, j - 1);
			char br = get_pos(board, i + 1, j + 1);

			int a = tl == opp && get_pos(board, i - 2, j - 2) == 0;
			int b = tr == opp && get_pos(board, i - 2, j + 2) == 0;
			int c = bl == opp && get_pos(board, i + 2, j - 2) == 0;
			int d = br == opp && get_pos(board, i + 2, j + 2) == 0;

			if (a || b || c || d) {
				(*xs)[index] = i;
				(*ys)[index] = j;
				index++;
			}
			j++;
		}
		i++;
	}

	return count;
}
int find_takes_pawn(matrice board, TurnEnum player, int x, int y, int ** xs, int ** ys) {
	int opp = player == White ? Black : White;
	char pawn = get_pos(board, x, y);

	if (pawn != (char)player) return -1;

	char tl = get_pos(board, x - 1, y - 1) == opp;
	char tr = get_pos(board, x - 1, y + 1) == opp;
	char bl = get_pos(board, x + 1, y - 1) == opp;
	char br = get_pos(board, x + 1, y + 1) == opp;

	int tlv = tl && get_pos(board, x - 2, y - 2) == 0;
	int trv = tr && get_pos(board, x - 2, y + 2) == 0;
	int blv = bl && get_pos(board, x + 2, y - 2) == 0;
	int brv = br && get_pos(board, x + 2, y + 2) == 0;

	int count = tlv + trv + blv + brv;

	if (count == 0) return 0;

	if ((*xs = malloc(sizeof(int) * count)) == NULL) return -1;
	if ((*ys = malloc(sizeof(int) * count)) == NULL) {
		free(*xs);
		return -1;
	}

		
	int index = 0;
	if (tlv) {
		(*xs)[index] = x - 1;
		(*ys)[index++] = y - 1;
	}
	if (trv) {
		(*xs)[index] = x - 1;
		(*ys)[index++] = y + 1;
	}
	if (blv) {
		(*xs)[index] = x + 1;
		(*ys)[index++] = y - 1;
	}
	if (brv) {
		(*xs)[index] = x + 1;
		(*ys)[index++] = y + 1;
	}

	return count;
}

int find_promotables(matrice board, TurnEnum player, int ** xs, int ** ys) {
	int size = get_size(board);

	int white_trow = 0;
	int black_trow = size - 1;
	int row = player == White ? white_trow : black_trow;

	int count = 0;

	int j = 0;
	while (j < size) {
		if (get_pos(board, row, j) == (char)player) count++;
		j++;
	}

	if (count == 0) return 0;

	if ((*xs = malloc(sizeof(int) * count)) == NULL) return -1;
	if ((*ys = malloc(sizeof(int) * count)) == NULL) {
		free(*xs);
		return -1;
	}

	j = 0;
	int index = 0;
	while (j < size) {
		if (get_pos(board, row, j) == (char)player) {
			(*xs)[index] = row;
			(*ys)[index] = j;
			index++;
		}
		j++;
	}

	return count;
}

static int find_closest_to(matrice board, int x, int y, int * ox, int * oy) {
	long int max = 0;
	int size = get_size(board);
	char pawn = get_pos(board, x, y);
	if (pawn <= 0) return 0;

	TurnEnum opp = pawn == White ? Black : White;
	int i = 0;
	while (i < size) {
		int j = 0;
		while (j < size) {
			if (get_pos(board, i, j) == (char)opp) {
				if (max == 0) {
					max = (x - i) * (x - i) + (y - j) * (y - j);
					*ox = i;
					*oy = j;
				} else {
					long int dist = (x - i) * (x - j) + (y - j) * (y -j);
					if (dist < max) {
						*ox = i;
						max = dist;
						*oy = j;
					}
				}
			}
			j++;
		}
		i++;
	}

	return max != 0;
}
static void find_first_free(matrice board, TurnEnum player, int * x, int * y) {
	int size = get_size(board);
	int i = player == White ? size - 1 : 0;
	int delta = player == White ? 1 : -1;

	while (i >= 0 && i < size) {
		int j = player == White ? 0 : size - 1;
		while (j < size && j >= 0) {
			if (placeable_square(i, j) && get_pos(board, i, j) == 0) {
				*x = i;
				*y = j;
				return;
			}
			j += delta;
		}
		i -= delta;
	}
}

void cycle(matrice board) {
	prompt_player(board);

	if (get_ended(board)) return;

	int promoteables;
	int * xs, * ys;
	if ((promoteables = find_promotables(board, get_turn(board), &xs, &ys)) > 0) {
		int i = 0;
		while (i < promoteables) {
			int x = xs[i];
			int y = ys[i];

			int tx, ty;
			if (find_closest_to(board, x, y, &tx, &ty)) {
				set_pos(board, tx, ty, 0);

				int fx, fy;
				find_first_free(board, get_turn(board), &fx, &fy);
				set_pos(board, x, y, 0);
				set_pos(board, fx, fy, get_turn(board));
			}

			i++;
		}

		free(xs);
		free(ys);
	}

	switch_turn(board);
	clear_screen();

	preview(board);
}

void end_game(matrice game, TurnEnum winner) {
	printf("\x1b[33m%s\x1b[0m a gagné !\n", player_name(winner));
}
