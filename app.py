from flask import Flask, render_template_string
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Backup Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --primary: #2563eb;
            --success-bg: #dcfce7;
            --success-text: #16a34a;
            --error-bg: #fee2e2;
            --error-text: #dc2626;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            padding: 2.5rem 1rem;
            line-height: 1.5;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        header {
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1.5rem;
        }

        h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.025em;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.25rem;
        }

        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }

        .grid-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .info-item {
            padding: 1.25rem;
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }

        .info-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .info-value {
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 0.5rem;
            color: var(--text-main);
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            font-size: 0.85rem;
            font-weight: 600;
            border-radius: 9999px;
            margin-top: 0.5rem;
        }

        .status-badge.success {
            background-color: var(--success-bg);
            color: var(--success-text);
        }

        .status-badge.error {
            background-color: var(--error-bg);
            color: var(--error-text);
        }

        h2 {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Table Styling */
        .table-container {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        th, td {
            padding: 0.875rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: #f8fafc;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        td {
            color: var(--text-main);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: #f8fafc;
        }

        /* Monospace Logs Styling */
        pre {
            background-color: #f8fafc;
            color: #334155;
            border: 1px solid var(--border);
            padding: 1.25rem;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            max-height: 350px;
            overflow-y: auto;
            line-height: 1.6;
        }

        /* Custom Scrollbar for Logs */
        pre::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        pre::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        pre::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        pre::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Cloud Backup Monitor</h1>
            <p class="subtitle">Dashboard pemantauan otomatis backup data terenkripsi ke Backblaze B2</p>
        </header>

        <!-- Informasi Backup (Status & Waktu) -->
        <div class="grid-info">
            <div class="info-item">
                <div class="info-label">Status Backup Terakhir</div>
                <div>
                    {% if "berhasil" in status.lower() %}
                    <span class="status-badge success">● {{ status }}</span>
                    {% else %}
                    <span class="status-badge error">● {{ status }}</span>
                    {% endif %}
                </div>
            </div>
            <div class="info-item">
                <div class="info-label">Waktu Backup Terakhir</div>
                <div class="info-value">{{ last_backup_time }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Jumlah File Backup</div>
                <div class="info-value">{{ backups|length }} file</div>
            </div>
        </div>

        <!-- Daftar File Backup -->
        <div class="card">
            <h2>📦 File Backup Lokal</h2>
            <div class="table-container">
                {% if backups %}
                <table>
                    <thead>
                        <tr>
                            <th>Nama File</th>
                            <th>Ukuran</th>
                            <th>Waktu Pembuatan</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for f in backups %}
                        <tr>
                            <td><strong>{{ f.name }}</strong></td>
                            <td>{{ f.size }}</td>
                            <td>{{ f.time }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p style="text-align: center; color: var(--text-muted); padding: 2rem 0;">Belum ada file backup.</p>
                {% endif %}
            </div>
        </div>

        <!-- Log Aktivitas -->
        <div class="card">
            <h2>📝 Log Aktivitas (backup.log)</h2>
            <pre id="logConsole">{{ log }}</pre>
        </div>
    </div>

    <script>
        // Auto scroll log to bottom
        window.addEventListener('DOMContentLoaded', () => {
            const logConsole = document.getElementById('logConsole');
            if (logConsole) {
                logConsole.scrollTop = logConsole.scrollHeight;
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    backup_files = sorted(Path(".").glob("backup_*.zip"), reverse=True)
    
    # Process backup files to return detailed info (name, size, human-readable time)
    backups = []
    for p in backup_files:
        size_bytes = p.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.2f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            
        try:
            # Try to extract time from filename e.g. backup_20260710_112056.zip
            parts = p.stem.split("_")
            if len(parts) >= 3:
                dt_str = f"{parts[1]}_{parts[2]}"
                dt = datetime.strptime(dt_str, "%Y%m%d_%H%M%S")
                time_str = dt.strftime("%d-%m-%Y %H:%M:%S")
            else:
                time_str = datetime.fromtimestamp(p.stat().st_mtime).strftime("%d-%m-%Y %H:%M:%S")
        except Exception:
            time_str = datetime.fromtimestamp(p.stat().st_mtime).strftime("%d-%m-%Y %H:%M:%S")
            
        backups.append({
            "name": p.name,
            "size": size_str,
            "time": time_str
        })

    log_path = Path("backup.log")
    log = log_path.read_text(encoding="utf-8") if log_path.exists() else "Belum ada log."

    # Robust parsing of status and last backup time from files and backup.log
    last_backup_time = "Belum ada backup"
    status = "Belum ada backup"
    
    if backup_files:
        latest_file = backup_files[0]
        # Get last backup time
        if backups:
            last_backup_time = backups[0]["time"]
            
        # Parse status from backup.log
        status = "Backup terakhir berhasil"  # default fallback if files exist
        if log_path.exists():
            log_content = log_path.read_text(encoding="utf-8")
            latest_zip_name = latest_file.name
            
            # Find references to this zip file in the log
            if latest_zip_name in log_content:
                lines = log_content.splitlines()
                zip_lines = [l for l in lines if latest_zip_name in l]
                if zip_lines:
                    last_zip_line = zip_lines[-1]
                    # Check if upload/creation was successful
                    if "Upload berhasil" in last_zip_line or "File berhasil diunggah" in last_zip_line or "berhasil" in last_zip_line.lower():
                        status = "Backup terakhir berhasil"
                    elif "error" in last_zip_line.lower() or "failed" in last_zip_line.lower():
                        status = "Backup terakhir gagal"
                    else:
                        status = "Backup dibuat, status upload belum terkonfirmasi"
                else:
                    status = "Backup dibuat, belum diunggah"
            else:
                # If zip is not in log, it might have been created but not logged yet
                status = "Backup file terdeteksi, tetapi tidak tercatat di log"
    else:
        # Fallback if no files but logs exist
        if log_path.exists():
            log_content = log_path.read_text(encoding="utf-8")
            if "Upload berhasil" in log_content or "File berhasil diunggah" in log_content:
                status = "Backup terakhir berhasil"
                # Try to extract date/time from the last log line
                lines = log_content.splitlines()
                if lines:
                    last_line = lines[-1]
                    parts = last_line.split(" - ")
                    if parts:
                        last_backup_time = parts[0]

    return render_template_string(
        TEMPLATE,
        backups=backups,
        log=log,
        last_backup_time=last_backup_time,
        status=status,
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)