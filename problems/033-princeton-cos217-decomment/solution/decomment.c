/*
 * decomment.c
 *
 * A filter that removes C90 comments from standard input, replacing each
 * comment with a single space and preserving the original line numbering.
 *
 * The program is a deterministic finite automaton: every input character
 * causes exactly one state transition, and the state determines what (if
 * anything) is written to standard output. No global variables are used;
 * all state travels through the Ctx struct passed by pointer.
 */

#include <stdio.h>
#include <stdlib.h>

enum State {
    ST_NORMAL,       /* ordinary source text                        */
    ST_SLASH,        /* saw '/', waiting to see whether '*' follows  */
    ST_STRING,       /* inside a "..." literal                       */
    ST_STRING_ESC,   /* inside a "..." literal, after a backslash    */
    ST_CHARLIT,      /* inside a '...' literal                       */
    ST_CHARLIT_ESC,  /* inside a '...' literal, after a backslash    */
    ST_COMMENT,      /* inside a comment                             */
    ST_COMMENT_STAR  /* inside a comment, after a '*'                */
};

struct Ctx {
    enum State state;
    int line;          /* current input line, 1-based                  */
    int comment_line;  /* line on which the open comment started       */
};

/*
 * Advance the automaton by one character. Writes any surviving text to
 * stdout and returns the next state. ST_SLASH is handled by the caller
 * because deciding that a '/' did not open a comment requires processing
 * the same character twice.
 */
static enum State consume(struct Ctx *ctx, int c)
{
    switch (ctx->state) {

    case ST_NORMAL:
        if (c == '/') {
            return ST_SLASH;
        }
        if (c == '"') {
            putchar(c);
            return ST_STRING;
        }
        if (c == '\'') {
            putchar(c);
            return ST_CHARLIT;
        }
        putchar(c);
        return ST_NORMAL;

    case ST_COMMENT:
        if (c == '*') {
            return ST_COMMENT_STAR;
        }
        if (c == '\n') {
            putchar('\n');           /* keep the line count intact */
        }
        return ST_COMMENT;

    case ST_COMMENT_STAR:
        if (c == '/') {
            return ST_NORMAL;        /* comment closed */
        }
        if (c == '*') {
            return ST_COMMENT_STAR;  /* still looking at stars */
        }
        if (c == '\n') {
            putchar('\n');
        }
        return ST_COMMENT;

    case ST_STRING:
        putchar(c);
        if (c == '\\') {
            return ST_STRING_ESC;
        }
        if (c == '"') {
            return ST_NORMAL;
        }
        return ST_STRING;

    case ST_STRING_ESC:
        putchar(c);                  /* the escaped character is literal */
        return ST_STRING;

    case ST_CHARLIT:
        putchar(c);
        if (c == '\\') {
            return ST_CHARLIT_ESC;
        }
        if (c == '\'') {
            return ST_NORMAL;
        }
        return ST_CHARLIT;

    case ST_CHARLIT_ESC:
        putchar(c);
        return ST_CHARLIT;

    case ST_SLASH:
        break;                       /* handled in main */
    }

    return ST_NORMAL;                /* unreachable; keeps compilers quiet */
}

int main(void)
{
    struct Ctx ctx;
    int c;
    int fresh;      /* 1 when c has not yet been processed in this pass */
    int again;      /* 1 when the same c must be processed once more    */

    ctx.state = ST_NORMAL;
    ctx.line = 1;
    ctx.comment_line = 1;

    while ((c = getchar()) != EOF) {
        fresh = 1;
        do {
            again = 0;
            if (fresh && c == '\n') {
                ctx.line++;
            }
            fresh = 0;

            if (ctx.state == ST_SLASH) {
                if (c == '*') {
                    ctx.comment_line = ctx.line;
                    putchar(' ');        /* a comment is a token delimiter */
                    ctx.state = ST_COMMENT;
                } else {
                    putchar('/');        /* not a comment after all */
                    ctx.state = ST_NORMAL;
                    again = 1;           /* c still needs processing */
                }
                continue;
            }

            ctx.state = consume(&ctx, c);
        } while (again);
    }

    if (ctx.state == ST_SLASH) {
        putchar('/');               /* trailing slash with nothing after it */
    }

    if (ctx.state == ST_COMMENT || ctx.state == ST_COMMENT_STAR) {
        fprintf(stderr, "Error: line %d: unterminated comment\n",
                ctx.comment_line);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
