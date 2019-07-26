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
from flex_nav_flexbe_states.agvTimedStopstate import agvTimedStopstate
from flex_nav_turtlebot_flexbe_behaviors.agv_recovery_behaviour1_sm import AGVRecoveryBehaviour1SM
from flex_nav_flexbe_states.GetPoseLocalState import GetPoseLocalState
from flex_nav_flexbe_states.checklocalstate import checklocalstate
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 09 2017
@author: Josh Cohen
'''
class TurtlebotFlexPlanner2_AGV_Navgraph_Param_replan12SM(Behavior):
	'''
	Uses Flexible Navigation to control the Turtlebot robot
	'''


	def __init__(self):
		super(TurtlebotFlexPlanner2_AGV_Navgraph_Param_replan12SM, self).__init__()
		self.name = 'Turtlebot Flex Planner2_AGV_Navgraph_Param_replan12'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(AGVRecoveryBehaviour1SM, 'AGV Recovery Behaviour1')

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

		# x:98 y:203, x:219 y:195, x:450 y:235, x:337 y:190, x:430 y:322, x:530 y:322, x:630 y:322, x:575 y:55
		_sm_teb_0 = ConcurrencyContainer(outcomes=['finished', 'failed', 'danger', 'preempted'], input_keys=['plan'], conditions=[
										('finished', [('TEB', 'done')]),
										('failed', [('TEB', 'failed')]),
										('preempted', [('TEB', 'preempted')]),
										('danger', [('AGVcollisionCheck', 'bumper')])
										])

		with _sm_teb_0:
			# x:190 y:35
			OperatableStateMachine.add('TEB',
										FollowPathState(topic="low_level_planner1", topiclisten="/listen"),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempted'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
										remapping={'plan': 'plan'})

			# x:409 y:36
			OperatableStateMachine.add('AGVcollisionCheck',
										agvstatusstate(bumper_topic='/scan'),
										transitions={'bumper': 'danger'},
										autonomy={'bumper': Autonomy.Off})


		# x:35 y:227, x:172 y:223, x:363 y:243, x:537 y:18, x:472 y:241, x:547 y:181, x:544 y:99, x:674 y:184
		_sm_dwa_1 = ConcurrencyContainer(outcomes=['finished', 'failed', 'danger', 'preempted'], input_keys=['plan'], conditions=[
										('failed', [('DWA', 'failed')]),
										('finished', [('DWA', 'done')]),
										('preempted', [('DWA', 'preempted')]),
										('danger', [('AGVcollisionCheck', 'bumper')])
										])

		with _sm_dwa_1:
			# x:101 y:78
			OperatableStateMachine.add('DWA',
										FollowPathState(topic="low_level_planner", topiclisten="/listen"),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempted'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
										remapping={'plan': 'plan'})

			# x:362 y:85
			OperatableStateMachine.add('AGVcollisionCheck',
										agvstatusstate(bumper_topic='/scan'),
										transitions={'bumper': 'danger'},
										autonomy={'bumper': Autonomy.Off})



		with _state_machine:
			# x:193 y:26
			OperatableStateMachine.add('ClearCostmap',
										ClearCostmapsState(costmap_topics=['high_level_planner/clear_costmap','low_level_planner/clear_costmap'], timeout=5.0),
										transitions={'done': 'getPose', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:193 y:162
			OperatableStateMachine.add('Receive Path',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'ExecutePlan', 'empty': 'Continue', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.High, 'failed': Autonomy.High},
										remapping={'goal': 'goal', 'local': 'local', 'plan': 'plan'})

			# x:194 y:233
			OperatableStateMachine.add('ExecutePlan',
										OperatorDecisionState(outcomes=["yes","continue"], hint="Execute the current plan?", suggestion="yes"),
										transitions={'yes': 'check', 'continue': 'Continue'},
										autonomy={'yes': Autonomy.Off, 'continue': Autonomy.Full})

			# x:547 y:244
			OperatableStateMachine.add('DWA',
										_sm_dwa_1,
										transitions={'finished': 'getPose', 'failed': 'zero', 'danger': 'AGVstop', 'preempted': 'Continue'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'danger': Autonomy.Inherit, 'preempted': Autonomy.Inherit},
										remapping={'plan': 'plan'})

			# x:518 y:119
			OperatableStateMachine.add('Continue',
										OperatorDecisionState(outcomes=["yes","no","recover","clearcostmap"], hint="Continue planning to new goal?", suggestion="yes"),
										transitions={'yes': 'getPose', 'no': 'finished', 'recover': 'LogRecovery', 'clearcostmap': 'ClearCostmap'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full, 'recover': Autonomy.Full, 'clearcostmap': Autonomy.Full})

			# x:812 y:478
			OperatableStateMachine.add('Log Fail',
										LogState(text="Path execution failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'Recover'},
										autonomy={'done': Autonomy.Off})

			# x:1046 y:50
			OperatableStateMachine.add('Log Recovered',
										LogState(text="Re-plan after recovery", severity=Logger.REPORT_HINT),
										transitions={'done': 'New Plan'},
										autonomy={'done': Autonomy.Off})

			# x:814 y:51
			OperatableStateMachine.add('New Plan',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'check', 'empty': 'getPose', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Low, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal': 'goal', 'local': 'local', 'plan': 'plan'})

			# x:913 y:341
			OperatableStateMachine.add('Recover',
										OperatorDecisionState(outcomes=["yes","no"], hint="Should we attempt recovery?", suggestion="yes"),
										transitions={'yes': 'LogRecovery', 'no': 'finished'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:949 y:249
			OperatableStateMachine.add('LogRecovery',
										LogState(text="Starting recovery behavior", severity=Logger.REPORT_HINT),
										transitions={'done': 'AGV Recovery Behaviour1'},
										autonomy={'done': Autonomy.Off})

			# x:915 y:162
			OperatableStateMachine.add('AutoReplan',
										OperatorDecisionState(outcomes=["yes","no"], hint="Re-plan to current goal?", suggestion="yes"),
										transitions={'yes': 'Log Recovered', 'no': 'Continue'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:662 y:479
			OperatableStateMachine.add('AGVstop',
										agvTimedStopstate(timeout=2.0, cmd_topic='/cmd_vel', odom_topic='/odom'),
										transitions={'done': 'Log Fail', 'failed': 'Log Fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:545 y:327
			OperatableStateMachine.add('TEB',
										_sm_teb_0,
										transitions={'finished': 'getPose', 'failed': 'zero', 'danger': 'AGVstop', 'preempted': 'Continue'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'danger': Autonomy.Inherit, 'preempted': Autonomy.Inherit},
										remapping={'plan': 'plan'})

			# x:1074 y:197
			OperatableStateMachine.add('AGV Recovery Behaviour1',
										self.use_behavior(AGVRecoveryBehaviour1SM, 'AGV Recovery Behaviour1'),
										transitions={'finished': 'AutoReplan', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:198 y:96
			OperatableStateMachine.add('getPose',
										GetPoseLocalState(topic_goal='move_base_simple/goal', topic_local='/localplanner'),
										transitions={'done': 'Receive Path'},
										autonomy={'done': Autonomy.Off},
										remapping={'goal': 'goal', 'local': 'local'})

			# x:195 y:327
			OperatableStateMachine.add('check',
										checklocalstate(),
										transitions={'TEB': 'TEB', 'DWA': 'DWA'},
										autonomy={'TEB': Autonomy.Off, 'DWA': Autonomy.Off},
										remapping={'plan': 'plan', 'local': 'local'})

			# x:719 y:352
			OperatableStateMachine.add('zero',
										agvTimedStopstate(timeout=4, cmd_topic='/cmd_vel', odom_topic='/odom'),
										transitions={'done': 'AutoReplan', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
