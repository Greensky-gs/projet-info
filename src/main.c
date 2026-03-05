#include <stdio.h>
#include <stdlib.h>
#include "matrice.h"
#include "preview.h"
#include "game.h"
#include "prompt.h"

int main() {
	matrice m = start_game(8);

	clear_screen();
	preview(m);

	while (1) {
		cycle(m);

		if (get_ended(m)) break;
	}

	destroy_matrice(&m);
}
