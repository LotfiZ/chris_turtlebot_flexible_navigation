#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_turtlebot_flexbe_behaviors.agv_flex_planner_sm import AGVFlexPlannerSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 17 2019
@author: Deepanshu
'''
class Special_behaviourSM(Behavior):
	'''
	Implements special behaviour and switches between DWA and TEB
	'''


	def __init__(self):
		super(Special_behaviourSM, self).__init__()
		self.name = 'Special_behaviour'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(AGVFlexPlannerSM, 'AGV Flex Planner')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:322, x:130 y:322
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:92 y:80
			OperatableStateMachine.add('AGV Flex Planner',
										self.use_behavior(AGVFlexPlannerSM, 'AGV Flex Planner'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
