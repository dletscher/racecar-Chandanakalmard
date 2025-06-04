#Main objective i am implementing is if any obstacle is close to the car turn the opposite direction.
#If the car is near to obstacles, tries to avoid obstacles by turning away from them
#Observe the velocity and see if the car is going soo slow thn accelerate.
class Agent:
    def __init__(self):
        self.stuck_number=0
    def chooseAction(self, observations, possibleActions):
        threshold=1.7 # This will decide the distance if the obstacle is close ie: if its close to 1.7 
        goal_velocity=0.09 # this will tell on which speed we want to reach the goal
        low_speed=0.3
        min_velocity=0.2 # I am using this to check the min speed which i consider the car stuck

        lidar=observations['lidar'] # As we know we have 5 distances ie: left,front-left,front,front-right,right
        velocity=observations['velocity'] # this will capture current speed of the car 

        #Here i am checking if the obstacle are close in every direction
        close_to_left_obstacle=lidar[0]<threshold
        close_to_front_left_obstacle=lidar[1]<threshold
        close_to_front_obstacle=lidar[2]<threshold
        close_to_front_right_obstacle=lidar[3]<threshold
        close_to_right_obstacle=lidar[4]<threshold

        #Here we are checking if the car is going too slow thn increase stuck count
        #I implemented this logic becuase if velocity is too low than the car will be stuck in the beginning itself.
        if velocity<min_velocity:
            self.stuck_number+=1
        else:
            self.stuck_number=0

        if self.stuck_number>10:
            self.stuck_number=0
            if ('right','accelerate') in possibleActions:
                return ('right','accelerate')
            elif ('straight','accelerate') in possibleActions:
                return ('straight','accelerate')
            else:
                return possibleActions[0]

        #if its not curve or anything i have set the default action to go straight and accelearate.
        action=('straight','accelerate') if ('straight','accelerate') in possibleActions else possibleActions[0]

        #If the obstacle is close in the front or front_left/right apply brake and turn the opposite.
        if close_to_front_obstacle or close_to_front_left_obstacle or close_to_front_right_obstacle:
            if close_to_front_left_obstacle and ('right','brake') in possibleActions:
                action=('right','brake')
            elif close_to_front_right_obstacle and ('left','brake') in possibleActions:
                action=('left','brake')
            elif ('straight','brake') in possibleActions:
                action=('straight','brake')
        elif  close_to_left_obstacle and ('right','coast') in possibleActions: #if it is complete left slowly move to right and visa versa
            action=('right','coast')
        elif close_to_right_obstacle and ('left','coast') in possibleActions:
            action=('left','coast')
        else:#trying to make it speed this part is for project but tried implementing here , still implementing
            if velocity<low_speed: #if the speed is below 0.3 but not stopped or stuck  we can keep accelerating
                action=('straight','accelerate') if ('straight','accelerate') in possibleActions else action
            elif velocity<goal_velocity:
                action=('straight','accelerate') if ('straight','accelerate') in possibleActions else action
            else:
                action=('straight','coast') if ('straight','coast') in possibleActions else action #if not slow or stuck moving

        return action
