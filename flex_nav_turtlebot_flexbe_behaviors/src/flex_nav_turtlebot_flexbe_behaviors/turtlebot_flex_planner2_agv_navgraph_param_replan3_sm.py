#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
from flex_nav_flexbe_states.get_path_state import GetPathState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flex_nav_flexbe_states.follow_path_state import FollowPathState
from flex_nav_flexbe_states.agvstatusstate import agvstatusstate
from flexbe_states.log_state import LogState
from flex_nav_flexbe_states.get_pose_state import GetPoseState
from flex_nav_flexbe_states.check import Check
from flex_nav_flexbe_states.agvTimedStopstate import agvTimedStopstate
from flex_nav_turtlebot_flexbe_behaviors.agv_recovery_behaviour_sm import AGVRecoveryBehaviourSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 09 2017
@author: Josh Cohen
'''
class TurtlebotFlexPlanner2_AGV_Navgraph_Param_replan3SM(Behavior):
	'''
	Uses Flexible Navigation to control the Turtlebot robot
	'''


	def __init__(self):
		super(TurtlebotFlexPlanner2_AGV_Navgraph_Param_replan3SM, self).__init__()
		self.name = 'Turtlebot Flex Planner2_AGV_Navgraph_Param_replan3'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(AGVRecoveryBehaviourSM, 'AGV Recovery Behaviour')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:753 y:303, x:1234 y:18
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:35 y:227, x:172 y:223, x:363 y:243, x:537 y:18, x:472 y:241, x:547 y:181, x:544 y:99, x:674 y:184
		_sm_container_0 = ConcurrencyContainer(outcomes=['finished', 'failed', 'danger', 'preempted'], input_keys=['plan'], conditions=[
										('failed', [('DWA', 'failed')]),
										('finished', [('DWA', 'done')]),
										('preempted', [('DWA', 'preempted')]),
										('danger', [('SAfetY', 'bumper')])
										])

		with _sm_container_0:
			# x:101 y:78
			OperatableStateMachine.add('DWA',
										FollowPathState(topic="low_level_planner"),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempted'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
										remapping={'plan': 'plan'})

			# x:362 y:85
			OperatableStateMachine.add('SAfetY',
										agvstatusstate(bumper_topic='/scan'),
										transitions={'bumper': 'danger'},
										autonomy={'bumper': Autonomy.Off})



		with _state_machine:
			# x:193 y:26
			OperatableStateMachine.add('ClearCostmap',
										ClearCostmapsState(costmap_topics=['high_level_planner/clear_costmap','low_level_planner/clear_costmap'], timeout=5.0),
										transitions={'done': 'Receive Goal', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:189 y:172
			OperatableStateMachine.add('Receive Path',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'ExecutePlan', 'empty': 'Continue', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.High, 'failed': Autonomy.High},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:189 y:248
			OperatableStateMachine.add('ExecutePlan',
										OperatorDecisionState(outcomes=["yes","continue"], hint="Execute the current plan?", suggestion="yes"),
										transitions={'yes': 'CHECK', 'continue': 'Continue'},
										autonomy={'yes': Autonomy.High, 'continue': Autonomy.Full})

			# x:511 y:241
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'Receive Goal', 'failed': 'AutoReplan', 'danger': 'AGVstop', 'preempted': 'Continue'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'danger': Autonomy.Inherit, 'preempted': Autonomy.Inherit},
										remapping={'plan': 'plan'})

			# x:549 y:111
			OperatableStateMachine.add('Continue',
										OperatorDecisionState(outcomes=["yes","no","recover","clearcostmap"], hint="Continue planning to new goal?", suggestion="yes"),
										transitions={'yes': 'Receive Goal', 'no': 'finished', 'recover': 'LogRecovery', 'clearcostmap': 'ClearCostmap'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full, 'recover': Autonomy.Full, 'clearcostmap': Autonomy.Full})

			# x:818 y:477
			OperatableStateMachine.add('Log Fail',
										LogState(text="Path execution failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'Recover'},
										autonomy={'done': Autonomy.Off})

			# x:943 y:54
			OperatableStateMachine.add('Log Recovered',
										LogState(text="Re-plan after recovery", severity=Logger.REPORT_HINT),
										transitions={'done': 'New Plan'},
										autonomy={'done': Autonomy.Off})

			# x:770 y:55
			OperatableStateMachine.add('New Plan',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'Container', 'empty': 'Receive Goal', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:190 y:99
			OperatableStateMachine.add('Receive Goal',
										GetPoseState(topic='move_base_simple/goal'),
										transitions={'done': 'Receive Path'},
										autonomy={'done': Autonomy.Off},
										remapping={'goal': 'goal'})

			# x:913 y:341
			OperatableStateMachine.add('Recover',
										OperatorDecisionState(outcomes=["yes","no"], hint="Should we attempt recovery?", suggestion="yes"),
										transitions={'yes': 'LogRecovery', 'no': 'finished'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:949 y:249
			OperatableStateMachine.add('LogRecovery',
										LogState(text="Starting recovery behavior", severity=Logger.REPORT_HINT),
										transitions={'done': 'AGV Recovery Behaviour'},
										autonomy={'done': Autonomy.Off})

			# x:915 y:162
			OperatableStateMachine.add('AutoReplan',
										OperatorDecisionState(outcomes=["yes","no"], hint="Re-plan to current goal?", suggestion="yes"),
										transitions={'yes': 'Log Recovered', 'no': 'Continue'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:510 y:328
			OperatableStateMachine.add('TEB',
										FollowPathState(topic="low_level_planner1"),
										transitions={'done': 'Receive Goal', 'failed': 'failed', 'preempted': 'Continue'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.High, 'preempted': Autonomy.High},
										remapping={'plan': 'plan'})

			# x:192 y:325
			OperatableStateMachine.add('CHECK',
										Check(topic="/location", blocking=True, clear=False),
										transitions={'True': 'Container', 'False': 'TEB', 'Continue': 'Continue'},
										autonomy={'True': Autonomy.High, 'False': Autonomy.High, 'Continue': Autonomy.High},
										remapping={'plan': 'plan'})

			# x:654 y:480
			OperatableStateMachine.add('AGVstop',
										agvTimedStopstate(timeout=2.0, cmd_topic='/cmd_vel', odom_topic='/odom'),
										transitions={'done': 'Log Fail', 'failed': 'Log Fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1071 y:201
			OperatableStateMachine.add('AGV Recovery Behaviour',
										self.use_behavior(AGVRecoveryBehaviourSM, 'AGV Recovery Behaviour'),
										transitions={'finished': 'AutoReplan', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
