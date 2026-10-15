import matplotlib.pyplot as plt
import os

def main():
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.text(0.5, 0.5, 'Figure Placeholder', ha='center', va='center')
    ax.axis('off')
    # Save the figure so LaTeX can find it
    out_path = os.path.join(os.path.dirname(__file__), 'dummy.png')
    plt.savefig(out_path)
    plt.close()

if __name__ == "__main__":
    main()
