/*
 * CSAPP Malloc Lab 教学版：隐式空闲链表 + 边界标签 + 首次适应。
 * 独立于官方 framework 编写的演示实现（不复制任何现有 solution）。
 *
 * 堆布局（每个块 / each block）:
 *   [ 4B header | payload... | 4B footer ]   ← 已分配块
 *   [ 4B header |            | 4B footer ]   ← 空闲块（payload 区闲置）
 * header/footer = size | alloc_bit (size 为 4 的倍数，低位作 alloc 标志)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define WSIZE 4
#define DSIZE 8
#define CHUNKSIZE (1 << 12)

static unsigned char *heap_start = NULL;   /* 堆起始 / heap base */
static size_t heap_size = 0;
static unsigned char *brk_ptr = NULL;      /* 当前 program break */

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define ALIGN(size) (((size) + 7) & ~7)
#define PACK(size, alloc) ((size) | (alloc))
#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (unsigned int)(val))
#define GET_SIZE(p) (GET(p) & ~7)
#define GET_ALLOC(p) (GET(p) & 1)
#define HDRP(bp) ((unsigned char *)(bp) - WSIZE)
#define FTRP(bp) ((unsigned char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE)
#define NEXT_BLKP(bp) ((unsigned char *)(bp) + GET_SIZE(HDRP(bp)))
#define PREV_BLKP(bp) ((unsigned char *)(bp) - GET_SIZE((unsigned char *)(bp) - DSIZE))

static void *extend_heap(size_t words);
static void *coalesce(void *bp);
static void place(void *bp, size_t asize);

/* 初始化堆 / initialize the heap */
int mm_init(unsigned char *base, size_t size) {
    /*
     * 关键：第一个块的 payload 必须 8 字节对齐。
     * 静态数组 base 通常 16 字节对齐；若偏移 WSIZE(4) 会破坏 8 字节对齐。
     * 用 DSIZE(8) 偏移，并放两个 WSIZE 的占位字。
     * HDRP(bp)=bp-4 落在 base+4，不越界且保持对齐。
     */
    heap_start = base + DSIZE;
    heap_size = size;
    brk_ptr = heap_start;
    PUT(base, 0);        /* 占位字 / padding word */
    PUT(base + WSIZE, 0); /* 占位字 / padding word */
    return 0;
}

/* 扩展堆：向系统"申请"一整块 / grow the heap by CHUNKSIZE */
static void *extend_heap(size_t words) {
    size_t size = ALIGN(words);
    if (brk_ptr + size > heap_start + heap_size - WSIZE) return NULL;
    unsigned char *bp = brk_ptr;
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));
    brk_ptr = NEXT_BLKP(bp);
    return bp;
}

/* 首次适应查找空闲块 / first-fit search */
static void *find_fit(size_t asize) {
    if (heap_start == brk_ptr) return NULL;
    for (unsigned char *bp = heap_start; bp < brk_ptr; bp = NEXT_BLKP(bp)) {
        if (!GET_ALLOC(HDRP(bp)) && GET_SIZE(HDRP(bp)) >= asize) return bp;
    }
    return NULL;
}

/* 放置：必要时分割空闲块 / split the free block if there's leftover */
static void place(void *bp, size_t asize) {
    size_t csize = GET_SIZE(HDRP(bp));
    if (csize - asize >= (2 * DSIZE)) {
        PUT(HDRP(bp), PACK(asize, 1));
        PUT(FTRP(bp), PACK(asize, 1));
        unsigned char *rest = NEXT_BLKP(bp);
        PUT(HDRP(rest), PACK(csize - asize, 0));
        PUT(FTRP(rest), PACK(csize - asize, 0));
    } else {
        PUT(HDRP(bp), PACK(csize, 1));
        PUT(FTRP(bp), PACK(csize, 1));
    }
}

/* 合并：检查前后块是否空闲 / coalesce with free neighbors */
static void *coalesce(void *bp) {
    int is_first = (bp == heap_start);          /* 第一个块没有前驱 */
    size_t prev_alloc = is_first ? 1 : GET_ALLOC(FTRP(PREV_BLKP(bp)));
    int at_end = (NEXT_BLKP(bp) >= brk_ptr);    /* 最后一个块没有后继 */
    size_t next_alloc = at_end ? 1 : GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));

    if (prev_alloc && next_alloc) {
        return bp;
    } else if (prev_alloc && !next_alloc) {
        size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
        PUT(HDRP(bp), PACK(size, 0));
        PUT(FTRP(bp), PACK(size, 0));
    } else if (!prev_alloc && next_alloc) {
        size += GET_SIZE(HDRP(PREV_BLKP(bp)));
        PUT(FTRP(bp), PACK(size, 0));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        bp = PREV_BLKP(bp);
    } else {
        size += GET_SIZE(HDRP(PREV_BLKP(bp))) + GET_SIZE(HDRP(NEXT_BLKP(bp)));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        PUT(FTRP(NEXT_BLKP(bp)), PACK(size, 0));
        bp = PREV_BLKP(bp);
    }
    return bp;
}

void *mm_malloc(size_t size) {
    if (size == 0) return NULL;
    size_t asize = ALIGN(size + DSIZE);   /* 加上 header/footer */
    void *bp = find_fit(asize);
    if (bp == NULL) {
        bp = extend_heap(MAX(asize, CHUNKSIZE));
        if (bp == NULL) return NULL;
    }
    place(bp, asize);
    return bp;
}

void mm_free(void *bp) {
    if (bp == NULL) return;
    size_t size = GET_SIZE(HDRP(bp));
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));
    coalesce(bp);
}

/* 统计当前空闲块数（用于测试验证合并）/ count free blocks */
int count_free_blocks(void) {
    int n = 0;
    for (unsigned char *bp = heap_start; bp < brk_ptr; bp = NEXT_BLKP(bp)) {
        if (!GET_ALLOC(HDRP(bp))) n++;
    }
    return n;
}
