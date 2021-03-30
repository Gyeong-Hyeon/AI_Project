def msg_processor(msg_code):
 
    msg_code = int(msg_code)

    msg_list = [
        (
            'Successfully signed in :)',
            'success'
        ),
        (
            'User does not exist :( Please sign up',
            'warning'
        ),
        (
            'Password is wrong :(',
            'warning'
        ),
        (
            'Please fill in all blanks!',
            'warning'
        ),
        (
            'This username is already taken :(',
            'warning'
        ),
        (
            'Successfully signed up :)',
            'success'
        )
    ]

    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }
