#include <stdlib.h>
#include <stdio.h>
#include "matrice.h"

#define METADATA_SIZE sizeof(int) + sizeof(char) + sizeof(char)

matrice create_matrice(int size) {
	size_t allocated = METADATA_SIZE + size * size;
	matrice m;
	if ((m = malloc(allocated)) == NULL) return NULL;
	size_t i = 0;
	while (i < allocated) {
		*(char *)((void *)m + i++) = 0;
	}

	m[0] = size;
	*((char *)(void *)m + sizeof(int)) = 0; // Tour
	*((char *)(void *)m + sizeof(char) + sizeof(int)) = 0; // Terminé

	return (char *)((void *)m + METADATA_SIZE);
}
char set_turn(matrice m, TurnEnum val) {
	return *((char *)(void *)m - sizeof(char) - sizeof(char)) = (char)val;
}
void destroy_matrice(matrice * p) {
	free((void *)(*p) - (METADATA_SIZE));
	*p = NULL;
}
int get_size(matrice m) {
	return *(char *)((void *)m - (METADATA_SIZE));
}
int in_matrice(int x, int y, int size) {
	return 0 <= x && x < size && 0 <= y && y < size;
}

TurnEnum get_turn(matrice m) {
	return *((char *)((void *)m - sizeof(char) - sizeof(char)));
}
TurnEnum switch_turn(matrice m) {
	TurnEnum turn = get_turn(m);
	return *((char *)((void *)m -  sizeof(char) - sizeof(char))) = turn == White ? Black : White;
}
char get_pos(matrice m, int x, int y) {
	int size = get_size(m);
	if (!in_matrice(x, y, size)) return -1;
	return *(m + x * size + y);
}
int set_pos(matrice m, int x, int y, char v) {
	int size = get_size(m);
	if (!in_matrice(x, y, size)) return 0;

	*(m + x * size + y) = v;
	return 1;
}

char get_ended(matrice m) {
	return *((char *)(void *)m - sizeof(char));
}
char set_ended(matrice m, char ended) {
	return *((char *)(void *)m - sizeof(char)) = ended;
}
