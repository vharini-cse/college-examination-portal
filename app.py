from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "pec-exam-portal-demo-secret"

EXAMS = [
    {
        "id": 1, "code": "CC-401", "name": "Cloud Computing",
        "duration": 30, "description": "Cloud models, virtualization, services and deployment concepts.",
        "questions_data": [
            {"q": "Which cloud model provides virtualized computing resources?", "options": ["SaaS", "IaaS", "DBaaS", "FaaS"], "answer": 1},
            {"q": "Which is a public cloud provider?", "options": ["AWS", "Notepad", "BIOS", "Git"], "answer": 0},
            {"q": "What does SaaS stand for?", "options": ["Storage as a Service", "Software as a Service", "Security as a System", "Server as a System"], "answer": 1},
            {"q": "What technology creates multiple virtual machines on one physical machine?", "options": ["Virtualization", "Compilation", "Encryption", "Indexing"], "answer": 0},
            {"q": "Which deployment model is dedicated to one organization?", "options": ["Public cloud", "Private cloud", "Community browser", "Hybrid browser"], "answer": 1},
            {"q": "Which property lets resources scale with demand?", "options": ["Elasticity", "Fragmentation", "Compilation", "Defragmentation"], "answer": 0},
            {"q": "Which model provides a platform for application development?", "options": ["IaaS", "PaaS", "SaaS", "DaaS"], "answer": 1},
            {"q": "A combination of private and public cloud is called:", "options": ["Hybrid cloud", "Local cloud", "Single cloud", "Offline cloud"], "answer": 0},
            {"q": "Which is a major benefit of cloud computing?", "options": ["On-demand resources", "No network required", "Only local access", "Fixed capacity only"], "answer": 0},
            {"q": "Which service is commonly used for cloud object storage?", "options": ["Amazon S3", "CPU", "RAM", "HTML"], "answer": 0},
        ]
    },
    {
        "id": 2, "code": "OS-402", "name": "Operating Systems",
        "duration": 45, "description": "Processes, memory management, scheduling and file systems.",
        "questions_data": [
            {"q": "Which component manages processes in an operating system?", "options": ["Kernel", "Compiler", "Browser", "Router"], "answer": 0},
            {"q": "Which scheduling algorithm uses a time quantum?", "options": ["FCFS", "Round Robin", "SJF", "Priority only"], "answer": 1},
            {"q": "Virtual memory commonly uses:", "options": ["Disk space", "Keyboard", "Printer", "Monitor"], "answer": 0},
            {"q": "A process waiting for an event is in which state?", "options": ["Ready", "Waiting", "Running", "New"], "answer": 1},
            {"q": "Which is a file system example?", "options": ["NTFS", "HTTP", "HTML", "SMTP"], "answer": 0},
            {"q": "Deadlock involves processes waiting for:", "options": ["Resources", "Passwords", "Files only", "Screens"], "answer": 0},
            {"q": "Which memory is closest to the CPU?", "options": ["Cache", "Hard disk", "USB", "DVD"], "answer": 0},
            {"q": "What is multitasking?", "options": ["Running multiple tasks seemingly simultaneously", "Deleting tasks", "Formatting disks", "Installing drivers"], "answer": 0},
            {"q": "Which is an operating system?", "options": ["Linux", "Python", "Chrome", "MySQL"], "answer": 0},
            {"q": "A program in execution is called a:", "options": ["Process", "File", "Folder", "Thread pool"], "answer": 0},
        ]
    },
    {
        "id": 3, "code": "DB-403", "name": "Database Management Systems",
        "duration": 30, "description": "Relational databases, SQL, keys and normalization.",
        "questions_data": [
            {"q": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Question Language", "System Query Link", "Structured Queue Logic"], "answer": 0},
            {"q": "Which command retrieves data?", "options": ["SELECT", "DELETE", "DROP", "ALTER"], "answer": 0},
            {"q": "A primary key must be:", "options": ["Unique", "Always text", "Nullable", "Duplicated"], "answer": 0},
            {"q": "Which is a relational database?", "options": ["MySQL", "HTML", "CSS", "Flask"], "answer": 0},
            {"q": "Normalization helps reduce:", "options": ["Redundancy", "Security", "Availability", "Queries"], "answer": 0},
            {"q": "Which command adds a new row?", "options": ["INSERT", "UPDATE", "CREATE", "SELECT"], "answer": 0},
            {"q": "Which clause filters rows?", "options": ["WHERE", "FROM", "ORDER", "GROUP"], "answer": 0},
            {"q": "A foreign key references a:", "options": ["Primary key", "CSS class", "URL", "Python function"], "answer": 0},
            {"q": "Which command modifies existing rows?", "options": ["UPDATE", "INSERT", "CREATE", "GRANT"], "answer": 0},
            {"q": "Which SQL clause sorts results?", "options": ["ORDER BY", "SORT WITH", "ARRANGE", "GROUP WITH"], "answer": 0},
        ]
    }
]

@app.context_processor
def common():
    return {"logged_in": "user" in session, "current_user": session.get("user"), "role": session.get("role")}

@app.route("/")
def home():
    return render_template("index.html", exams=EXAMS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "student")
        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")
        session["user"] = username
        session["role"] = role
        return redirect(url_for("admin" if role == "admin" else "dashboard"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", exams=EXAMS)

@app.route("/exam/<int:exam_id>")
def exam(exam_id):
    if "user" not in session:
        return redirect(url_for("login"))
    exam_data = next((e for e in EXAMS if e["id"] == exam_id), None)
    if not exam_data:
        return "Exam not found", 404
    return render_template("exam.html", exam=exam_data)

@app.route("/submit/<int:exam_id>", methods=["POST"])
def submit(exam_id):
    if "user" not in session:
        return redirect(url_for("login"))
    exam_data = next((e for e in EXAMS if e["id"] == exam_id), None)
    if not exam_data:
        return "Exam not found", 404

    score = 0
    attempted = 0
    for index, question in enumerate(exam_data["questions_data"]):
        answer = request.form.get(f"q{index}")
        if answer is not None:
            attempted += 1
            if int(answer) == question["answer"]:
                score += 1

    total = len(exam_data["questions_data"])
    session["last_result"] = {
        "exam": exam_data["name"],
        "score": score,
        "total": total,
        "percentage": round(score / total * 100),
        "attempted": attempted,
        "user": session["user"]
    }
    return redirect(url_for("result"))

@app.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("login"))
    result_data = session.get("last_result")
    if not result_data:
        return redirect(url_for("dashboard"))
    return render_template("result.html", result=result_data)

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    return render_template("admin.html", exams=EXAMS)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
