import time
from threading import Lock, Thread

class SessionManager:
    def __init__(self, ttl=300):
        """
        Initialize the SessionManager.
        
        Parameters:
        - ttl (int):
        """
        self.sessions = {}
        self.ttl = ttl 
        self.lock = Lock()
        self.cleanup_thread = Thread(target=self._cleanup_sessions, daemon=True)
        self.cleanup_thread.start()

    def add_to_session(self, session_id: str, prompt: str, response: str):
        """
        adds a new prompt and response to the specified session.
        """
        with self.lock:
            now = time.time()
            if session_id not in self.sessions:
                self.sessions[session_id] = {"history": [], "last_updated": now}
            self.sessions[session_id]["history"].append({"prompt": prompt, "response": response})
            self.sessions[session_id]["last_updated"] = now

    def get_session(self, session_id: str):
        with self.lock:
            session = self.sessions.get(session_id)
            return session["history"] if session else []

    def _cleanup_sessions(self):
       # clean up expired
        while True:
            time.sleep(60)  
            with self.lock:
                now = time.time()
                expired_sessions = [s for s, data in self.sessions.items() if now - data["last_updated"] > self.ttl]
                for s in expired_sessions:
                    del self.sessions[s]

# Global session manager instance 
session_manager = SessionManager()

def add_to_session(session_id: str, prompt: str, response: str):
    session_manager.add_to_session(session_id, prompt, response)

def get_session(session_id: str):
    return session_manager.get_session(session_id)
