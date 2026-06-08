// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cleaner_msgs:msg/CleanerState.idl
// generated code does not contain a copyright notice

#ifndef CLEANER_MSGS__MSG__DETAIL__CLEANER_STATE__BUILDER_HPP_
#define CLEANER_MSGS__MSG__DETAIL__CLEANER_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cleaner_msgs/msg/detail/cleaner_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cleaner_msgs
{

namespace msg
{

namespace builder
{

class Init_CleanerState_events_json
{
public:
  explicit Init_CleanerState_events_json(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  ::cleaner_msgs::msg::CleanerState events_json(::cleaner_msgs::msg::CleanerState::_events_json_type arg)
  {
    msg_.events_json = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_last_violation
{
public:
  explicit Init_CleanerState_last_violation(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_events_json last_violation(::cleaner_msgs::msg::CleanerState::_last_violation_type arg)
  {
    msg_.last_violation = std::move(arg);
    return Init_CleanerState_events_json(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_max_speed
{
public:
  explicit Init_CleanerState_max_speed(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_last_violation max_speed(::cleaner_msgs::msg::CleanerState::_max_speed_type arg)
  {
    msg_.max_speed = std::move(arg);
    return Init_CleanerState_last_violation(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_safe_backstop
{
public:
  explicit Init_CleanerState_safe_backstop(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_max_speed safe_backstop(::cleaner_msgs::msg::CleanerState::_safe_backstop_type arg)
  {
    msg_.safe_backstop = std::move(arg);
    return Init_CleanerState_max_speed(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_roe_ok
{
public:
  explicit Init_CleanerState_roe_ok(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_safe_backstop roe_ok(::cleaner_msgs::msg::CleanerState::_roe_ok_type arg)
  {
    msg_.roe_ok = std::move(arg);
    return Init_CleanerState_safe_backstop(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_history_json
{
public:
  explicit Init_CleanerState_history_json(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_roe_ok history_json(::cleaner_msgs::msg::CleanerState::_history_json_type arg)
  {
    msg_.history_json = std::move(arg);
    return Init_CleanerState_roe_ok(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_queue_status
{
public:
  explicit Init_CleanerState_queue_status(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_history_json queue_status(::cleaner_msgs::msg::CleanerState::_queue_status_type arg)
  {
    msg_.queue_status = std::move(arg);
    return Init_CleanerState_history_json(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_current_index
{
public:
  explicit Init_CleanerState_current_index(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_queue_status current_index(::cleaner_msgs::msg::CleanerState::_current_index_type arg)
  {
    msg_.current_index = std::move(arg);
    return Init_CleanerState_queue_status(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_plan_json
{
public:
  explicit Init_CleanerState_plan_json(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_current_index plan_json(::cleaner_msgs::msg::CleanerState::_plan_json_type arg)
  {
    msg_.plan_json = std::move(arg);
    return Init_CleanerState_current_index(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_vision_json
{
public:
  explicit Init_CleanerState_vision_json(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_plan_json vision_json(::cleaner_msgs::msg::CleanerState::_vision_json_type arg)
  {
    msg_.vision_json = std::move(arg);
    return Init_CleanerState_plan_json(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_lost_sec
{
public:
  explicit Init_CleanerState_lost_sec(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_vision_json lost_sec(::cleaner_msgs::msg::CleanerState::_lost_sec_type arg)
  {
    msg_.lost_sec = std::move(arg);
    return Init_CleanerState_vision_json(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_primary_id
{
public:
  explicit Init_CleanerState_primary_id(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_lost_sec primary_id(::cleaner_msgs::msg::CleanerState::_primary_id_type arg)
  {
    msg_.primary_id = std::move(arg);
    return Init_CleanerState_lost_sec(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_battery_voltage
{
public:
  explicit Init_CleanerState_battery_voltage(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_primary_id battery_voltage(::cleaner_msgs::msg::CleanerState::_battery_voltage_type arg)
  {
    msg_.battery_voltage = std::move(arg);
    return Init_CleanerState_primary_id(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_battery_soc
{
public:
  explicit Init_CleanerState_battery_soc(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_battery_voltage battery_soc(::cleaner_msgs::msg::CleanerState::_battery_soc_type arg)
  {
    msg_.battery_soc = std::move(arg);
    return Init_CleanerState_battery_voltage(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_vel_wz
{
public:
  explicit Init_CleanerState_vel_wz(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_battery_soc vel_wz(::cleaner_msgs::msg::CleanerState::_vel_wz_type arg)
  {
    msg_.vel_wz = std::move(arg);
    return Init_CleanerState_battery_soc(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_vel_vy
{
public:
  explicit Init_CleanerState_vel_vy(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_vel_wz vel_vy(::cleaner_msgs::msg::CleanerState::_vel_vy_type arg)
  {
    msg_.vel_vy = std::move(arg);
    return Init_CleanerState_vel_wz(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_vel_vx
{
public:
  explicit Init_CleanerState_vel_vx(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_vel_vy vel_vx(::cleaner_msgs::msg::CleanerState::_vel_vx_type arg)
  {
    msg_.vel_vx = std::move(arg);
    return Init_CleanerState_vel_vy(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_pose_yaw
{
public:
  explicit Init_CleanerState_pose_yaw(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_vel_vx pose_yaw(::cleaner_msgs::msg::CleanerState::_pose_yaw_type arg)
  {
    msg_.pose_yaw = std::move(arg);
    return Init_CleanerState_vel_vx(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_pose_y
{
public:
  explicit Init_CleanerState_pose_y(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_pose_yaw pose_y(::cleaner_msgs::msg::CleanerState::_pose_y_type arg)
  {
    msg_.pose_y = std::move(arg);
    return Init_CleanerState_pose_yaw(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_pose_x
{
public:
  explicit Init_CleanerState_pose_x(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_pose_y pose_x(::cleaner_msgs::msg::CleanerState::_pose_x_type arg)
  {
    msg_.pose_x = std::move(arg);
    return Init_CleanerState_pose_y(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_pose_frame
{
public:
  explicit Init_CleanerState_pose_frame(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_pose_x pose_frame(::cleaner_msgs::msg::CleanerState::_pose_frame_type arg)
  {
    msg_.pose_frame = std::move(arg);
    return Init_CleanerState_pose_x(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_system_state
{
public:
  explicit Init_CleanerState_system_state(::cleaner_msgs::msg::CleanerState & msg)
  : msg_(msg)
  {}
  Init_CleanerState_pose_frame system_state(::cleaner_msgs::msg::CleanerState::_system_state_type arg)
  {
    msg_.system_state = std::move(arg);
    return Init_CleanerState_pose_frame(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

class Init_CleanerState_stamp
{
public:
  Init_CleanerState_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CleanerState_system_state stamp(::cleaner_msgs::msg::CleanerState::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_CleanerState_system_state(msg_);
  }

private:
  ::cleaner_msgs::msg::CleanerState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cleaner_msgs::msg::CleanerState>()
{
  return cleaner_msgs::msg::builder::Init_CleanerState_stamp();
}

}  // namespace cleaner_msgs

#endif  // CLEANER_MSGS__MSG__DETAIL__CLEANER_STATE__BUILDER_HPP_
