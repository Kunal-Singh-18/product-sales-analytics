import matplotlib.pyplot as plt
from api.constants import CHART_TYPES

def visualize_results(results):

    metric = results["metric"]
    group_by = results["group_by"]

    if group_by:

        chart_type = CHART_TYPES[group_by]

    elif metric.startswith("top_"):

        chart_type = "bar"

    else:

        print(
            "\nVisualization requires grouped analytical data."
            "\nCharts are meaningful only when comparing values "
            "across categories or rankings."
            "\nPlease run the analysis again using a "
            "'Group By' field or choose a ranking metric."
        )

        return

    if chart_type == "bar":

        plot_bar_chart(results)

    elif chart_type == "line":

        plot_line_chart(results)

    elif chart_type == "pie":

        plot_pie_chart(results)


def plot_bar_chart(results):

    data = results["results"]

    if not data:

        print("\nNo data available for visualization.")
        return

    keys = list(data[0].keys())

    y_key = None

    for key in keys:
        if isinstance(data[0][key], (int, float)):
            y_key = key
            break

    x_key = next(key for key in keys if key != y_key)

    x_values = [row[x_key] for row in data]
    y_values = [row[y_key] for row in data]

    plt.figure(figsize=(10, 6))

    plt.bar(x_values, y_values)

    metric = results["metric"].replace("_", " ").title()

    if results["group_by"]:

        group_by = results["group_by"].replace("_", " ").title()

        title = f"{metric} by {group_by}"
        x_label = group_by

    else:

        title = metric
        x_label = x_key.replace("_", " ").title()

    plt.title(title)

    plt.xlabel(x_label)

    plt.ylabel(y_key.replace("_", " ").title())

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


def plot_line_chart(results):

    data = results["results"]

    if not data:

        print("\nNo data available for visualization.")
        return

    keys = list(data[0].keys())

    y_key = None

    for key in keys:
        if isinstance(data[0][key], (int, float)):
            y_key = key
            break

    x_key = next(key for key in keys if key != y_key)

    x_values = [row[x_key] for row in data]
    y_values = [row[y_key] for row in data]

    plt.figure(figsize=(10, 6))

    plt.plot(
        x_values,
        y_values,
        marker="o",
        linewidth=2
    )

    metric = results["metric"].replace("_", " ").title()

    if results["group_by"]:

        group_by = results["group_by"].replace("_", " ").title()

        title = f"{metric} by {group_by}"
        x_label = group_by

    else:

        title = metric
        x_label = x_key.replace("_", " ").title()

    plt.title(title)

    plt.xlabel(x_label)

    plt.ylabel(y_key.replace("_", " ").title())

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def plot_pie_chart(results):

    data = results["results"]

    if not data:

        print("\nNo data available for visualization.")
        return

    keys = list(data[0].keys())

    y_key = None

    for key in keys:
        if isinstance(data[0][key], (int, float)):
            y_key = key
            break

    x_key = next(key for key in keys if key != y_key)

    labels = [row[x_key] for row in data]
    values = [row[y_key] for row in data]
    
    print(data[0])

    for key in data[0]:
        print(key, type(data[0][key]))

    plt.figure(figsize=(8, 8))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    metric = results["metric"].replace("_", " ").title()

    if results["group_by"]:

        group_by = results["group_by"].replace("_", " ").title()

        title = f"{metric} by {group_by}"

    else:

        title = metric

    plt.title(title)

    plt.tight_layout()

    plt.show()