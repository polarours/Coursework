#include "game.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "snake_utils.h"

/* Helper function definitions */
static void set_board_at(game_t *game, unsigned int row, unsigned int col, char ch);
static bool is_tail(char c);
static bool is_head(char c);
static bool is_snake(char c);
static char body_to_tail(char c);
static char head_to_body(char c);
static unsigned int get_next_row(unsigned int cur_row, char c);
static unsigned int get_next_col(unsigned int cur_col, char c);
static void find_head(game_t *game, unsigned int snum);
static char next_square(game_t *game, unsigned int snum);
static void update_tail(game_t *game, unsigned int snum);
static void update_head(game_t *game, unsigned int snum);

/* Task 1 */
game_t *create_default_game() {
  static const char *rows[] = {"####################",
                               "#                  #",
                               "# d>D    *         #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "#                  #",
                               "####################"};
  unsigned int num_rows = 18;
  unsigned int row_len = 21; /* 20 columns + newline + terminator */

  game_t *game = malloc(sizeof(game_t));
  if (game == NULL) {
    return NULL;
  }
  game->num_rows = num_rows;
  game->board = malloc(num_rows * sizeof(char *));
  if (game->board == NULL) {
    free(game);
    return NULL;
  }
  for (unsigned int i = 0; i < num_rows; i++) {
    game->board[i] = malloc(row_len * sizeof(char));
    strcpy(game->board[i], rows[i]);
    strcat(game->board[i], "\n");
  }
  /* The default board already contains one snake: tail at (2,2), head at (2,4). */
  game->num_snakes = 1;
  game->snakes = malloc(sizeof(snake_t));
  game->snakes[0].tail_row = 2;
  game->snakes[0].tail_col = 2;
  game->snakes[0].head_row = 2;
  game->snakes[0].head_col = 4;
  game->snakes[0].live = true;
  return game;
}

/* Task 2 */
void free_game(game_t *game) {
  if (game == NULL) {
    return;
  }
  for (unsigned int i = 0; i < game->num_rows; i++) {
    free(game->board[i]);
  }
  free(game->board);
  free(game->snakes);
  free(game);
}

/* Task 3 */
void print_board(game_t *game, FILE *fp) {
  for (unsigned int i = 0; i < game->num_rows; i++) {
    fprintf(fp, "%s", game->board[i]);
  }
}

/*
  Saves the current game into filename. Does not modify the game object.
  (already implemented for you).
*/
void save_board(game_t *game, char *filename) {
  FILE *f = fopen(filename, "w");
  print_board(game, f);
  fclose(f);
}

/* Task 4.1 */

/*
  Helper function to get a character from the board
  (already implemented for you).
*/
char get_board_at(game_t *game, unsigned int row, unsigned int col) { return game->board[row][col]; }

/*
  Helper function to set a character on the board
  (already implemented for you).
*/
static void set_board_at(game_t *game, unsigned int row, unsigned int col, char ch) {
  game->board[row][col] = ch;
}

/*
  Returns true if c is part of the snake's tail.
  The snake consists of these characters: "wasd"
  Returns false otherwise.
*/
static bool is_tail(char c) {
  return c == 'w' || c == 'a' || c == 's' || c == 'd';
}

/*
  Returns true if c is part of the snake's head.
  The snake consists of these characters: "WASDx"
  Returns false otherwise.
*/
static bool is_head(char c) {
  return c == 'W' || c == 'A' || c == 'S' || c == 'D' || c == 'x';
}

/*
  Returns true if c is part of the snake.
  The snake consists of these characters: "wasd^<v>WASDx"
*/
static bool is_snake(char c) {
  return is_tail(c) || is_head(c) || c == '^' || c == '<' || c == 'v' || c == '>';
}

/*
  Converts a character in the snake's body ("^<v>")
  to the matching character representing the snake's
  tail ("wasd").
*/
static char body_to_tail(char c) {
  switch (c) {
  case '^':
    return 'w';
  case '<':
    return 'a';
  case 'v':
    return 's';
  case '>':
    return 'd';
  default:
    return '?';
  }
}

