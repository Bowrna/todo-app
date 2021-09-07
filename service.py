from models import ToDoModel
class ToDoService:
    def __init__(self):
        self.model = ToDoModel()
        
    def create(self, params):
        return self.model.create(params["Title"],params["Description"])

    def list(self):
        response = self.model.list_items()
        return response

    def delete(self, id):
        return self.model.delete(id)

    def update(self, id, update_dict):
        return self.model.update(id, update_dict)

    def get(self, id):
        return self.model.get(id)