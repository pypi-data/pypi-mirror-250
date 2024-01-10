""" Common models
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, Iterator, List, TypeVar

O = TypeVar('O', bound=type(dataclass))


class Object:

    @classmethod
    def from_mcli(cls, obj: Any) -> 'Object':
        raise NotImplementedError(f"from_mcli not implemented for {cls}")

    def _get_display_columns(self) -> Dict[str, str]:
        return {}


def generate_html_table(data: List[O], columns: Dict[str, str]):
    res = []
    res.append("<table border=\"1\" class=\"dataframe\">")

    # header
    res.append("<thead>")
    res.append("<tr style=\"text-align: right;\">")
    for col in columns.values():
        res.append(f"<th>{col}</th>")
    res.append("</tr>")
    res.append("</thead>")

    # body
    res.append("<tbody>")
    for row in data:
        res.append("<tr>")
        for col in columns:
            value = getattr(row, col, '')
            res.append(f"<td>{value}</td>")
        res.append("</tr>")
    res.append("</tbody>")

    res.append("</table>")
    return "\n".join(res)


class ObjectList(Generic[O]):
    """Common helper for list of objects
    """

    def __init__(self, data: List[O], obj_type: O):
        new_data = []
        for o in data:
            if isinstance(o, obj_type):
                new_data.append(o)
            else:
                new_data.append(obj_type.from_mcli(o))
        self.data = new_data
        self.type = obj_type

    def __iter__(self) -> Iterator[O]:
        return iter(self.data)

    def __getitem__(self, index: int) -> O:
        return self.data[index]

    def __len__(self) -> int:
        return len(self.data)

    @property
    def display_columns(self) -> Dict[str, str]:
        return self.type._get_display_columns(self.type)  # pylint: disable=protected-access

    def __str__(self):
        return '[' + ", ".join([str(i) for i in self.data]) + ']'

    def _repr_html_(self) -> str:
        return generate_html_table(self.data, self.display_columns)

    def to_pandas(self):
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd  # type: ignore
        except ImportError as e:
            raise ImportError("Please install pandas to use this feature") from e

        cols = self.display_columns
        res = {col: [] for col in cols}
        for row in self.data:
            for col in cols:
                value = getattr(row, col)
                res[col].append(value)

        return pd.DataFrame(data=res)
