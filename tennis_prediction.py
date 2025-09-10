import pandas as pd
import os
import math

# === Load Elo data (Excel or CSV) ===
file_excel = "elo_ranking.xlsx"
file_csv = "elo_ranking.csv"

if os.path.exists(file_excel):
    try:
        elo_df = pd.read_excel(file_excel, engine="openpyxl")
    except ImportError:
        raise ImportError(
            "You need to install openpyxl for Excel support.\n"
            "Run: pip install openpyxl"
        )
elif os.path.exists(file_csv):
    elo_df = pd.read_csv(file_csv)
else:
    raise FileNotFoundError("No file 'elo_ranking.xlsx' or 'elo_ranking.csv' found.")

# Normalize player names
elo_df["Player"] = elo_df["Player"].str.strip().str.lower()

# === Elo rating fetch ===
def get_player_elo(player_name, surface="overall"):
    player_name = player_name.lower().strip()
    row = elo_df.loc[elo_df["Player"] == player_name]

    if row.empty:
        raise ValueError(f"Player '{player_name}' not found in dataset.")

    if surface == "overall":
        return float(row["Elo"].iloc[0])
    elif surface == "hard":
        return float(row["hElo"].iloc[0])
    elif surface == "clay":
        return float(row["cElo"].iloc[0])
    elif surface == "grass":
        return float(row["gElo"].iloc[0])
    else:
        raise ValueError("Surface must be one of: overall, hard, clay, grass")

# === Elo probability formula ===
def elo_win_probability(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

# === Best-of-5 adjustment ===
def adjust_best_of_five(prob_best_of_three):
    p = prob_best_of_three
    # Probability of winning best-of-5 = at least 3 sets out of 5
    return (p**3 * (10*p**2 - 15*p + 6))  # simplified closed form

# === Prediction ===
def predict_match(player1, player2, surface="overall", best_of=3):
    elo1 = get_player_elo(player1, surface)
    elo2 = get_player_elo(player2, surface)

    prob1 = elo_win_probability(elo1, elo2)
    prob2 = 1 - prob1

    if best_of == 5:
        prob1 = adjust_best_of_five(prob1)
        prob2 = 1 - prob1

    print(f"\nSurface: {surface.capitalize()} | Format: Best-of-{best_of}")
    print(f"{player1.title()} (Elo: {elo1:.1f}) vs {player2.title()} (Elo: {elo2:.1f})")
    print(f"Win probability: {player1.title()} {prob1*100:.1f}% | {player2.title()} {prob2*100:.1f}%")

    return prob1, prob2

# === Run ===
if __name__ == "__main__":
    p1 = input("Enter first player: ")
    p2 = input("Enter second player: ")
    surface = input("Enter surface (overall, hard, clay, grass): ")
    best_of = int(input("Best of (3 or 5): "))

    predict_match(p1, p2, surface, best_of)
