#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from example_interfaces.msg import Int64


class NumberSubscriberNode(LifecycleNode):
    def __init__(self):
        super().__init__("number_subscriber")
        self.get_logger().info("IN constructor")
        self.subscription_ = None
        self.data=None

    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_configure")
        self.subscription_ = self.create_subscription(
            Int64, "number", self.listener_callback, 10)
        
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_activate")
        self.subscription_.activate()
        print(self.data)
        return super().on_activate(previous_state)

    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_deactivate")
        self.subscription_.deactivate()
        return super().on_deactivate(previous_state)

    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_cleanup")
        self.destroy_lifecycle_subscription(self.subscription_)
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_shutdown")
        self.destroy_lifecycle_subscription(self.subscription_)
        return TransitionCallbackReturn.SUCCESS

    def on_error(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_error")
        # Do some checks, if ok, then return SUCCESS, if not FAILURE
        return TransitionCallbackReturn.FAILURE

    def listener_callback(self, msg):
        # print(msg.data)
        self.get_logger().info(f'Received number: {self.data}')
        self.data=msg.data


def main(args=None):
    rclpy.init(args=args)
    node = NumberSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
