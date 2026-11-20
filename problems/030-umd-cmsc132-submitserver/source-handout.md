# 原始作业说明 / Original Assignment Materials

> UMD CMSC132 的 Project 1 没有文字题面文件——课程以 **PublicTests.java 作为规格**
> （15 个官方测试逐条钉死方法语义，含作者 Larry Herman 的版权声明）。
> 下面按原样汇集：官方 PublicTests.java 全文 + SubmitServer.java 接口注释。
> 中文导读见 `01-题目解读.md`。
>
> No prose handout: the official PublicTests.java IS the specification.
> Original materials collected verbatim below.

---

## 官方 PublicTests.java（原文）

```java
package tests;

// (c) Larry Herman, 2016.  You are allowed to use this code yourself, but
// not to provide it to anyone else.

import submitserver.SubmitServer;
import org.junit.*;
import static org.junit.Assert.*;

public class PublicTests {

  // Tests calling addSubmission() to add one submission for one student to
  // a SubmitServer object, then calling numSubmissions(name) on that
  // student.
  @Test public void testPublic1() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Paula Pupil", 74);

    assertEquals(1, server.numSubmissions("Paula Pupil"));
  }

  // Tests calling addSubmission() to add several submissions for one
  // student to a SubmitServer object, then calling numSubmissions(name) on
  // that student.
  @Test public void testPublic2() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 64);
    server.addSubmission("Leanne Learner", 68);
    server.addSubmission("Leanne Learner", 72);
    server.addSubmission("Leanne Learner", 70);
    server.addSubmission("Leanne Learner", 0);
    server.addSubmission("Leanne Learner", 70);
    server.addSubmission("Leanne Learner", 84);

    assertEquals(7, server.numSubmissions("Leanne Learner"));
  }

  // Tests calling addSubmission() and numSubmissions() for different
  // students in a SubmitServer.
  @Test public void testPublic3() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Schuyler Scholar", 92);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 0);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Theresa Terrapin", 62);
    server.addSubmission("Theresa Terrapin", 55);
    server.addSubmission("Schuyler Scholar", 95);
    server.addSubmission("Leanne Learner", 93);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 93);
    server.addSubmission("Ursula Undergraduate", 57);

    assertEquals(2, server.numSubmissions("Leanne Learner"));
    assertEquals(4, server.numSubmissions("Schuyler Scholar"));
    assertEquals(4, server.numSubmissions("Theresa Terrapin"));
    assertEquals(2, server.numSubmissions("Ursula Undergraduate"));
  }

  // Tests calling numSubmissions() (the overloaded form without a
  // parameter) on a SubmitServer object storing different numbers of
  // submissions.
  @Test public void testPublic4() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Schuyler Scholar", 92);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 0);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Theresa Terrapin", 62);
    server.addSubmission("Theresa Terrapin", 55);
    server.addSubmission("Schuyler Scholar", 95);
    server.addSubmission("Leanne Learner", 93);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 93);
    server.addSubmission("Ursula Undergraduate", 57);

    assertEquals(12, server.numSubmissions());
  }

  // Tests calling bestSubmissionNumber() on a student who made several
  // submissions.
  @Test public void testPublic5() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 92);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 96);

    assertEquals(4, server.bestSubmissionNumber("Sophie Sophomore"));
  }

  // Tests calling bestSubmissionNumber() on the name of a nonexistent
  // student.
  @Test public void testPublic6() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertEquals(-1, server.bestSubmissionNumber("Misty Mysterious"));
  }

  // Tests calling bestSubmissionScore() on a student who made several
  // submissions.
  @Test public void testPublic7() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 92);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 96);

    assertEquals(96, server.bestSubmissionScore("Sophie Sophomore"));
  }

  // Tests calling bestSubmissionScore() on the name of a nonexistent
  // student.
  @Test public void testPublic8() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertEquals(-1, server.bestSubmissionScore("Misty Mysterious"));
  }

  // Tests calling satisfactory() on a student with satisfactory
  // submissions.
  @Test public void testPublic9() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 0);
    server.addSubmission("Freddy Freshman", 0);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 0);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 0);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertTrue(server.satisfactory("Freddy Freshman"));
  }

  // Tests calling satisifactory() on the name of a nonexistent student.
  @Test public void testPublic10() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Junior Junior, Jr.", 87);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertFalse(server.satisfactory("Misty Mysterious"));
  }

  // Tests calling gotExtraCredit() in one case.
  @Test public void testPublic11() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Schuyler Scholar", 92);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 0);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Theresa Terrapin", 62);
    server.addSubmission("Theresa Terrapin", 55);
    server.addSubmission("Schuyler Scholar", 95);
    server.addSubmission("Leanne Learner", 93);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 93);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Junior Junior, Jr.", 100);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertEquals(1, server.gotExtraCredit());
  }

  // Tests calling changeScore() in one case.
  @Test public void testPublic12() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Schuyler Scholar", 92);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 0);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Theresa Terrapin", 62);
    server.addSubmission("Theresa Terrapin", 55);
    server.addSubmission("Schuyler Scholar", 95);
    server.addSubmission("Leanne Learner", 93);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 93);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Junior Junior, Jr.", 100);
    server.addSubmission("Freddy Freshman", 84);
    server.addSubmission("Freddy Freshman", 55);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Freddy Freshman", 68);
    server.addSubmission("Freddy Freshman", 48);
    server.addSubmission("Ursula Undergraduate", 57);
    server.addSubmission("Sophie Sophomore", 96);
    server.addSubmission("Sophie Sophomore", 0);
    server.addSubmission("Sophie Sophomore", 75);
    server.addSubmission("Sophie Sophomore", 92);

    assertEquals(96, server.bestSubmissionScore("Sophie Sophomore"));
    server.changeScore("Sophie Sophomore", 1, 98);
    assertEquals(98, server.bestSubmissionScore("Sophie Sophomore"));
  }

  // Tests addSubmission() with a too-small negative score.
  @Test public void testPublic13() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Leanne Learner", -10);
    server.addSubmission("Leanne Learner", 92);

    assertEquals(2, server.numSubmissions());
    assertEquals(2, server.numSubmissions("Leanne Learner"));
  }

  // Tests addSubmission() with a too-large score greater than 100.
  @Test public void testPublic14() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Leanne Learner", 101);
    server.addSubmission("Leanne Learner", 92);

    assertEquals(2, server.numSubmissions());
    assertEquals(2, server.numSubmissions("Leanne Learner"));
  }

  // Tests calling some of the methods with names (references) that are null.
  @Test public void testPublic15() {
    SubmitServer server= new SubmitServer();

    server.addSubmission("Leanne Learner", 83);
    server.addSubmission("Schuyler Scholar", 92);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 0);
    server.addSubmission("Ursula Undergraduate", 77);
    server.addSubmission("Theresa Terrapin", 62);
    server.addSubmission("Theresa Terrapin", 55);
    server.addSubmission("Schuyler Scholar", 95);
    server.addSubmission("Leanne Learner", 93);
    server.addSubmission("Theresa Terrapin", 84);
    server.addSubmission("Schuyler Scholar", 93);
    server.addSubmission("Ursula Undergraduate", 57);

    assertEquals(-1, server.numSubmissions(null));
    assertEquals(-1, server.bestSubmissionNumber(null));
    assertEquals(-1, server.bestSubmissionScore(null));
    assertFalse(server.satisfactory(null));
  }

}

```

