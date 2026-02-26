#include <stdio.h>
#include <stdlib.h>
#include "matrice.h"
#include "game.h"
#include "prompt.h"

static char * player_name(TurnEnum p) {
	if (p == White) return "\x1b[33mBlanc\x1b[0m";
	return "\x1b[33mNoir\x1b[0m";
}
static char * display_move(char mv[], int x, int y) {
	mv[0] = 65 + x;
   	mv[1] = 49 + y;

	return mv;	
}
static void empty_stdin() {
	int c;
	while ((c = getchar()) != 0 && c != '\n');
}

static void prompt_move_pawn(int moves_count, int size, int * xs, int * ys, int * x, int * y) {
	int valid = 0;
	int sx, sy;

	while (!valid) {
		int i = 0;
		char mv[3] = {0};
		while (i < moves_count) {
			display_move(mv, xs[i], ys[i]);
			printf("\x1b[31m%s\x1b[0m ", mv);

			i++;
		}
		printf("\n> ");
		fflush(stdout);

		char read[4] = {0};
		if (fgets(read, 3, stdin) == NULL) {
			empty_stdin();
			printf("Une erreur a eu lieu lors de la lecture de votre entrée\n");
			continue;
		}
		empty_stdin();

		sx = read[0] - 65;
		sy = read[1] - 49;

		if (sx >= size || sx < 0 || sy >= size || sy < 0) {
			printf("Votre saisie n'est pas valide\n");
			continue;
		}

		int find_index = 0;
		while (find_index < moves_count && !valid) {
			if (sx == xs[find_index] && sy == ys[find_index]) {
				valid = 1;
			}
			find_index++;
		}
		if (!valid) {
			printf("Votre saisie n'est pas un des coups proposés, veuillez réessayer :\n");
		}
	}

	*x = sx;
	*y = sy;
}

void prompt_player(matrice board) {
	TurnEnum turn = get_turn(board);
	int size = get_size(board);

	int * xs, *ys;
	int moves_count = find_pawns_moves(board, turn, &xs, &ys);

	if (moves_count <= 0) {
		printf("%s, vous n'avez pas de coup\n", player_name(turn));
		return;
	}

	printf("%s, choisissez un coup parmi ceux proposés \x1b[90m(%d)\x1b[0m :\n", player_name(turn), moves_count);

	int sx, sy;

	prompt_move_pawn(moves_count, size, xs, ys, &sx, &sy);


	free(xs);
	free(ys);
}
