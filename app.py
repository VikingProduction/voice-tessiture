import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import librosa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# Paramètres globaux
sample_rate = 22050            # Fréquence d'échantillonnage (Hz)
audio_buffer = []              # Buffer pour stocker les données audio
buffer_lock = threading.Lock() # Pour un accès thread-safe au buffer
stream = None                  # Référence au flux audio

def audio_callback(indata, frames, time, status):
    """
    Callback appelé pour chaque bloc de données capturées.
    On extrait le canal mono et on ajoute les données dans le buffer.
    """
    global audio_buffer
    if status:
        print("Status d'enregistrement :", status)
    data = indata[:, 0]  # Extraction du canal mono
    with buffer_lock:
        audio_buffer.extend(data.tolist())

def classify_voice(min_freq, max_freq):
    """
    Classification de la tessiture en 6 catégories.
    
    Pour une voix féminine (max_freq > 800 Hz) :
      - Soprano : min_freq ≥ 250 Hz
      - Mezzo-soprano : 200 Hz ≤ min_freq < 250 Hz
      - Contralto : min_freq < 200 Hz
      
    Pour une voix masculine (max_freq ≤ 800 Hz) :
      - Ténor : min_freq ≥ 130 Hz
      - Baritone : 100 Hz ≤ min_freq < 130 Hz
      - Basse : min_freq < 100 Hz
    """
    if max_freq > 800:
        if min_freq >= 250:
            return "Soprano"
        elif min_freq >= 200:
            return "Mezzo-soprano"
        else:
            return "Contralto"
    else:
        if min_freq >= 130:
            return "Ténor"
        elif min_freq >= 100:
            return "Baritone"
        else:
            return "Basse"

def start_recording():
    """
    Démarre l'enregistrement en streaming.
    Le buffer est réinitialisé et le guide utilisateur s'actualise.
    """
    global stream, audio_buffer
    with buffer_lock:
        audio_buffer = []  # Réinitialisation du buffer
    try:
        stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate)
        stream.start()
        guide_label.config(text=(
            "Enregistrement en cours...\n\n"
            "Consignes pour une analyse optimale :\n"
            "1. Installez-vous dans un environnement calme avec un microphone de qualité.\n"
            "2. Commencez par chanter votre note la plus basse.\n"
            "3. Progressez lentement jusqu'à votre note la plus haute en tenant chaque note quelques secondes.\n"
            "4. Variez l'intensité (du pianissimo au fortissimo) si possible.\n"
            "5. Cliquez sur 'Terminer l'enregistrement' une fois terminé."
        ))
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de démarrer l'enregistrement : {e}")

def stop_recording():
    """
    Arrête l'enregistrement et lance l'analyse de l'audio capturé.
    """
    global stream
    if stream:
        stream.stop()
        stream.close()
        stream = None
    guide_label.config(text="Enregistrement terminé.\nAnalyse en cours, veuillez patienter...")
    with buffer_lock:
        data = np.array(audio_buffer)
    if data.size < sample_rate:
        messagebox.showwarning("Avertissement", "Enregistrement trop court pour une analyse fiable.")
        guide_label.config(text="Enregistrement trop court. Veuillez réessayer.")
        return
    analyze_audio(data)

def analyze_audio(data):
    """
    Analyse l'audio enregistré :
      - Extraction de la fréquence fondamentale avec librosa.pyin.
      - Calcul de la tessiture (note la plus basse et la plus haute).
      - Classification selon 6 catégories.
      - Affichage du Voice Range Profile (VRP) et des résultats.
    """
    global sample_rate
    try:
        f0, voiced_flag, voiced_prob = librosa.pyin(
            data,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sample_rate
        )
        times = librosa.times_like(f0, sr=sample_rate)
        
        # Mise à jour du graphique du profil vocal
        ax.clear()
        ax.plot(times, f0, label="Fréquence fondamentale (f0)", color="red")
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Fréquence (Hz)")
        ax.set_title("Voice Range Profile (VRP)")
        ax.legend()
        canvas.draw()
        
        # Filtrer les valeurs non définies
        f0_valid = f0[~np.isnan(f0)]
        if f0_valid.size > 0:
            min_freq = np.min(f0_valid)
            max_freq = np.max(f0_valid)
            voice_type = classify_voice(min_freq, max_freq)
            info_text = (f"Tessiture détectée : {min_freq:.2f} Hz - {max_freq:.2f} Hz\n"
                         f"Type de voix estimé : {voice_type}")
            result_label.config(text=info_text)
            guide_label.config(text="Analyse terminée. Vous pouvez relancer une nouvelle session d'enregistrement.")
        else:
            result_label.config(text="Aucune fréquence détectée.")
            guide_label.config(text="Analyse terminée, mais aucune fréquence n'a pu être détectée.\nVeuillez réessayer.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'analyse : {e}")
        guide_label.config(text="Erreur lors de l'analyse. Veuillez réessayer.")

# Configuration de l'interface graphique avec Tkinter
root = tk.Tk()
root.title("Profil Vocal Professionnel - Identification de la Tessiture")

# Cadre supérieur avec le guide d'utilisation
frame_top = tk.Frame(root)
frame_top.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

guide_label = tk.Label(frame_top, text=(
    "Guide d'utilisation :\n"
    "1. Installez-vous dans un environnement silencieux avec un microphone de qualité.\n"
    "2. Cliquez sur 'Démarrer l'enregistrement'.\n"
    "3. Chantez de votre note la plus basse à la plus haute, en tenant chaque note quelques secondes et en variant l'intensité.\n"
    "4. Cliquez sur 'Terminer l'enregistrement' une fois terminé."
), justify="left")
guide_label.pack(side=tk.TOP, anchor="w", pady=5)

# Cadre pour les boutons de commande
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

btn_start = tk.Button(frame_buttons, text="Démarrer l'enregistrement", command=start_recording)
btn_start.pack(side=tk.LEFT, padx=5)

btn_stop = tk.Button(frame_buttons, text="Terminer l'enregistrement", command=stop_recording)
btn_stop.pack(side=tk.LEFT, padx=5)

# Label pour afficher les résultats de l'analyse
result_label = tk.Label(root, text="Résultats : N/A", font=("Arial", 12), fg="blue")
result_label.pack(side=tk.TOP, pady=5)

# Cadre pour l'affichage du graphique (Voice Range Profile)
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Lancement de l'interface graphique
root.mainloop()
