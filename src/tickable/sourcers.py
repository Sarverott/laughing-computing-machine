# Ponowny import po resecie środowiska
import json
import time
import numpy as np

label = "chaos_duel"


def NOW_PTR():
    return round(time.time() * 1000)

class FileSnapper:
    def __init__(self, filepath=f"../evo_snapshot_{label}_{NOW_PTR()}.json"):
        self.filepath = filepath

    def export_generation(self, best_individual, fitness_story, preference_census):
        """
        Eksportuje wyniki ewolucji do formatu .omnis-like (w stylu TOML/JSON snapshotu).
        Zakłada, że `fitness_story` to lista fitnessów, a `preference_census` to lista macierzy 3x3.
        """
        avg_fitness = [float(np.mean(gen)) for gen in fitness_story]
        max_fitness = [float(np.max(gen)) for gen in fitness_story]

        final_census = preference_census[-1].tolist()
        cumulative_heat = np.sum(preference_census, axis=0).tolist()

        export_data = {
            "omnis.darkpoint": {
                "title": f"Evolutionary Duel Report – {label}",
                "timestamp": NOW_PTR(),
                "type": "evolution_snapshot",
                "meta": {
                    "winner_genome": best_individual,
                    "final_fitness": float(max_fitness[-1]),
                    "generations": len(fitness_story)
                },
                "fitness_progress": {
                    "average": avg_fitness,
                    "maximum": max_fitness
                },
                "first_move_heatmap_final": final_census,
                "first_move_heatmap_total": cumulative_heat
            }
        }
        with open(self.filepath, "w") as f:
            json.dump(export_data, f, indent=2)

        return self.filepath