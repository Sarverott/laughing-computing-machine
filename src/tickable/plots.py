import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
from collections import Counter

def plot_fitness_3d(fitness_story):
    """
    Wizualizuje trajektorie fitnessów populacji w czasie w 3D.
    Każdy osobnik to linia w przestrzeni pokoleń (x), fitnessu (z), i indeksu (y).
    Najlepszy osobnik ostatniego pokolenia wyróżniony czerwonym kolorem.
    """
    generations = len(fitness_story)
    population_size = len(fitness_story[0]) if generations > 0 else 0

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Transponujemy dane: osobnik → lista fitnessów w czasie
    fitness_array = np.array(fitness_story).T

    # Zaznaczamy najlepszego osobnika
    best_index = np.argmax(fitness_array[:, -1])

    for i, fitness_track in enumerate(fitness_array):
        x = np.arange(generations)
        y = np.full_like(x, i)
        z = fitness_track
        color = 'red' if i == best_index else 'saddlebrown'
        alpha = 1.0 if i == best_index else 0.4
        ax.plot(x, y, z, color=color, alpha=alpha)

    ax.set_title("Fitness 3D – trajektorie osobników w czasie")
    ax.set_xlabel("Pokolenie")
    ax.set_ylabel("Indeks osobnika")
    ax.set_zlabel("Fitness")
    plt.tight_layout()
    plt.show()

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

def plot_game_sequence(game):
    #  """
    # Wyświetla sekwencję ruchów z `game.movestory` jako 3x3 siatkę plansz.
    # Wymaga, by `game` miał atrybuty:
    # - .movestory: lista (name, (x, y))
    # - .board: końcowy stan planszy (numpy.array)
    # """
    states = []
    board = np.zeros_like(game.board)
    for who, move in game.movestory:
        x, y = move
        board_copy = board.copy()
        board_copy[x * 3 + y] = -1 if who == "Evo" else 1
        states.append(board_copy.reshape(3, 3))
        board[x * 3 + y] = -1 if who == "Evo" else 1

    num_states = len(states)
    cols = 3
    rows = int(np.ceil(num_states / cols))

    fig = plt.figure(figsize=(4 * cols, 4 * rows))
    spec = gridspec.GridSpec(rows, cols, figure=fig)

    for idx, state in enumerate(states):
        ax = fig.add_subplot(spec[idx])
        table_data = [["X" if val == -1 else "O" if val == 1 else "" for val in row] for row in state]
        table = ax.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.2]*3)
        table.scale(1, 2)
        ax.axis('off')
        ax.set_title(f"Ruch {idx+1}", pad=10)

    fig.suptitle("Sekwencja ruchów – gra ewolucyjna", fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_genome_similarity(population):
    """
    Tworzy heatmapę podobieństwa genotypów (macierz Hamming distance).
    """
    n = len(population)
    similarity_matrix = np.zeros((n, n))

    # Hamming distance: ile pozycji jest różnych
    for i in range(n):
        for j in range(n):
            similarity_matrix[i, j] = np.sum(np.array(population[i]) != np.array(population[j]))

    df = pd.DataFrame(similarity_matrix)
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=False, cmap='coolwarm', square=True, cbar_kws={'label': 'Dystans Hammingowy'})
    plt.title("Macierz podobieństwa genotypów")
    plt.xlabel("Osobnik")
    plt.ylabel("Osobnik")
    plt.tight_layout()
    plt.show()

def plot_tactic_effectiveness(signature_block):
    """
    Rysuje skuteczność poszczególnych reakcji z danego podpisu stanu gry.
    Wykres słupkowy pokazuje procent zwycięstw dla każdego ruchu (x, y).
    
    Parameters:
        signature_block: dict {(x, y): {"win": N, "loss": M}}
    """
    moves = []
    win_rates = []
    counts = []

    for move, stats in signature_block.items():
        total = stats["win"] + stats["loss"]
        if total == 0:
            continue
        rate = stats["win"] / total
        moves.append(str(move))
        win_rates.append(rate)
        counts.append(total)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(moves, win_rates, color='teal', edgecolor='black')
    plt.title("Skuteczność reakcji w danym stanie gry")
    plt.xlabel("Ruch (x, y)")
    plt.ylabel("Procent zwycięstw")
    plt.ylim(0, 1)

    # dodaj liczby wystąpień
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.02, f"{count}", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def plot_tactic_histogram(state_signatures):
    """
    Tworzy histogram najczęściej występujących wektorów stanu gry (signature).
    Wejściem jest lista hashowalnych reprezentacji wyników helpers.gamestate(game).
    """
    signature_counts = Counter(state_signatures)
    common_signatures = signature_counts.most_common(10)  # Top 10

    labels = [str(sig) for sig, _ in common_signatures]
    values = [count for _, count in common_signatures]

    plt.figure(figsize=(12, 6))
    plt.barh(range(len(labels)), values, color='teal')
    plt.yticks(range(len(labels)), labels)
    plt.xlabel("Liczba wystąpień")
    plt.title("Najczęstsze wzorce stanów taktycznych (gamestate)")
    plt.tight_layout()
    plt.show()