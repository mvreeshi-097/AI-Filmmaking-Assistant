from flask import Flask, render_template, request, jsonify, send_file
import io
import sqlite3

app = Flask(__name__)

# ------------------------------
# DATABASE INITIALIZATION
# ------------------------------
def init_db():
    conn = sqlite3.connect("movieai.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_type TEXT,
            theme TEXT,
            setting TEXT,
            tone TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# ------------------------------
# HOME ROUTE
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------
# GENERATE MODULE ROUTE
# ------------------------------
@app.route("/generate-module", methods=["POST"])
def generate_module():
    data = request.get_json()
    module_type = data.get("type")
    inputs = data.get("inputs")

    if not module_type or not inputs:
        return jsonify({"error": "Missing data"}), 400

    theme = inputs.get("main_theme", "Unknown Theme")
    setting = inputs.get("setting", "Unknown Setting")
    tone = inputs.get("tone", "Neutral Tone")

    responses = {

        "character": f"""
🎭 CHARACTER BIBLE

Core Concept:
A {tone} story about {theme} set in {setting}.

Protagonist:
- Background shaped by {setting}
- Driven by emotional conflict
- Moral flaw connected to {theme}

Antagonist:
- Represents the darker side of {theme}
- Intelligent, strategic, emotionally layered

Character Arc:
Transformation through struggle and revelation.
""",

        "screenplay": f"""
🎬 SCREENPLAY STRUCTURE

ACT I – Setup
World of {setting} is introduced.
Theme of {theme} established.

ACT II – Conflict
Tension rises with {tone} emotional beats.
Characters face irreversible decisions.

ACT III – Resolution
Climactic confrontation.
Theme of {theme} reaches emotional closure.
""",

        "shots": f"""
📸 SHOT BREAKDOWN

Opening Wide Shot – Establish {setting}
Close-up – Emotional tension reflecting {tone}
Tracking Shot – Character pursuit
Final Frame – Symbolic representation of {theme}
""",

        "budget": f"""
💰 PRODUCTION BUDGET ESTIMATE

Theme Complexity: {theme}
Location Demand: {setting}
Visual Tone Style: {tone}

Low Budget: $2M (Indie Scale)
Mid Budget: $8M (Studio Backed)
High Budget: $20M+ (Cinematic Production)
""",

        "schedule": f"""
📅 PRODUCTION SCHEDULE

Pre-production – 3 Weeks
Location Setup – {setting}
Principal Shooting – 6 Weeks
Post-production (Tone Enhancement: {tone}) – 5 Weeks
""",

        "moodboard": f"""
🎨 MOODBOARD DIRECTION

Primary Theme: {theme}
Visual Setting Influence: {setting}
Color Style: Inspired by {tone}

Lighting: Cinematic contrast
Texture: Film grain vintage finish
""",

        "casting": f"""
🎥 CASTING SUGGESTIONS

Protagonist – Actor capable of portraying {tone} depth
Antagonist – Intense performer reflecting {theme}
Supporting Roles – Diverse casting fitting {setting}
""",

        "dialogue": f"""
🗣 DIALOGUE STYLE

Tone: {tone}
Theme Expression: {theme}
Setting Influence: {setting}

Dialogue Format:
Short, emotionally charged, subtext-driven lines.
"""
    }

    result_text = responses.get(module_type, "Module not found")

    # ------------------------------
    # SAVE TO DATABASE
    # ------------------------------
    conn = sqlite3.connect("movieai.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (module_type, theme, setting, tone, result)
        VALUES (?, ?, ?, ?, ?)
    """, (module_type, theme, setting, tone, result_text))
    conn.commit()
    conn.close()

    return jsonify({"result": result_text})


# ------------------------------
# VIEW HISTORY ROUTE
# ------------------------------
@app.route("/history")
def get_history():
    conn = sqlite3.connect("movieai.db")
    cursor = conn.cursor()
    cursor.execute("SELECT result FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    history_list = [{"result": row[0]} for row in rows]

    return jsonify({"history": history_list})


# ------------------------------
# EXPORT SCREENPLAY ROUTE
# ------------------------------
@app.route("/export-screenplay", methods=["POST"])
def export_screenplay():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "No content provided"}), 400

    screenplay_format = f"""
TITLE: UNTITLED FILM

FADE IN:

{content}

FADE OUT.
"""

    buffer = io.BytesIO()
    buffer.write(screenplay_format.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="screenplay.txt",
        mimetype="text/plain"
    )


# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)