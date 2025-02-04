class Router:

    route_apps = {'stock'}
    tableIn2p3 = {"famille","modele","labo"}
    tableLocal = {"preferes"}


    def db_for_read(self,model,**hints):

        if model._meta.app_label in self.tableIn2p3:
            return 'in2p3'
        return 'local'

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.tableIn2p3:
            return 'in2p3'
        return 'local'

    def allow_relation(self,obj1,obj2,**hints):
      return True


    def allow_migrate(self,db,app_label,model_name=None, **hints):
        if db=='in2p3':
           return model_name in self.tableIn2p3
        if db=='local':
            return model_name in self.tableLocal
        return False