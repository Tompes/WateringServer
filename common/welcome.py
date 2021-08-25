from common.properties import version, project_name, port, address


class Welcome():
    def __init__(self) -> None:
        self.version = version
        self.project_name = project_name
        self.sayHello()

    def sayHello(self):
        print("#" * 50);
        print("#" + "+ Welcome to use %s!" % self.project_name)
        print("#" + "+ Version: " + self.version)
        print("#" + "+ Listening at http://%s:%d" % (address, port))
        print("#" * 50);
