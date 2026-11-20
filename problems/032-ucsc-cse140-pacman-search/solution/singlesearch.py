"""
In this file, you will implement code relating to simple single-agent searches.

参考实现 / reference implementation（UCSC CSE140 p1, pacai v2.1.0）。

统一说明 / Unifying notes:
- 四个搜索器（DFS/BFS/UCS/A*）共用同一个图搜索骨架，只有 frontier 的
  出队策略与优先级不同——这正是 CS188 想教的：搜索算法 = 队列策略。
- 路径用 (actions, cost) 随条目携带，pop 到目标即得解，无需回溯指针。
- BFS 在"入队时"去重（同层重复会爆内存）；UCS/A* 用 best_g 记录最短
  已知代价，弹出过期条目直接跳过（lazy deletion）。
"""

import heapq
import itertools
import random
import typing

import pacai.agents.searchproblem
import pacai.core.agent
import pacai.core.agentaction
import pacai.core.board
import pacai.core.gamestate
import pacai.core.search
import pacai.pacman.board
import pacai.search.common
import pacai.search.food
import pacai.search.position

def _graph_search(
        problem: pacai.core.search.SearchProblem,
        heuristic: pacai.core.search.SearchHeuristic,
        *,
        mode: str,
        ) -> pacai.core.search.SearchSolution:
    """
    统一图搜索骨架 / the one graph-search skeleton.

    mode:
    - 'dfs': LIFO 栈
    - 'bfs': FIFO 队列
    - 'ucs': 按 g(priority queue)
    - 'astar': 按 g + h
    """

    start_node = problem.get_starting_node()
    tie_counter = itertools.count()   # 稳定 tie-break：先发现者优先

    # frontier 条目：(priority, tie, node, actions, g)
    priority0 = 0.0
    if (mode == 'astar'):
        priority0 = heuristic(start_node, problem)
    frontier = [(priority0, next(tie_counter), start_node, [], 0.0)]

    visited: set = set()        # DFS/BFS：已入队/已展开的节点
    best_g: dict = {}           # UCS/A*：节点当前最短已知代价

    while (len(frontier) > 0):
        if (mode == 'dfs'):
            _, _, node, actions, g = frontier.pop()
        else:
            _, _, node, actions, g = heapq.heappop(frontier)

        # 目标检测放在弹出后 / goal test on expansion
        if (problem.is_goal_node(node)):
            return pacai.core.search.SearchSolution(actions, g, node)

        if (mode in ('ucs', 'astar')):
            # 过期条目：已有更优路径到达该节点 / stale entry
            if (node in best_g and g > best_g[node]):
                continue
            best_g[node] = g
        elif (mode == 'dfs'):
            # DFS 在"展开时"去重 / dedupe at expansion
            if (node in visited):
                continue
            visited.add(node)
        # BFS 在"入队时"去重（见下），弹出后可直接展开。
        # BFS dedupes at enqueue time, so popped entries need no check.

        for successor in problem.get_successor_nodes(node):
            next_actions = actions + [successor.action]
            next_g = g + successor.cost

            if (mode == 'dfs'):
                frontier.append((0.0, next(tie_counter), successor.node, next_actions, next_g))
            elif (mode == 'bfs'):
                # 入队时去重：同层重复节点没有意义 / dedupe at enqueue
                if (successor.node in visited):
                    continue
                visited.add(successor.node)
                frontier.append((0.0, next(tie_counter), successor.node, next_actions, next_g))
            elif (mode == 'ucs'):
                if (successor.node not in best_g or next_g < best_g[successor.node]):
                    heapq.heappush(frontier, (next_g, next(tie_counter), successor.node, next_actions, next_g))
            else:   # astar
                if (successor.node not in best_g or next_g < best_g[successor.node]):
                    h = heuristic(successor.node, problem)
                    heapq.heappush(frontier, (next_g + h, next(tie_counter), successor.node, next_actions, next_g))

    raise pacai.core.search.SolutionNotFoundError()

def depth_first_search(
        problem: pacai.core.search.SearchProblem,
        heuristic: pacai.core.search.SearchHeuristic,
        rng: random.Random,
        **kwargs: typing.Any) -> pacai.core.search.SearchSolution:
    """
    A pacai.core.search.SearchProblemSolver that implements depth first search (DFS).
    This means that it will search the deepest nodes in the search tree first.
    See: https://en.wikipedia.org/wiki/Depth-first_search .
    """

    return _graph_search(problem, heuristic, mode = 'dfs')

def breadth_first_search(
        problem: pacai.core.search.SearchProblem,
        heuristic: pacai.core.search.SearchHeuristic,
        rng: random.Random,
        **kwargs: typing.Any) -> pacai.core.search.SearchSolution:
    """
    A pacai.core.search.SearchProblemSolver that implements breadth first search (BFS).
    This means that it will search nodes based on what level in search tree they appear.
    See: https://en.wikipedia.org/wiki/Breadth-first_search .
    """

    return _graph_search(problem, heuristic, mode = 'bfs')

