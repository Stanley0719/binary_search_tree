from dataclasses import dataclass


@dataclass
class Node:
    value: int
    index: int
    depth: int
    parent: "Node | None" = None
    left: "Node | None" = None
    right: "Node | None" = None


@dataclass
class Insertion:
    value: int
    node: Node
    route: list[Node]
    directions: list[str]


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None
        self.insertions: list[Insertion] = []

    def insert(self, value: int) -> Insertion:
        node = Node(value=value, index=len(self.insertions), depth=0)
        route: list[Node] = []
        directions: list[str] = []

        if self.root is None:
            self.root = node
            route.append(node)
        else:
            current = self.root
            while True:
                route.append(current)
                if value < current.value:
                    directions.append("左")
                    if current.left is None:
                        node.parent = current
                        node.depth = current.depth + 1
                        current.left = node
                        break
                    current = current.left
                else:
                    directions.append("右")
                    if current.right is None:
                        node.parent = current
                        node.depth = current.depth + 1
                        current.right = node
                        break
                    current = current.right
            route.append(node)

        insertion = Insertion(
            value=value,
            node=node,
            route=route,
            directions=directions,
        )
        self.insertions.append(insertion)
        return insertion

    def nodes_in_order(self) -> list[Node]:
        result: list[Node] = []

        def visit(node: Node | None) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node)
            visit(node.right)

        visit(self.root)
        return result


def parse_sequence(text: str) -> list[int]:
    parts = text.replace(",", " ").split()
    if not parts:
        raise ValueError("請輸入至少一個整數。")

    try:
        return [int(part) for part in parts]
    except ValueError as error:
        raise ValueError("序列只能包含整數，請以逗號或空格分隔。") from error
