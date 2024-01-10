from flask import Flask
from flask_jwt_extended import JWTManager


class Resource:
    path = None

    @classmethod
    def get_http_methods(cls) -> list:
        has_method = lambda method: method in dir(cls) and callable(getattr(cls, method))
        return {
            'get': cls.get if has_method('get') else None,
            'post': cls.post if has_method('post') else None,
            'put': cls.put if has_method('put') else None,
            'patch': cls.patch if has_method('patch') else None,
            'delete': cls.delete if has_method('delete') else None
        }
    
    @classmethod
    def validate_path(cls):
        if cls.path is None:
            raise Exception("path is not defined")
        if not isinstance(cls.path, str):
            raise Exception("path must be a string")
        if not cls.path.startswith("/"):
            raise Exception("path must start with /")
        


class Api():
    def __init__(self, prefix: str = "/api") -> None:
        self.jwt = JWTManager()
        self.prefix = prefix

    def init_app(self, app: Flask) -> None:
        self.app = app
        self._add_resources()
        self.jwt.init_app(app)

    def _add_resources(self) -> None:
        resource_list = Resource.__subclasses__()
        print("add resources", resource_list)

        for resource in resource_list:
            resource.validate_path()
            resource_path = self.prefix + resource.path
            http_methods = resource.get_http_methods()
            print("http methods", http_methods)

            for http_method, method in http_methods.items():
                if method:
                    print("add url rule", resource_path, method, http_method)
                    self.app.add_url_rule(
                        rule=resource_path, 
                        view_func=method, 
                        methods=[http_method.upper()]
                    )
