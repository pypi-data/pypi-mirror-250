from .agent import Agent
import geopandas as gpd
import pandas as pd
import fiona
import copy

class Model:
    def __init__ (self, space: gpd.GeoDataFrame, agents= []):
        """
        A class containing the GIS map and all the agents

        Attributes
        ----------
        space: geopandas object
            a spatial map with polygons read as a geopandas object
        agents: list of Agent objects, default= []
            a list of agents currently in the model
        
        Methods
        -------
        create_agent(properties= {})
            Create an agent with an input dictionary of properties
        agents_with_id(id)
            Search for agents by id
        agents_with_props(condition):
            Search for agents based on its properties
        agents_at(loc_index)
            Find agents based on their location index
        move_agents(agents, new_loc_index)
            Move an agent to a new location
        remove_agents(agents)
            Removes agents from the model
        save_space(file_directory)
            Saves the space to a shape file name
        """
        self.space = space
        self.space["agents"] = [list() for i in range(len(self.space.index))]
        self.space["n_agents"] = [len(self.space.at[i, "agents"]) for i in range(len(self.space.index))]
        self.agents = agents
        self.__id_counter = 0
        for a in self.agents:
            if self.__id_counter < a.id:
                self.__id_counter = a.id
        
    def create_agent(self, properties= {}):
        """
        Create an agent with an input dictionary of properties

        Parameters
        ----------
        properties: dictionary, default= {}
            a dictionary of the properties of agents

        Returns
        -------
        Agent object
            the created Agent object
        """
        a_temp = Agent(properties)
        a_temp.id = self.__id_counter
        self.__id_counter += 1
        self.agents.append(a_temp)
        return(a_temp)

    def create_agents(self, N:int, properties= {}):
        """
        Create a number of agents of type abp.Agent with an input dictionary of properties

        Parameters
        ----------
        N: int
            the number of agents

        properties: dictionary, default= {}
            a dictionary of the properties of agents

        Returns
        -------
        list of Agent objects
            the created Agents
        """
        created_agents = list()
        for n in range(N):
            a_temp = Agent(properties)
            a_temp.id = self.__id_counter
            self.__id_counter += 1
            self.agents.append(a_temp)
            self.created_agents.append(a_temp)
        return(created_agents)
    
    def add_agent(self, agent:Agent, loc_index:int= None):
        """
        add an agent to the model

        Parameters
        ----------
        agent: Agent
            a previously created agent
        
        loc_index: int, default= None
            the index of the patch at which the agent is places

        Returns
        -------
        N/A
        """
        agent.id = self.__id_counter
        self.__id_counter += 1
        self.agents.append(agent)
        if loc_index is not None:
            self.space.at[loc_index, "agents"].append(agent)
            self.space.at[loc_index, "n_agents"] += 1

    
    def agents_with_id(self, id: int):
        """
        Search for agents by id

        Parameters
        ----------
        id: int or list
            the id(s) of the agent to search for

        Returns
        -------
        an Agent object (if id is int) or a list of Agent objects (if id is list)
            the Agent(s) with the provided id(s)

        """
        if type(id) is int:
            for a in self.agents:
                if a.id == id:
                    return a
 
        elif type(id) is list:
            list_temp = []
            for a in self.agents:
                for id_temp in id:
                    if a.id == id_temp:
                        list_temp.append(a)
            return list_temp
        
        else:
            print("Invalid ID")

    def agents_with_props(self, condition: str or function):
        """
        Search for agents based on their properties

        Parameters
        ----------
        condition: str
            a string representing a condition to be evaluated across all agents in the model
            the properties are accessed as `agent.props["property_name"]`
        
        condition: function
            a function taking in an abp.Agent and returning true if the condition is satisfied


        Returns
        -------
        list of Agent objects
            the list of Agent objects fulfilling the condition
        """
        list_temp = []
        for agent in self.agents:
            if eval(condition):
                list_temp.append(agent)
        return list_temp
    
    def agents_at(self, loc_index: str):
        """
        Find all the agents based on their location index

        Parameters
        ----------
        loc_index: int
            the index of the polygon in the space
        
        Returns
        -------
        list of Agent objects
            list of Agent objects located in input index
        """
        return(self.space.at[loc_index, 'agents'])

    def move_agents(self, agents: list or Agent, new_loc_index: int):
        """
        Move an agent to a new location

        Parameters
        ----------
        agents: list of Agent objects or an Agent object
            the agents to move to a new location
        new_loc_index: int
            the index of the polygon in the sapce to which agents will move
        
        Returns
        -------
        N/A
        """
        if type(agents) is list:
            for a in agents:
                if a.location_index is not None:
                    self.space.at[a.location_index, "agents"].remove(a)
                a.location_index = new_loc_index
                self.space.at[new_loc_index, "agents"].append(a)
                self.space.at[new_loc_index, "n_agents"] += 1
        else:
            if agents.location_index is not None:
                self.space.at[agents.location_index, "agents"].remove(agents)
            agents.location_index = new_loc_index
            self.space.at[new_loc_index, "agents"].append(agents)
            self.space.at[new_loc_index, "n_agents"] += 1

    def remove_agents(self, agents: list or Agent):
        """
        Removes agents from the model

        Parameters
        ----------
        agents: list of Agent objects or an Agent object
            the agents to remove from the model
        
        Returns
        -------
        N/A
        """
        if type(agents) is list:
            for a in agents:
                self.space.at[a.location_index, 'agents'].remove(a)
                self.space.at[a.location_index, "n_agents"] -= 1
                self.agents.remove(a)
        
        elif type(agents) is Agent:
            self.space.at[agents.location_index, 'agents'].remove(agents)
            self.space.at[agents.location_index, "n_agents"] -= 1
            self.agents.remove(agents)
        
        else:
            print('Error: agents are not of type Agent or a list of objects of type Agent')

    def save_space(self, file_directory: str):
        """
        Saves the space to a shape file name

        Parameters
        ----------
        file_directory: str
            the full directory of the file to be saved (should end in .shp or .pkl)
        
        Returns
        -------
        N/A
        """
        temp_space = copy.deepcopy(self.space)
        if file_directory[-3:] == 'pkl':
            temp_space.to_pickle(rf'{file_directory}')
        elif file_directory[-3:] == 'shp':
            for c in temp_space.columns:
                for i in temp_space.index:
                    if type(temp_space.at[i, c]) is list:
                        temp_space.at[i, c] = str(temp_space.at[i, c])
            temp_space.to_file(rf'{file_directory}')
        else:
            return('Error: Invalid file type. Insert .shp or .pkl at the end of your file directory string')
        
    def index_at_ij(self, i: int, j: int):
        """
        Finds the patches based on their i and j location (i and j are the indices of a patch in x-direction and y-direction respectively)
        i and j are created during the create_patches function.

        Parameters
        ----------
        i: int
            the index of the patch in x-direction (starts from 1)
        j: int
            the index of the patch in y-direction (starts from 1)
        
        Returns
        -------
        int
            index of the polygon in the abpandas.space geodataframe
        """
        try:
            temp_index_a = self.space[self.space['i'] == i]
            temp_index_b = temp_index_a[temp_index_a['j'] == j]
            return temp_index_b.index[0]
        except:
            print("Error: invalid i or j")
