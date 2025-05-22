import streamlit as st
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

st.title("📊 Task Scheduler using Topological Sorting (Kahn's Algorithm)")

# Input tasks
n = st.number_input("Enter number of tasks", min_value=1, step=1)
tasks = []

if n:
    st.subheader("Enter Task Names:")
    for i in range(n):
        task = st.text_input(f"Task {i+1}", key=f"task_{i}")
        tasks.append(task)

# Input dependencies
e = st.number_input("Enter number of dependencies", min_value=0, step=1)
dependencies = []

if e:
    st.subheader("Enter Dependencies (Task1 must come before Task2):")
    for i in range(e):
        col1, col2 = st.columns(2)
        with col1:
            pre = st.selectbox(f"Dependency {i+1} - Task 1", tasks, key=f"pre_{i}")
        with col2:
            post = st.selectbox(f"Dependency {i+1} - Task 2", tasks, key=f"post_{i}")
        if pre and post and pre != post:
            dependencies.append((pre, post))

if st.button("Compute Topological Order"):
    if len(set(tasks)) != n or "" in tasks:
        st.error("Please enter valid and unique task names.")
    else:
        # Build graph and in-degree map
        graph = defaultdict(list)
        in_degree = {task: 0 for task in tasks}

        for pre, post in dependencies:
            graph[pre].append(post)
            in_degree[post] += 1

        # Kahn's Algorithm
        queue = deque([task for task in tasks if in_degree[task] == 0])
        topo_order = []

        while queue:
            current = queue.popleft()
            topo_order.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(topo_order) == len(tasks):
            st.success("✅ Valid Topological Order (Execution Sequence):")
            for i, task in enumerate(topo_order, 1):
                st.markdown(f"**{i}. {task}**")

            # Visualize using networkx
            G = nx.DiGraph()
            G.add_edges_from(dependencies)
            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(G)
            nx.draw(
                G, pos, ax=ax,
                with_labels=True,
                node_color="skyblue",
                node_size=3000,
                font_size=10,
                font_weight="bold",
                arrows=True,
                arrowstyle='-|>',
                arrowsize=20
            )
            st.pyplot(fig)
        else:
            st.error("❌ Cycle detected! No valid task execution order.")

