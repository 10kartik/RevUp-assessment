from typing import Dict, List

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
    
    def get_history(self, session_id: str) -> List[Dict]:
        print(f"Getting history for session: {session_id}")
        return self.sessions.get(session_id, [])
    
    def update_history(self, session_id: str, user_query: str, agent_response: str):
        print(f"Updating history for session: {session_id}")
        history = self.sessions.setdefault(session_id, [])
        
        # Add user query
        history.append({"role": "user", "content": user_query})
        
        # Add agent response
        history.append({"role": "assistant", "content": agent_response})
        
        # Keep only last 10 exchanges to manage context window
        if len(history) > 20:
            self.sessions[session_id] = history[-20:]