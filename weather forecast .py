import tkinter as tk
import requests

# ---------------- API SECTION ----------------
def get_weather(city):
    api_key = "4e016303d3763e25ef617227953242b9"  # your API key
    base_url = "https://api.openweathermap.org/data/2.5/weather?"

    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]

        return {
            "temp": main['temp'],
            "humidity": main['humidity'],
            "condition": weather['main'],
            "description": weather['description'],
            "wind": wind['speed']
        }
    else:
        return None

# ---------------- UI ----------------
root = tk.Tk()
root.title("Weather App")
root.geometry("600x400")

# Create a gradient background using Canvas
canvas = tk.Canvas(root, width=600, height=400, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw_gradient(canvas, color1, color2):
    """Draw vertical gradient"""
    steps = 100
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    r_ratio = (r2 - r1) / steps
    g_ratio = (g2 - g1) / steps
    b_ratio = (b2 - b1) / steps

    for i in range(steps):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_rectangle(0, (400/steps)*i, 600, (400/steps)*(i+1), outline="", fill=color)

draw_gradient(canvas, "#3c9ee7", "#000428")  # blue gradient

# Fake transparent effect with a stippled rectangle
canvas.create_rectangle(
    100, 100, 500, 300,
    fill="white", stipple="gray50", outline=""
)

# Frame for inputs & results (normal white background)
frame = tk.Frame(canvas, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Entry
city_entry = tk.Entry(frame, font=("Arial", 14), width=20, justify="center")
city_entry.grid(row=0, column=0, padx=5, pady=10)

# Button
btn = tk.Button(frame, text="Get Weather", font=("Arial", 12, "bold"),
                bg="#3c9ee7", fg="white", command=lambda: show_weather())
btn.grid(row=0, column=1, padx=10)

# Result label
result_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), bg="white")
result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def show_weather():
    city = city_entry.get()
    data = get_weather(city)
    if data:
        result_label.config(
            text=f"{city}\n"
                 f"🌡 {data['temp']}°C\n"
                 f"💧 {data['humidity']}%\n"
                 f"☁ {data['description'].title()}\n"
                 f"💨 {data['wind']} m/s"
        )
    else:
        result_label.config(text="❌ City not found!")

root.mainloop()
