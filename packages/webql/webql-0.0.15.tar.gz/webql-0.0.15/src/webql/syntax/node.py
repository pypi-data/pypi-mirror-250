from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

DEFAULT_INDENT = 2


class Node(BaseModel):
    name: str
    # Freeze the model to make it immutable
    model_config = ConfigDict(frozen=True)

    @property
    def query_name(self) -> str:
        """
        Returns the query name of the node.
        """
        return self.name

    def _dump(self, level: int = 0, indent: int = DEFAULT_INDENT) -> str:
        indent_spaces = " " * indent * level
        res = self.query_name
        return f"{indent_spaces}{res}"

    def dump(self, indent: int = DEFAULT_INDENT) -> str:
        """
        Dump the node to a WebQL Query formatted string.
        """
        return self._dump(level=0, indent=indent)

    def __str__(self) -> str:
        return self.dump()


class IdNode(Node):
    """
    {
        search_btn
    }
    """


class IdListNode(IdNode):
    """
    {
        search_btns[]
    }
    """

    @property
    def query_name(self) -> str:
        return f"{self.name}[]"


class ContainerNode(Node):
    """
    {
        container {
            child1
            child2
        }
    }
    """

    children: Annotated[SerializeAsAny[list[Node]], Field(default_factory=list)]

    def _dump(self, level: int = 0, indent: int = DEFAULT_INDENT) -> str:
        indent_spaces = " " * indent * level
        node_name = f"{self.query_name} " if self.query_name else ""
        header = f"{indent_spaces}{node_name}{{\n"
        # pylint: disable=protected-access
        body = "\n".join([child._dump(indent=indent, level=level + 1) for child in self.children])
        footer = f"\n{indent_spaces}}}"
        return f"{header}{body}{footer}"


class ContainerListNode(ContainerNode):
    """
    {
        container_list[] {
            child1
            child2
        }
    }
    """

    @property
    def query_name(self) -> str:
        return f"{self.name}[]"
