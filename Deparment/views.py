import http.server
import socketserver
import json
import urllib.parse

# --- Simulate Data (instead of database interaction) ---
# In a real app, you'd fetch this from your Ticket model
tickets_data = [
    {"id": 1, "subject": "Printer Issue", "description": "Printer in office 3 not working.", "priority": "High", "status": "Open"},
    {"id": 2, "subject": "Software Install", "description": "Need Photoshop installed on my PC.", "priority": "Medium", "status": "In Progress"},
    {"id": 3, "subject": "Network Slow", "description": "Internet connection is very slow today.", "priority": "High", "status": "Resolved"},
]
def get_all_tickets():
    """Simulates a view to return all tickets."""
    return json.dumps(tickets_data).encode('utf-8'), 'application/json', 200

def get_ticket_detail(ticket_id):
    """Simulates a view to return a single ticket by ID."""
    try:
        ticket_id = int(ticket_id)
        ticket = next((t for t in tickets_data if t["id"] == ticket_id), None)
        if ticket:
            return json.dumps(ticket).encode('utf-8'), 'application/json', 200
        else:
            return json.dumps({"error": "Ticket not found"}).encode('utf-8'), 'application/json', 404
    except ValueError:
        return json.dumps({"error": "Invalid ticket ID"}).encode('utf-8'), 'application/json', 400

def handle_not_found():
    """Simulates a 404 Not Found view."""
    return json.dumps({"error": "Not Found"}).encode('utf-8'), 'application/json', 404

# --- Basic "Routing" (manual URL dispatch) ---
# This is where you map paths to your "view" functions
def route_request(path, query_params):
    if path == '/tickets':
        return get_all_tickets()
    elif path.startswith('/tickets/'):
        parts = path.split('/')
        if len(parts) == 3 and parts[2].isdigit(): # /tickets/ID
            ticket_id = parts[2]
            return get_ticket_detail(ticket_id)
    return handle_not_found() # Default for unhandled paths

# --- Custom HTTP Request Handler ---
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

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
        print(f"Serving at port {PORT}")
        print(f"Try: http://localhost:{PORT}/tickets")
        print(f"Try: http://localhost:{PORT}/tickets/1")
        print(f"Try: http://localhost:{PORT}/tickets/99")
        httpd.serve_forever()