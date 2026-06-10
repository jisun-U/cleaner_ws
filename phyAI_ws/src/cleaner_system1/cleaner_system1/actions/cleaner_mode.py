#!/usr/bin/env python3
import math
import time
from typing import Any, Dict, List, Optional

import rclpy
from rclpy.node import Node

from cleaner_system1.actions.move_to import Nav2Navigator, exec_move_to


def _normalize_goals(params: Dict[str, Any]) -> List[Dict[str, float]]:
    goals = params.get("goals")
    if isinstance(goals, list) and len(goals) >= 2:
        return goals

    start_goal = params.get("start_goal")
    end_goal = params.get("end_goal")
    if isinstance(start_goal, dict) and isinstance(end_goal, dict):
        return [start_goal, end_goal]

    return []


def _build_patrol_sequence(goals: List[Dict[str, float]]) -> List[Dict[str, float]]:
    if len(goals) == 2:
        return [goals[0], goals[1]]
    return goals + goals[-2:0:-1]


def _normalize_area_goals(params: Dict[str, Any]) -> List[Dict[str, float]]:
    area = params.get("area")
    if not isinstance(area, dict):
        return []

    try:
        min_x = float(area["min_x"])
        max_x = float(area["max_x"])
        min_y = float(area["min_y"])
        max_y = float(area["max_y"])
    except Exception:
        return []

    if max_x <= min_x or max_y <= min_y:
        return []

    lane_spacing = max(0.1, float(params.get("lane_spacing", 0.5)))
    sweep_axis = str(params.get("sweep_axis", "y")).lower()
    start_corner = str(params.get("start_corner", "bottom_left")).lower()

    if sweep_axis not in ("x", "y"):
        sweep_axis = "y"

    start_from_min_x = "left" in start_corner
    start_from_min_y = "bottom" in start_corner

    if sweep_axis == "y":
        lane_values = _frange(min_y, max_y, lane_spacing)
        lane_values = lane_values if start_from_min_y else list(reversed(lane_values))

        near_x = min_x if start_from_min_x else max_x
        far_x = max_x if start_from_min_x else min_x
        left_to_right = True
        goals: List[Dict[str, float]] = []

        for lane_y in lane_values:
            src_x, dst_x = (near_x, far_x) if left_to_right else (far_x, near_x)
            yaw = 0.0 if dst_x >= src_x else math.pi
            goals.append({"x": src_x, "y": lane_y, "yaw": yaw})
            goals.append({"x": dst_x, "y": lane_y, "yaw": yaw})
            left_to_right = not left_to_right
        return goals

    lane_values = _frange(min_x, max_x, lane_spacing)
    lane_values = lane_values if start_from_min_x else list(reversed(lane_values))

    near_y = min_y if start_from_min_y else max_y
    far_y = max_y if start_from_min_y else min_y
    bottom_to_top = True
    goals = []

    for lane_x in lane_values:
        src_y, dst_y = (near_y, far_y) if bottom_to_top else (far_y, near_y)
        yaw = math.pi * 0.5 if dst_y >= src_y else -math.pi * 0.5
        goals.append({"x": lane_x, "y": src_y, "yaw": yaw})
        goals.append({"x": lane_x, "y": dst_y, "yaw": yaw})
        bottom_to_top = not bottom_to_top
    return goals


def _frange(start: float, stop: float, step: float) -> List[float]:
    values: List[float] = []
    cur = start
    while cur < stop:
        values.append(cur)
        cur += step
    if not values or values[-1] < stop:
        values.append(stop)
    return values


def _wait_interval(node: Node, interval_sec: float) -> bool:
    if interval_sec <= 0.0:
        return True

    wait_until = time.time() + interval_sec
    while rclpy.ok() and time.time() < wait_until:
        time.sleep(0.1)

    if not rclpy.ok():
        node.get_logger().warn("[cleaner_mode] interrupted during interval wait")
        return False
    return True


def exec_cleaner_mode(
    node: Node,
    navigator: Nav2Navigator,
    nav_feedback: Dict[str, Any],
    params: Dict[str, Any],
    replan_rules: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    System-1 unit action: cleaner_mode

    Supported params:
    - area: {min_x, max_x, min_y, max_y}
    - lane_spacing: area coverage lane gap in meters
    - sweep_axis: "x" | "y"
    - start_corner: bottom_left | bottom_right | top_left | top_right
    - goals/start_goal/end_goal: legacy point patrol mode
    - interval_sec: wait after each waypoint
    - cycles: repeat count
    """
    area_goals = _normalize_area_goals(params)
    waypoint_goals = _normalize_goals(params)

    if area_goals:
        base_sequence = area_goals
        mode = "area_coverage"
    elif len(waypoint_goals) >= 2:
        base_sequence = _build_patrol_sequence(waypoint_goals)
        mode = "patrol"
    else:
        node.get_logger().error(
            "[cleaner_mode] need either 'area' or at least 2 goals"
        )
        return False

    interval_sec = max(0.0, float(params.get("interval_sec", 0.0)))
    cycles = max(1, int(params.get("cycles", 1)))

    node.get_logger().info(
        f"[cleaner_mode] start: mode={mode}, points={len(base_sequence)}, "
        f"cycles={cycles}, interval_sec={interval_sec:.2f}"
    )

    for cycle_idx in range(cycles):
        node.get_logger().info(f"[cleaner_mode] cycle {cycle_idx + 1}/{cycles}")

        for point_idx, goal in enumerate(base_sequence):
            node.get_logger().info(
                f"[cleaner_mode] move {point_idx + 1}/{len(base_sequence)} -> {goal}"
            )
            ok = exec_move_to(node, navigator, nav_feedback, goal, replan_rules)
            if not ok:
                node.get_logger().warn(
                    f"[cleaner_mode] move failed at cycle={cycle_idx + 1}, point={point_idx + 1}"
                )
                return False

            if not _wait_interval(node, interval_sec):
                return False

    node.get_logger().info("[cleaner_mode] completed")
    return True
