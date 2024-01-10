import typing
from jsonbind.core.type_binding import TypeBinding, JsonTypes, Bindings
from jsonbind.special.serializable import Serializable

Number = typing.Union[bool, int, float]


class Object(Serializable):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._output_names: typing.Dict[str, str] = dict()

    def __eq__(self, other: "Object") -> bool:
        for key, value in self.__dict__.items():
            if key not in other.__dict__:
                return False
            if other.__dict__[key] != value:
                return False
        return True

    def get_members(self) -> typing.List[typing.Tuple[str, typing.Any]]:
        members: typing.List[typing.Tuple[str, typing.Any]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            members.append((key, value))
        return members

    def get_columns(self) -> typing.List[typing.Tuple[str, type]]:
        columns: typing.List[typing.Tuple[str, type]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                columns += [(key + "." + column_name, column_type) for column_name, column_type in value.get_columns()]
            else:
                columns.append((key, value.__class__))
        return columns

    def get_numeric_columns(self) -> typing.List[typing.Tuple[str, type]]:
        columns: typing.List[typing.Tuple[str, type]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                columns += [(key + "." + column_name, column_type) for column_name, column_type in value.get_numeric_columns()]
            else:
                if isinstance(value, Number):
                    columns.append((key, value.__class__))
        return columns

    def get_values(self) -> typing.List[typing.Tuple[str, typing.Any]]:
        values = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                values += [(key + "." + column_name, column_value) for column_name, column_value in value.get_values()]
            else:
                values.append((key, value))
        return values

    def get_numeric_values(self) -> typing.List[typing.Tuple[str, Number]]:
        values: typing.List[typing.Tuple[str, Number]] = list()
        for key, value in self.__dict__.items():
            if not key or key.startswith('_'):
                continue
            if isinstance(value, Object):
                values += [(key + "." + column_name, column_value) for column_name, column_value in value.get_numeric_values()]
            else:
                if isinstance(value, Number):
                    values.append((key, value))
        return values

    def set_values(self, values: typing.List[typing.Tuple[str, typing.Any]]):
        for column_name, column_value in values:
            Object.__setitem__(self, column_name, column_value)

    def convert_to(self, cls: type) -> "Object":
        if not issubclass(cls, Object):
            raise RuntimeError("type must derive from jsonbind.Object")
        values = self.get_values()
        nv = cls()
        nv.set_values(values=values)
        return nv

    def __getitem__(self, key: str) -> typing.Any:
        pos = key.find(".")
        if pos >= 0:
            child_key = key[pos+1:]
            key = key[:pos]
            if key not in self.__dict__:
                raise KeyError("key '{}' not found".format(key))
            child = self.__dict__[key]
            if isinstance(child, Object):
                return Object.__getitem__(self=child,
                                          key=child_key)
            else:
                raise KeyError("key '{}' not found".format(child_key))
        else:
            if key not in self.__dict__:
                raise KeyError("key '{}' not found".format(key))
            return self.__dict__[key]

    def __setitem__(self, key, value):
        pos = key.find(".")
        if pos >= 0:
            child_key = key[pos+1:]
            key = key[:pos]
            if key not in self.__dict__:
                self.__dict__[key] = Object()

            child = self.__dict__[key]
            if isinstance(child, Object):
                return Object.__setitem__(self=child,
                                          key=child_key,
                                          value=value)
            else:
                raise KeyError("key '{}' not found".format(child_key))
        else:
            if hasattr(self, key):
                if not isinstance(value,self.__dict__[key].__class__):
                    value = self.__dict__[key].__class__(value)
            else:
                Bindings.get_binding(value.__class__)
            setattr(self, key, value)

    def __copy__(self) -> "Object":
        new_object = self.__class__()
        new_object.__dict__.update(self.__dict__)
        return new_object

    def __deepcopy__(self, memo: dict = None) -> "List":
        from copy import deepcopy
        new_object = self.__class__()
        memo[id(self)] = new_object
        for key, value in self.__dict__.items():
            new_object.__dict__[key] = deepcopy(value, memo=memo)
        return new_object


class ObjectBinding(TypeBinding):
    def __init__(self):
        super().__init__(json_type=dict, python_type=Object)

    def to_json_value(self, python_value: typing.Any) -> typing.Union[JsonTypes]:
        json_value = dict()
        for member_name in vars(python_value):
            if member_name.startswith('_'):
                continue
            member = getattr(python_value, member_name)
            member_type = member.__class__
            bond = Bindings.get_binding(member_type)
            if not bond:
                raise TypeError("no binding found for member {} of type {}".format(member_name, member_type.__name__))
            json_value[member_name] = bond.to_json_value(getattr(python_value, member_name))
        return json_value

    def to_python_value(self, json_value: typing.Union[JsonTypes], python_type: type) -> typing.Any:
        python_value = python_type()
        for member_name, member_json_value in json_value.items():
            if member_name in python_value.__dict__:
                member = getattr(python_value, member_name)
                member_type = member.__class__
                member_python_value = Bindings.to_python_value(json_value=member_json_value,
                                                               python_type=member_type)
                setattr(python_value, member_name, member_python_value)
            else:
                setattr(python_value, member_name, member_json_value)
        return python_value


Bindings.set_binding(ObjectBinding())

