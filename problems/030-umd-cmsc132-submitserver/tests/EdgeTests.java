package tests;

import submitserver.SubmitServer;
import org.junit.*;
import static org.junit.Assert.*;

/**
 * 030 边界测试补充：官方 PublicTests 覆盖常规流程，本文件测
 * 空服务器、null 参数与非法分数的语义（实测 upstream 实现的行为，
 * 断言以其当前语义为准——见 README 的边界语义记录）。
 */
public class EdgeTests {

    @Test public void emptyServerCounts() {
        SubmitServer s = new SubmitServer();
        assertEquals(0, s.numSubmissions());
        assertEquals(0, s.numSubmissions("nobody"));
    }

    @Test public void nullNameBehavior() {
        SubmitServer s = new SubmitServer();
        // upstream 实现对 null 返回 -1（官方测试未覆盖此分支）
        assertEquals(-1, s.numSubmissions(null));
    }

    @Test public void invalidScoreIsIgnored() {
        SubmitServer s = new SubmitServer();
        s.addSubmission("A", 101);   // 超范围：upstream 静默忽略
        s.addSubmission("B", -1);
        assertEquals(0, s.numSubmissions());
    }

    @Test public void sameNameMultipleSubmissions() {
        SubmitServer s = new SubmitServer();
        s.addSubmission("A", 50).addSubmission("A", 80).addSubmission("A", 60);
        assertEquals(3, s.numSubmissions("A"));
        assertEquals(80, s.bestSubmissionScore("A"));
        assertEquals(2, s.bestSubmissionNumber("A"));   // 1-based
    }
}