/*
  Converts a character in the snake's head ("WASD")
  to the matching character representing the snake's
  body ("^<v>").
*/
static char head_to_body(char c) {
  switch (c) {
  case 'W':
    return '^';
  case 'A':
    return '<';
  case 'S':
    return 'v';
  case 'D':
    return '>';
  default:
    return '?';
  }
}

/*
  Returns cur_row + 1 if c is 'v' or 's' or 'S'.
  Returns cur_row - 1 if c is '^' or 'w' or 'W'.
  Returns cur_row otherwise.
*/
static unsigned int get_next_row(unsigned int cur_row, char c) {
  if (c == 'v' || c == 's' || c == 'S') {
    return cur_row + 1;
  }
  if (c == '^' || c == 'w' || c == 'W') {
    return cur_row - 1;
  }
  return cur_row;
}

/*
  Returns cur_col + 1 if c is '>' or 'd' or 'D'.
  Returns cur_col - 1 if c is '<' or 'a' or 'A'.
  Returns cur_col otherwise.
*/
static unsigned int get_next_col(unsigned int cur_col, char c) {
  if (c == '>' || c == 'd' || c == 'D') {
    return cur_col + 1;
  }
  if (c == '<' || c == 'a' || c == 'A') {
    return cur_col - 1;
  }
  return cur_col;
}

/*
  Task 4.2

  Helper function for update_game. Return the character in the cell the snake is moving into.

  This function should not modify anything.
*/
static char next_square(game_t *game, unsigned int snum) {
  snake_t *snake = &game->snakes[snum];
  char head = get_board_at(game, snake->head_row, snake->head_col);
  unsigned int row = get_next_row(snake->head_row, head);
  unsigned int col = get_next_col(snake->head_col, head);
  return get_board_at(game, row, col);
}

/*
  Task 4.3

  Helper function for update_game. Update the head...

  ...on the board: add a character where the snake is moving

  ...in the snake struct: update the row and col of the head

  Note that this function ignores food, walls, and snake bodies when moving the head.
*/
static void update_head(game_t *game, unsigned int snum) {
  snake_t *snake = &game->snakes[snum];
  char head = get_board_at(game, snake->head_row, snake->head_col);
  unsigned int new_row = get_next_row(snake->head_row, head);
  unsigned int new_col = get_next_col(snake->head_col, head);

  set_board_at(game, snake->head_row, snake->head_col, head_to_body(head));
  set_board_at(game, new_row, new_col, head);

  snake->head_row = new_row;
  snake->head_col = new_col;
}

/*
  Task 4.4

  Helper function for update_game. Update the tail...

  ...on the board: blank out the current tail, and change the new
  tail from a body character (^<v>) into a tail character (wasd)

  ...in the snake struct: update the row and col of the tail
*/
static void update_tail(game_t *game, unsigned int snum) {
  snake_t *snake = &game->snakes[snum];
  char tail = get_board_at(game, snake->tail_row, snake->tail_col);
  unsigned int next_row = get_next_row(snake->tail_row, tail);
  unsigned int next_col = get_next_col(snake->tail_col, tail);
  char body = get_board_at(game, next_row, next_col);

  set_board_at(game, snake->tail_row, snake->tail_col, ' ');
  set_board_at(game, next_row, next_col, body_to_tail(body));

  snake->tail_row = next_row;
  snake->tail_col = next_col;
}

/* Task 4.5 */
void update_game(game_t *game, int (*add_food)(game_t *game)) {
  for (unsigned int i = 0; i < game->num_snakes; i++) {
    snake_t *snake = &game->snakes[i];
    if (!snake->live) {
      continue;
    }

    char next = next_square(game, i);

    /* A wall or any part of a snake (including this one) kills the head. */
    if (next == '#' || is_snake(next)) {
      set_board_at(game, snake->head_row, snake->head_col, 'x');
      snake->live = false;
      continue;
    }

    update_head(game, i);

    if (next == '*') {
      add_food(game); /* eating grows the snake: the tail stays put */
    } else {
      update_tail(game, i);
    }
  }
}

