// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from action_tutorials_interfaces:action/Youngrok.idl
// generated code does not contain a copyright notice

#ifndef ACTION_TUTORIALS_INTERFACES__ACTION__DETAIL__YOUNGROK__BUILDER_HPP_
#define ACTION_TUTORIALS_INTERFACES__ACTION__DETAIL__YOUNGROK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "action_tutorials_interfaces/action/detail/youngrok__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_Goal_order
{
public:
  Init_Youngrok_Goal_order()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::action_tutorials_interfaces::action::Youngrok_Goal order(::action_tutorials_interfaces::action::Youngrok_Goal::_order_type arg)
  {
    msg_.order = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_Goal>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_Goal_order();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_Result_sequence
{
public:
  Init_Youngrok_Result_sequence()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::action_tutorials_interfaces::action::Youngrok_Result sequence(::action_tutorials_interfaces::action::Youngrok_Result::_sequence_type arg)
  {
    msg_.sequence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_Result>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_Result_sequence();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_Feedback_partial_sequence
{
public:
  Init_Youngrok_Feedback_partial_sequence()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::action_tutorials_interfaces::action::Youngrok_Feedback partial_sequence(::action_tutorials_interfaces::action::Youngrok_Feedback::_partial_sequence_type arg)
  {
    msg_.partial_sequence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_Feedback>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_Feedback_partial_sequence();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_SendGoal_Request_goal
{
public:
  explicit Init_Youngrok_SendGoal_Request_goal(::action_tutorials_interfaces::action::Youngrok_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Request goal(::action_tutorials_interfaces::action::Youngrok_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Request msg_;
};

class Init_Youngrok_SendGoal_Request_goal_id
{
public:
  Init_Youngrok_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Youngrok_SendGoal_Request_goal goal_id(::action_tutorials_interfaces::action::Youngrok_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Youngrok_SendGoal_Request_goal(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_SendGoal_Request>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_SendGoal_Request_goal_id();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_SendGoal_Response_stamp
{
public:
  explicit Init_Youngrok_SendGoal_Response_stamp(::action_tutorials_interfaces::action::Youngrok_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Response stamp(::action_tutorials_interfaces::action::Youngrok_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Response msg_;
};

class Init_Youngrok_SendGoal_Response_accepted
{
public:
  Init_Youngrok_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Youngrok_SendGoal_Response_stamp accepted(::action_tutorials_interfaces::action::Youngrok_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Youngrok_SendGoal_Response_stamp(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_SendGoal_Response>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_SendGoal_Response_accepted();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_GetResult_Request_goal_id
{
public:
  Init_Youngrok_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::action_tutorials_interfaces::action::Youngrok_GetResult_Request goal_id(::action_tutorials_interfaces::action::Youngrok_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_GetResult_Request>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_GetResult_Request_goal_id();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_GetResult_Response_result
{
public:
  explicit Init_Youngrok_GetResult_Response_result(::action_tutorials_interfaces::action::Youngrok_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::action_tutorials_interfaces::action::Youngrok_GetResult_Response result(::action_tutorials_interfaces::action::Youngrok_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_GetResult_Response msg_;
};

class Init_Youngrok_GetResult_Response_status
{
public:
  Init_Youngrok_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Youngrok_GetResult_Response_result status(::action_tutorials_interfaces::action::Youngrok_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Youngrok_GetResult_Response_result(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_GetResult_Response>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_GetResult_Response_status();
}

}  // namespace action_tutorials_interfaces


namespace action_tutorials_interfaces
{

namespace action
{

namespace builder
{

class Init_Youngrok_FeedbackMessage_feedback
{
public:
  explicit Init_Youngrok_FeedbackMessage_feedback(::action_tutorials_interfaces::action::Youngrok_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::action_tutorials_interfaces::action::Youngrok_FeedbackMessage feedback(::action_tutorials_interfaces::action::Youngrok_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_FeedbackMessage msg_;
};

class Init_Youngrok_FeedbackMessage_goal_id
{
public:
  Init_Youngrok_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Youngrok_FeedbackMessage_feedback goal_id(::action_tutorials_interfaces::action::Youngrok_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Youngrok_FeedbackMessage_feedback(msg_);
  }

private:
  ::action_tutorials_interfaces::action::Youngrok_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_tutorials_interfaces::action::Youngrok_FeedbackMessage>()
{
  return action_tutorials_interfaces::action::builder::Init_Youngrok_FeedbackMessage_goal_id();
}

}  // namespace action_tutorials_interfaces

#endif  // ACTION_TUTORIALS_INTERFACES__ACTION__DETAIL__YOUNGROK__BUILDER_HPP_
