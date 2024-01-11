class playbookController:
    """"""

    _controller_name = "playbookController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def updatePlaybook(self, name):
        """

        Args:
            name: (string): 
            body: (): 

        Consumes: application/json

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "playbook": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/playbook/updatePlaybook'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createPlaybook(self, name):
        """

        Args:
            name: (string): 
            body: (): 

        Consumes: application/json

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "playbook": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/playbook/createPlaybook'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listPlaybooks(self):
        """

        Args:

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "items": {
                  "$ref": "#/components/schemas/PlaybookPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/playbook/listPlaybooks'
        actions = ['get']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getPlaybook(self, name):
        """

        Args:
            name: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "playbook": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/playbook/getPlaybook'
        actions = ['get']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deletePlaybook(self, name):
        """

        Args:
            name: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "playbook": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/playbook/deletePlaybook'
        actions = ['delete']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
