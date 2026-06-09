// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cleaner_msgs:msg/PlanCommand.idl
// generated code does not contain a copyright notice
#include "cleaner_msgs/msg/detail/plan_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `mission_id`
// Member `plan_json`
#include "rosidl_runtime_c/string_functions.h"

bool
cleaner_msgs__msg__PlanCommand__init(cleaner_msgs__msg__PlanCommand * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    cleaner_msgs__msg__PlanCommand__fini(msg);
    return false;
  }
  // mission_id
  if (!rosidl_runtime_c__String__init(&msg->mission_id)) {
    cleaner_msgs__msg__PlanCommand__fini(msg);
    return false;
  }
  // plan_json
  if (!rosidl_runtime_c__String__init(&msg->plan_json)) {
    cleaner_msgs__msg__PlanCommand__fini(msg);
    return false;
  }
  return true;
}

void
cleaner_msgs__msg__PlanCommand__fini(cleaner_msgs__msg__PlanCommand * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
  // mission_id
  rosidl_runtime_c__String__fini(&msg->mission_id);
  // plan_json
  rosidl_runtime_c__String__fini(&msg->plan_json);
}

bool
cleaner_msgs__msg__PlanCommand__are_equal(const cleaner_msgs__msg__PlanCommand * lhs, const cleaner_msgs__msg__PlanCommand * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  // mission_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mission_id), &(rhs->mission_id)))
  {
    return false;
  }
  // plan_json
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->plan_json), &(rhs->plan_json)))
  {
    return false;
  }
  return true;
}

bool
cleaner_msgs__msg__PlanCommand__copy(
  const cleaner_msgs__msg__PlanCommand * input,
  cleaner_msgs__msg__PlanCommand * output)
{
  if (!input || !output) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  // mission_id
  if (!rosidl_runtime_c__String__copy(
      &(input->mission_id), &(output->mission_id)))
  {
    return false;
  }
  // plan_json
  if (!rosidl_runtime_c__String__copy(
      &(input->plan_json), &(output->plan_json)))
  {
    return false;
  }
  return true;
}

cleaner_msgs__msg__PlanCommand *
cleaner_msgs__msg__PlanCommand__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cleaner_msgs__msg__PlanCommand * msg = (cleaner_msgs__msg__PlanCommand *)allocator.allocate(sizeof(cleaner_msgs__msg__PlanCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cleaner_msgs__msg__PlanCommand));
  bool success = cleaner_msgs__msg__PlanCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cleaner_msgs__msg__PlanCommand__destroy(cleaner_msgs__msg__PlanCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cleaner_msgs__msg__PlanCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cleaner_msgs__msg__PlanCommand__Sequence__init(cleaner_msgs__msg__PlanCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cleaner_msgs__msg__PlanCommand * data = NULL;

  if (size) {
    data = (cleaner_msgs__msg__PlanCommand *)allocator.zero_allocate(size, sizeof(cleaner_msgs__msg__PlanCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cleaner_msgs__msg__PlanCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cleaner_msgs__msg__PlanCommand__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
cleaner_msgs__msg__PlanCommand__Sequence__fini(cleaner_msgs__msg__PlanCommand__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      cleaner_msgs__msg__PlanCommand__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

cleaner_msgs__msg__PlanCommand__Sequence *
cleaner_msgs__msg__PlanCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cleaner_msgs__msg__PlanCommand__Sequence * array = (cleaner_msgs__msg__PlanCommand__Sequence *)allocator.allocate(sizeof(cleaner_msgs__msg__PlanCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cleaner_msgs__msg__PlanCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cleaner_msgs__msg__PlanCommand__Sequence__destroy(cleaner_msgs__msg__PlanCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cleaner_msgs__msg__PlanCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cleaner_msgs__msg__PlanCommand__Sequence__are_equal(const cleaner_msgs__msg__PlanCommand__Sequence * lhs, const cleaner_msgs__msg__PlanCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cleaner_msgs__msg__PlanCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cleaner_msgs__msg__PlanCommand__Sequence__copy(
  const cleaner_msgs__msg__PlanCommand__Sequence * input,
  cleaner_msgs__msg__PlanCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cleaner_msgs__msg__PlanCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    cleaner_msgs__msg__PlanCommand * data =
      (cleaner_msgs__msg__PlanCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cleaner_msgs__msg__PlanCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          cleaner_msgs__msg__PlanCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cleaner_msgs__msg__PlanCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
