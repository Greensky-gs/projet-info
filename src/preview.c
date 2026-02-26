#include <stdio.h>
#include "matrice.h"
#include "game.h"
  
static void print_header(int size) {
	printf("    \x1b[91m");
	int j = 0;
	while (j++ < size) printf(" %d  ", j);
	printf("\x1b[0m\n");
		
	printf("   ╔");
	int i = 0;

	while (i++ < size - 1) printf("═══╦");

	printf("═══╗\n");
}
static void print_sep(int size) {
	printf("   ╠");
  

	int i = 0;
	while (i++ < size - 1) printf("═══╬");

	printf("═══╣\n");
}
static void print_footer(int size) {
	printf("   ╚");
	int i = 0;
	while (i++ < size - 1) printf("═══╩");

	printf("═══╝\n");
}


void preview(matrice m) {
	TurnEnum turn = get_turn(m);
	int size = get_size(m);

	print_header(size);

	int i = 0;
	while (i < size) {
		int j = 0;

		printf(" \x1b[91m%c\x1b[0m ", 65 + i);

		printf("║");
		while (j < size) {
			char c = get_pos(m, i, j);
			if (c == White) {
				printf(" ●");
			} else if (c == Black) {
				printf(" ○");
			} else {
				printf("  ");
			}
			printf(" ║");	
			j++;
		}

		if (turn == White && i == 7) printf("  <--");
		if (turn == Black && i == 0) printf("  <--");

		printf("\n");
		if (i < size - 1) print_sep(size);
		i++;
	}

	print_footer(size);
}
