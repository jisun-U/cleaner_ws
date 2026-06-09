// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cleaner_msgs:msg/PlanCommand.idl
// generated code does not contain a copyright notice

#ifndef CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__STRUCT_H_
#define CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'mission_id'
// Member 'plan_json'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/PlanCommand in the package cleaner_msgs.
typedef struct cleaner_msgs__msg__PlanCommand
{
  builtin_interfaces__msg__Time stamp;
  rosidl_runtime_c__String mission_id;
  rosidl_runtime_c__String plan_json;
} cleaner_msgs__msg__PlanCommand;

// Struct for a sequence of cleaner_msgs__msg__PlanCommand.
typedef struct cleaner_msgs__msg__PlanCommand__Sequence
{
  cleaner_msgs__msg__PlanCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cleaner_msgs__msg__PlanCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__STRUCT_H_
