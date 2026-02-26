#ifndef __MATRICE_H__
#define __MATRICE_H__ 1

typedef enum {
	White = 'w',
	Black = 'n'
} TurnEnum;

typedef char * matrice;

extern matrice create_matrice(int);
extern void destroy_matrice(matrice *);

extern char set_char(matrice, char);
extern int get_size(matrice);
extern int in_matrice(int, int, int);
extern char get_pos(matrice, int, int);
extern int set_pos(matrice, int, int, char);
extern TurnEnum get_turn(matrice);
extern TurnEnum switch_turn(matrice);

#endif
