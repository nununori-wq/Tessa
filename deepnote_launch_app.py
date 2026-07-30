# =============================================================
# RUN THIS CELL LAST, to launch the app inside Deepnote.
#
# Deepnote needs Streamlit bound to 0.0.0.0 on a specific port
# so its proxy can forward it to a preview tab/URL. Running
# `streamlit run app.py` with defaults will NOT be reachable.
# =============================================================

!streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false

# After this cell starts, Deepnote should show an "Open app" /
# preview link for port 8501 (usually a button that appears near
# the cell output, or under the project's "Integrations"/"Apps"
# panel). If you don't see it automatically, look for a
# "Ports" or "Preview" tab in the Deepnote sidebar and open 8501.
