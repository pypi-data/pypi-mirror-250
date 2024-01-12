class Agent:
    def __init__(self, properties= {}):
        """
        a class representing a computational unit with properties that can interact with other agents and with a space

        Attributes
        ----------
        properties: dictionary, default= {}
            the properties of the agent object
        __id: int
            a unique id given to each agent (accessed by the Model class when creating the Agent)
        location_index: int, default= None
            the index to which the agent is assigned (accessed by the Model class when creating or moving the Agent)
        """
        self.props = properties
        self.__id = 0
        self.location_index = None
        self.location_xy = None