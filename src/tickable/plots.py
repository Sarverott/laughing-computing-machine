import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def plot_first_move_preference(preference_census):
    cumulative = np.sum(preference_census, axis=0)
    df = pd.DataFrame(cumulative, columns=["A", "B", "C"], index=["1", "2", "3"])
    plt.figure(figsize=(6, 5))
    sns.heatmap(df, annot=True, cmap="YlGnBu", cbar=True)
    plt.title("Skumulowana preferencja pól (pierwszy ruch)")
    plt.tight_layout()
    plt.show()

def plot_fitness_over_time(fitness_history):
    avg_fitness = [np.mean(gen) for gen in fitness_history]
    max_fitness = [np.max(gen) for gen in fitness_history]

    plt.figure(figsize=(10, 5))
    plt.plot(avg_fitness, label="Średni fitness")
    plt.plot(max_fitness, label="Maksymalny fitness")
    plt.title("Ewolucja fitnessu w czasie")
    plt.xlabel("Pokolenie")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_all_statistics(fitness_story, preference_census):
    generations = len(fitness_story)
    
    # Obliczenia metryk
    avg_fitness = [np.mean(gen) for gen in fitness_story]
    max_fitness = [np.max(gen) for gen in fitness_story]
    cumulative_heat = np.sum(preference_census, axis=0)

    # Tworzenie subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Fitness w czasie
    axs[0, 0].plot(avg_fitness, label="Średni fitness")
    axs[0, 0].plot(max_fitness, label="Maksymalny fitness")
    axs[0, 0].set_title("Fitness w czasie")
    axs[0, 0].set_xlabel("Pokolenie")
    axs[0, 0].set_ylabel("Fitness")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Heatmapa finalna
    final_heat = preference_census[-1]
    final_df = pd.DataFrame(final_heat, columns=["A", "B", "C"], index=["1", "2", "3"])
    sns.heatmap(final_df, annot=True, cmap="coolwarm", cbar=True, ax=axs[0, 1])
    axs[0, 1].set_title("Preferencje pierwszego ruchu (ostatnia generacja)")

    # Heatmapa skumulowana
    cumulative_df = pd.DataFrame(cumulative_heat, columns=["A", "B", "C"], index=["1", "2", "3"])
    sns.heatmap(cumulative_df, annot=True, cmap="coolwarm", cbar=True, ax=axs[1, 0])
    axs[1, 0].set_title("Preferencje pierwszego ruchu (skumulowane)")

    # Histogram dominujących pól
    dominant_counts = cumulative_heat.flatten()
    axs[1, 1].bar(range(9), dominant_counts, tick_label=[f"{i//3},{i%3}" for i in range(9)])
    axs[1, 1].set_title("Dominacja pól w łącznych preferencjach")
    axs[1, 1].set_xlabel("Pozycja pola (rząd, kolumna)")
    axs[1, 1].set_ylabel("Liczba wyborów")

    plt.tight_layout()
    plt.show()

def display_game_state(game):
    board = game.display_board()
    state = game.state()

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_title("Aktualny stan gry: Kółko i krzyżyk", fontsize=14, pad=15)

    table_data = [["X" if cell == -1 else "O" if cell == 1 else "" for cell in row] for row in board]
    table = ax.table(
        cellText=table_data,
        cellLoc='center',
        loc='center',
        colWidths=[0.2]*3
    )
    table.scale(1, 2)
    for (i, j), cell in table.get_celld().items():
        cell.set_fontsize(24)
        cell.set_height(0.3)

    ax.axis('off')

    info_text = f"""\
Tura: {state['turn']}
Gra zakończona: {'Tak' if state['endgame'] else 'Nie'}
Zwycięzca: {state['winner'] or 'Brak'}
Następny ruch: {state['now_plays']}\
"""
    fig.text(1.05, 0.5, info_text, fontsize=12, va='center', ha='left',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0f0f0"))

    plt.tight_layout()
    plt.show()

# --- Narzędzie wizualizacyjne ---
def game_predictions(histogram, preferences):
    x = np.arange(1, 10)
    win_prob = np.clip(histogram["win"], 0, 1)
    lose_prob = np.clip(histogram["lose"], 0, 1)

    board_df = pd.DataFrame(preferences, columns=['A', 'B', 'C'], index=['1', '2', '3'])

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].plot(x, win_prob, label='f(x) - szansa na wygraną', marker='o')
    axs[0].plot(x, lose_prob, label='g(x) - szansa na przegraną', marker='x')
    axs[0].set_title('Szansa na wygraną/przegraną w zależności od ruchu')
    axs[0].set_xlabel('Ruch (x)')
    axs[0].set_ylabel('Prawdopodobieństwo')
    axs[0].legend()
    axs[0].grid(True)
    sns.heatmap(board_df, annot=True, cmap='coolwarm', cbar=True, ax=axs[1])
    axs[1].set_title('Heatmapa preferencji pól planszy')
    plt.tight_layout()
    plt.show()

def make_histogram(fitness_history, size=9):
    """
    Przekształca historię fitnessów z wielu generacji w histogram
    szansy na wygraną i przegraną dopasowany do długości wykresu f(x), g(x).

    Parameters:
        fitness_history (list of list): lista fitnessów z każdej generacji
        size (int): liczba punktów w osi x (domyślnie 9 = liczba tur w grze)

    Returns:
        dict: {"win": [...], "lose": [...]}
    """
    fitness_avg_per_gen = [np.mean(gen) if gen else 0.0 for gen in fitness_history]

    # Skalowanie do 'size' punktów
    if len(fitness_avg_per_gen) < size:
        # Dublowanie wartości jeśli za mało pokoleń
        expanded = np.interp(
            np.linspace(0, len(fitness_avg_per_gen) - 1, size),
            np.arange(len(fitness_avg_per_gen)),
            fitness_avg_per_gen
        )
    else:
        # Wybranie reprezentatywnych indeksów
        x_indices = np.linspace(0, len(fitness_avg_per_gen) - 1, size).astype(int)
        expanded = np.array(fitness_avg_per_gen)[x_indices]

    expanded = np.clip(expanded, 0, 1)

    return {
        "win": expanded,
        "lose": 1 - expanded
    }