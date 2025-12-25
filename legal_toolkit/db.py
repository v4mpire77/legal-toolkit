import streamlit as st
from supabase import Client

class DatabaseManager:
    def __init__(self, client: Client):
        self.client = client

    def save_case(self, user_id, title, case_type, data, description=""):
        try:
            row = {
                "user_id": user_id,
                "title": title,
                "case_type": case_type,
                "data": data,
                "description": description
            }
            data, count = self.client.table("cases").insert(row).execute()
            return data
        except Exception as e:
            st.error(f"Error saving case: {e}")
            return None

    def get_user_cases(self, user_id):
        try:
            # Sort by created_at desc
            response = self.client.table("cases").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching cases: {e}")
            return []

    def delete_case(self, case_id):
        try:
            self.client.table("cases").delete().eq("id", case_id).execute()
            return True
        except Exception as e:
            st.error(f"Error deleting case: {e}")
            return False