---

## SubmitServer.java 接口与注释（原文）

```java
//SUBMIT SERVER by Anna Blendermann
//Honor Pledge - I have not received help on this assignment
package submitserver;
import java.util.ArrayList;

//SUBMIT SERVER CLASS******************************************************
//submitserver class stores and manipulates two lists of data, one for student
//names and one for their corresponding submissions
public class SubmitServer 
{
	//Two arraylist will represent the submit server database
	//one arraylist for the submitted names and one for corresponding scores
	private ArrayList<String> names_list = new ArrayList<String>();
	private ArrayList<Integer> scores_list = new ArrayList<Integer>();

	//ADD SUBMISSION METHOD************************************************
	//addSubmission adds one student submission to the same index of both
	//arraylists - name to names_list and score to scores_list
	public SubmitServer addSubmission(String name, int score) 
	{
		if(!name.isEmpty() && (score>=0 && score<=100)) 
		{
			names_list.add(name);
			scores_list.add(score);
		} 
		return this;
	}

	//NUM SUBMISSIONS METHOD***********************************************
	//numSubmissions interates the first arraylist, finds the number of times
	//the target student is listed on the server, and returns that number
	public int numSubmissions(String name) 
	{
		int numSubmissions = 0;
		if(name == null)
			return -1;
		else //name is valid
		{
			for(int x=0; x<names_list.size(); x++) 
			{
				if(names_list.get(x).equals(name))
					numSubmissions++;
			}
		}
		return numSubmissions;	
	}

	//NUM SUBMISSIONS METHOD*************************************************
	//numSubmissions returns the total number of submissions to the server
	public int numSubmissions() 
	{
		return names_list.size(); 
	}

	//BEST SUBMISSION NUMBER METHOD******************************************
	//bestSubmissionNumber checks if the target student exists in the server
	//and if so, iterates through a separate arraylist of their grades to find the best
	public int bestSubmissionNumber(String name) 
	{
		ArrayList<Integer> grades = new ArrayList<Integer>();
		int bestNumber = 0, bestIndex = 0;

		if(!names_list.contains(name) || name==null)
			return -1;
		else //server contains target student
		{
			//finds all grades from the target student
			for(int x=0; x<names_list.size(); x++) 
			{
				if(names_list.get(x).equals(name))
					grades.add(scores_list.get(x));
			}
			//finds the best grade from the target student
			for(int x=0; x<grades.size(); x++) 
			{
				if(grades.get(x)>=bestNumber)
				{
					bestNumber = grades.get(x);
					bestIndex = x+1; 
				}
			}
		}
		return bestIndex;
	} //end of method

	//BEST SUBMISSION SCORE METHOD*******************************************
	//bestSubmissionScore uses the bestSubmissionNumber to find the index of the
	//best submission from the target student
	public int bestSubmissionScore(String name) 
	{
		ArrayList<Integer> grades = new ArrayList<Integer>();
		int bestIndex = bestSubmissionNumber(name)-1;

		if(!names_list.contains(name) || name==null)
			return -1;
		else //server contains target student
		{
			//finds all grades from the target student
			for(int x=0; x<names_list.size(); x++) 
			{
				if(names_list.get(x).equals(name))
					grades.add(scores_list.get(x));
			}
			return grades.get(bestIndex);
		}
	}

	//STATISFACTORY METHOD***************************************************
	//satisfactory checks both arraylists for a submission greater than zero
	//from the target student (if student exists)
	public boolean satisfactory(String name) 
	{	
		if(!names_list.contains(name) || name==null)
			return false;
		else //server contains target student
		{
			for(int x=0; x<names_list.size(); x++)
			{
				if(names_list.get(x).equals(name))
				{
					if(scores_list.get(x)>0)
						return true;
				}
			}
		}
		return false;
	}

	//GOT EXTRA CREDIT METHOD*************************************************
	//gotExtraCredit accumulates students with grades of 100 and then removes
	//duplicates from that subset arraylist, returns arraylist size
	public int gotExtraCredit() 
	{
		ArrayList<Integer> studentIndex = new ArrayList<Integer>();

		//puts students with grades of 100 into studentIndex arraylist
		for(int x=0; x<names_list.size(); x++)
		{
			if(scores_list.get(x)==100)
				studentIndex.add(x);
		}
		//removes students with more than 1 submission
		for (int x=0; x<studentIndex.size(); x++) 
		{
			for (int y= x+1; y<studentIndex.size(); y++) 
			{
				if (studentIndex.get(x).equals(studentIndex.get(y)))
				{
					studentIndex.remove(x);
					studentIndex.remove(y);
				}
			}
		}
		return studentIndex.size();
	}

	//CHANGE SCORE METHOD*****************************************************
	//changeScore changes the score of a target student based upon their
	//submission number, which is different from the index
	public boolean changeScore(String name, int submissionNumber, int newScore) 
	{
		int num = 0;
		for(int x=0; x<names_list.size(); x++)
		{
			if(names_list.get(x).equals(name))
			{
				num = num+1;
				if(num==submissionNumber)
				{
					scores_list.set(x, newScore);
					return true;
				}
			}
		}	
		return false;
	}
} //end of SubmitServer class
```
