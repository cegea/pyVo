import json
import time
import threading
import subprocess
import logging
from datetime import datetime, timedelta
from acestream.server import Server
from acestream.engine import Engine
from acestream.stream import Stream

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("recording.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_streams(file_path):
    """Load streams from a JSON file."""
    logger.info(f"Loading streams from {file_path}...")
    with open(file_path, 'r') as file:
        streams = json.load(file)
    logger.info(f"Loaded {len(streams)} streams.")
    return streams

def record_stream(server, stream_id, output_file, start_time, end_time):
    """Record a stream from start_time to end_time."""
    logger.info(f"Preparing to record stream {stream_id} from {start_time} to {end_time}...")

    engine = Engine('acestreamengine', client_console=True)
    
    # Ensure server is available
    if not server.available:
        logger.warning("Local server not available. Starting AceStream engine...")
        engine.start()
        while not engine.running:
            logger.info("Waiting for AceStream engine to start...")
            time.sleep(1)
        logger.info("AceStream engine started.")

    stream = Stream(server, id=stream_id)
    try:
        # Wait until the start time
        now = datetime.now()
        wait_time = (start_time - now).total_seconds()
        if wait_time > 0:
            logger.info(f"Waiting {wait_time:.2f} seconds until recording starts...")
            time.sleep(wait_time)
        
        # Start the stream
        logger.info(f"Starting stream {stream_id, stream.playback_url}...")
        stream.start(hls=True, transcode_audio=True)
        logger.info(f"Stream started. Recording to {output_file}.")

        # Record using mpv
        process = subprocess.Popen([
            'mpv', 
            stream.playback_url, 
            '--record-file', output_file
        ])
        
        # Monitor the stream until the end time
        while datetime.now() < end_time:
            if process.poll() is not None:  # If mpv exits, restart it
                logger.error(f"Stream {stream_id} disconnected. Restarting recording...")
                process = subprocess.Popen([
                    'mpv',                      
                    f'--stream-record={output_file}', 
                    stream.playback_url
                ])
            time.sleep(10)
        
        # Stop recording
        logger.info(f"Stopping recording for stream {stream_id}...")
        process.terminate()
        process.wait()
        logger.info(f"Recording completed for stream {stream_id}.")
    finally:
        logger.info(f"Stopping stream {stream_id}...")
        stream.stop()
        engine.stop()
        logger.info(f"Engine stopped for stream {stream_id}.")

def schedule_recordings(json_file):
    """Schedule recordings for all streams in the JSON file."""
    streams = load_streams(json_file)
    server = Server(host='127.0.0.1', port=6878)

    for stream in streams:
        stream_id = stream['id']
        output_file = stream['output_file']
        start_time = datetime.fromisoformat(stream['start_time'])
        end_time = datetime.fromisoformat(stream['end_time'])

        logger.info(f"Scheduling recording for stream {stream_id}...")
        # Start a thread for each recording
        threading.Thread(
            target=record_stream, 
            args=(server, stream_id, output_file, start_time, end_time), 
            daemon=True
        ).start()

if __name__ == "__main__":
    logger.info("Starting the recording scheduler...")
    try:
        # Replace 'streams.json' with your JSON file path
        schedule_recordings('streams.json')
        logger.info("All recordings scheduled. Waiting for threads to complete...")
        
        # Keep the main thread alive
        while threading.active_count() > 1:
            time.sleep(1)
        
        logger.info("All recordings completed.")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
