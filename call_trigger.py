def call_trigger(trigger, obstaclemap, identifier, obstacle):
    if trigger[0] == "REPLACE":
        if trigger[1] == "obstacle":
            original = obstacle if trigger[2] == "self" else trigger[2]
            try:
                replacement = int(trigger[3])
            except:
                replacement = trigger[3]
            obstaclemap.replace_obs(obstacle=original, identifier=identifier, new=replacement)
    elif trigger[0] == "DELETE":
        to_delete = obstacle if trigger[2] == "self" else None
        if trigger[1] == "obstacle":
            obstaclemap.delete_obs(obstacle=to_delete, identifier=trigger[2])
        elif trigger[1] == "character":
            obstaclemap.delete_character(character=to_delete, identifier=identifier)
        elif trigger[1] == "trigger":
            obstaclemap.delete_trigger(trigger=to_delete, identifier=identifier)
    elif trigger[0] == "ADD":
        if trigger[1] == "obstacle":
            obstaclemap.add_obstacle(info=trigger[2])
        elif trigger[1] == "item":
            obstaclemap.add_item({"type": trigger[2], "x": obstacle.grid_pos[0], "y": obstacle.grid_pos[1]})
    elif trigger[0] == "KILLALL":
        obstaclemap.killall()
    elif trigger[0] == "SPAWN":
        if trigger[1] == "character":
            if type(trigger[2]) == dict:
                obstaclemap.spawn_character(info=trigger[2])
            else:
                obstaclemap.spawn_character(name=trigger[2], x=trigger[3], y=trigger[4])
    elif trigger[0] == "OPEN":
        if trigger[1] == "door":
            obstaclemap.open_door(trigger[2])
    elif trigger[0] == "CLOSE":
        if trigger[1] == "door":
            obstaclemap.close_door(trigger[2])
    elif trigger[0] == "DEACTIVATE":
        if trigger[1] == "trigger":
            obstaclemap.deactivate_trigger(trigger[2])
    elif trigger[0] == "ACTIVATE":
        if trigger[1] == "trigger":
            obstaclemap.activate_trigger(trigger[2])
    elif trigger[0] == "CHANGEMAP":
        if len(trigger) > 2:
            obstaclemap.changemap(trigger[1], [trigger[2], trigger[3]])
        else:
            obstaclemap.changemap(trigger[1])
    elif trigger[0] == "TRYCHANGEMAP":
        if len(trigger) > 3:
            obstaclemap.trychangemap(trigger[1], trigger[2], [trigger[3], trigger[4]])
        else:
            obstaclemap.trychangemap(trigger[1], trigger[2])
    elif trigger[0] == "KILL":
        if trigger[1] == "character":
            obstaclemap.kill(trigger[2])
    elif trigger[0] == "WINGAME":
        obstaclemap.wingame()
    elif trigger[0] == "TRYWINGAME":
        obstaclemap.trywingame()
