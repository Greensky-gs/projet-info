#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrice.h"
#include "preview.h"
#include "game.h"
#include "prompt.h"

void clear_screen() {
	printf("\e[1;1H[\e[2J");	
}

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
	while ((c = getchar()) != EOF && c != '\n' && c != 0);
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
			printf("Une erreur a eu lieu lors de la lecture de votre entrée\n");
			continue;
		}
		if (strchr(read, '\n') == NULL) empty_stdin();

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
static int prompt_square(matrice board, TurnEnum player, int x, int y, int * dx, int * dy) {
	int valid = 0;
	int moves;
	int * xs, * ys;
	int sx, sy;
	int size = get_size(board);

	if ((moves = find_squares_move(board, player, x, y, &xs, &ys)) <= 0) return -1;
	char mvbuffer[4] = {0};
	char rdbuffer[4] = {0};

	while (!valid) {
		display_move(mvbuffer, x, y);
		printf("Choisissez une case pour le pion \x1b[33m%s\x1b[0m :\n ", mvbuffer);
		int i = 0;
		while (i < moves) {
			display_move(mvbuffer, xs[i], ys[i]);
			i++;
			printf("\x1b[91m%s\x1b[0m ", mvbuffer);
		}
		printf("\n>> ");
		fflush(stdout);

		if (fgets(rdbuffer, 3, stdin) == NULL) {
			printf("Une erreur a eu lieu lors de votre saisie\n");
			continue;
		}
		if (strchr(rdbuffer, '\n') == NULL) empty_stdin();

		sx = rdbuffer[0] - 65;
		sy = rdbuffer[1] - 49;

		if (sx >= size || sx < 0 || sy >= size || sy < 0) {
			printf("Votre saisie n'est pas valide\n");
			continue;
		}

		int find_index = 0;
		while (find_index < moves && !valid) {
			if (sx == xs[find_index] && sy == ys[find_index]) {
				valid = 1;
			}
			find_index++;
		}
		if (!valid) {
			printf("Votre saisie n'est pas un des coups proposés, veuillez réessayer :\n");
		}
	}

	*dx = sx;
	*dy = sy;

	free(xs);
	free(ys);
	return 1;
}

void prompt_moves(matrice board, int size, TurnEnum turn, int moves_count, int * xs, int * ys) {
	printf("%s, choisissez un déplacement parmi ceux proposés \x1b[90m(%d)\x1b[0m :\n", player_name(turn), moves_count);

	int sx, sy;

	prompt_move_pawn(moves_count, size, xs, ys, &sx, &sy);

	int dx, dy;

	prompt_square(board, turn, sx, sy, &dx, &dy);

	move_pawn(board, turn, sx, sy, dx, dy);
}

static void prompt_capturing_pawn(matrice board, TurnEnum turn, int count, int * xs, int * ys, int * outputx, int * outputy) {
	int size = get_size(board);

	int sx, sy;
	char rdinput[4] = {0};
	char mvbuffer[4] = {0};

	int valid = 0;
	while (!valid) {
		printf("%s, choisissez un des pions pour capturer :\n", player_name(turn));
		int i = 0;
		while (i < count) {
			display_move(mvbuffer, xs[i], ys[i]);
			printf(" \x1b[31m%s\x1b[0m", mvbuffer);
			i++;
		}
		printf("\n> ");
		fflush(stdout);

		if (fgets(rdinput, 3, stdin) == NULL) {
			printf("Une erreur a eu lieu lors de la lecture\n");
			continue;
		}
		if (strchr(rdinput, '\n') == NULL) empty_stdin();

		int x = rdinput[0] - 65;
		int y = rdinput[1] - 49;

		if (x < 0 || x >= size || y < 0 || y >= size) {
			printf("Ce n'est pas une position valide.\n");
			continue;
		}

		i = 0;
		while (i < count && !valid) {
			if (xs[i] == x && ys[i] == y) {
				sx = x;
				sy = y;
				valid = 1;
			} else {
				i++;
			}
		}
		printf("x, y = (%d, %d)\n", x, y);

		if (!valid) printf("Veuillez choisir un des choix proposés\n");
	}

	*outputx = sx;
	*outputy = sy;
}
static void prompt_capture(matrice board, TurnEnum player, int x, int y, int count, int * xs, int * ys, int * outputx, int * outputy) {
	int size = get_size(board);
	int valid = 0;

	char mvbuffer[4] = {0};
	char rdinput[4] = {0};

	while (!valid) {
		display_move(mvbuffer, x, y);
		printf("%s, choisissez le pion que vous voulez capturer avec votre pion \x1b[33m%s\x1b[0m\n", player_name(player), mvbuffer);
		int i = 0;
		while (i < count) {
			display_move(mvbuffer, xs[i], ys[i]);
			printf(" \x1b[31m%s\x1b[0m", mvbuffer);
			i++;
		}
		printf("\n>> ");
		fflush(stdout);

		if ((fgets(rdinput, 4, stdin)) == NULL) {
			printf("Une erreur a eu lieu lors de la lecture\n");
			continue;
		}

		if (strchr(rdinput, '\n') == NULL) empty_stdin();

		int x = rdinput[0] - 65;
		int y = rdinput[1] - 49;

		if (x < 0 || x >= size || y < 0 || y >= size) {
			printf("Cette saisie n'est pas valide\n");
			continue;
		}

		i = 0;
		while (i < count && !valid) {
			if (xs[i] == x && ys[i] == y) {
				*outputx = x;
				*outputy = y;
				valid = 1;
			} else {
				i++;
			}
		}
		if (!valid) {
			printf("Veuillez choisir un pion parmi ceux proposés.\n");
		}
	}
}

static void prompt_captures(matrice board, TurnEnum turn, int count, int * xs, int * ys) {
	int pawnx, pawny;
	prompt_capturing_pawn(board, turn, count, xs, ys, &pawnx, &pawny);
	printf("Pawnx = %d, pawny = %d\n", pawnx, pawny);

	int capturedx, capturedy;

	int captureables_count;
	int * cxs, * cys;

	while ((captureables_count = find_takes_pawn(board, turn, pawnx, pawny, &cxs, &cys)) > 0) {
		clear_screen();
		preview(board);

		prompt_capture(board, turn, pawnx, pawny, captureables_count, cxs, cys, &capturedx, &capturedy);

		set_pos(board, capturedx, capturedy, 0);

		int dx = capturedx - pawnx;
		int dy = capturedy - pawny;

		set_pos(board, pawnx, pawny, 0);

		pawnx = pawnx + 2 * dx;
		pawny = pawny + 2 * dy;

		set_pos(board, pawnx, pawny, turn);

		free(cxs);
		free(cys);
	}
}

void prompt_player(matrice board) {
	TurnEnum turn = get_turn(board);
	int size = get_size(board);

	int * xs, *ys;
	int * capturesx = 0, *capturesy = 0;
	
	int captures_count = find_pawn_takes(board, turn, &capturesx, &capturesy);
	int moves_count = find_pawns_moves(board, turn, &xs, &ys);

	if (moves_count <= 0 && captures_count <= 0) {
		printf("%s, vous n'avez pas de coup\n", player_name(turn));
		set_ended(board, 1);
		end_game(board, turn == Black ? White : Black);
		return;
	}

	if (captures_count > 0) {
		prompt_captures(board, turn, captures_count, capturesx, capturesy);
	} else {
		prompt_moves(board, size, turn, moves_count, xs, ys);
	}

	if (captures_count > 0) {
		free(capturesy);
		free(capturesx);
	}
	if (moves_count > 0) {
		free(xs);
		free(ys);
	}
}
