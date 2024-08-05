def reward_function(params):
    '''
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
    "distance_from_center": float,         # distance in meters from the track center 
    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": float,                      # agent's yaw in degrees
    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
    "progress": float,                     # percentage of track completed
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # agent's steering angle in degrees
    "steps": int,                          # number steps completed
    "track_length": float,                 # track length in meters.
    "track_width": float,                  # width of the track
    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
    '''
# print(reward_function({"distance_from_center": 100, "track_width": 50,"steering_angle": 20,"progress": 0.5,"steps": 5,"speed": 100,"is_offtrack": 'false', "all_wheels_on_track": 'true'}))
    
 # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering_angle = abs(params['steering_angle']) # Only need the absolute steering angle
    progress = params['progress']
    speed = params['speed']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']

# Reward for staying on the track
    reward = 1.0 if all_wheels_on_track else -1.0
    
# Reward for distance from center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        return 1e-3  # likely crashed/ close to off track

# Reward for speed
    reward += speed / 4.0

# Reward Boost for progress
    progress_dict = {
        10: 10,
        20: 20,
        30: 40,
        40: 80,
        50: 160,
        60: 320,
        70: 640,
        80: 1280,
        90: 2560,
        100: 5120
    }
    int_progress = int(progress)
    if int_progress % 10 == 0:
        try:
            reward += progress_dict[int_progress]
        except:
            pass
           
# Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 12
# Penalize reward if the car is steering too much
    if steering_angle > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    penalty_factor = 1
# Calculate lateral acceleration (simple model: speed^2 * steering angle)
    lateral_acceleration = speed ** 2 * abs(steering_angle)    
# Penalize high lateral acceleration
    reward += -lateral_acceleration * penalty_factor

# Simple friction model
#    grip_factor = 1 - (distance_from_center / track_width)  
# Penalize based on lateral force (steering angle and speed)
#    lateral_force = abs(steering_angle) * speed    
# Reward maintaining traction
#    reward += grip_factor - lateral_force * penalty_factor

# Penalty for going off track
    if is_offtrack:
        reward -= distance_from_center

    return float(reward)
