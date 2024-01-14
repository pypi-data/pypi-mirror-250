# grphpkg (Still in progress not published)
**grphpkg** is a simple graph library that has DFS and BFS implemented that you can create your own operation.

```python
import Graph
matrix_representation = [
    [0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0]
]

g = Graph(matrix_representation)
g.print_graph()
g.dfs(0, lambda x: print(str(x)+" ", end=""))
g.draw_graph()
```
Create your callback function and pass it in dfs or bfs to execute your operation
## Graph visualization
Call draw graph function
```
g.draw_graph()
```

<img src="./documents/graph.png"/>

## Installing
```
pip install grphpkg
```

## Documentation

