import matplotlib.pyplot as plt
import numpy as np


def plot_pressure(
        list_to_plot,
        legend=None,
        xlabel="Angle [degree]",
        ylabel="Pressure [bar]",
        color_mode=None,
        title=None,
        channel=None,
        save_dir=None):
    leg_colors = ["blue", "red"]
    if color_mode == "-b-r1":
        colors = ["-b" if k % 2 == 0 else "-r" for k in range(20)]
    elif color_mode == ".b-r1":
        colors = [".b" if k % 2 == 0 else "-r" for k in range(20)]
    elif color_mode == ".b.r1":
        colors = [".b" if k % 2 == 0 else ".r" for k in range(20)]
    elif color_mode == "-b-r2":
        colors = ["-b" for _ in range(10)]
        colors.extend(["-r" for _ in range(10)])
    elif color_mode == ".b-r2":
        colors = [".b" for _ in range(10)]
        colors.extend(["-r" for _ in range(10)])
    elif color_mode == ".b.r2":
        colors = [".b" for _ in range(10)]
        colors.extend([".r" for _ in range(10)])
    elif color_mode == ".b-stat":
        colors = ["-r", "-m", "-m", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b"]
        leg_colors = ["red", "magenta", "blue"]
    elif color_mode == "-stat":
        colors = ["-r", "-m", "-m", "-y", "-y"]
        leg_colors = ["red", "magenta", "yellow"]
    elif color_mode == "-res.b":
        colors = ["-r", "-g", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b", ".b"]
        leg_colors = ["red", "green", "blue"]
    elif color_mode == "-res-y":
        colors = ["-r", "-g", "-y", "-y", "-b", "-b", "-b", "-b", "-b", "-b", "-b", "-b"]
        leg_colors = ["red", "green", "yellow", "blue"]
    else:
        colors = ["-r", "-g", "-y", "-b"]
        leg_colors = ["red", "green", "yellow", "blue"]

    fig, ax = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(20)
    plt.ylim(0, 10)
    plt.grid(visible=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    for ind, values in enumerate(list_to_plot):
        plt.plot(range(-360, 360), values, colors[ind])

    if legend is not None:
        plt.legend(legend)
        ax = plt.gca()
        leg = ax.get_legend()
        for k in range(len(leg.legendHandles)):
            leg.legendHandles[k].set_color(leg_colors[k])

    if title is not None:
        plt.title(title)

    if channel is not None:
        for k in range(len(channel.index)):
            plt.text(-300 + 50 * k, 9, str(list(channel.index)[k]), weight="bold")
            plt.text(-300 + 50 * k, 8.5, str(channel.values.round(2)[k]), weight="bold")

    if save_dir is not None:
        title = title.replace(" ", "_")
        plt.savefig(save_dir + "/" + title + ".jpg", format="jpg")

    plt.show()
    plt.close()


def show_basic_kriging_plot_1d(
        X: np.array,
        y: np.array,
        X_train: np.array,
        y_train: np.array,
        kriging_mean: np.array,
        kriging_std: np.array,
        var_name: str,
        y_label="f(x)",
        save_dir=None
):
    plt.scatter(X, y, label="Test observations", )
    plt.scatter(X_train, y_train, label="Train observations")

    plt.plot(X, kriging_mean, label="Mean prediction")
    plt.fill_between(
        X.ravel(),
        kriging_mean - 1.96 * kriging_std,
        kriging_mean + 1.96 * kriging_std,
        alpha=0.5,
        label=r"95% confidence interval",
    )
    offset = (np.max(X) - np.min(X)) / 10
    plt.xlim((np.min(X) - offset, np.max(X) + offset))
    plt.legend()
    plt.xlabel(f"{var_name}")
    plt.ylabel(y_label)
    title = f"Behavior for varying {var_name}"
    plt.title(title)
    if save_dir is not None:
        title = title.replace(" ", "_")
        plt.savefig(save_dir + "/" + title + ".jpg", format="jpg")
    plt.show()


def show_basic_kriging_plot_1d_with_grid(
        X: np.array,
        y: np.array,
        X_train: np.array,
        y_train: np.array,
        X_grid: np.array,
        kriging_mean: np.array,
        kriging_std: np.array,
        var_name: str,
        y_label="f(x)",
        save_dir=None
):
    plt.scatter(X, y, label="Test observations", )
    plt.scatter(X_train, y_train, label="Train observations")
    plt.plot(X_grid, kriging_mean, label="Mean prediction")
    plt.fill_between(
        X_grid.ravel(),
        kriging_mean - 1.96 * kriging_std,
        kriging_mean + 1.96 * kriging_std,
        alpha=0.5,
        label=r"95% confidence interval",
    )
    offset = (np.max(X) - np.min(X)) / 34
    plt.xlim((np.min(X) - offset, np.max(X) + offset))
    plt.legend()
    plt.xlabel(f"{var_name}")
    plt.ylabel(y_label)
    plt.title(f"Behavior for varying {var_name}")
    title = f"Behavior for varying {var_name}"
    plt.title(title)
    if save_dir is not None:
        title = title.replace(" ", "_")
        plt.savefig(save_dir + "/" + title + ".jpg", format="jpg")
    plt.show()


def show_basic_kriging_improvement_1d(
        X: np.array,
        y: np.array,
        X_train: np.array,
        y_train: np.array,
        kriging_mean: np.array,
        kriging_std: np.array,
        new_x: np.array,
        new_y: float,
        var_name: str,
        y_label="f(x)",
        save_dir=None):
    plt.plot(X, y, label=r"$f(x)$", linestyle="dotted")
    plt.scatter(X_train, y_train, label="Observations")
    plt.scatter(new_x, new_y, label="Added Observation", marker="*", s=200, c="purple")
    plt.plot(X, kriging_mean, label="Mean prediction")
    plt.fill_between(
        X.ravel(),
        kriging_mean - 1.96 * kriging_std,
        kriging_mean + 1.96 * kriging_std,
        alpha=0.5,
        label=r"95% confidence interval",
    )
    plt.legend()
    plt.xlabel(f"{var_name}")
    plt.ylabel(y_label)
    title = f"Behavior for varying {var_name}"
    plt.title(title)
    if save_dir is not None:
        title = title.replace(" ", "_")
        plt.savefig(save_dir + "/" + title + ".jpg", format="jpg")

    if "current max" in var_name:
        plt.scatter(X_train[y_train.argmax()], y_train.max(), marker="*", s=300, c="red")

    plt.show()


def show_multiD_slices_plots(
        X_row: np.array,
        y_point: float,
        X_grid: np.array,
        gaussian_process_,
        y_label="f(x)",
        save_dir=None):
    kriging_mean, kriging_std = gaussian_process_.predict(X_grid, return_std=True)
    for i in range(X_row.shape[1]):
        plt.scatter(X_row[i], y_point, label="Observation")
        plt.plot(X_grid[i], kriging_mean[i], label="Mean prediction")
        plt.fill_between(
            X_grid.iloc[:, i].ravel(),
            kriging_mean - 1.96 * kriging_std[:, i],
            kriging_mean + 1.96 * kriging_std[:, i],
            alpha=0.5,
            label=r"95% confidence interval",
        )
        offset = (np.max(X_grid.iloc[:, i]) - np.min(X_grid.iloc[:, i])) / 34
        plt.xlim((np.min(X_grid.iloc[:, i]) - offset, np.max(X_grid.iloc[:, i]) + offset))
        plt.legend()

        var_name = X_grid.columns[i]
        plt.xlabel(f"{var_name}")
        plt.ylabel(y_label)
        plt.title(f"Behavior for varying {var_name}")
        plt.show()
