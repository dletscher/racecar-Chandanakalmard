#Main objective i am implementing is if any obstacle is close to the car turn the opposite direction.
#If the car is near to obstacles, tries to avoid obstacles by turning away from them
#Observe the velocity and see if the car is going soo slow thn accelerate.
class Agent:
    def __init__(self):
        self.stuck_number=0
    def chooseAction(self, observations, possibleActions):
        threshold=1.6 # This will decide the distance if the obstacle is close ie: if its close to 1.45
        goal_velocity = 8.0
        high_speed_goal_velocity = 11.0# this will tell on which speed we want to reach the goal
        min_velocity=0.35# I am using this to check the min speed which i consider the car stuck

        lidar=observations['lidar'] # As we know we have 5 distances ie: left,front-left,front,front-right,right
        velocity=observations['velocity'] # this will capture current speed of the car 

        #5 distances
        left=lidar[0]
        front_left=lidar[1]
        front=lidar[2]
        front_right=lidar[3]
        right=lidar[4]

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

        if self.stuck_number>5:
            self.stuck_number=0
            if ('right','accelerate') in possibleActions:
                return ('right','accelerate')
            elif ('left', 'accelerate') in possibleActions:
                return ('left', 'accelerate')    
            elif ('straight','accelerate') in possibleActions:
                return ('straight','accelerate')
            else:
                return possibleActions[0]

        #if its not curve or anything i have set the default action to go straight and accelearate.
        action=('straight','accelerate') if ('straight','accelerate') in possibleActions else possibleActions[0]

        #If the obstacle is close in the front or front_left/right apply brake and turn the opposite.
        if close_to_front_obstacle or close_to_front_left_obstacle or close_to_front_right_obstacle:
            if right>left and ('right','brake') in possibleActions:
                return ('right','brake')
            elif left>=right and ('left','brake') in possibleActions:
                return('left', 'brake')
            elif ('straight','brake') in possibleActions:
                return ('straight','brake')
        
        #I am trying to void getting so close to the obstacle
        if close_to_left_obstacle and ('right','coast') in possibleActions:
            return ('right','coast')
        if close_to_right_obstacle and ('left','coast') in possibleActions:
            return ('left','coast')
        if close_to_front_left_obstacle and ('right','coast') in possibleActions:
            return ('right','coast')
        if close_to_front_right_obstacle and ('left','coast') in possibleActions:
            return ('left','coast')
        
        #This will speed when the front is clear 
        if front>3.5 and velocity<high_speed_goal_velocity:
            if ('straight','accelerate') in possibleActions:
                return ('straight','accelerate')
        #Speed up wen it is going slow thn the desired speed
        if velocity<goal_velocity and ('straight','accelerate') in possibleActions:
            return ('straight','accelerate')

        if ('straight','accelerate') in possibleActions:
            return ('straight','accelerate')

        return action                    
        