/* Task 5.1 */
char *read_line(FILE *fp) {
  if (fp == NULL) {
    return NULL;
  }
  unsigned int capacity = 32;
  unsigned int length = 0;
  char *line = malloc(capacity * sizeof(char));
  if (line == NULL) {
    return NULL;
  }
  line[0] = '\0';

  while (fgets(line + length, (int)(capacity - length), fp) != NULL) {
    length += (unsigned int)strlen(line + length);
    if (length > 0 && line[length - 1] == '\n') {
      return line;
    }
    /* The buffer filled without reaching a newline: grow and keep reading. */
    capacity *= 2;
    char *bigger = realloc(line, capacity * sizeof(char));
    if (bigger == NULL) {
      free(line);
      return NULL;
    }
    line = bigger;
  }

  if (length == 0) {
    free(line);
    return NULL;
  }
  return line;
}

/* Task 5.2 */
game_t *load_board(FILE *fp) {
  if (fp == NULL) {
    return NULL;
  }
  unsigned int capacity = 8;
  unsigned int num_rows = 0;
  char **board = malloc(capacity * sizeof(char *));
  if (board == NULL) {
    return NULL;
  }

  char *line;
  while ((line = read_line(fp)) != NULL) {
    if (num_rows == capacity) {
      capacity *= 2;
      char **bigger = realloc(board, capacity * sizeof(char *));
      if (bigger == NULL) {
        free(line);
        for (unsigned int i = 0; i < num_rows; i++) {
          free(board[i]);
        }
        free(board);
        return NULL;
      }
      board = bigger;
    }
    board[num_rows] = line;
    num_rows++;
  }

  if (num_rows == 0) {
    free(board);
    return NULL;
  }

  game_t *game = malloc(sizeof(game_t));
  if (game == NULL) {
    for (unsigned int i = 0; i < num_rows; i++) {
      free(board[i]);
    }
    free(board);
    return NULL;
  }
  game->num_rows = num_rows;
  game->board = board;
  game->num_snakes = 0;
  game->snakes = NULL;
  return game;
}

/*
  Task 6.1

  Helper function for initialize_snakes.
  Given a snake struct with the tail row and col filled in,
  trace through the board to find the head row and col, and
  fill in the head row and col in the struct.
*/
static void find_head(game_t *game, unsigned int snum) {
  snake_t *snake = &game->snakes[snum];
  unsigned int row = snake->tail_row;
  unsigned int col = snake->tail_col;
  char c = get_board_at(game, row, col);

  while (!is_head(c)) {
    row = get_next_row(row, c);
    col = get_next_col(col, c);
    c = get_board_at(game, row, col);
  }

  snake->head_row = row;
  snake->head_col = col;
}

/* Task 6.2 */
game_t *initialize_snakes(game_t *game) {
  unsigned int count = 0;
  for (unsigned int r = 0; r < game->num_rows; r++) {
    for (unsigned int c = 0; game->board[r][c] != '\0' && game->board[r][c] != '\n'; c++) {
      if (is_tail(game->board[r][c])) {
        count++;
      }
    }
  }

  game->num_snakes = count;
  game->snakes = count > 0 ? malloc(count * sizeof(snake_t)) : NULL;

  unsigned int snum = 0;
  for (unsigned int r = 0; r < game->num_rows; r++) {
    for (unsigned int c = 0; game->board[r][c] != '\0' && game->board[r][c] != '\n'; c++) {
      if (is_tail(game->board[r][c])) {
        game->snakes[snum].tail_row = r;
        game->snakes[snum].tail_col = c;
        game->snakes[snum].live = true;
        find_head(game, snum);
        snum++;
      }
    }
  }

  return game;
}
