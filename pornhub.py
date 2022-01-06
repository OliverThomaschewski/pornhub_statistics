import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import stats

__author__  = "Oliver Thomaschewski"
__date__    = "10/21"

# Farben für Diagramme und Schrift (Kann auch im rc_context direkt als String oder Hex eingegeben werden. Siehe Zeile 99)

bar_color = "#F7971D"
text_color = "#FFFFFF"


# VORBEREITUNG DER DATEN

#Dataframes erstellen
dfv = pd.concat(pd.read_json("dfv.json.gz", lines=True, chunksize=100e3))
dfv["added"] = pd.to_datetime(dfv["added"], unit="ms")
dfv = dfv.set_index("videoid", drop=False)

# Dataframes nach Bedingung
isPremium = dfv[dfv.eval('ispremium==True')]
isNotPremium = dfv[dfv.eval('ispremium==False')]


# DURATION PREMIUM VS: NON-PREMIUM
meanPremiumDur = np.mean(isPremium["duration"].tolist())
meanNotPremiumDur = np.mean(isNotPremium["duration"].tolist())
medianPremiumDur = np.median(isPremium["duration"].tolist())
medianNotPremiumDur = np.median(isNotPremium["duration"].tolist())
modePremiumDur = stats.mode(isPremium["duration"].tolist())
modeNotPremiumDur = stats.mode(isNotPremium["duration"].tolist())
stdPremiumDur = np.std(isPremium["duration"].tolist())
stdNotPremiumDur = np.std(isNotPremium["duration"].tolist())

# Printing Values
print("DURATION\n")
print(f"Die durchschnittliche Premium Duration ist: {meanPremiumDur/60} Minuten")
print(f"Die durchschnittliche Non-Premium Duration ist: {meanNotPremiumDur/60} Minuten")
print(f"Der Median von Premium Duration ist: {medianPremiumDur/60} Minuten")
print(f"Der Median von Non-Premium Duration ist: {medianNotPremiumDur/60} Minuten")
print(f"Der Modalwert der Premium Duration ist: {modePremiumDur} Minuten")
print(f"Der Modalwert der Non-Premium Duration ist: {modeNotPremiumDur} Minuten")
print(f"Die Standardabweichung der Premium Duration ist: {stdPremiumDur/60} Minuten")
print(f"Die Standardabweichung der Non-Premium Duration ist: {stdNotPremiumDur/60}\n\n\n")


# VIEWS PREMIUM VS. NON-PREMIUM

meanPremiumView = np.mean(isPremium["views"].tolist())
meanNotPremiumView = np.mean(isNotPremium["views"].tolist())
medianPremiumView = np.median(isPremium["views"].tolist())
medianNotPremiumView = np.median(isNotPremium["views"].tolist())
modePremiumView = stats.mode(isPremium["views"].tolist())
modeNotPremiumView = stats.mode(isNotPremium["views"].tolist())
stdPremiumView = np.std(isPremium["views"].tolist())
stdNotPremiumView = np.std(isNotPremium["views"].tolist())

print("Views\n")
print(f"Die durchschnittliche Premium Views Anzahl ist: {meanPremiumView}")
print(f"Die durchschnittliche Non-Premium Views Anzahl ist: {meanNotPremiumView}")
print(f"Der Median der Premium Views ist: {medianPremiumView}")
print(f"Die Median der Non-Premium Views ist: {medianNotPremiumView}")
print(f"Der Modalwert der Premium Views ist: {modePremiumView}")
print(f"Die Modalwert der Non-Premium Views ist: {modeNotPremiumView}")
print(f"Die Standardabweichung der Premium Views ist: {stdPremiumView}")
print(f"Die Standardabweichung der Non-Premium Views ist: {stdNotPremiumView}\n\n\n")


# Values from Duration and Views in a List of Tuples (Could also be put into two lists right away)

klicks = [(round(tup[0] / 60, 0), tup[1] /100000) for tup in list(dfv[["duration", "views"]].to_records(index=False))]


# Calculation of Correlation Coefficient

# Split Klicks in two lists(would also work with the zip() function)

duration = list()
views = list()

for i in klicks:
    duration.append(i[0])
    views.append(i[1])

print(f"Der KoEff ist: {np.corrcoef(duration, views)}")





# PLOT DIAGRAMS


# DEFAULT COLORS FOR PLOT WITH RC_CONTEXT

with plt.rc_context({"xtick.color": text_color,     # Farbe der x-Achseneinheiten
                     "ytick.color": text_color,     # Farbe der y-Achseneinheiten
                     "axes.edgecolor": "black",     # Farbe der x und y-Achsen
                     "axes.titlecolor": text_color, # Farbe des Titels
                     "axes.labelcolor": text_color, # Farbe der Labels
                     "axes.facecolor": "black",     # Hintergrundfarbe der Plotfläche selbst
                     "figure.facecolor": "black",   # Hintergrundarbe des aeußeren Randes

                     }):

    # Average Duration
    ax = plt.axes()
    plt.title(" Avg. Duration Premium vs. Non-Premium")
    ax.set_ylabel("Duration [Min]")
    plt.bar([0, 1], [meanPremiumDur / 60, meanNotPremiumDur / 60], tick_label=["Premium", "Not Premium"], color= bar_color)
    plt.show()


    # Average Views

    ax = plt.axes()
    plt.title("Avg Views Premium vs. Non-Premium")
    ax.set_ylabel("Views")
    plt.bar([0, 1], [meanPremiumView, meanNotPremiumView / 60], tick_label=["Premium", "Not Premium"], color= bar_color)
    plt.show()


    # Laenge vs. Klicks

    ax = plt.axes()
    plt.title("Views vs. Duration [Premium & Non-Premium]")
    ax.set_xlabel("Duration [Min]", color=text_color)
    ax.set_ylabel("Views [100 000]", color=text_color)
    ax.set_facecolor("black")
    plt.scatter(*zip(*klicks), s=0.5, color=bar_color) #klicks in zwei Listen Duration und Views aufteilen & Punktgrößen verkleinern
    plt.xlim(0,100) # Größe der x Achse festlegen
    plt.ylim(0.01,400) # Größe der y Achse festlegen
    plt.show()


