import http.server
import socketserver
import urllib.parse

# --- Simulate Data (instead of database interaction) ---
# In a real app, you'd fetch this from your Ticket model
tickets_data = [
    {"id": 1, "subject": "Printer Issue", "description": "Printer in office 3 not working.", "priority": "High", "status": "Open"},
    {"id": 2, "subject": "Software Install", "description": "Need Photoshop installed on my PC.", "priority": "Medium", "status": "In Progress"},
    {"id": 3, "subject": "Network Slow", "description": "Internet connection is very slow today.", "priority": "High", "status": "Resolved"},
]

# --- Our "View" functions (now generating HTML) ---

def get_all_tickets_html():
    """Simulates a view to return all tickets as an HTML page."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>All Tickets</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .status-Open { color: blue; }
            .status-InProgress { color: orange; }
            .status-Resolved { color: green; }
            .status-High { font-weight: bold; color: red; }
            a { text-decoration: none; color: #007bff; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>All Tickets</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Subject</th>
                    <th>Description</th>
                    <th>Priority</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for ticket in tickets_data:
        html_content += f"""
                <tr>
                    <td>{ticket['id']}</td>
                    <td><a href="/tickets/{ticket['id']}">{ticket['subject']}</a></td>
                    <td>{ticket['description']}</td>
                    <td class="status-{ticket['priority'].replace(' ', '')}">{ticket['priority']}</td>
                    <td class="status-{ticket['status'].replace(' ', '')}">{ticket['status']}</td>
                </tr>
        """
    html_content += """
            </tbody>
        </table>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    """
    return html_content.encode('utf-8'), 'text/html', 200

def get_ticket_detail_html(ticket_id):
    """Simulates a view to return a single ticket's detail as an HTML page."""
    try:
        ticket_id = int(ticket_id)
        ticket = next((t for t in tickets_data if t["id"] == ticket_id), None)
        if ticket:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ticket #{ticket['id']}</title>
                <style>
                    body {{ font-family: sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    p {{ margin-bottom: 10px; }}
                    .label {{ font-weight: bold; margin-right: 5px; }}
                    .status-Open {{ color: blue; }}
                    .status-InProgress {{ color: orange; }}
                    .status-Resolved {{ color: green; }}
                    .status-High {{ font-weight: bold; color: red; }}
                    a {{ text-decoration: none; color: #007bff; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <h1>Ticket Details: #{ticket['id']} - {ticket['subject']}</h1>
                <p><span class="label">Description:</span> {ticket['description']}</p>
                <p><span class="label">Priority:</span> <span class="status-{ticket['priority'].replace(' ', '')}">{ticket['priority']}</span></p>
                <p><span class="label">Status:</span> <span class="status-{ticket['status'].replace(' ', '')}">{ticket['status']}</span></p>
                <p><a href="/tickets">Back to all tickets</a></p>
                <p><a href="/">Go to Home</a></p>
            </body>
            </html>
            """
            return html_content.encode('utf-8'), 'text/html', 200
        else:
            return handle_not_found_html() # Return 404 as HTML
    except ValueError:
        # Invalid ID format
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bad Request</title>
            <style>body { font-family: sans-serif; margin: 20px; } h1 { color: red; }</style>
        </head>
        <body>
            <h1>400 Bad Request</h1>
            <p>The ticket ID provided is invalid. Please provide a valid number.</p>
            <p><a href="/">Go to Home</a></p>
        </body>
        </html>
        """
        return html_content.encode('utf-8'), 'text/html', 400

def home_page_html():
    """Serves a simple HTML home page."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Ticketing System Home</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 10px; }}
            a {{ text-decoration: none; color: #007bff; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Welcome to the Simple Ticketing System!</h1>
        <p>This is a very basic web server serving HTML pages.</p>
        <h2>Navigation:</h2>
        <ul>
            <li><a href="/tickets">View All Tickets</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content.encode('utf-8'), 'text/html', 200

def handle_not_found_html():
    """Simulates a 404 Not Found view returning HTML."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Not Found</title>
        <style>body { font-family: sans-serif; margin: 20px; } h1 { color: red; }</style>
    </head>
    <body>
        <h1>404 Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    """
    return html_content.encode('utf-8'), 'text/html', 404

# --- Basic "Routing" (manual URL dispatch) ---
def route_request(path, query_params):
    if path == '/':
        return home_page_html()
    elif path == '/tickets':
        return get_all_tickets_html()
    elif path.startswith('/tickets/'):
        parts = path.split('/')
        if len(parts) == 3 and parts[2].isdigit(): # /tickets/ID
            ticket_id = parts[2]
            return get_ticket_detail_html(ticket_id)
    return handle_not_found_html() # Default for unhandled paths

# --- Custom HTTP Request Handler ---
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Call the routing function
        content, content_type, status_code = route_request(path, query_params)

        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)

# --- Server Setup ---
PORT = 8000

if __name__ == "__main__":
    Handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTML pages at http://localhost:{PORT}")
        print("-" * 40)
        print("Available URLs:")
        print(f"  - Home page: http://localhost:{PORT}/")
        print(f"  - All tickets: http://localhost:{PORT}/tickets")
        print(f"  - Individual ticket (e.g., ID 1): http://localhost:{PORT}/tickets/1")
        print(f"  - Individual ticket (e.g., ID 2): http://localhost:{PORT}/tickets/2")
        print(f"  - Non-existent ticket: http://localhost:{PORT}/tickets/99")
        print("-" * 40)
        httpd.serve_forever()