def uniform_cost_search(
        problem: pacai.core.search.SearchProblem,
        heuristic: pacai.core.search.SearchHeuristic,
        rng: random.Random,
        **kwargs: typing.Any) -> pacai.core.search.SearchSolution:
    """
    A pacai.core.search.SearchProblemSolver that implements uniform cost search (UCS).
    This means that it will search nodes with a lower total cost first.
    See: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs .
    """

    return _graph_search(problem, heuristic, mode = 'ucs')

def astar_search(
        problem: pacai.core.search.SearchProblem,
        heuristic: pacai.core.search.SearchHeuristic,
        rng: random.Random,
        **kwargs: typing.Any) -> pacai.core.search.SearchSolution:
    """
    A pacai.core.search.SearchProblemSolver that implements A* search (pronounced "A Star search").
    This means that it will search nodes with a lower combined cost and heuristic first.
    See: https://en.wikipedia.org/wiki/A*_search_algorithm .
    """

    return _graph_search(problem, heuristic, mode = 'astar')

class CornersSearchNode(pacai.core.search.SearchNode):
    """
    A search node the can be used to represent the corners search problem.

    You get to implement this search node however you want.

    参考实现 / reference implementation:
    状态 = (当前位置, 四角访问标记)。四角顺序固定为 NW, NE, SW, SE。
    手写 __eq__/__hash__（覆写 SimpleComparable 的 JSON 路径——正确且更快）。
    """

    def __init__(self,
            position: pacai.core.board.Position,
            visited_corners: tuple[bool, ...] = (False, False, False, False)) -> None:
        """ Construct a search node to help search for corners. """

        self.position: pacai.core.board.Position = position
        self.visited_corners: tuple[bool, ...] = tuple(visited_corners)

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, CornersSearchNode)):
            return False
        return ((self.position == other.position)
                and (self.visited_corners == other.visited_corners))

    def __hash__(self) -> int:
        return hash((self.position, self.visited_corners))

