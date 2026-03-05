#include <stdio.h>
#include "matrice.h"
#include "game.h"

#ifdef _WIN32
	#include <windows.h>
#else
	#include <unistd.h>
	#include <sys/ioctl.h>
#endif

static void get_terminal_size(int * rows, int * cols) {
#ifdef _WIN32
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
	*cols = csbi.srWindow.right - csbi.srWindow.left + 1;
	*rows = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
#else
	struct winsize w;
	ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
	*rows = w.ws_row;
	*cols = w.ws_col;
#endif
}

static void print_top(int size) {
	printf("    \x1b[91m ");
	int j = 0;
	while (j++ < size) printf("%d ", j);
	printf("\x1b[0m\n");

	printf("   ╔");
	int i = 0;
	while (i++ < size) printf("══");

	printf("╗\n");
}
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
static void print_bottom(int size) {
	printf("   ╚");
	int i = 0;
	while (i++ < size) printf("══");

	printf("╝\n");
}
static void print_footer(int size) {
	printf("   ╚");
	int i = 0;
	while (i++ < size - 1) printf("═══╩");

	printf("═══╝\n");
}

static void print_pawn(matrice m, int i, int j, int with_space) {
	if (with_space) printf(" ");
	char c = get_pos(m, i, j);
	if (c == White) {
		printf("●");
	} else if (c == Black) {
		printf("○");
	} else {
		printf(" ");
	}
}


static void preview_quadrillage(matrice m) {
	TurnEnum turn = get_turn(m);
	int size = get_size(m);

	print_header(size);

	int i = 0;
	while (i < size) {
		int j = 0;

		printf(" \x1b[91m%c\x1b[0m ", 65 + i);

		printf("║");
		while (j < size) {
			print_pawn(m, i, j, 1);
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

static void preview_reduced(matrice m) {
	int size = get_size(m);
	TurnEnum turn = get_turn(m);
	print_top(size);

	int i = 0;
	while (i < size) {
		int j = 0;
		printf(" \x1b[91m%c\x1b[0m ", 65 + i);

		printf("║");
		while (j < size) {
			print_pawn(m, i, j, 1);
			j++;
		}

		printf("║");
		if (turn == White && i == 7) printf("  <--");
		if (turn == Black && i == 0) printf("  <--");

		printf("\n");

		i++;
	}

	print_bottom(size);
}

void preview(matrice m) {
	int rows, cols;
	get_terminal_size(&rows, &cols);

	int board_size = get_size(m);
	int total_size = board_size * 3 + board_size + 4;
	if (total_size <= cols) preview_quadrillage(m);
	else preview_reduced(m);
}
