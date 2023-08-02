from streamlit.connections import ExperimentalBaseConnection
import streamlit as st
import os

from . repl_controller import ReplController

# REF: https://docs.streamlit.io/library/api-reference/connections/st.experimental_connection
# REF: https://docs.streamlit.io/library/advanced-features/connecting-to-data
# REF: https://experimental-connection.streamlit.app/Build_your_own
# REF: https://github.com/streamlit/files-connection

# TODO: pass additional CLI params
# TODO: option: ignore cache

CONTROLLER_OPTIONS = ['command', 'prompt', 'encoding']

# PARAMETERS PRIORITIES:
# 1. function kwargs
# 2. environment variables
# 3. secrets.toml

class ReplConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs):
        kw = kwargs.copy()
        for k in CONTROLLER_OPTIONS:
            if k in kw: continue
            k_env = f'{self._connection_name}_{k}'
            if k_env in os.environ:
                kw[k] = os.environ[k_env]
            elif k in self._secrets:
                kw[k] = self._secrets[k]
        return ReplController(**kw)

    def query(self, query, ttl=None, **kwargs):
        @st.cache_data(ttl=ttl)
        def _query(query: str, **kwargs):
            return self._send(query, **kwargs)
        return _query(query, **kwargs)

    def _send(self, text):
        return self._instance.send(text)

    def reset(self):
        self._instance.reset()
