from streamlit.connections import ExperimentalBaseConnection
import streamlit as st

from . repl_controler import ReplControler

# REF: https://docs.streamlit.io/library/advanced-features/connecting-to-data
# REF: https://experimental-connection.streamlit.app/Build_your_own
# REF: https://github.com/streamlit/files-connection

# TODO: kwargs from env ???
# TODO: pass additional CLI params
# TODO: option: ignore cache

class ReplConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs):
        kw = {}
        for k in ['command', 'prompt', 'encoding']:
            if k in kwargs:
                kw[k] = kwargs.pop(k)
            else:
                kw[k] = self._secrets.get(k)
        return ReplControler(**kw, **kwargs)

    def query(self, query, ttl=3600, **kwargs):
        @st.cache_data(ttl=ttl)
        def _query(query: str, **kwargs):
            return self._send(query, **kwargs)
        return _query(query, **kwargs)

    def _send(self, text):
        return self._instance.send(text)
