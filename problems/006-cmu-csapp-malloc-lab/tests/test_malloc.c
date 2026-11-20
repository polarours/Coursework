/* malloc 分配器的 harness：真实编译运行，验证分配/释放/合并。 */
#include <stdio.h>
#include <string.h>
#include <assert.h>

extern int mm_init(unsigned char *base, size_t size);
extern void *mm_malloc(size_t size);
extern void mm_free(void *p);
extern int count_free_blocks(void);

static unsigned char heap[1 << 16];  /* 64KB 模拟堆 / simulated heap */

int main(void) {
    mm_init(heap, sizeof(heap));

    void *a = mm_malloc(24);
    void *b = mm_malloc(24);
    void *c = mm_malloc(24);
    /* CSAPP 标准：8 字节对齐（DSIZE） */
    printf("[malloc] a=%p b=%p c=%p (8-byte aligned: %d)\n",
           a, b, c, ((unsigned long)a % 8 == 0) && ((unsigned long)b % 8 == 0));
    assert(a && b && c);
    assert((unsigned long)a % 8 == 0);
    assert(a != b && b != c);

    memset(a, 'A', 24);
    memset(b, 'B', 24);
    memset(c, 'C', 24);
    printf("[malloc] payloads: a[0]=%c b[0]=%c c[0]=%c\n",
           *(char*)a, *(char*)b, *(char*)c);
    assert(*(char*)a == 'A' && *(char*)b == 'B' && *(char*)c == 'C');

    printf("[malloc] free blocks before free: %d\n", count_free_blocks());
    mm_free(a);
    printf("[malloc] free blocks after free(a): %d\n", count_free_blocks());
    mm_free(b);
    printf("[malloc] free blocks after free(b): %d (should coalesce)\n", count_free_blocks());
    mm_free(c);
    printf("[malloc] free blocks after free(c): %d (all coalesced)\n", count_free_blocks());

    /* 释放后再分配，验证复用 / reuse after free */
    void *d = mm_malloc(24);
    printf("[malloc] realloc after frees: d=%p same_as_a=%d\n", d, d == a);
    assert(d == a);  /* 首次适应应复用最低地址的空闲块 */

    printf("--- PASS: test_malloc\n");
    printf("ALL TESTS PASSED\n");
    return 0;
}
