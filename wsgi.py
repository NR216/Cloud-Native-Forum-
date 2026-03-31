from app import create_app, socketio

app = create_app()

# Initialize metrics hooks
from app.metrics import init_metrics
init_metrics(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
