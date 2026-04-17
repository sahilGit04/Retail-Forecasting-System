import matplotlib.pyplot as plt

def plot_sales(df):
    plt.plot(df['date'], df['sales'])
    plt.title("Sales Trend")
    plt.show()