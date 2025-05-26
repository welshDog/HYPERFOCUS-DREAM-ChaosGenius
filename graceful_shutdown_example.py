import signal
import sys
import time

def signal_handler(sig, frame):
    print('\n🛑 Gracefully shutting down... Thanks for using Hyperfocus Zone!')
    # Clean up any resources here
    sys.exit(0)  # Exit with code 0 (success)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

print('🚀 Hyperfocus Zone running... Press Ctrl+C to stop gracefully')

try:
    while True:
        # Your main application logic here
        print('⚡ Working...')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n🛑 Shutting down gracefully...')
    sys.exit(0)