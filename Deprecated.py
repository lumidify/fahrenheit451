        """
        self.layers[layer] = []
        with open(path) as f:
            maplines = f.readlines()
        state = ""
        obs = {}
        for line in maplines:
            if line != "\n" and not line.startswith("#"):
                if line.startswith("***reserve obs***"):
                    state = "reserve"
                elif line.startswith("***current obs***"):
                    state = "current"
                elif line.startswith("*obs"):
                    if len(obs) > 0:
                        if state == "reserve":
                            self.reserves[obs["id"]] = self.create_obstacle(obs)
                        elif state == "current":
                            self.layers[layer].append(self.create_obstacle(obs))
                    obs = {"type": line.split()[1]}
                else:
                    line_split = line.split("=")
                    value = line_split[1].strip()
                    if line_split[0] in ["x", "y", "height", "width"]:
                        value = float(value)
                    obs[line_split[0]] = value
        if len(obs) > 0:
            if state == "reserve":
                self.reserves[obs["id"]] = self.create_obstacle(obs)
            elif state == "current":
                self.layers[layer].append(self.create_obstacle(obs))
        """
        """
        with open(path) as f:
            lines = f.readlines()
            current = {}
            for line in lines:
                line_split = line.split("=")
                if line.startswith("#") or line.strip() == "":
                    continue
                elif line.startswith("*character"):
                    if len(current) > 0:
                        self.charactermap.append(self.create_character(current))
                        current = {}
                    current["name"] = line.split()[1].strip()
                else:
                    value = line_split[1].strip()
                    if value == "None":
                        value = None
                    elif line_split[0] == "items_dropped":
                        value = [x.strip() for x in value.split(",")]
                    elif line_split[0] == "waypoints":
                        value = [[float(y) for y in x.split()] for x in value.split(",")]
                    elif line_split[0] == "random_walk_area":
                        value = [float(x) for x in value.split()]
                    elif line_split[0] == "health":
                        value = int(value)
                    elif line_split[0] in ["x", "y"]:
                        value = float(value)
                    current[line_split[0]] = value
            if len(current) > 0:
                self.charactermap.append(self.create_character(current))
        """
        """
        with open(path) as f:
            lines = f.readlines()
            current = {}
            for line in lines:
                if line.startswith("#") or line.strip() == "":
                    continue
                elif line.startswith("*trigger"):
                    if len(current) > 0:
                        self.triggers.append(Trigger(obstaclemap=self, **current))
                else:
                    line_split = line.split("=")
                    value = line_split[1].strip()
                    if line_split[0] in ["x", "y", "width", "height"]:
                        value = float(value)
                    elif line_split[0] == "deactivate_after_use":
                        if value == "False":
                            value = False
                        elif value == "True":
                            value = True
                    current[line_split[0]] = value
            if len(current) > 0:
                self.triggers.append(Trigger(obstaclemap=self, **current))
        """
