"""
Utilities for working with JSON
"""
import json
from dataclasses import dataclass
from typing import Dict, get_args, get_origin, Union, Any, get_type_hints

try:
    from typing import Self
except ImportError:
    # Python 3.7 compatibility
    from typing import Generic as Self


@dataclass
class JSONSerializable:
    """
    Base class for JSON serializable dataclasses.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert an object to a dictionary.
        """
        ret: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if isinstance(v, JSONSerializable):
                ret[k] = v.to_dict()
            elif isinstance(v, (list, set, tuple)):
                ret[k] = [
                    x.to_dict() if isinstance(x, JSONSerializable) else x for x in v  # type: ignore
                ]
            elif isinstance(v, dict):
                ret[k] = {
                    kk: vv.to_dict() if isinstance(vv, JSONSerializable) else vv
                    for kk, vv in v.items()  # type: ignore
                }
            else:
                ret[k] = v
        return ret

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Self:
        """
        Create an object from a dictionary.
        """

        def _fit_to_type(cc: Any, v: Any) -> Any:
            """
            Helper function to convert a value v to a class type cc
            """
            cc_orig = get_origin(cc) or cc

            # If the type is None or a primitive, return the value as is
            if cc is None or cc_orig in {str, int, float, bool, Any}:
                return v

            # If the type is a list or set, convert each element
            if cc_orig in {list, set}:
                element_class = get_args(cc)[0]
                return [_fit_to_type(element_class, x) for x in v]

            # If the field is a tuple, convert each element
            if cc_orig == tuple:
                return tuple(
                    _fit_to_type(element_class, x)
                    for element_class, x in zip(get_args(cc), v)
                )

            # If the field is a dict, convert each element
            if cc_orig == dict:
                key_class, value_class = get_args(cc)
                return {
                    _fit_to_type(key_class, kk): _fit_to_type(value_class, vv)
                    for kk, vv in v.items()
                }

            if cc_orig == Union:
                # If the field is a Union, try each type until one works
                for cc_child in get_args(cc):
                    try:
                        return _fit_to_type(cc_child, v)
                    except Exception:  # pylint: disable=broad-except
                        pass

            # If the field is a JSONSerializable, convert it
            if issubclass(cc_orig, JSONSerializable):
                return cc.from_dict(v)

            # Otherwise, raise an error
            raise RuntimeError(f"Unknown type {cc}")

        kwargs = {}
        for k, v in d.items():
            child_class = get_type_hints(cls).get(k, None)
            kwargs[k] = _fit_to_type(child_class, v)
        return cls(**kwargs)

    def to_json(self) -> str:
        """
        Convert an object to a JSON string.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, s: str) -> Self:
        """
        Create an object from a JSON string.
        """
        return cls.from_dict(json.loads(s))
