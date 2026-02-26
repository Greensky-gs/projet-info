#include <stdio.h>
#include <stdlib.h>
#include "matrice.h"
#include "preview.h"
#include "game.h"
#include "prompt.h"

int main() {
	matrice m = start_game(8);

	preview(m);

	prompt_player(m);

	destroy_matrice(&m);
}
