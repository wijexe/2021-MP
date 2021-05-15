clients = {}

class Moderator():
    def create_data(self, name):
        if name not in clients:
            clients[name] = []
            clients[name].append([False, False])
        return clients

    def become_an_admin(self, name):
        clients.update({name: [[False, True]]})
        return clients

    def ban(self, name):
        clients.update({name: [[True, False]]})
        return clients

    def unban(self, name):
        clients.update({name: [[False, False]]})
        return clients

    def admin(self, name, message):
        if clients[name][0][1]:
            for name in clients:
                if message.endswith("/ban" + ' ' + name) or message.endswith("/ban" + name):
                    self.ban(name)
                    continue
                if message.endswith("/unban" + ' ' + name) or message.endswith("/unban" + name):
                    self.unban(name)
                    continue
