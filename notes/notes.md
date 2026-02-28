## Json
    like a dictionary but in Json format
    - key value pairs
    - can be nested
    - used for communication between different parts of the system
    - can be used to store data in a structured way
    RESEARCH FURTHER TYPE SHIT


## gtk
    a library for creating graphical user interfaces (GUIs)
    - used for creating the user interface of the system
    - can be used to create buttons, labels, text boxes, etc.
    - can be used to create a responsive and user-friendly interface
    RESEARCH FURTHER

## getters
    All get Json
    - /
        empty Json
        response code

    - /get_mode
        imu_instruction
        script
        gamepad
    - /get_imu
        x   y   z
        vx  vy  vz
        ax  ay  az
        roll    pitch   yaw
        vroll   vpitch  vyaw
    - /get_scripts
        list of strings
        script paths

## setters
    all takes Json
    - /set_mode
        modes to choose from
            imu_instruction
            script
            gamepad
        use this to get a success or fail code
            automatically returns
            tells us the way in which it fails or if it succeeds
    - /set_imu
        x   y   z
        vx  vy  vz
        ax  ay  az
        roll    pitch   yaw
        vroll   vpitch  vyaw

        NULL
            keep as is
    - /run_script

# status codes
    200 OK
    400 Bad Request
    404 Not Found
    500 Internal Server Error
    get
        r.status_code