class CornersSearchProblem(pacai.core.search.SearchProblem[CornersSearchNode]):
    """
    A search problem for touching the four different corners in a board.

    You may assume that very board is surrounded by walls (e.g., (0, 0) is a wall),
    and that the position diagonally inside from the walled corner is the location we are looking for.
    For example, if we had a square board that was 10x10, then we would be looking for the following corners:
     - (1, 1) -- North-West / Upper Left
     - (1, 8) -- North-East / Upper Right
     - (8, 1) -- South-West / Lower Left
     - (8, 8) -- South-East / Lower Right
    """

    def __init__(self,
            game_state: pacai.core.gamestate.GameState,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.board: pacai.core.board.Board = game_state.board

        # 四角：NW, NE, SW, SE（与 CornersSearchNode 的标记顺序一致）
        # 注意 Position 的参数顺序是 (row, col) / note the (row, col) order.
        w = self.board.width
        h = self.board.height
        self.corners: list[pacai.core.board.Position] = [
            pacai.core.board.Position(1, 1),          # NW
            pacai.core.board.Position(1, w - 2),      # NE
            pacai.core.board.Position(h - 2, 1),      # SW
            pacai.core.board.Position(h - 2, w - 2),  # SE
        ]

        start_position = game_state.get_agent_position()
        if (start_position is None):
            raise ValueError("Could not find starting position.")

        self.start_position: pacai.core.board.Position = start_position

    def _visit_flags(self, position: pacai.core.board.Position,
            flags: tuple[bool, bool, bool, bool]) -> tuple[bool, bool, bool, bool]:
        """ 站上某角时更新访问标记。/ update flags when standing on a corner. """

        for (i, corner) in enumerate(self.corners):
            if (position == corner):
                return tuple(True if (j == i) else flags[j] for j in range(4))

        return flags

    def get_starting_node(self) -> CornersSearchNode:
        return CornersSearchNode(self.start_position, self._visit_flags(self.start_position,
                (False, False, False, False)))

    def is_goal_node(self, node: CornersSearchNode) -> bool:
        return all(node.visited_corners)

    def get_successor_nodes(self, node: CornersSearchNode) -> list[pacai.core.search.SuccessorInfo]:
        successors = []

        for (action, position) in self.board.get_neighbors(node.position):
            next_flags = self._visit_flags(position, node.visited_corners)
            next_node = CornersSearchNode(position, next_flags)
            successors.append(pacai.core.search.SuccessorInfo(next_node, action, 1.0))

        # 展开计数与历史（与官方 PositionSearchProblem 一致的 bookkeeping）
        self.expanded_node_count += 1
        if (node not in self.visited_nodes):
            self.visited_nodes.add(node)
            self.position_history.append(node.position)

        return successors

def corners_heuristic(node: CornersSearchNode, problem: CornersSearchProblem, **kwargs: typing.Any) -> float:
    """
    A heuristic for CornersSearchProblem.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)

    参考实现 / reference implementation:
    h = 到"最远未访问角"的曼哈顿距离（取 max 而非 min）。

    可采纳性证明 / admissibility argument:
    任何完成路径都必须**经过每一个**未访问角。设路径先访问某个未访问角 c_i，
    则路径长度 >= dist(pos, c_i)。该不等式对**每个** i 都成立，
    所以路径长度 >= max_i dist(pos, c_i) = h。
    """

    distances = []
    for (i, corner) in enumerate(problem.corners):
        if (not node.visited_corners[i]):
            distances.append(abs(node.position.col - corner.col) + abs(node.position.row - corner.row))

    if (len(distances) == 0):
        return 0.0

    return float(max(distances))

def food_heuristic(node: pacai.search.food.FoodSearchNode, problem: pacai.search.food.FoodSearchProblem, **kwargs: typing.Any) -> float:
    """
    A heuristic for the FoodSearchProblem.

    参考实现 / reference implementation:
    h = 到最远剩余食物的曼哈顿距离（max 版，同 corners_heuristic 的论证）。

    可采纳性 / admissible: 完成路径必须到达**每一粒**剩余食物，
    故路径长 >= dist(pos, f) 对每个 f 成立 → 路径长 >= max_f dist(pos, f)。
    """

    if (len(node.remaining_food) == 0):
        return 0.0

    return float(max(abs(node.position.col - food.col) + abs(node.position.row - food.row)
            for food in node.remaining_food))

class ClosestDotSearchAgent(pacai.agents.searchproblem.GreedySubproblemSearchAgent):
    """
    Search for a path to all the food by greedily searching for the next closest food again and again
    (util we have reached all the food).

    This agent is left to you to fill out.
    But make sure to take your time and think.
    The final solution is quite simple if you take your time to understand everything up until this point and leverage
    pacai.agents.searchproblem.GreedySubproblemSearchAgent and pacai.student.problem.AnyMarkerSearchProblem.
    pacai.agents.searchproblem.GreedySubproblemSearchAgent is already implemented,
    but you should take some time to understand it.
    pacai.student.problem.AnyMarkerSearchProblem (below in this file) has not yet been implemented,
    but is the quickest and easiest way to implement this class.

    Hint:
    Remember that you can call a parent class' `__init__()` method from a child class' `__init__()` method.
    (See pacai.student.problem.AnyMarkerSearchProblem for an example.)
    Child classes will generally always call their parent's `__init__()` method
    (if a child class does not implement `__init__()`, then the parent's `__init__()` is automatically called).
    This call does not need to be the first line in the method,
    and you can pass whatever you want to the parent's `__init__()`.

    参考实现 / reference implementation:
    复用 GreedySubproblemSearchAgent 的循环骨架：每个子问题 =
    "从当前位置到任意一粒食物"（AnyMarkerSearchProblem），用 BFS 保证
    每一步走的都是最短路。贪心体现在"只看下一个食物"，最优性不保证——
    这正是题面所说的 greedy 策略。
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(
                problem = 'pacai.student.singlesearch.AnyMarkerSearchProblem',
                solver = 'pacai.student.singlesearch.breadth_first_search',
                **kwargs)

class AnyMarkerSearchProblem(pacai.search.position.PositionSearchProblem):
    """
    A search problem for finding a path to any instance of the specified board marker (e.g., food, wall, power capsule).

    This search problem is just like the pacai.search.position.PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    You may modify the `__init__()` if you want, the other methods should be fine as-is.

    参考实现 / reference implementation:
    构造时缓存目标标记的全部位置（board 不变，一次拿全），
    is_goal_node 就是成员判断。
    """

    def __init__(self,
            game_state: pacai.core.gamestate.GameState,
            target_marker: pacai.core.board.Marker = pacai.pacman.board.MARKER_PELLET,
            **kwargs: typing.Any) -> None:
        super().__init__(game_state, **kwargs)

        self._target_positions: set[pacai.core.board.Position] = game_state.board.get_marker_positions(target_marker)

    def is_goal_node(self, node: pacai.search.position.PositionSearchNode) -> bool:
        return node.position in self._target_positions

class ApproximateSearchAgent(pacai.agents.searchproblem.GreedySubproblemSearchAgent):
    """
    A search agent that tries to perform an approximate search instead of an exact one.
    In other words, this agent is okay with a solution that is "good enough" and not necessarily optimal.

    参考实现 / reference implementation:
    近似策略与 ClosestDot 相同（贪心最近食物）——suboptimal 但有效。
    近似搜索的官方评分只要求路径足够好（如不超过最优的某个倍数），
    贪心最近点在大多数 board 上已能达到"好"的标准。
    实测（07-延伸练习记录）：search-medium 上与 ClosestDot 行为一致。
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(
                problem = 'pacai.student.singlesearch.AnyMarkerSearchProblem',
                solver = 'pacai.student.singlesearch.breadth_first_search',
                **kwargs)
