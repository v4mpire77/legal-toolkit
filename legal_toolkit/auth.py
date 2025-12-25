import os
import streamlit as st
from supabase import create_client, Client

class AuthManager:
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
        self.client: Client = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                st.error(f"Failed to initialize Supabase: {e}")

    def is_configured(self):
        return self.client is not None

    def sign_up(self, email, password):
        try:
            res = self.client.auth.sign_up({
                "email": email, 
                "password": password
            })
            return res
        except Exception as e:
            st.error(str(e))
            return None

    def sign_in(self, email, password):
        try:
            res = self.client.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            return res
        except Exception as e:
            st.error(str(e))
            return None

    def sign_in_with_google(self):
        try:
            # This returns a URL that the user needs to be redirected to
            res = self.client.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": st.secrets.get("REDIRECT_URL", "https://legal-toolkit.streamlit.app/")
                }
            })
            return res
        except Exception as e:
            st.error(str(e))
            return None

    def sign_out(self):
        try:
            self.client.auth.sign_out()
        except Exception as e:
            pass # Ignore errors on logout

    def get_user(self):
        if not self.client: return None
        try:
            # Check local session or fetch user
            user = self.client.auth.get_user()
            return user
        except:
            return None
